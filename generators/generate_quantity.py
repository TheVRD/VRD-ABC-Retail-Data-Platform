# ==========================================================
# Module Name         : generateQuantity
# Project             : Test Data Generator
# Purpose             : generate quantity
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.product import Product

from master_data.products.products import PRODUCTS

from random import randint


def generate_quantity(
        product: Product
)-> int:
    """
    Generate a random quantity based on product

    Returns
    -------
    rendomly generated quantity value 
    """

    #Validation tests

    if not product:
        raise ValueError("input value of product cannot be empty")
    
    if not isinstance(product, Product):
        raise TypeError("input value is not of Product type")
    
    if product.minQuantity < 1 or product.maxQuantity <= product.minQuantity:
        raise ValueError("incorrect min or max quantity values in product")
    
    #Generate random quantity

    return randint(
        product.minQuantity,
        product.maxQuantity
    )
    

