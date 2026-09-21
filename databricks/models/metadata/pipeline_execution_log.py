# Databricks notebook source
# ==========================================================
# Notebook Name      : pipeline_execution_log
# Project            : ABC Retail Data Platform
# Purpose            : dataclass for pipeline execution log
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from dataclasses import dataclass
from datetime import datetime, date

# COMMAND ----------

@dataclass(frozen=True)
class PipelineExecutionLog:
    execution_id: str
    pipeline_name: str
    notebook_name: str
    data_entity: str
    environment: str
    processing_date: date
    start_timestamp: datetime
    status: str
    end_timestamp: datetime | None = None
    rows_processed: int | None = None
    error_message: str | None = None
