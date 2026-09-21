# Databricks notebook source
# ==========================================================
# Notebook Name      : scd2_utils
# Project            : ABC Retail Data Platform
# Purpose            : SCD type 2 implementation
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from functools import reduce

from pyspark.sql import Column, DataFrame
from pyspark.sql.functions import col, count
from pyspark.sql import functions as F

from delta.tables import DeltaTable

# COMMAND ----------

def build_scd2_change_condition(
    tracked_columns: list[str],
) -> Column:
    """
    Builds a null-safe Spark condition that identifies
    changes in SCD2-tracked columns.

    The returned condition evaluates to True when
    at least one tracked column differs between source
    and target.
    """

    if not tracked_columns:
        raise ValueError("Tracked columns cannot be empty.")

    if any(not column_name for column_name in tracked_columns):
        raise ValueError("Tracked column names cannot be empty.")

    change_conditions = [
        ~col(f"target.{column_name}").eqNullSafe(
            col(f"source.{column_name}")
        )
        for column_name in tracked_columns
    ]

    return reduce(
        lambda condition1, condition2: condition1 | condition2,
        change_conditions
    )

# COMMAND ----------

def validate_scd2_source_uniqueness(
    source_df: DataFrame,
    business_key: str
) -> None:
    """
    Validates that each business key occurs only once
    in the incoming SCD2 source.

    Raises:
        ValueError: If duplicate business keys are found.
    """

    if source_df is None:
        raise ValueError("Source DataFrame cannot be None.")

    if not business_key:
        raise ValueError("Business key cannot be empty.")

    duplicate_df = (
        source_df
        .groupBy(business_key)
        .agg(count("*").alias("record_count"))
        .filter(col("record_count") > 1)
    )

    if not duplicate_df.isEmpty():
        duplicate_keys = [
            row[business_key]
            for row in duplicate_df.collect()
        ]

        raise ValueError(
            f"Duplicate business keys found in SCD2 source: "
            f"{duplicate_keys}"
        )

# COMMAND ----------

def prepare_scd2_merge_source(
    source_df: DataFrame,
    target_df: DataFrame,
    business_key: str,
    tracked_columns: list[str],
    change_timestamp_column: str
) -> DataFrame:
    """
    Prepares the source DataFrame for an SCD2 Delta MERGE.

    Generates:
        - INSERT row for new customers
        - EXPIRE + INSERT rows for changed customers
        - No rows for unchanged customers
    """

    if source_df is None:
        raise ValueError("Source DataFrame cannot be None.")

    if target_df is None:
        raise ValueError("Target DataFrame cannot be None.")

    if not business_key:
        raise ValueError("Business key cannot be empty.")

    if not tracked_columns:
        raise ValueError("Tracked columns cannot be empty.")

    if not change_timestamp_column:
        raise ValueError("Change timestamp column cannot be empty.")

    # Only the current target version participates
    # in change detection.
    current_target_df = target_df.filter(
        F.col("is_current") == True
    )

    comparison_df = (
        source_df.alias("source")
        .join(
            current_target_df.alias("target"),
            F.col(f"source.{business_key}")
            == F.col(f"target.{business_key}"),
            "left"
        )
    )

    change_condition = build_scd2_change_condition(
        tracked_columns
    )

    customer_exists = F.col(
        f"target.{business_key}"
    ).isNotNull()

    # New customer
    new_customer_df = (
        comparison_df
        .filter(~customer_exists)
        .select(
            F.col(f"source.{business_key}").alias(business_key),
            *[
                F.col(f"source.{column_name}").alias(column_name)
                for column_name in tracked_columns
            ],
            F.col(
                f"source.{change_timestamp_column}"
            ).alias(change_timestamp_column)
        )
        .withColumn(
            "action",
            F.lit("INSERT")
        )
    )

    # Existing customer whose tracked attributes changed
    changed_customer_df = (
        comparison_df
        .filter(customer_exists & change_condition)
    )

    # Row used to expire the existing target record
    expire_df = (
        changed_customer_df
        .select(
            F.col(f"source.{business_key}").alias(business_key),
            *[
                F.col(f"source.{column_name}").alias(column_name)
                for column_name in tracked_columns
            ],
            F.col(
                f"source.{change_timestamp_column}"
            ).alias(change_timestamp_column)
        )
        .withColumn(
            "action",
            F.lit("EXPIRE")
        )
    )

    # Row used to insert the new version
    insert_changed_df = (
        changed_customer_df
        .select(
            F.col(f"source.{business_key}").alias(business_key),
            *[
                F.col(f"source.{column_name}").alias(column_name)
                for column_name in tracked_columns
            ],
            F.col(
                f"source.{change_timestamp_column}"
            ).alias(change_timestamp_column)
        )
        .withColumn(
            "action",
            F.lit("INSERT")
        )
    )

    return (
        expire_df
        .unionByName(insert_changed_df)
        .unionByName(new_customer_df)
    )

# COMMAND ----------

def apply_scd2_merge(
    target_table_name: str,
    merge_source_df: DataFrame,
    business_key: str,
    tracked_columns: list[str]
) -> None:
    """
    Applies an SCD Type 2 merge to a Delta target table.

    EXPIRE rows update the current target record.
    INSERT rows create new target versions.
    """

    if not target_table_name:
        raise ValueError("Target table name cannot be empty.")

    if merge_source_df is None:
        raise ValueError("Merge source DataFrame cannot be None.")

    if not business_key:
        raise ValueError("Business key cannot be empty.")

    if not tracked_columns:
        raise ValueError("Tracked columns cannot be empty.")

    target_table = DeltaTable.forName(
        spark,
        target_table_name
    )

    # Dynamically build the INSERT mapping
    insert_values = {
        business_key: F.col(
            f"source.{business_key}"
        )
    }

    insert_values.update({
        column_name: F.col(
            f"source.{column_name}"
        )
        for column_name in tracked_columns
    })

    # Static SCD2 metadata columns
    insert_values.update({
        "effective_from": F.col(
            "source.change_timestamp"
        ),
        "effective_to": F.to_timestamp(
            F.lit("9999-12-31 00:00:00")
        ),
        "is_current": F.lit(True)
    })

    (
        target_table.alias("target")
        .merge(
            merge_source_df.alias("source"),
            (
                F.col(f"target.{business_key}")
                == F.col(f"source.{business_key}")
            )
            &
            (
                F.col("source.action") == F.lit("EXPIRE")
            )
            &
            (
                F.col("target.is_current") == F.lit(True)
            )
        )
        .whenMatchedUpdate(
            set={
                "effective_to": F.col(
                    "source.change_timestamp"
                ),
                "is_current": F.lit(False)
            }
        )
        .whenNotMatchedInsert(
            values=insert_values
        )
        .execute()
    )