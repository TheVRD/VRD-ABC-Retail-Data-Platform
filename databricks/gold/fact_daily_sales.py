# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_daily_sales
# Project            : ABC Retail Data Platform
# Purpose            : daily sales fact table
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/gold_config

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

# COMMAND ----------

daily_sales_df = aggregate_daily_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=daily_sales_df,
    table_name=FACT_DAILY_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.gold.fact_daily_sales
# MAGIC ORDER BY processing_date;