# Databricks notebook source
from dataclasses import dataclass
from datetime import datetime

# COMMAND ----------

@dataclass(frozen=True)
class PipelineExecutionUpdate:
    execution_id: str
    status: str
    end_timestamp: datetime
    rows_processed: int | None = None
    error_message: str | None = None