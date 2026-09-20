# ==========================================================
# Module Name         : generate_customers
# Project             : Test Data Generator
# Purpose             : generate customers
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.customer import Customer

from random import choice



def generate_customer(
        customers: tuple[Customer, ...]
) -> Customer:
    """
    This method returns one random customer object from customers tuple

    Input:
    -----
        customers: tuple[Customer, ...]

    Output:
    ------
        Customer
    """

    if not customers:
        raise ValueError("customer tuple cannot be empty")
    
    if not isinstance(customers, tuple):
        raise TypeError("customers must be a tuple")
    

    return choice(customers)