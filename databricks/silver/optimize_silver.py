# Databricks notebook source
# MAGIC %md
# MAGIC **OPTIMIZE**

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     storeId,
# MAGIC     SUM(totalAmount) AS total_revenue
# MAGIC FROM vrdworkspace1.silver.sales
# MAGIC GROUP BY storeId;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC OPTIMIZE vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     storeId,
# MAGIC     SUM(totalAmount) AS total_revenue
# MAGIC FROM vrdworkspace1.silver.sales
# MAGIC GROUP BY storeId;

# COMMAND ----------

# MAGIC %md
# MAGIC **Data Skipping + Z-Order / Clustering**

# COMMAND ----------

#Cardiniality

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT storeId) AS distinct_stores,
# MAGIC     COUNT(DISTINCT storeCity) AS distinct_cities,
# MAGIC     COUNT(DISTINCT productId) AS distinct_products,
# MAGIC     COUNT(DISTINCT category) AS distinct_categories,
# MAGIC     COUNT(DISTINCT paymentMode) AS distinct_payment_modes,
# MAGIC     COUNT(DISTINCT customerId) AS distinct_customers
# MAGIC FROM vrdworkspace1.silver.sales;

# COMMAND ----------

#Data Range

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     MIN(saleTimeStamp) AS min_sale_timestamp,
# MAGIC     MAX(saleTimeStamp) AS max_sale_timestamp
# MAGIC FROM vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN FORMATTED
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %run ../utils/delta_utils

# COMMAND ----------

silver_df = read_delta_table(
    table_name="vrdworkspace1.silver.sales"
)

(
    silver_df
    .repartition(20)
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "vrdworkspace1.silver.sales_optimization_test"
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales_optimization_test;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN FORMATTED
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     source_file_path,
# MAGIC     COUNT(*) AS rows,
# MAGIC     COUNT(DISTINCT customerId) AS distinct_customers
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test
# MAGIC GROUP BY source_file_path
# MAGIC ORDER BY source_file_path;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     customerId,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test
# MAGIC WHERE customerId = 'CUS02416'
# MAGIC GROUP BY customerId;

# COMMAND ----------

from pyspark.sql.functions import spark_partition_id

silver_df = read_delta_table(
    table_name="vrdworkspace1.silver.sales_optimization_test"
)

(
    silver_df
    .repartition(100)
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "vrdworkspace1.silver.sales_optimization_test_100"
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT customerId) AS distinct_customers
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC EXPLAIN FORMATTED
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     customerId,
# MAGIC     COUNT(*) AS rows
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC WHERE customerId = 'CUS02416'
# MAGIC GROUP BY customerId;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     source_file_path,
# MAGIC     COUNT(*) AS rows,
# MAGIC     COUNT(DISTINCT customerId) AS distinct_customers
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC GROUP BY source_file_path
# MAGIC ORDER BY source_file_path;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE vrdworkspace1.silver.sales_optimization_test_100
# MAGIC ZORDER BY (customerId);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY
# MAGIC vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL vrdworkspace1.silver.sales_optimization_test_100 VERSION AS OF 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC VERSION AS OF 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC delete from vrdworkspace1.silver.sales_optimization_test_100 where customerId = 'CUS02416'

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) as totalrows from vrdworkspace1.silver.sales_optimization_test_100

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from vrdworkspace1.silver.sales_optimization_test_100
# MAGIC version as of 1
# MAGIC where customerId = 'CUS02416'

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TBLPROPERTIES
# MAGIC vrdworkspace1.silver.sales_optimization_test_100;

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC DRY RUN;

# COMMAND ----------

# MAGIC %sql
# MAGIC REORG TABLE vrdworkspace1.silver.sales_optimization_test_100
# MAGIC APPLY (PURGE);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS historical_rows
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC VERSION AS OF 1
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS current_rows
# MAGIC FROM vrdworkspace1.silver.sales_optimization_test_100
# MAGIC WHERE customerId = 'CUS02416';

# COMMAND ----------

