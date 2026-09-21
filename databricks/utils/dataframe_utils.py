# Databricks notebook source
# ==========================================================
# Notebook Name      : dataframe_utils
# Project            : ABC Retail Data Platform
# Purpose            : function to convert dataclass object to dataframe
# Author             : TheVRD
# ==========================================================

# COMMAND ----------

from dataclasses import asdict, fields, is_dataclass
from datetime import date, datetime
from enum import Enum
from types import UnionType
from typing import get_args, get_origin
from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    LongType
)

# COMMAND ----------

TYPE_MAPPING = {
    str: StringType(),
    int: LongType(),
    float: DoubleType(),
    bool: BooleanType(),
    date: DateType(),
    datetime: TimestampType()
}

# COMMAND ----------

def dataclass_to_dict(dataclass_object) -> dict:
    """
    Converts a dataclass object into a dictionary
    suitable for Spark serialization.
    """

    object_dict = asdict(dataclass_object)

    return {
        key: (
            value.value
            if isinstance(value, Enum)
            else value
        )
        for key, value in object_dict.items()
    }

# COMMAND ----------

def dataclass_to_schema(
    dataclass_type
) -> StructType:
    """
    Creates a Spark StructType schema from a dataclass.
    """

    if not is_dataclass(dataclass_type):
        raise TypeError("dataclass_type must be a dataclass")

    struct_fields = []

    for field in fields(dataclass_type):

        field_type = field.type
        nullable = False

        origin = get_origin(field_type)

        # Handles Optional[T] and T | None
        if origin in (UnionType,):
            nullable = True

            actual_types = [
                t
                for t in get_args(field_type)
                if t is not type(None)
            ]

            field_type = actual_types[0]

        elif origin is not None:
            # Handles Optional from typing module
            args = get_args(field_type)

            if type(None) in args:
                nullable = True

                actual_types = [
                    t
                    for t in args
                    if t is not type(None)
                ]

                field_type = actual_types[0]

        spark_type = TYPE_MAPPING.get(field_type)

        if spark_type is None:
            raise TypeError(
                f"Unsupported datatype: {field_type}"
            )

        struct_fields.append(
            StructField(
                field.name,
                spark_type,
                nullable
            )
        )

    return StructType(struct_fields)

# COMMAND ----------

def dataclass_to_dataframe(dataclass_object):

    object_dict = dataclass_to_dict(dataclass_object)
    schema = dataclass_to_schema(
        type(dataclass_object)
    )

    return spark.createDataFrame(
        [object_dict],
        schema=schema
    )