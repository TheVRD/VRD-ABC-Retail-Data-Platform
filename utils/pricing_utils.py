# ==========================================================
# Module Name         : pricing_utils
# Project             : Test Data Generator
# Purpose             : Util functions related to prices
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

def calculate_total_amount(
        unit_price: int,
        quantity: int
)-> int:
    """
    This function takes input of unit_price and quantity

    Returns
    -------
    Amount
    """
    return unit_price * quantity

