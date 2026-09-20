# ==========================================================
# Module Name         : generator_config
# Project             : Test Data Generator
# Purpose             : Centralized configuration variables
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================


from datetime import datetime

# Data Volume
SALES_RECORD_COUNT = 200000

#Time Values
SALES_START_DATE = datetime(2025, 1, 1)
SALES_END_DATE = datetime(2025, 12, 31)

#ID constants

ID_PADDING = 5
SALE_ID_PREFIX = "SAL"

#Data Toggle

GENERATE_CLEAN = True
GENERATE_CORRUPTED = True


#========================================================================
# Random Seed
# It helps generating same data set with same configuration to avoid generating random data everytime we run this code
#========================================================================
RANDOM_SEED = 42

