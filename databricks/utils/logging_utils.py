# Databricks notebook source
# ==========================================================
# Notebook Name      : logging_utils
# Project            : ABC Retail Data Platform
# Purpose            : Logging utility functions for this project
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC
# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../models/metadata/pipeline_execution_log

# COMMAND ----------

# MAGIC %run ../models/metadata/pipeline_status

# COMMAND ----------

# MAGIC %run ../models/metadata/pipeline_execution_update

# COMMAND ----------

# MAGIC %run ../models/metadata/data_processing_update

# COMMAND ----------

# MAGIC %run ../models/metadata/file_processing_log

# COMMAND ----------

# MAGIC %run ../models/metadata/data_processing_log

# COMMAND ----------

# MAGIC %run ../models/delta/write_mode

# COMMAND ----------

# MAGIC %run ./dataframe_utils

# COMMAND ----------

# MAGIC %run ./delta_utils

# COMMAND ----------

import uuid
from datetime import datetime, UTC
from delta.tables import DeltaTable
from pyspark.sql import DataFrame

# COMMAND ----------

from dataclasses import fields
from datetime import date, datetime
from types import UnionType
from typing import Union, get_args, get_origin

# COMMAND ----------

from dataclasses import asdict, is_dataclass

# COMMAND ----------

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DateType,
    TimestampType,
    LongType
)

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

def dataclass_to_schema(dataclass_type) -> StructType:
    """
    Converts a dataclass definition into a Spark StructType.
    """

    if not isinstance(dataclass_type, type):
        raise TypeError("dataclass_type must be a dataclass type")

    schema_fields = []

    for field in fields(dataclass_type):

        field_type = field.type
        nullable = False

        origin = get_origin(field_type)

        if origin in (Union, UnionType):
            args = get_args(field_type)

            non_none = [
                arg
                for arg in args
                if arg is not type(None)
            ]

            field_type = non_none[0]
            nullable = True

        if field_type is str:
            spark_type = StringType()

        elif field_type is int:
            spark_type = LongType()

        elif field_type is datetime:
            spark_type = TimestampType()

        elif field_type is date:
            spark_type = DateType()

        else:
            raise TypeError(
                f"Unsupported datatype: {field_type}"
            )

        schema_fields.append(
            StructField(
                field.name,
                spark_type,
                nullable
            )
        )

    return StructType(schema_fields)

# COMMAND ----------

def dataclass_to_dataframe(
    dataclass_object
) -> DataFrame:
    """
    Converts a dataclass object to a Spark DataFrame.
    """

    if dataclass_object is None:
        raise ValueError(
            "dataclass_object cannot be None"
        )

    if not is_dataclass(dataclass_object):
        raise TypeError(
            "dataclass_object must be a dataclass object"
        )

    object_dict = asdict(dataclass_object)

    schema = dataclass_to_schema(
        type(dataclass_object)
    )

    return spark.createDataFrame(
        [object_dict],
        schema=schema
    )

# COMMAND ----------

