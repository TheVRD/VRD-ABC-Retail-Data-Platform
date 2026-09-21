# Databricks notebook source
# ==========================================================
# Notebook Name      : transformation_rule
# Project            : ABC Retail Data Platform
# Purpose            : dataclass transformation rule
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from dataclasses import dataclass
from typing import Callable, Any

# COMMAND ----------

@dataclass(frozen=True)
class TransformationRule:
    name: str
    transformer: Callable
    transformer_kwargs: dict[str, Any]