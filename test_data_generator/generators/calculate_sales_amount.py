# ==========================================================
# Module Name         : generateAmount
# Project             : Test Data Generator
# Purpose             : generate amount from products
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================


def calculate_sales_amount(
        quantity_val: int,
        unit_price: int
) -> int:
    """
    Generate Amount from unit price and quantity

    Input
    -----
        quantity_val: int,
        unit_price: int
    Output
    ------
        Amount 
    """
    if not quantity_val:
        raise ValueError("Quantity should not be empty")
    
    if not unit_price:
        raise ValueError("unit price should not be empty")
    
    if quantity_val <= 0:
        raise ValueError("quantity should not be less than equal to 0")
    
    if unit_price <= 0:
        raise ValueError("unit price should not be less than equal to 0")
    
    return (quantity_val * unit_price)
