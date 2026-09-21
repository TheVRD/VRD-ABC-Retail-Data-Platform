# Databricks notebook source
# ==========================================================
# Notebook Name      : bootstrap_environment
# Project            : ABC Retail Data Platform
# Purpose            : Bootstrap project environment
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

# MAGIC %run ../config/config

# COMMAND ----------

print("=" * 70)
print("Bootstrapping ABC Retail Environment")
print("=" * 70)

# COMMAND ----------

# MAGIC %run ./create_schemas

# COMMAND ----------

# MAGIC %run ./create_metadata_tables

# COMMAND ----------

print("=" * 70)
print("Bootstrap completed successfully.")
print("=" * 70)