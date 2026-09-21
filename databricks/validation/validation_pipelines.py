# Databricks notebook source
# ==========================================================
# Notebook Name      : validation_pipeline
# Project            : ABC Retail Data Platform
# Purpose            : Validation pipeline functions
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../models/validation/validation_rule

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

from pyspark.sql import DataFrame

# COMMAND ----------

def execute_validation_pipeline(
    *,
    df: DataFrame,
    validation_rules: tuple[ValidationRule, ...]
) -> tuple[DataFrame, DataFrame]:
    """
    Executes a validation pipeline on a DataFrame.

    Args:
        df: The DataFrame to validate.
        validation_rules: A tuple of ValidationRule objects.

    Returns:
        A tuple containing the valid DataFrame and a invalid dataframe
    """

    if not isinstance(df, DataFrame):
        raise TypeError("df must be a dataframe")
    if not isinstance(validation_rules, tuple):
        raise TypeError("validation_rules must be a tuple")

    if not validation_rules:
        raise ValueError("Validation rules must not be empty")

    if not all(
        isinstance(rule, ValidationRule)
        for rule in validation_rules
    ):
        raise TypeError("All validation rules must be instances of ValidationRule")
    
    current_valid_df = df
    all_invalid_df = df.limit(0)

    for rule in validation_rules:
        valid_df, invalid_df = rule.validator(
            df=current_valid_df,
            **rule.validator_kwargs
        )
        current_valid_df = valid_df#.cache()
        #current_valid_df.count()
        

        all_invalid_df = all_invalid_df.unionByName(invalid_df)
        
        if ENVIRONMENT == "DEV":
            print(f"Running {rule.name}")
            print(f"Valid records: {valid_df.count()}")
            print(f"Invalid records: {invalid_df.count()}")

    return (
        current_valid_df,
        all_invalid_df
    )
    

