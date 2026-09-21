# Databricks notebook source
# ==========================================================
# Notebook Name      : validation_rule
# Project            : ABC Retail Data Platform
# Purpose            : dataclass validation rule
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from dataclasses import dataclass
from typing import Callable, Any

# COMMAND ----------

@dataclass(frozen=True)
class ValidationRule:
    name: str
    validator: Callable
    validator_kwargs: dict[str, Any]