# MAGIC %md
# MAGIC **SCD2 TYPE 2 TEST**

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE vrdworkspace1.silver.customer_scd2_test (
# MAGIC     customerId STRING,
# MAGIC     customerName STRING,
# MAGIC     city STRING,
# MAGIC     effective_from TIMESTAMP,
# MAGIC     effective_to TIMESTAMP,
# MAGIC     is_current BOOLEAN
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO vrdworkspace1.silver.customer_scd2_test
# MAGIC VALUES
# MAGIC     ('CUS001', 'Rahul Sharma', 'Delhi',
# MAGIC      TIMESTAMP('2026-09-01 00:00:00'),
# MAGIC      TIMESTAMP('9999-12-31 00:00:00'),
# MAGIC      true),
# MAGIC
# MAGIC     ('CUS002', 'Amit Kumar', 'Mumbai',
# MAGIC      TIMESTAMP('2026-09-01 00:00:00'),
# MAGIC      TIMESTAMP('9999-12-31 00:00:00'),
# MAGIC      true),
# MAGIC
# MAGIC     ('CUS003', 'Priya Singh', 'Noida',
# MAGIC      TIMESTAMP('2026-09-01 00:00:00'),
# MAGIC      TIMESTAMP('9999-12-31 00:00:00'),
# MAGIC      true);

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vrdworkspace1.silver.customer_scd2_test
# MAGIC order by customerId

# COMMAND ----------

from pyspark.sql import functions as F

incoming_data = [
    ("CUS001", "Rahul Sharma", "Noida"),
    ("CUS002", "Amit Kumar", "Mumbai"),
    ("CUS004", "Neha Verma", "Delhi")
]

incoming_df = spark.createDataFrame(
    incoming_data,
    ["customerId", "customerName", "city"]
).withColumn(
    "change_timestamp",
    F.lit("2026-09-18 10:00:00").cast("timestamp")
)

display(incoming_df)

# COMMAND ----------

# MAGIC %run ../utils/scd2_utils

# COMMAND ----------

target_df = spark.table(
    "vrdworkspace1.silver.customer_scd2_test"
)

display(target_df)

# COMMAND ----------

current_target_df = target_df.filter(
    F.col("is_current") == True
)

comparison_df = (
    incoming_df.alias("source")
    .join(
        current_target_df.alias("target"),
        F.col("source.customerId") == F.col("target.customerId"),
        "left"
    )
)

# COMMAND ----------

change_condition = build_scd2_change_condition(
    ["customerName", "city"]
)

# COMMAND ----------

result_df = comparison_df.select(
    F.col("source.customerId").alias("customerId"),

    F.col("source.customerName").alias("source_name"),
    F.col("target.customerName").alias("target_name"),

    F.col("source.city").alias("source_city"),
    F.col("target.city").alias("target_city"),

    F.col("target.customerId").isNotNull().alias("customer_exists"),

    change_condition.alias("change_detected")
)

# COMMAND ----------

result_df = (
    result_df
    .withColumn(
        "is_new_customer",
        ~F.col("customer_exists")
    )
    .withColumn(
        "is_existing_changed",
        F.col("customer_exists") &
        F.col("change_detected")
    )
)

display(result_df)

# COMMAND ----------

validate_scd2_source_uniqueness(
    source_df=incoming_df,
    business_key="customerId"
)

# COMMAND ----------

duplicate_data = [
    ("CUS001", "Rahul Sharma", "Noida"),
    ("CUS001", "Rahul Sharma", "Bangalore"),
    ("CUS002", "Amit Kumar", "Mumbai")
]

duplicate_df = spark.createDataFrame(
    duplicate_data,
    ["customerId", "customerName", "city"]
)

# COMMAND ----------

validate_scd2_source_uniqueness(
    source_df=duplicate_df,
    business_key="customerId"
)

# COMMAND ----------

merge_source_df = prepare_scd2_merge_source(
    source_df=incoming_df,
    target_df=target_df,
    business_key="customerId",
    tracked_columns=[
        "customerName",
        "city"
    ],
    change_timestamp_column="change_timestamp"
)

display(
    merge_source_df.orderBy(
        "customerId",
        "action"
    )
)

# COMMAND ----------

SCD2_TRACKED_COLUMNS = [
    "customerName",
    "city"
]

# COMMAND ----------

apply_scd2_merge(
    target_table_name="vrdworkspace1.silver.customer_scd2_test",
    merge_source_df=merge_source_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS
)

# COMMAND ----------

display(
    spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    ).orderBy(
        "customerId",
        "effective_from"
    )
)

