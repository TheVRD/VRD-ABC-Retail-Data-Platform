# Databricks notebook source
# ==========================================================
# Notebook Name      : gold_config
# Project            : ABC Retail Data Platform
# Purpose            : configuration notebook for gold layer
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ./config

# COMMAND ----------

# MAGIC %run ../utils/delta_utils

# COMMAND ----------



# COMMAND ----------

# MAGIC %run ../gold/utils/gold_aggregation_utils

# COMMAND ----------

# MAGIC %run ../models/delta/write_mode

# COMMAND ----------

# MAGIC %run ../utils/logging_utils

# COMMAND ----------

FACT_DAILY_SALES_TABLE = "fact_daily_sales"
FACT_STORE_SALES_TABLE = "fact_store_sales"
FACT_CITY_SALES_TABLE = "fact_city_sales"
FACT_PRODUCT_SALES_TABLE = "fact_product_sales"
FACT_CATEGORY_SALES_TABLE = "fact_category_sales"
FACT_PAYMENT_MODE_SALES_TABLE = "fact_payment_mode_sales"

# COMMAND ----------

FACT_DAILY_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_DAILY_SALES_TABLE}"
)
FACT_STORE_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_STORE_SALES_TABLE}"
)
FACT_CITY_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_CITY_SALES_TABLE}"
)
FACT_PRODUCT_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_PRODUCT_SALES_TABLE}"
)
FACT_CATEGORY_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_CATEGORY_SALES_TABLE}"
)
FACT_PAYMENT_MODE_SALES_TABLE_NAME = (
    f"{CATALOG}.{GOLD_SCHEMA}.{FACT_PAYMENT_MODE_SALES_TABLE}"
)

# COMMAND ----------

SILVER_SALES_TABLE = (
    f"{CATALOG}.{SILVER_SCHEMA}.{SALES_TABLE}"
)