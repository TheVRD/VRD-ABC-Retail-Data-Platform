# ==========================================================
# Module Name         : bad_data_config
# Project             : Test Data Generator
# Purpose             : Centralized configuration values for bad data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================


#========================================================================
# Data Quality Settings
# you can change it as per requirement
#========================================================================

DUPLICATE_PERCENTAGE = 0.05

NULL_PERCENTAGE = 0.05

INVALID_DATA_PERCENTAGE = 0.05

NEGATIVE_VALUE_PERCENTAGE = 0.05

WRONG_FIELD_VALUE_PERCENTAGE = 0.05

WRONG_AMOUNT_VALUE_PERCENTAGE = 0.05

MIN_NEGATIVE_VALUE = -10000

MAX_NEGATIVE_VALUE = -1

NULLABLE_FIELDS = (
    "customerName",
    "paymentMode",
    "storeCity",
    "productName",
    "category"
)

INVALID_FIELDS = (
    "customerName",
    "paymentMode",
    "storeCity",
    "productName",
    "category"
)

NEGATIVE_FIELDS = (
    "quantity",
    "unitPrice",
    "totalAmount"
)
WRONG_VALUE_FIELDS = (
    "paymentMode",
)

AMOUNT_FIELD_NAME = "totalAmount"

WRONG_VALUES = (
    "bitcoin",
    "card",
    "up",
    "cc",
    "cheque",
    "loan",
    "e.,sa,la,ds",
    "..........",
    "what the hel is this "
)
"""
INVALID_FIELDS = (
    "paymentMode"
)
"""
ENABLE_DUPLICATES = True
ENABLE_NULLS = True
ENABLE_INVALID_VALUES = False
ENABLE_NEGATIVE_VALUES = True
ENABLE_WRONG_VALUES = True
ENABLE_WRONG_AMOUNT = True

ENABLE_BAD_DATA = True

