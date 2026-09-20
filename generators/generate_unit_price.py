# ==========================================================
# Module Name         : generateAmount
# Project             : Test Data Generator
# Purpose             : generate amount from products
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.product import Product
from random import gauss


def generate_unit_price(
        product: Product
) -> int:
    """
    Generate a realistic selling amount for a product.

    Parameters
    ----------
    product : Product
        Product for which the amount is generated.

    Returns
    -------
    int
        Selling amount.
    """

    sigmaVal = (product.maxPrice - product.minPrice)/6

    #for _ in range(100): use this for production
    
    while True:
        amountVal = int(gauss(product.meanSellingPrice, sigmaVal))
        if product.minPrice < amountVal < product.maxPrice:
            return amountVal
    
    





