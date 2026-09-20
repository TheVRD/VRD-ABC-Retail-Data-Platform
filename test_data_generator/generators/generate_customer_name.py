# ==========================================================
# Module Name         : customer_generator
# Project             : Test Data Generator
# Purpose             : generate data related to customer
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.master_data.customers.names import FIRST_NAMES, LAST_NAMES

from random import choice


def generate_customer_name() -> str:
    """
    Generate a random customer name.

    Returns
    -------
    str
        Full Customer Name in the format:
        FirstName LastName
    """

    firstName = choice(FIRST_NAMES)
    lastName = choice(LAST_NAMES)

    return f"{firstName} {lastName}"