def log_pipeline_start(
    *,
    pipeline_name: str,
    notebook_name: str,
    data_entity: str
) -> str:
    """
    Log the start of a pipeline run
    Parameters
    ----------
    pipeline_name : str
        Name of the pipeline
    notbook_name : str
        Name of the notebook
    data_entity : str
        Name of the data entity
    Returns
    -------
    str
        execution id of the run
    """

    if not isinstance(pipeline_name, str):
        raise TypeError("pipeline_name must be a string")

    if not isinstance(notebook_name, str):
        raise TypeError("notebook_name must be a string")

    if not isinstance(data_entity, str):
        raise TypeError("data_entity must be a string")

    if not pipeline_name:
        raise ValueError("pipeline_name cannot be empty")

    if not notebook_name:
        raise ValueError("notebook_name cannot be empty")

    if not data_entity:
        raise ValueError("data_entity cannot be empty") 

    execution_id = str(uuid.uuid4())

    environment = ENVIRONMENT #spark.conf.get("project.environment") this value is from spark conf when we are not running conf notebook

    processing_date = PROCESSING_DATE

    start_timestamp = datetime.now(UTC)

    pipeline_log_table_name = f"{CATALOG}.{METADATA_SCHEMA}.{PIPELINE_LOG_TABLE}"

    execution_log = PipelineExecutionLog(
        execution_id = execution_id,
        pipeline_name = pipeline_name,
        notebook_name = notebook_name,
        data_entity = data_entity,
        environment = environment,
        processing_date = processing_date,
        start_timestamp = start_timestamp,
        status = STARTED_STATUS,
        end_timestamp = None,
        rows_processed = None,
        error_message = None
     )

    log_df = dataclass_to_dataframe(
        execution_log
    )
    #log_df.printSchema()
    spark.table(f"{CATALOG}.{METADATA_SCHEMA}.{PIPELINE_LOG_TABLE}").printSchema()

    write_delta_table(
        log_df,
        pipeline_log_table_name,
        WriteMode.APPEND
    )

    return execution_id

# COMMAND ----------

def _build_pipeline_end_dataframe(
    *,
    execution_id: str,
    status: str,
    rows_processed: int | None,
    error_message: str | None,
    end_timestamp: datetime
) -> DataFrame:
    """
    Helper function to build a dataframe with the end of a pipeline run
    Parameters
    ----------
    execution_id : str
        Execution id of the run
    status : PipelineStatus
        Status of the run
    rows_processed : int, optional
        Number of rows processed, by default None
    error_message : str
        Error message, by default None
    end_timestamp : datetime
        End timestamp of the run
    Returns
    -------
    DataFrame
        Dataframe with the end of a pipeline run
    """

    update = PipelineExecutionUpdate(
        execution_id=execution_id,
        status=status,
        end_timestamp=end_timestamp,
        rows_processed=rows_processed,
        error_message=error_message
    )

    return dataclass_to_dataframe(update)

# COMMAND ----------

def log_pipeline_end(
    *,
    execution_id: str,
    status: str,
    rows_processed: int | None = None,
    error_message: str | None = None
) -> None:
    """
    Log the end of a pipeline run
    Parameters
    ----------
    execution_id : str
        Execution id of the run
    status : PipelineStatus
        Status of the run
    rows_processed : int, optional
        Number of rows processed, by default None
    error_message : str, optional
        Error message, by default None
    Returns
    -------
    None
    """

    if not isinstance(execution_id, str):
        raise TypeError("execution_id must be a string")

    if error_message is not None and not isinstance(error_message, str):
        raise TypeError("error_message must be a string or None")

    if not execution_id:
        raise ValueError("execution_id cannot be empty")

    if rows_processed is not None and rows_processed < 0:
        raise ValueError("rows_processed cannot be negative")



    pipeline_log_table_name = f"{CATALOG}.{METADATA_SCHEMA}.{PIPELINE_LOG_TABLE}"

    end_timestamp = datetime.now(UTC)

    update_df = _build_pipeline_end_dataframe(
        execution_id = execution_id,
        status = status,
        rows_processed = rows_processed,
        error_message = error_message,
        end_timestamp = end_timestamp
    )
    
    delta_table = DeltaTable.forName(
        spark,
        pipeline_log_table_name
    )

    (
        delta_table.alias("target")
        .merge(
            source = update_df.alias("source"),
            condition = "target.execution_id = source.execution_id"
        )
        .whenMatchedUpdate(
            set = {
                "status": "source.status",
                "end_timestamp": "source.end_timestamp",
                "rows_processed": "source.rows_processed",
                "error_message": "source.error_message"
            }
        )
        .execute()
    )

# COMMAND ----------

