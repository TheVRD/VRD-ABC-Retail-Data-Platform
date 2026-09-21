# Databricks notebook source
# ==========================================================
# Notebook Name      : validation_rules
# Project            : ABC Retail Data Platform
# Purpose            : sales validation rules
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

SALES_REQUIRED_COLUMNS = (
    "saleId",
    "customerId",
    "productId",
    "storeId",
    "quantity",
    "unitPrice",
    "totalAmount",
    "saleTimeStamp"
)

# COMMAND ----------

SALES_PRIMARY_KEY_COLUMNS = (
    "saleId",
)

# COMMAND ----------

SALES_POSITIVE_NUMBER_COLUMNS = (
    "quantity",
    "unitPrice",
    "totalAmount"
)

# COMMAND ----------

ALLOWED_PAYMENT_MODES = (
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Gift Card",
    "Net Banking"
)