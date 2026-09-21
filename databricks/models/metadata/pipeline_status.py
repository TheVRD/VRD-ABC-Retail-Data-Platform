# Databricks notebook source
# ==========================================================
# Notebook Name      : pipeline_status
# Project            : ABC Retail Data Platform
# Purpose            : pipeline status Enum
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from enum import Enum

# COMMAND ----------

class PipelineStatus(str, Enum):
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"