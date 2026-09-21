# Databricks notebook source
# ==========================================================
# Notebook Name      : fact_payment_mode_sales
# Project            : ABC Retail Data Platform
# Purpose            : payment mode sales table creation
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/gold_config

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

# COMMAND ----------

payment_mode_sales_df = aggregate_payment_mode_sales(
    df=silver_df
)

# COMMAND ----------

write_delta_table(
    df=payment_mode_sales_df,
    table_name=FACT_PAYMENT_MODE_SALES_TABLE_NAME,
    mode=WriteMode.OVERWRITE
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.gold.fact_payment_mode_sales order by total_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_daily_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_store_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM vrdworkspace1.gold.fact_daily_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_city_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_product_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_category_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.gold.fact_payment_mode_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM vrdworkspace1.gold.fact_city_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM vrdworkspace1.gold.fact_product_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM vrdworkspace1.gold.fact_category_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM vrdworkspace1.gold.fact_payment_mode_sales;