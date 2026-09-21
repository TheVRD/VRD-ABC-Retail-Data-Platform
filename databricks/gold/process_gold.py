# Databricks notebook source
# ==========================================================
# Notebook Name      : process_gold
# Project            : ABC Retail Data Platform
# Purpose            : orchastration function for gold layer
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

dbutils.widgets.text("processing_date", "")

processing_date = dbutils.widgets.get("processing_date")

if not processing_date:
    raise ValueError("processing_date parameter is required from ADF")

# COMMAND ----------

print("Creating fact daily sales")

# COMMAND ----------

# MAGIC %run  ./fact_daily_sales

# COMMAND ----------

print("creating store sales")

# COMMAND ----------

# MAGIC %run ./fact_store_sales

# COMMAND ----------

print("creating product sales")

# COMMAND ----------

# MAGIC %run ./fact_product_sales

# COMMAND ----------

print("creating city sales")

# COMMAND ----------

# MAGIC %run ./fact_city_sales

# COMMAND ----------

print("creating category sales")

# COMMAND ----------

# MAGIC %run ./fact_category_sales

# COMMAND ----------

print("creating payment mode sales")

# COMMAND ----------

# MAGIC %run ./fact_payment_mode_sales