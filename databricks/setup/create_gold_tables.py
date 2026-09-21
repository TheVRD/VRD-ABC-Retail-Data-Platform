# Databricks notebook source
# ==========================================================
# Notebook Name      : create_gold_tables
# Project            : ABC Retail Data Platform
# Purpose            : creating schemas
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS vrdworkspace1.gold.fact_daily_sales
# MAGIC (
# MAGIC     processing_date DATE,
# MAGIC     total_orders BIGINT,
# MAGIC     total_quantity BIGINT,
# MAGIC     total_revenue BIGINT,
# MAGIC     average_order_value DOUBLE
# MAGIC )
# MAGIC USING DELTA;