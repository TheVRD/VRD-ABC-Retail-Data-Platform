# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_city_sales
# Project            : ABC Retail Data Platform
# Purpose            : city sales fact table genration notebook
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/gold_config

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

# COMMAND ----------

city_sales_df = aggregate_city_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=city_sales_df,
    table_name=FACT_CITY_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.gold.fact_city_sales order by total_revenue

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(DISTINCT storeCity) AS distinct_cities
# MAGIC FROM vrdworkspace1.gold.fact_city_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     storeCity,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM vrdworkspace1.gold.fact_city_sales
# MAGIC GROUP BY storeCity
# MAGIC HAVING COUNT(*) > 1;