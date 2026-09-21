# Databricks notebook source
# ==========================================================
# Notebook Name      : gold_aggregation_utils
# Project            : ABC Retail Data Platform
# Purpose            : gold layer aggregation functions
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    to_date,
    col,
    count,
    sum,
    first,
    round
)

# COMMAND ----------

def aggregate_daily_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates daily sales data from the provided DataFrame.

    Parameters:
        df (DataFrame): The input DataFrame containing sales data.

    Returns:
        DataFrame: A new DataFrame containing aggregated daily sales data.
    """
    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "saleId",
        "quantity",
        "totalAmount",
        "saleTimeStamp"
    }
    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set    
        ]
    
    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not in the input DataFrame"
            )
    daily_sales_df = (
        df
        .withColumn(
            "processing_date",
            to_date(col("saleTimeStamp"))
        )
        .groupBy("processing_date")
        .agg(
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(
                col("total_revenue") / col("total_orders"), 2
            )
        )
    )
    return daily_sales_df

# COMMAND ----------

def aggregate_store_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates store sales data from the provided DataFrame.

    Parameters:
        df (DataFrame): The input DataFrame containing sales data.

    Returns:
        DataFrame: A new DataFrame containing aggregated store sales data.
    """
    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "storeId",
        "storeCity",
        "saleId",
        "quantity",
        "totalAmount"
    }
    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set
    ]

    if missing_columns:
        raise ValueError(f"Columns {missing_columns} not in the input DataFrame")

    store_sales_df = (
        df
        .groupBy("storeId")
        .agg(
            first("storeCity", ignorenulls = True).alias("storeCity"),
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(col("total_revenue") / col("total_orders"), 2)
        )
    )

    return store_sales_df

# COMMAND ----------

def aggregate_city_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates sales data at city level.

    Grain:
        One row per city.

    Args:
        df: Input sales DataFrame.

    Returns:
        DataFrame containing city-level sales metrics.
    """

    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "storeCity",
        "saleId",
        "quantity",
        "totalAmount"
    }

    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set
    ]

    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not in the input DataFrame"
        )

    city_sales_df = (
        df
        .groupBy("storeCity")
        .agg(
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(
                col("total_revenue") / col("total_orders"),
                2
            )
        )
    )

    return city_sales_df

# COMMAND ----------

def aggregate_product_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates sales data at product level.

    Grain:
        One row per product.

    Args:
        df: Input sales DataFrame.

    Returns:
        DataFrame containing product-level sales metrics.
    """

    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "productId",
        "productName",
        "category",
        "saleId",
        "quantity",
        "totalAmount"
    }

    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set
    ]

    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not in the input DataFrame"
        )

    product_sales_df = (
        df
        .groupBy("productId")
        .agg(
            first(
                "productName",
                ignorenulls=True
            ).alias("productName"),
            first(
                "category",
                ignorenulls=True
            ).alias("category"),
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(
                col("total_revenue") / col("total_orders"),
                2
            )
        )
    )

    return product_sales_df

# COMMAND ----------

def aggregate_category_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates sales data at category level.

    Grain:
        One row per category.

    Args:
        df: Input sales DataFrame.

    Returns:
        DataFrame containing category-level sales metrics.
    """

    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "category",
        "saleId",
        "quantity",
        "totalAmount"
    }

    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set
    ]

    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not in the input DataFrame"
        )

    category_sales_df = (
        df
        .groupBy("category")
        .agg(
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(
                col("total_revenue") / col("total_orders"),
                2
            )
        )
    )

    return category_sales_df

# COMMAND ----------

def aggregate_payment_mode_sales(
    *,
    df: DataFrame
) -> DataFrame:
    """
    Aggregates sales data at payment mode level.

    Grain:
        One row per payment mode.

    Args:
        df: Input sales DataFrame.

    Returns:
        DataFrame containing payment-mode-level sales metrics.
    """

    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a DataFrame.")

    required_columns = {
        "paymentMode",
        "saleId",
        "quantity",
        "totalAmount"
    }

    columns_set = set(df.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in columns_set
    ]

    if missing_columns:
        raise ValueError(
            f"Columns {missing_columns} not in the input DataFrame"
        )

    payment_mode_sales_df = (
        df
        .groupBy("paymentMode")
        .agg(
            count("saleId").alias("total_orders"),
            sum("quantity").alias("total_quantity"),
            sum("totalAmount").alias("total_revenue")
        )
        .withColumn(
            "average_order_value",
            round(
                col("total_revenue") / col("total_orders"),
                2
            )
        )
    )

    return payment_mode_sales_df

# COMMAND ----------

# MAGIC %run ../../utils/delta_utils
# MAGIC

# COMMAND ----------

# MAGIC %run ../../config/config

# COMMAND ----------

SILVER_SALES_TABLE = (
    f"{CATALOG}.{SILVER_SCHEMA}.{SALES_TABLE}"
)

# COMMAND ----------

silver_df = read_delta_table(
    table_name=SILVER_SALES_TABLE
)

daily_sales_df = aggregate_daily_sales(
    df=silver_df
)

daily_sales_df.orderBy("processing_date").show()

# COMMAND ----------

daily_sales_df.count()