def log_data_processing_start(
    *,
    source_file_path: str,
    source_layer: str,
    target_layer: str,
    pipeline_name: str,
    data_entity: str,
    execution_id: str
) -> None:
    """
    Logs the start of processing for a source file.

    Parameters
    ----------
    execution_id : str
        Execution ID of the parent pipeline run.
    file_path : str
        Full path of the source file.
    file_name : str
        Name of the source file.
    pipeline_name : str
        Name of the pipeline processing the file.
    data_entity : str
        Data entity being processed.
    """

    if not isinstance(execution_id, str):
        raise TypeError("execution_id must be a string")

    if not isinstance(pipeline_name, str):
        raise TypeError("pipeline_name must be a string")

    if not isinstance(data_entity, str):
        raise TypeError("data_entity must be a string")

    if not execution_id.strip():
        raise ValueError("execution_id cannot be empty")

    if not pipeline_name.strip():
        raise ValueError("pipeline_name cannot be empty")

    if not data_entity.strip():
        raise ValueError("data_entity cannot be empty")

    environment = ENVIRONMENT
    start_timestamp = datetime.now(UTC)

    data_log_table_name = (
        f"{CATALOG}.{METADATA_SCHEMA}.{DATA_PROCESSING_LOG_TABLE}"
    )

    data_processing_log =DataProcessingLog(
        source_file_path=source_file_path,
        source_layer=source_layer,
        target_layer=target_layer,
        pipeline_name=pipeline_name,
        data_entity=data_entity,
        environment=environment,
        execution_id=execution_id,
        processing_status=STARTED_STATUS,
        start_timestamp=start_timestamp,
        end_timestamp=None,
        rows_processed=None,
        error_message=None

    )

    log_df = dataclass_to_dataframe(
        data_processing_log
    )

    write_delta_table(
        df=log_df,
        table_name=data_log_table_name,
        mode=WriteMode.APPEND
    )

# COMMAND ----------

def log_data_processing_end(
    *,
    execution_id: str,
    source_file_path: str,
    source_layer: str,
    target_layer: str,
    status: str,
    rows_processed: int | None = None,
    error_message: str | None = None
) -> None:
    """
    Logs the completion of processing for a source file.

    Parameters
    ----------
    execution_id : str
        Execution ID of the parent pipeline run.
    file_path : str
        Full path of the source file.
    status : str
        Final processing status.
    rows_processed : int, optional
        Number of rows processed.
    error_message : str, optional
        Error message when processing fails.
    """

    if not isinstance(execution_id, str):
        raise TypeError("execution_id must be a string")

    if not isinstance(status, str):
        raise TypeError("status must be a string")

    if error_message is not None and not isinstance(error_message, str):
        raise TypeError("error_message must be a string or None")

    if not execution_id.strip():
        raise ValueError("execution_id cannot be empty")

    if not status.strip():
        raise ValueError("status cannot be empty")

    if rows_processed is not None and rows_processed < 0:
        raise ValueError("rows_processed cannot be negative")

    data_log_table_name = (
        f"{CATALOG}.{METADATA_SCHEMA}.{DATA_PROCESSING_LOG_TABLE}"
    )

    end_timestamp = datetime.now(UTC)

    update = DataProcessingUpdate(
        execution_id=execution_id,
        source_file_path=source_file_path,
        source_layer=source_layer,
        target_layer=target_layer,
        processing_status=status,
        end_timestamp=end_timestamp,
        rows_processed=rows_processed,
        error_message=error_message
    )
    update_df = dataclass_to_dataframe(update)
    merge_condition = """
                target.execution_id = source.execution_id
                AND target.source_file_path = source.source_file_path
                AND target.source_layer = source.source_layer
                AND target.target_layer = source.target_layer
                """


    delta_table = DeltaTable.forName(
        spark,
        data_log_table_name
    )

    (
        delta_table.alias("target")
        .merge(
            source=update_df.alias("source"),
            condition=merge_condition
        )
        .whenMatchedUpdate(
            set={
                "processing_status": "source.processing_status",
                "end_timestamp": "source.end_timestamp",
                "rows_processed": "source.rows_processed",
                "error_message": "source.error_message"
            }
        )
        .execute()
    )

