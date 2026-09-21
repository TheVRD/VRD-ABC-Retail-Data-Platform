# Databricks notebook source
# ==========================================================
# Notebook Name      : metadata_utils
# Project            : ABC Retail Data Platform
# Purpose            : metadata utils notebook for adding metadata to the dataframes
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

#imports
from pyspark.sql import DataFrame
from pyspark.sql.functions import input_file_name, current_timestamp, lit, col
from pyspark.sql import functions as F


# COMMAND ----------

def add_metadata_columns(
    df: DataFrame,
    processing_date: str,
    pipeline_name: str
) -> DataFrame:
    """
    Adds metadata columns to a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        DataFrame: The DataFrame with
    """
    if df is None:
        raise ValueError("Input DataFrame cannot be None.")

    if not processing_date:
        raise ValueError("Processing date cannot be empty.")

    if not pipeline_name:
        raise ValueError("Pipeline name cannot be empty.")


    return(
            df
            .withColumn("source_file_path", col("_metadata.file_path"))
            .withColumn("ingestion_timestamp", current_timestamp())
            .withColumn("processing_date", lit(processing_date))
            .withColumn("pipeline_name", lit(pipeline_name))
    )


    