# COMMAND ----------

merge_source_df = prepare_scd2_merge_source(
    source_df=incoming_df,
    target_df=spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    ),
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS,
    change_timestamp_column="change_timestamp"
)

# COMMAND ----------

display(merge_source_df)

# COMMAND ----------

apply_scd2_merge(
    target_table_name="vrdworkspace1.silver.customer_scd2_test",
    merge_source_df=merge_source_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS
)

# COMMAND ----------

display(
    spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    ).orderBy(
        "customerId",
        "effective_from"
    )
)

# COMMAND ----------

second_change_data = [
    ("CUS001", "Rahul Sharma", "Gurgaon")
]

second_incoming_df = spark.createDataFrame(
    second_change_data,
    ["customerId", "customerName", "city"]
).withColumn(
    "change_timestamp",
    F.lit("2026-09-19 10:00:00").cast("timestamp")
)

display(second_incoming_df)

# COMMAND ----------

current_target_df = spark.table(
    "vrdworkspace1.silver.customer_scd2_test"
)

second_merge_source_df = prepare_scd2_merge_source(
    source_df=second_incoming_df,
    target_df=current_target_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS,
    change_timestamp_column="change_timestamp"
)

display(second_merge_source_df)

# COMMAND ----------

apply_scd2_merge(
    target_table_name="vrdworkspace1.silver.customer_scd2_test",
    merge_source_df=second_merge_source_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS
)

# COMMAND ----------

display(
    spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    )
    .filter(F.col("customerId") == "CUS001")
    .orderBy("effective_from")
)

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType

null_test_data = [
    ("CUS005", "Raj Mehta", None)
]

null_test_schema = StructType([
    StructField("customerId", StringType(), False),
    StructField("customerName", StringType(), True),
    StructField("city", StringType(), True)
])

null_test_df = spark.createDataFrame(
    null_test_data,
    schema=null_test_schema
).withColumn(
    "change_timestamp",
    F.lit("2026-09-19 11:00:00").cast("timestamp")
)

display(null_test_df)

# COMMAND ----------

null_merge_source_df = prepare_scd2_merge_source(
    source_df=null_test_df,
    target_df=spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    ),
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS,
    change_timestamp_column="change_timestamp"
)

display(null_merge_source_df)

# COMMAND ----------

apply_scd2_merge(
    target_table_name="vrdworkspace1.silver.customer_scd2_test",
    merge_source_df=null_merge_source_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS
)

# COMMAND ----------

null_to_value_data = [
    ("CUS005", "Raj Mehta", "Delhi")
]

null_to_value_df = spark.createDataFrame(
    null_to_value_data,
    ["customerId", "customerName", "city"]
).withColumn(
    "change_timestamp",
    F.lit("2026-09-19 12:00:00").cast("timestamp")
)

# COMMAND ----------

null_to_value_merge_df = prepare_scd2_merge_source(
    source_df=null_to_value_df,
    target_df=spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    ),
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS,
    change_timestamp_column="change_timestamp"
)

display(null_to_value_merge_df)

# COMMAND ----------

apply_scd2_merge(
    target_table_name="vrdworkspace1.silver.customer_scd2_test",
    merge_source_df=null_to_value_merge_df,
    business_key="customerId",
    tracked_columns=SCD2_TRACKED_COLUMNS
)

# COMMAND ----------

display(
    spark.table(
        "vrdworkspace1.silver.customer_scd2_test"
    )
    .filter(F.col("customerId") == "CUS005")
    .orderBy("effective_from")
)