# COMMAND ----------

def is_data_processed(
    *,
    source_file_path: str,
    source_layer: str,
    target_layer: str,
    data_entity: str
) -> bool:

    if not isinstance(source_file_path, str):
        raise TypeError(
            "source_file_path must be a string"
        )

    if not isinstance(source_layer, str):
        raise TypeError(
            "source_layer must be a string"
        )

    if not isinstance(target_layer, str):
        raise TypeError(
            "target_layer must be a string"
        )

    if not isinstance(data_entity, str):
        raise TypeError(
            "data_entity must be a string"
        )

    if not source_file_path:
        raise ValueError(
            "source_file_path cannot be empty"
        )

    if not source_layer:
        raise ValueError(
            "source_layer cannot be empty"
        )

    if not target_layer:
        raise ValueError(
            "target_layer cannot be empty"
        )

    if not data_entity:
        raise ValueError(
            "data_entity cannot be empty"
        )

    processing_log_table = (
        f"{CATALOG}."
        f"{METADATA_SCHEMA}."
        f"{DATA_PROCESSING_LOG_TABLE}"
    )

    return (
        spark.table(processing_log_table)
        .filter(
            (col("source_file_path") == source_file_path)
            & (col("source_layer") == source_layer)
            & (col("target_layer") == target_layer)
            & (col("data_entity") == data_entity)
            & (col("processing_status") == SUCCESS_STATUS)
        )
        .limit(1)
        .count()
        > 0
    )

# COMMAND ----------

def log_file_start(
    *,
    execution_id: str,
    file_path: str,
    file_name: str,
    pipeline_name: str,
    data_entity: str
) -> None:
    """
    Logs the start of processing for a source file.

    Parameters
    ----------
    execution_id : str
        Execution ID of the parent pipeline run.
    file_path : str
        Full path of the source file.
    file_name : str
        Name of the source file.
    pipeline_name : str
        Name of the pipeline processing the file.
    data_entity : str
        Data entity being processed.
    """

    if not isinstance(execution_id, str):
        raise TypeError("execution_id must be a string")

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")

    if not isinstance(pipeline_name, str):
        raise TypeError("pipeline_name must be a string")

    if not isinstance(data_entity, str):
        raise TypeError("data_entity must be a string")

    if not execution_id.strip():
        raise ValueError("execution_id cannot be empty")

    if not file_path.strip():
        raise ValueError("file_path cannot be empty")

    if not file_name.strip():
        raise ValueError("file_name cannot be empty")

    if not pipeline_name.strip():
        raise ValueError("pipeline_name cannot be empty")

    if not data_entity.strip():
        raise ValueError("data_entity cannot be empty")

    environment = ENVIRONMENT
    start_timestamp = datetime.now(UTC)

    file_log_table_name = (
        f"{CATALOG}.{METADATA_SCHEMA}.{FILE_PROCESSING_LOG_TABLE}"
    )

    file_processing_log = FileProcessingLog(
        file_path=file_path,
        file_name=file_name,
        pipeline_name=pipeline_name,
        data_entity=data_entity,
        environment=environment,
        processing_status=STARTED_STATUS,
        start_timestamp=start_timestamp,
        execution_id=execution_id,
        end_timestamp=None,
        rows_processed=None,
        error_message=None
    )

    log_df = dataclass_to_dataframe(
        file_processing_log
    )

    write_delta_table(
        df=log_df,
        table_name=file_log_table_name,
        mode=WriteMode.APPEND
    )

# COMMAND ----------

