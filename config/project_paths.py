# ==========================================================
# Module Name         : project paths
# Project             : Test Data Generator
# Purpose             : Centralized paths related to our project
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

CUSTOMER_FILE = "customers.csv"
CUSTOMER_MASTER_FILE = DATA_DIR / CUSTOMER_FILE

GENERATED_DATA_DIR = PROJECT_ROOT / "output"

CLEAN_SALES_FILE = "clean/sales.csv"
CORRUPTED_SALES_FILE = "corrupt/corrupt_sales.csv"

CLEAN_SALES_DATA_PATH = GENERATED_DATA_DIR / CLEAN_SALES_FILE
CORRUPT_SALES_DATA_PATH = GENERATED_DATA_DIR / CORRUPTED_SALES_FILE


