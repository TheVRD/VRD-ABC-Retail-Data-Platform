# Databricks notebook source
from dataclasses import dataclass
from datetime import datetime

# COMMAND ----------

@dataclass(frozen=True)
class DataProcessingUpdate:
    execution_id: str
    source_file_path: str
    source_layer: str
    target_layer: str
    processing_status: str
    end_timestamp: datetime
    rows_processed: int | None = None
    error_message: str | None = None