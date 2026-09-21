# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_product_sales
# Project            : ABC Retail Data Platform
# Purpose            : product sales table creation
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/gold_config

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

# COMMAND ----------

product_sales_df = aggregate_product_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=product_sales_df,
    table_name=FACT_PRODUCT_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.gold.fact_product_sales order by productId