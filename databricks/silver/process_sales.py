# Databricks notebook source
# ==========================================================
# Notebook Name      : process_sales
# Project            : ABC Retail Data Platform
# Purpose            : processing sales data after applying different validators
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

dbutils.widgets.text("processing_date", "")

processing_date = dbutils.widgets.get("processing_date")

if not processing_date:
    raise ValueError("processing_date parameter is required from ADF")

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

# MAGIC %run ../utils/delta_utils

# COMMAND ----------

# MAGIC %run ../utils/logging_utils

# COMMAND ----------

# MAGIC %run ../validation/sales_validation

# COMMAND ----------

# MAGIC %run ../transformations/sales_transformation

# COMMAND ----------

# MAGIC %run ../models/delta/write_mode

# COMMAND ----------

BRONZE_SALES_TABLE = (
    f"{CATALOG}.{BRONZE_SCHEMA}.{SALES_RAW_TABLE}"
)
SILVER_SALES_TABLE = (
    f"{CATALOG}.{SILVER_SCHEMA}.{SALES_TABLE}"
)
QUARANTINE_SALES_TABLE = (
    f"{CATALOG}.{QUARANTINE_SCHEMA}.{SALES_QUARANTINE_TABLE}"
)

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

execution_id = log_pipeline_start(
    pipeline_name=PIPELINE_NAME,
    notebook_name="process_sales",
    data_entity=DATA_ENTITY
)

# COMMAND ----------

try:

    # --------------------------------------------------
    # 1. Identify files pending Bronze → Silver
    # --------------------------------------------------

    pending_files_df = get_pending_files(
        source_layer=BRONZE_LAYER,
        target_layer=SILVER_LAYER,
        data_entity=DATA_ENTITY
    )

    pending_files = [
        row["source_file_path"]
        for row in pending_files_df.collect()
    ]

    print(f"Pending files: {len(pending_files)}")

    # --------------------------------------------------
    # 2. Nothing to process
    # --------------------------------------------------

    total_rows_processed = 0

    if not pending_files:
        print("No new files to process.")

    else:

        # --------------------------------------------------
        # 3. Read only pending Bronze records
        # --------------------------------------------------

        bronze_df = (
            read_delta_table(
                table_name=BRONZE_SALES_TABLE
            )
            .filter(
                col("source_file_path").isin(pending_files)
            )
        )

        # --------------------------------------------------
        # 4. Process each pending file
        # --------------------------------------------------

        for source_file_path in pending_files:

            log_data_processing_start(
                execution_id=execution_id,
                source_file_path=source_file_path,
                source_layer=BRONZE_LAYER,
                target_layer=SILVER_LAYER,
                pipeline_name=PIPELINE_NAME,
                data_entity=DATA_ENTITY
            )

            try:

                source_df = (
                    bronze_df
                    .filter(
                        col("source_file_path") == source_file_path
                    )
                )

                rows_read = source_df.count()

                print(
                    f"Processing file: {source_file_path}"
                )

                print(
                    f"Rows read: {rows_read}"
                )

                valid_df, invalid_df = validate_sales(
                    sales_df=source_df
                )

                print("Validation complete")

                transformed_df = transform_sales(
                    sales_df=valid_df
                )

                print("Transformation complete")

                rows_processed = transformed_df.count()

                write_delta_table(
                    df=transformed_df,
                    table_name=SILVER_SALES_TABLE,
                    mode=WriteMode.APPEND
                )

                if not invalid_df.isEmpty():

                    write_delta_table(
                        df=invalid_df,
                        table_name=QUARANTINE_SALES_TABLE,
                        mode=WriteMode.APPEND
                    )

                log_data_processing_end(
                    execution_id=execution_id,
                    source_file_path=source_file_path,
                    source_layer=BRONZE_LAYER,
                    target_layer=SILVER_LAYER,
                    status=SUCCESS_STATUS,
                    rows_processed=rows_processed
                )

                total_rows_processed += rows_processed

            except Exception as e:

                log_data_processing_end(
                    execution_id=execution_id,
                    source_file_path=source_file_path,
                    source_layer=BRONZE_LAYER,
                    target_layer=SILVER_LAYER,
                    status=FAILED_STATUS,
                    error_message=str(e)
                )

                raise

    log_pipeline_end(
        execution_id=execution_id,
        status=SUCCESS_STATUS,
        rows_processed=total_rows_processed
    )

except Exception as e:

    log_pipeline_end(
        execution_id=execution_id,
        status=FAILED_STATUS,
        error_message=str(e)
    )

    raise

# COMMAND ----------

if ENVIRONMENT == "DEV":
    print("Sales processing completed successfully.")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.metadata.data_processing_log where source_file_path = "abfss://datalake@stvrdde001.dfs.core.windows.net/landing/sales/2026/09/19/corrupt_sales.csv"

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.quarantine.sales_quarantine;

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from vrdworkspace1.quarantine.sales_quarantine;

# COMMAND ----------

pending_files_df = get_pending_files(
    source_layer="bronze",
    target_layer="silver",
    data_entity="sales"
)

pending_files_df.show(truncate=False)

# COMMAND ----------

pending_files_df.count()

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM vrdworkspace1.silver.sales;