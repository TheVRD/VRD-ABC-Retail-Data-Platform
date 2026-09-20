# ==========================================================
# Module Name         : generateProduct
# Project             : Test Data Generator
# Purpose             : Product model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from random import choices

from models.product import Product
from master_data.products.products import PRODUCTS
from utils.random_utils import weighted_choice

PRODUCT_WEIGHTS = tuple(product.weight for product in PRODUCTS)

def generate_product() -> Product:
    
    """
    Generate a random product based on configured weights.

    Returns
    -------
    Product
        Randomly selected Product object.
    """

    return weighted_choice(PRODUCTS)