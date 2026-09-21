# Databricks notebook source
# ==========================================================
# Notebook Name      : file_processing_log
# Project            : ABC Retail Data Platform
# Purpose            : dataclass for file execution log
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from dataclasses import dataclass
from datetime import datetime

# COMMAND ----------

@dataclass(frozen=True)
class FileProcessingLog:
    file_path: str
    file_name: str
    pipeline_name: str
    data_entity: str
    environment: str
    processing_status: str
    start_timestamp: datetime
    execution_id: str
    end_timestamp: datetime | None = None
    rows_processed: int | None = None
    error_message: str | None = None

