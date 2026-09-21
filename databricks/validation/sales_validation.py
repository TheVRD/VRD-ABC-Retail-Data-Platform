# Databricks notebook source
# ==========================================================
# Notebook Name      : sales_validation
# Project            : ABC Retail Data Platform
# Purpose            : sales data validation
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../config/validation_rules

# COMMAND ----------

# MAGIC %run ../models/validation/validation_rule

# COMMAND ----------

# MAGIC %run ./validation_utils

# COMMAND ----------

# MAGIC %run ./validation_pipelines

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

SALES_VALIDATION_RULES = (
    ValidationRule(
        name="Not null validation",
        validator=validate_not_null,
        validator_kwargs={
            "columns": SALES_REQUIRED_COLUMNS
        }
    ),
    ValidationRule(
        name="Duplicates validation",
        validator=validate_duplicates,
        validator_kwargs={
            "columns": SALES_PRIMARY_KEY_COLUMNS
        }
    ),
    
    ValidationRule(
    name="Validate Positive Numbers",
    validator=validate_positive_numbers,
    validator_kwargs={
        "columns": SALES_POSITIVE_NUMBER_COLUMNS
        }
    ),

    ValidationRule(
    name="Validate Payment Mode",
    validator=validate_allowed_values,
    validator_kwargs={
        "column": "paymentMode",
        "allowed_values": ALLOWED_PAYMENT_MODES
        }
    )
)

# COMMAND ----------

def validate_sales(
    *,
    sales_df: DataFrame
) -> tuple[DataFrame, DataFrame]:
    """
    Validates the sales data.

    Args:
        sales_df (DataFrame): The sales data.

    Returns:
        tuple[DataFrame, DataFrame]: A tuple containing the valid and invalid sales data.
    """

    if not isinstance(sales_df, DataFrame):
        raise TypeError("sales_df must be a DataFrame.")

    return execute_validation_pipeline(
        df=sales_df,
        validation_rules=SALES_VALIDATION_RULES
    )



