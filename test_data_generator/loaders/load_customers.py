# ==========================================================
# Module Name         : load_customers
# Project             : Test Data Generator
# Purpose             : load_customer data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.customer import Customer
from test_data_generator.config.project_paths import CUSTOMER_MASTER_FILE
from test_data_generator.utils.csv_utils import load_dataclass_list_from_csv



def load_customers() -> tuple[Customer, ...]:
    """
    load list of customer data

    output
    ------
        list of customer
    """
    return load_dataclass_list_from_csv(
        CUSTOMER_MASTER_FILE,
        Customer
    )

