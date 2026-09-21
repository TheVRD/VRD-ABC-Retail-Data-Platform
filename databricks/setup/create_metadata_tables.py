# Databricks notebook source
# ==========================================================
# Notebook Name      : create_metadata_tables
# Project            : ABC Retail Data Platform
# Purpose            : creating schemas
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../utils/ddl_utils

# COMMAND ----------

queries = (
    create_pipeline_execution_log_table_query(
        catalog=CATALOG,
        schema=METADATA_SCHEMA
    ),
)

for query in queries:
    spark.sql(query)

if ENVIRONMENT == "DEV":
    print("Metadata tables created successfully.")