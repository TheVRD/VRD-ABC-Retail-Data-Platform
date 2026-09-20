# ==========================================================
# Module Name         : generate_timestamp
# Project             : Test Data Generator
# Purpose             : generate timestamps
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from datetime import datetime, timedelta

from random import randint

from test_data_generator.config.generator_config import SALES_START_DATE, SALES_END_DATE


def generate_timestamp() -> datetime:
    """
    Generate a random sales timestamp between the configured
    sales start and end dates.

    Returns
    -------
    datetime
        Random sales timestamp.
    """
    
    if not SALES_START_DATE or not SALES_END_DATE:
        raise ValueError("SALES START DATE or SALES END DATE is not defined")
    
    if not SALES_END_DATE > SALES_START_DATE:
        raise ValueError("End date should be greater than start date")
    
    dateDiff = SALES_END_DATE - SALES_START_DATE

    date_difference_seconds = int(dateDiff.total_seconds())

    random_seconds_val = randint(0, date_difference_seconds)

    generated_timestamp = SALES_START_DATE + timedelta(seconds=random_seconds_val)

    return generated_timestamp
    

