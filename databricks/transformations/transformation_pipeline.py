# Databricks notebook source
# ==========================================================
# Notebook Name      : transformation_pipeline
# Project            : ABC Retail Data Platform
# Purpose            : transformation pipeline
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../models/transformation/transformation_rule

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

def execute_transformation_pipeline(
    *,
    df: DataFrame,
    transform_rules: tuple[TransformationRule, ...]
) -> DataFrame:
    """
    Applies a sequence of transformation rules to a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        transform_rules (tuple[TransformationRule, ...]): A tuple of transformation rules to apply.

    Returns:
        DataFrame: The transformed DataFrame
    """
    if not isinstance(df, DataFrame):
        raise TypeError("df must be a dataframe")
    if not isinstance(transform_rules, tuple):
        raise TypeError("transform_rules must be a tuple")

    if not transform_rules:
        raise ValueError("transformation rules must not be empty")

    if not all(
        isinstance(rule, TransformationRule)
        for rule in transform_rules
    ):
        raise TypeError("All elements in transform_rules must be instances of TransformationRule")

    all_transformed_df = df

    for rule in transform_rules:
        all_transformed_df = rule.transformer(
            df=all_transformed_df,
            **rule.transformer_kwargs
        )
        print(f"transformation rule {rule.name} completed")

    return all_transformed_df


