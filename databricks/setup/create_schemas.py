# Databricks notebook source
# ==========================================================
# Notebook Name      : create_schemas
# Project            : ABC Retail Data Platform
# Purpose            : creating schemas
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../utils/ddl_utils

# COMMAND ----------

schemas  = (
BRONZE_SCHEMA,
SILVER_SCHEMA,
GOLD_SCHEMA,
QUARANTINE_SCHEMA,
METADATA_SCHEMA
)

for schema in schemas:
    query = create_schema_query(
        catalog = CATALOG,
        schema = schema
    )
    spark.sql(query)

    if ENVIRONMENT == "DEV":
        print(f"✓ {schema} schema ready")


# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN vrdworkspace1;