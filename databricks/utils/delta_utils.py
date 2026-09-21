# Databricks notebook source
# ==========================================================
# Notebook Name      : delta_utils
# Project            : ABC Retail Data Platform
# Purpose            : delta utils for writing delta tables to delta lake
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../models/delta/write_mode

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

def write_delta_table(
    df: DataFrame,
    table_name: str,
    mode: WriteMode
) -> None:
    """
    This method accepts a dataframe and writes it to a delta table

    args:
        df: dataframe to write
        table_name: name of the table to write to
        mode: mode to write to the table
    returns:
        None
    """
    if not isinstance(df, DataFrame):
        raise TypeError("df must be a DataFrame")

    if not isinstance(table_name, str):
        raise TypeError("table_name must be a string")

    if not table_name.strip():
        raise ValueError("table_name cannot be blank")

    if not isinstance(mode, WriteMode):
        raise TypeError("mode must be a WriteMode")
    
    (
        df.write
        .format("delta")
        .mode(mode.value)
        .saveAsTable(table_name)
    )

# COMMAND ----------

def read_delta_table(
    *,
    table_name: str
) -> DataFrame:
    """
    reads a delta table and returns a dataframe
    args:
        table_name: name of the table to read
    returns:
        dataframe
    """
    if not isinstance(table_name, str):
        raise TypeError("table name must be a string")
    if not table_name.strip():
        raise ValueError("table name cannot be blank")

    return spark.table(table_name)