# Databricks notebook source
# ==========================================================
# Notebook Name      : sales_transformation
# Project            : ABC Retail Data Platform
# Purpose            : sales data transformations
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../config/transformation_rules

# COMMAND ----------

# MAGIC %run ../models/transformation/transformation_rule

# COMMAND ----------

# MAGIC %run ./transformation_pipeline

# COMMAND ----------

# MAGIC %run ./transformation_utils

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

SALES_TRANSFORMATION_RULES = (
    TransformationRule(
        name="Trim Columnns Transformation",
        transformer=trim_columns,
        transformer_kwargs={
            "columns": SALES_TRIM_COLUMNS
        }
    ),
    TransformationRule(
        name="UpperCase Columns Transformation",
        transformer=uppercase_columns,
        transformer_kwargs={
            "columns": SALES_UPPER_CASE_COLUMNS
        }
    ),
    TransformationRule(
        name="Title Case Columns Transformation",
        transformer=title_case_columns,
        transformer_kwargs={
            "columns": SALES_TITLE_CASE_COLUMNS
        }
    ),
    TransformationRule(
        name="Re-calculate total amount Transformation",
        transformer=recalculate_total_amount,
        transformer_kwargs={
            "quantity_column": "quantity",
            "unit_price_column": "unitPrice",
            "total_amount_column": "totalAmount"
        }
    )
)

# COMMAND ----------

def transform_sales(
    *,
    sales_df: DataFrame
) -> DataFrame:
    """
    Applies all transformations to the sales dataframe.
    args:
      sales_df: DataFrame
    returns:
      DataFrame
    """
    if not isinstance(sales_df, DataFrame):
        raise TypeError("sales_df must be a DataFrame")
    return execute_transformation_pipeline(
        df=sales_df,
        transform_rules=SALES_TRANSFORMATION_RULES
    )