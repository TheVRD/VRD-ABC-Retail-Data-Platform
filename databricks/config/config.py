# Databricks notebook source
# ==========================================================
# Notebook Name      : config
# Project            : ABC Retail Data Platform
# Purpose            : Central Configuration Notebook
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

#Environment
ENVIRONMENT = "DEV"

# COMMAND ----------

from datetime import datetime

PROCESSING_DATE = datetime.strptime(
    processing_date,
    "%Y-%m-%d"
).date()

PROCESSING_YEAR = PROCESSING_DATE.strftime("%Y")
PROCESSING_MONTH = PROCESSING_DATE.strftime("%m")
PROCESSING_DAY = PROCESSING_DATE.strftime("%d")

# COMMAND ----------

# MAGIC %md
# MAGIC #Storage Configuration
# MAGIC
# MAGIC This section is used to configure the storage account and container for the data lake.

# COMMAND ----------

STORAGE_ACCOUNT = "stvrdde001"
CONTAINER = "datalake"

# COMMAND ----------

storage_account_key = dbutils.secrets.get(
    scope="abc-retail-secrets",
    key="storage-account-key"
)

# COMMAND ----------

# MAGIC %md
# MAGIC #CATALOG AND SCHEMA
# MAGIC Catalog and schema inforamtion related to our project

# COMMAND ----------

PROJECT_NAME  = "abc_Retail"
CATALOG = "vrdworkspace1"
LANDING_FOLDER = "landing"
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"
METADATA_SCHEMA = "metadata"
QUARANTINE_SCHEMA = "quarantine"
LOG_FOLDER = "logs"
CHECKPOINT_FOLDER = "checkpoints"

# COMMAND ----------

# MAGIC %md
# MAGIC #Tables

# COMMAND ----------

SALES_RAW_TABLE = "sales_raw"
SALES_TABLE = "sales"
SALES_QUARANTINE_TABLE = "sales_quarantine"
PIPELINE_LOG_TABLE = "pipeline_execution_log"
FILE_PROCESSING_LOG_TABLE = "file_processing_log"
DATA_PROCESSING_LOG_TABLE = "data_processing_log"

# COMMAND ----------

LANDING_LAYER = "landing"
BRONZE_LAYER = "bronze"
SILVER_LAYER = "silver"
GOLD_LAYER = "gold"
DATA_ENTITY = "sales"

# COMMAND ----------

# MAGIC %md
# MAGIC #Write Modes

# COMMAND ----------

OVERWRITE_MODE = "overwrite"
APPEND_MODE  = "append"

# COMMAND ----------

STARTED_STATUS = "started"
SUCCESS_STATUS = "success"
FAILED_STATUS = "failed"

# COMMAND ----------

# MAGIC %md
# MAGIC #SCHEMA QUERIES

# COMMAND ----------

BRONZE_SCHEMA_QUERY = f"""CREATE SCHEMA IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}"""
SILVER_SCHEMA_QUERY = f"""CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SILVER_SCHEMA}"""
GOLD_SCHEMA_QUERY = f"""CREATE SCHEMA IF NOT EXISTS {CATALOG}.{GOLD_SCHEMA}"""
QUARANTINE_SCHEMA_QUERY = f"""CREATE SCHEMA IF NOT EXISTS {CATALOG}.{QUARANTINE_SCHEMA}"""
METADATA_SCHEMA_QUERY = f"""CREATE SCHEMA IF NOT EXISTS {CATALOG}.{METADATA_SCHEMA}"""

# COMMAND ----------

# MAGIC %md
# MAGIC #PATHS

# COMMAND ----------


BASE_PATH = (
    f"abfss://{CONTAINER}"
    f"@{STORAGE_ACCOUNT}.dfs.core.windows.net"
) 

LANDING_PATH = f"{BASE_PATH}/{LANDING_FOLDER}"


# COMMAND ----------

# MAGIC %md
# MAGIC #RUNTIME_PARAMETERS

# COMMAND ----------

PIPELINE_NAME = "Sales Pipeline"

# COMMAND ----------

# MAGIC %md
# MAGIC #SPARK CONFIG

# COMMAND ----------

spark.conf.set(
    "project.environment", ENVIRONMENT
)

spark.conf.set(
    "project.catalog", CATALOG
)

spark.conf.set(
    "project.bronzeSchema", BRONZE_SCHEMA
)

spark.conf.set(
    "project.silverSchema", SILVER_SCHEMA
)

spark.conf.set(
    "project.goldSchema", GOLD_SCHEMA

)
spark.conf.set(
    "project.landingPath", LANDING_PATH
)

spark.conf.set(
    "project.processingDate", processing_date
)

spark.conf.set(
    "project.pipelineName", PIPELINE_NAME
)
spark.conf.set(
    "project.processingYear", PROCESSING_YEAR
)

spark.conf.set(
    "project.processingMonth", PROCESSING_MONTH
)

spark.conf.set(
    "project.processingDay", PROCESSING_DAY
)

spark.conf.set(
    f"fs.azure.account.key.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    storage_account_key
)

# COMMAND ----------

query = f"USE CATALOG {CATALOG}"
spark.sql(query)

current_catalog = spark.sql("SELECT current_catalog()").first()[0]
print(f"Using catalog: {current_catalog}")

# COMMAND ----------

dbutils.fs.ls(
    f"abfss://{CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
)

# COMMAND ----------

# MAGIC %md
# MAGIC #Validation

# COMMAND ----------

assert ENVIRONMENT in (
    "DEV",
    "TEST",
    "PROD"
)