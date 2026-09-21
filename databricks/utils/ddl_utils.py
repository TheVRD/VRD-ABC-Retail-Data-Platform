# Databricks notebook source
# ==========================================================
# Notebook Name      : ddl_utils
# Project            : ABC Retail Data Platform
# Purpose            : Centralized DDL query definitions
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

def create_pipeline_execution_log_table_query(
    *,
    catalog: str,
    schema: str
) -> str:
    """
     Returns the DDL query for creating the pipeline execution log table.

    Args:
        catalog: Unity Catalog name.
        schema: Metadata schema name.

    Returns:
        SQL DDL query.
    """
    if not isinstance(catalog, str):
        raise TypeError("catalog must be a string")
    if not isinstance(schema, str):
        raise TypeError("schema must be a string")

    if not catalog:
        raise ValueError("catalog must be a non-empty string")
    if not schema:
        raise ValueError("schema must be a non-empty string")

    return f"""
    CREATE TABLE IF NOT EXISTS
    {catalog}.{schema}.pipeline_execution_log
    (
        execution_id STRING,
        pipeline_name STRING,
        notebook_name STRING,
        data_entity STRING,
        environment STRING,
        processing_date DATE,
        start_timestamp TIMESTAMP,
        end_timestamp TIMESTAMP,
        status STRING,
        rows_processed BIGINT,
        error_message STRING
    )
    USING DELTA
    """



# COMMAND ----------

def create_schema_query(
    *,
    catalog: str,
    schema: str
) -> str:
    """
    Returns the DDL query for creating a schema.
    """

    if not isinstance(catalog, str):
        raise TypeError("catalog must be a string")

    if not isinstance(schema, str):
        raise TypeError("schema must be a string")

    if not catalog:
        raise ValueError("catalog cannot be empty")

    if not schema:
        raise ValueError("schema cannot be empty")

    return f"""
    CREATE SCHEMA IF NOT EXISTS
    {catalog}.{schema}
    """

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS vrdworkspace1.metadata.file_processing_log (
# MAGIC     file_path STRING NOT NULL,
# MAGIC     file_name STRING NOT NULL,
# MAGIC     pipeline_name STRING NOT NULL,
# MAGIC     data_entity STRING NOT NULL,
# MAGIC     environment STRING NOT NULL,
# MAGIC     processing_status STRING NOT NULL,
# MAGIC     start_timestamp TIMESTAMP NOT NULL,
# MAGIC     execution_id STRING NOT NULL,
# MAGIC     end_timestamp TIMESTAMP,
# MAGIC     rows_processed BIGINT,
# MAGIC     error_message STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE vrdworkspace1.metadata.file_processing_log;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.metadata.file_processing_log;