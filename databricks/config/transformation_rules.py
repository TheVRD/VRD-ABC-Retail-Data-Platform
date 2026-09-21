# Databricks notebook source
# ==========================================================
# Notebook Name      : transformation_rules
# Project            : ABC Retail Data Platform
# Purpose            : sales transformation rules
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

SALES_TRIM_COLUMNS = (
    "customerName",
    "productName",
    "category",
    "paymentMode",
    "storeCity",
    "saleId",
    "customerId",
    "productId",
    "storeId"
    
)

# COMMAND ----------

SALES_UPPER_CASE_COLUMNS = (
    "paymentMode",
)

# COMMAND ----------

SALES_TITLE_CASE_COLUMNS = (
    "customerName",
    "productName",
    "category",
    "storeCity"
)