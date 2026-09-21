# Databricks notebook source
# ==========================================================
# Notebook Name      : transformation_utils
# Project            : ABC Retail Data Platform
# Purpose            : transformation utils
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, upper, initcap

# COMMAND ----------

def _validate_transformation_inputs(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> None:
    """
    Validates the inputs to the transformation functions.
    args:
      df: The DataFrame to validate.
      columns: A tuple of column names to validate
    """
    if not isinstance(df, DataFrame):
        raise TypeError("df must be a DataFrame")
    if not isinstance(columns, tuple):
        raise TypeError("columns must be a tuple")
    if not columns:
        raise ValueError("columns cannot be empty")
    if not all(isinstance(column, str) for column in columns):
        raise TypeError("columns must be a tuple of strings")
    if len(columns) != len(set(columns)):
        raise ValueError("columns cannot contain duplicate values")

    column_set = set(df.columns)

    missing_columns = [
        column_name
        for column_name in columns
        if column_name not in column_set
    ]

    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not found in DataFrame"
        )

# COMMAND ----------

def trim_columns(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> DataFrame:
    """
    Trims the values in the specified columns of a DataFrame.
    args:
      df: The DataFrame to trim.
      columns: A tuple of column names to trim.
    returns:
      A new DataFrame with the specified columns trimmed.
    """
    _validate_transformation_inputs(
        df=df,
        columns=columns
    )

    current_df = df
    for column_name in columns:
        current_df = current_df.withColumn(
            column_name,
            trim(col(column_name))
        )
    return current_df

# COMMAND ----------

def uppercase_columns(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> DataFrame:
    """
    Converts the values in the specified columns of a DataFrame to uppercase.
    args:
      df: The DataFrame to convert.
      columns: A tuple of column names to convert.
    returns:
      A new DataFrame with the specified columns converted to uppercase.
    """
    _validate_transformation_inputs(
        df=df,
        columns=columns
    )

    current_df = df

    for column_name in columns:
        current_df = current_df.withColumn(
            column_name,
            upper(col(column_name))
        )
    return current_df



# COMMAND ----------

def title_case_columns(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> DataFrame:
    """
    Converts the values in the specified columns of a DataFrame to title case.
    args:
      df: The DataFrame to convert.
      columns: A tuple of column names to convert.
    returns:
      A new DataFrame with the specified columns converted to title case.
    """
    _validate_transformation_inputs(
        df=df,
        columns=columns
    )

    current_df = df

    for column_name in columns:
        current_df = current_df.withColumn(
            column_name,
            initcap(col(column_name))
        )
    
    return current_df

# COMMAND ----------

def recalculate_total_amount(
    *,
    df: DataFrame,
    quantity_column: str,
    unit_price_column: str,
    total_amount_column: str
) -> DataFrame:
    """
    Calculates the total amount for each row in a DataFrame based on the specified quantity columns and unit price column.
    args:
      df: The DataFrame to calculate the total amount for.
      quantity_column: The name of the column containing the quantity
      unit_price_column: The name of the column containing the unit price.
      total_amount_column: The name of the column to store the calculated total amount.
    returns:
      A new DataFrame with the total amount column recalculated.
    """

    if not isinstance(df, DataFrame):
        raise TypeError("df must be a DataFrame")
    if not isinstance(quantity_column, str):
        raise TypeError("quantity_column must be a string")
    if not isinstance(unit_price_column, str):
        raise TypeError("unit_price_column must be a string")
    if not isinstance(total_amount_column, str):
        raise TypeError("total_amount_column must be a string")
    if not quantity_column.strip():
        raise ValueError("quantity_column cannot be empty")
    if not unit_price_column.strip():
        raise ValueError("unit_price_column cannot be empty")
    if not total_amount_column.strip():
        raise ValueError("total_amount_column cannot be empty")
    columns_set = set(df.columns)
    if quantity_column not in columns_set:
        raise ValueError(f"Column {quantity_column} not found in DataFrame")
    if unit_price_column not in columns_set:
        raise ValueError(f"Column {unit_price_column} not found in DataFrame")

    current_df = df

    current_df = current_df.withColumn(
        total_amount_column,
        col(quantity_column) * col(unit_price_column)
    )
    return current_df