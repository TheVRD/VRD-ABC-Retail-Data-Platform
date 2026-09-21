# Databricks notebook source
D%sql
SHOW TABLES IN vrdworkspace1.metadata;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE vrdworkspace1.metadata.pipeline_execution_log;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.metadata.pipeline_execution_log
# MAGIC order by processing_date DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.metadata.file_processing_log;

# COMMAND ----------

# MAGIC %run ../utils/logging_utils

# COMMAND ----------

file_path = (
    "abfss://datalake@stvrdde001.dfs.core.windows.net/"
    "landing/sales/2026/08/17/corrupt_sales.csv"
)

print(
    is_file_processed(
        file_path=file_path
    )
)

# COMMAND ----------

new_file_path = (
    "abfss://datalake@stvrdde001.dfs.core.windows.net/"
    "landing/sales/2026/08/18/new_sales.csv"
)

print(
    is_file_processed(
        file_path=new_file_path
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS vrdworkspace1.metadata.data_processing_log (
# MAGIC     source_file_path STRING,
# MAGIC     source_layer STRING,
# MAGIC     target_layer STRING,
# MAGIC     data_entity STRING,
# MAGIC     execution_id STRING,
# MAGIC     processing_status STRING,
# MAGIC     start_timestamp TIMESTAMP,
# MAGIC     end_timestamp TIMESTAMP,
# MAGIC     rows_processed BIGINT,
# MAGIC     error_message STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE vrdworkspace1.metadata.data_processing_log
# MAGIC ADD COLUMNS (
# MAGIC     pipeline_name STRING,
# MAGIC     environment STRING
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE vrdworkspace1.metadata.data_processing_log;