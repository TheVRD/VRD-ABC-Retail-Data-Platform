# Databricks notebook source
# ==========================================================
# Notebook Name      : validation_utils
# Project            : ABC Retail Data Platform
# Purpose            : Reusable validation functions
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# COMMAND ----------

def _validate_validation_inputs(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> None:
    """
    Validates the inputs to the validator functions.
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

    column_set = set(df.schema.fieldNames())

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

def validate_not_null(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> tuple[DataFrame, DataFrame]:
    """
    Validates that the specified columns in the DataFrame are not null.
    args:
      df: The DataFrame to validate.
      columns: A tuple of column names to validate.
    returns:
      A tuple of two DataFrames:
        - The first DataFrame contains the rows that passed the validation.
        - The second DataFrame contains the rows that failed the validation.
    """
    _validate_validation_inputs(
        df=df,
        columns=columns
    )

    valid_condition = col(columns[0]).isNotNull()

    for column_name in columns[1:]:
        valid_condition = (
            valid_condition & col(column_name).isNotNull()
        )
    
    valid_df = df.filter(valid_condition)
    invalid_df = df.filter(~valid_condition)

    return (
        valid_df,
        invalid_df
    )
    


# COMMAND ----------

def validate_duplicates(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> tuple[DataFrame, DataFrame]:
    """
    Validates that the specified columns in the DataFrame do not contain duplicate values.
    args:
      df: The DataFrame to validate.
      columns: A tuple of column names to validate.
    returns:
      A tuple of two DataFrames:
        - The first DataFrame contains the rows that passed the validation.
        - The second DataFrame contains the rows that failed the validation.
    """
    _validate_validation_inputs(
        df=df,
        columns=columns
    )

    duplicate_keys_df = (
        df.groupBy(*columns)
          .count()
          .filter(col("count") > 1)
          .drop("count")
    )

    invalid_df = (
        df.join(
           duplicate_keys_df,
           "saleId",
           "inner" 
        )
    )
    
    valid_df = (
        df.join(
            duplicate_keys_df,
            "saleId",
            "left_anti"
        )
    )
    return (
        valid_df,
        invalid_df
    )

# COMMAND ----------

def validate_positive_numbers(
    *,
    df: DataFrame,
    columns: tuple[str, ...]
) -> tuple[DataFrame, DataFrame]:
    """
    Validates that the specified columns in the DataFrame contain positive numbers.
    args:
      df: The DataFrame to validate.
      columns: A tuple of column names to validate.
    returns:
      A tuple of two DataFrames:
        - The first DataFrame contains the rows that passed the validation.
        - The second DataFrame contains the rows that failed the validation
    """
    _validate_validation_inputs(
        df=df,
        columns=columns
    )

    valid_condition = col(columns[0]) >= 0

    for column_name in columns[1:]:
        valid_condition = (
            valid_condition & (col(column_name) >= 0)
        )

    valid_df = df.filter(valid_condition)
    invalid_df = df.filter(~valid_condition)
    
    return (
        valid_df,
        invalid_df
    )

# COMMAND ----------

def validate_allowed_values(
    *,
    df: DataFrame,
    column: str,
    allowed_values: tuple[str, ...]
) -> tuple[DataFrame, DataFrame]:
    """
    Validates that the specified column in the DataFrame contains only allowed values.
    args:
      df: The DataFrame to validate.
      column: The column name to validate.
      allowed_values: A tuple of allowed values.
    returns:
      A tuple of two DataFrames:
        - The first DataFrame contains the rows that passed the validation.
        - The second DataFrame contains the rows that failed the validation.
    """
    if not isinstance(df, DataFrame):
        raise TypeError("df must be a DataFrame")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    #if not isinstance(allowed_values, tuple):
    #    raise TypeError("allowed_values must be a tuple")
    if not allowed_values:
        raise ValueError("allowed_values cannot be empty")

    if not all(
        isinstance(value, str)
        for value in allowed_values
    ):
        raise TypeError("allowed_values must be a tuple of strings")
    
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in DataFrame")
        
    
    valid_condition = col(column).isin(*allowed_values)

    valid_df = df.filter(valid_condition)
    invalid_df = df.filter(~valid_condition)

    return (
        valid_df,
        invalid_df
    )


# COMMAND ----------

def validate_regex(
    *,
    df: DataFrame,
    column: str,
    regex_pattern: str
) -> tuple[DataFrame, DataFrame]:
    """
    Validates that the specified column in the DataFrame matches the given regular expression pattern.
    args:
      df: The DataFrame to validate.
      column: The column name to validate.
      regex_pattern: The regular expression pattern to match.
    returns:
      A tuple of two DataFrames:
        - The first DataFrame contains the rows that passed the validation.
    """
    if not isinstance(df, DataFrame):
        raise TypeError("df must be a DataFrame")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    if not isinstance(regex_pattern, str):
        raise TypeError("regex_pattern must be a string")
    if not column.strip():
        raise ValueError("column cannot be empty")
    if not regex_pattern.strip():
        raise ValueError("regex_pattern cannot be empty")
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in DataFrame")

    valid_condition = col(column).rlike(regex_pattern)

    valid_df = df.filter(valid_condition)
    invalid_df = df.filter(~valid_condition)

    return (
        valid_df,
        invalid_df
        )