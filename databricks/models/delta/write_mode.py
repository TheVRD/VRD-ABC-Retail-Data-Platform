# Databricks notebook source
# ==========================================================
# Notebook Name      : write_mode
# Project            : ABC Retail Data Platform
# Purpose            : write mode Enum
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from enum import Enum

# COMMAND ----------

class WriteMode(str, Enum):
    APPEND = "append"
    OVERWRITE = "overwrite"