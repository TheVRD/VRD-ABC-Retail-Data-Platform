# Databricks notebook source
# ==========================================================
# Notebook Name      : ingest_sales
# Project            : ABC Retail Data Platform
# Purpose            : ingestion of sales data from landing zone to bronze zone
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

dbutils.widgets.text("processing_date", "")

processing_date = dbutils.widgets.get("processing_date")

if not processing_date:
    raise ValueError("processing_date parameter is required from ADF")

# COMMAND ----------

# MAGIC %run ../config/bronze_config

# COMMAND ----------

execution_id = log_pipeline_start(
    pipeline_name=pipeline_name,
    notebook_name="ingest_sales",
    data_entity="sales"
)

# COMMAND ----------

try:

    if is_data_processed(
        source_file_path=sales_file_path,
        source_layer=LANDING_LAYER,
        target_layer=BRONZE_LAYER,
        data_entity=DATA_ENTITY
    ):
        print(
            f"File already processed. Skipping: "
            f"{sales_file_path}"
        )

    else:

        file_name = sales_file_path.split("/")[-1]

        log_data_processing_start(
            execution_id=execution_id,
            source_file_path=sales_file_path,
            source_layer=LANDING_LAYER,
            target_layer=BRONZE_LAYER,
            pipeline_name=pipeline_name,
            data_entity=DATA_ENTITY
        )

        sales_df = read_csv(
            path=sales_file_path
        )

        sales_df = add_metadata_columns(
            df=sales_df,
            processing_date=processing_date,
            pipeline_name=pipeline_name
        )

        rows_processed = sales_df.count()

        write_delta_table(
            df=sales_df,
            table_name=BRONZE_SALES_TABLE,
            mode=WriteMode.APPEND
        )

        log_data_processing_end(
            execution_id=execution_id,
            source_file_path=sales_file_path,
            source_layer=LANDING_LAYER,
            target_layer=BRONZE_LAYER,
            status=SUCCESS_STATUS,
            rows_processed=rows_processed
        )

        if ENVIRONMENT == "DEV":
            print(f"rows read: {rows_processed}")
            print(f"Landing: {sales_landing_path}")
            print("ingestion completed successfully")

        log_pipeline_end(
            execution_id=execution_id,
            status=SUCCESS_STATUS
        )

except Exception as e:

    error_message = str(e)

    log_file_end(
        execution_id=execution_id,
        source_file_path=sales_file_path,
        source_layer=LANDING_LAYER,
        target_layer=BRONZE_LAYER,
        status=FAILED_STATUS,
        error_message=str(e)
    )

    log_pipeline_end(
        execution_id=execution_id,
        status=FAILED_STATUS,
        error_message=error_message
    )

    raise

# COMMAND ----------

dbutils.secrets.get(
    scope="abc-retail-secrets",
    key="storage-account-key"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.metadata.data_processing_log;

# COMMAND ----------

# MAGIC %sql
# MAGIC describe vrdworkspace1.bronze.sales_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from vrdworkspace1.bronze.sales_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC select source_file_path, count(*) from vrdworkspace1.bronze.sales_raw
# MAGIC group by source_file_path;