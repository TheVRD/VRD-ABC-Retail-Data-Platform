# Databricks notebook source
# ==========================================================
# Notebook Name      : file_utils
# Project            : ABC Retail Data Platform
# Purpose            : file utils for reading different types of files
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

def read_csv(
    *,
    path: str,
    header: bool = True,
    infer_schema: bool = True
) -> DataFrame:
    """
    Reads a csv file and returns a dataframe

    args:
        path: path to the csv file
        header: whether the csv file has a header
        inferSchema: whether to infer the schema of the csv file
    returns:
        dataframe: dataframe of the csv file
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(header, bool):
        raise TypeError("header must be a boolean")
    if not isinstance(infer_schema, bool):
        raise TypeError("inferSchema must be a boolean")
    if not path:
        raise ValueError("path cannot be empty")
    
    return (
        spark.read
            .option("header", header)
            .option("inferSchema", infer_schema)
            .csv(path)
    )

# COMMAND ----------

