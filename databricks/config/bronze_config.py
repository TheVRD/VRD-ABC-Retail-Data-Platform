# Databricks notebook source
# ==========================================================
# Notebook Name      : bronze config
# Project            : ABC Retail Data Platform
# Purpose            : config file specific to bronze ingestion
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

print("Initializing required notebooks")

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../utils/file_utils

# COMMAND ----------

# MAGIC %run ../utils/delta_utils

# COMMAND ----------

# MAGIC %run ../utils/metadata_utils

# COMMAND ----------

# MAGIC %run ../models/delta/write_mode

# COMMAND ----------

# MAGIC %run ../utils/logging_utils

# COMMAND ----------

# MAGIC %run ../config/validation_rules

# COMMAND ----------

print("Completed Initialization")

# COMMAND ----------

landing_path = spark.conf.get("project.landingPath")
catalog = spark.conf.get("project.catalog")
bronze_schema = spark.conf.get("project.bronzeSchema")
processing_date = spark.conf.get("project.processingDate")
pipeline_name = spark.conf.get("project.pipelineName")
processing_year = spark.conf.get("project.processingYear")
processing_month = spark.conf.get("project.processingMonth")
processing_day = spark.conf.get("project.processingDay")
BRONZE_SALES_TABLE = (
    f"{CATALOG}.{BRONZE_SCHEMA}.{SALES_RAW_TABLE}"
)

# COMMAND ----------

sales_landing_path = (
    f"{landing_path}/sales/"
    f"{processing_year}/"
    f"{processing_month}/"
    f"{processing_day}"
)

# COMMAND ----------

sales_file_path = (
    f"{sales_landing_path}/corrupt_sales.csv"
)