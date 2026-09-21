# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_category_sales
# Project            : ABC Retail Data Platform
# Purpose            : category sales table creation
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/gold_config

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

# COMMAND ----------

category_sales_df = aggregate_category_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=category_sales_df,
    table_name=FACT_CATEGORY_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.gold.fact_category_sales