# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_store_sales
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

store_sales_df = aggregate_store_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=store_sales_df,
    table_name=FACT_STORE_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.gold.fact_store_sales order by storeId, storeCity

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     storeId,
# MAGIC     COUNT(DISTINCT storeCity) AS city_count
# MAGIC FROM vrdworkspace1.silver.sales
# MAGIC GROUP BY storeId
# MAGIC HAVING COUNT(DISTINCT storeCity) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(DISTINCT storeId) AS distinct_stores
# MAGIC FROM vrdworkspace1.gold.fact_store_sales;