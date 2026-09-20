# ==========================================================
# Module Name         : product
# Project             : Test Data Generator
# Purpose             : Product model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """
    Represents a product available for sale.
    """

    productId: str
    name: str
    category: str
    minPrice: float
    maxPrice: float
    meanSellingPrice: int
    weight: int
    minQuantity: int
    maxQuantity: int
    typicalQuantity: int