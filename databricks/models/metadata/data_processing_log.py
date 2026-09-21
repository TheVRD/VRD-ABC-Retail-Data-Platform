# Databricks notebook source
from dataclasses import dataclass
from datetime import datetime

# COMMAND ----------

@dataclass(frozen=True)
class DataProcessingLog:

    source_file_path: str
    source_layer: str
    target_layer: str
    pipeline_name: str
    data_entity: str
    environment: str
    execution_id: str
    processing_status: str
    start_timestamp: datetime
    end_timestamp: datetime | None = None
    rows_processed: int | None = None
    error_message: str | None = None