def log_file_end(
    *,
    execution_id: str,
    file_path: str,
    status: str,
    rows_processed: int | None = None,
    error_message: str | None = None
) -> None:
    """
    Logs the completion of processing for a source file.

    Parameters
    ----------
    execution_id : str
        Execution ID of the parent pipeline run.
    file_path : str
        Full path of the source file.
    status : str
        Final processing status.
    rows_processed : int, optional
        Number of rows processed.
    error_message : str, optional
        Error message when processing fails.
    """

    if not isinstance(execution_id, str):
        raise TypeError("execution_id must be a string")

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not isinstance(status, str):
        raise TypeError("status must be a string")

    if error_message is not None and not isinstance(error_message, str):
        raise TypeError("error_message must be a string or None")

    if not execution_id.strip():
        raise ValueError("execution_id cannot be empty")

    if not file_path.strip():
        raise ValueError("file_path cannot be empty")

    if not status.strip():
        raise ValueError("status cannot be empty")

    if rows_processed is not None and rows_processed < 0:
        raise ValueError("rows_processed cannot be negative")

    file_log_table_name = (
        f"{CATALOG}.{METADATA_SCHEMA}.{FILE_PROCESSING_LOG_TABLE}"
    )

    end_timestamp = datetime.now(UTC)

    update = FileProcessingUpdate(
        execution_id=execution_id,
        file_path=file_path,
        processing_status=status,
        end_timestamp=end_timestamp,
        rows_processed=rows_processed,
        error_message=error_message
    )
    update_df = dataclass_to_dataframe(update)


    delta_table = DeltaTable.forName(
        spark,
        file_log_table_name
    )

    (
        delta_table.alias("target")
        .merge(
            source=update_df.alias("source"),
            condition="""
                target.execution_id = source.execution_id
                AND target.file_path = source.file_path
            """
        )
        .whenMatchedUpdate(
            set={
                "processing_status": "source.processing_status",
                "end_timestamp": "source.end_timestamp",
                "rows_processed": "source.rows_processed",
                "error_message": "source.error_message"
            }
        )
        .execute()
    )

# COMMAND ----------

def is_file_processed(
    *,
    file_path: str
) -> bool:
    """
    Checks whether a file has already been successfully processed.

    Parameters
    ----------
    file_path : str
        Full path of the source file.

    Returns
    -------
    bool
        True if the file has a successful processing record,
        otherwise False.
    """

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not file_path.strip():
        raise ValueError("file_path cannot be empty")

    file_log_table_name = (
        f"{CATALOG}.{METADATA_SCHEMA}.{FILE_PROCESSING_LOG_TABLE}"
    )

    processed_file_df = (
        spark.table(file_log_table_name)
        .filter(
            (col("file_path") == file_path)
            & (col("processing_status") == SUCCESS_STATUS)
        )
        .limit(1)
    )

    return processed_file_df.count() > 0

# COMMAND ----------

def get_pending_files(
    *,
    source_layer: str,
    target_layer: str,
    data_entity: str
) -> DataFrame:

    if not source_layer:
        raise ValueError("Source layer cannot be empty.")

    if not target_layer:
        raise ValueError("Target layer cannot be empty.")

    if not data_entity:
        raise ValueError("Data entity cannot be empty.")

    processing_log_table = (
        f"{CATALOG}.{METADATA_SCHEMA}.{DATA_PROCESSING_LOG_TABLE}"
    )

    processing_log_df = read_delta_table(
        table_name=processing_log_table
    )

    # Files that successfully reached the source layer
    source_success_df = (
        processing_log_df
        .filter(
            (col("source_layer") == "landing") &
            (col("target_layer") == source_layer) &
            (col("data_entity") == data_entity) &
            (col("processing_status") == SUCCESS_STATUS)
        )
        .select("source_file_path")
        .distinct()
    )

    # Files that successfully reached the target layer
    target_success_df = (
        processing_log_df
        .filter(
            (col("source_layer") == source_layer) &
            (col("target_layer") == target_layer) &
            (col("data_entity") == data_entity) &
            (col("processing_status") == SUCCESS_STATUS)
        )
        .select("source_file_path")
        .distinct()
    )

    # Files successfully present in source layer
    # but not successfully processed into target layer
    pending_files_df = (
        source_success_df
        .join(
            target_success_df,
            on="source_file_path",
            how="left_anti"
        )
    )

    return pending_files_df