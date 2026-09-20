# ==========================================================
# Module Name         : products
# Project             : Test Data Generator
# Purpose             : Product master data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.product import Product

PRODUCTS = (

    Product(
        productId = "PR00001",
        name = "Laptop",
        category = "Electronics",
        minPrice = 35000,
        maxPrice = 120000,
        meanSellingPrice = 77500,
        weight = 5,
        minQuantity=1,
        maxQuantity=5,
        typicalQuantity=1
    ),

    Product(
        productId = "PR00002",
        name = "Mouse",
        category = "Electronics",
        minPrice = 300,
        maxPrice = 3000,
        meanSellingPrice = 500,
        weight = 50,
        minQuantity=1,
        maxQuantity=10,
        typicalQuantity=1
    ),

    Product(
        productId = "PR00003",
        name = "Monitor",
        category = "Electronics",
        minPrice = 5000,
        maxPrice = 15000,
        meanSellingPrice = 10000,
        weight = 25,
        minQuantity=1,
        maxQuantity=5,
        typicalQuantity=1
    ),

    Product(
        productId = "PR00004",
        name = "Pen",
        category = "Stationery",
        minPrice = 30,
        maxPrice = 500,
        meanSellingPrice = 75,
        weight = 100,
        minQuantity=1,
        maxQuantity=50,
        typicalQuantity=5
    ),

    Product(
        productId = "PR00005",
        name = "Notebook",
        category = "Stationery",
        minPrice = 10,
        maxPrice = 100,
        meanSellingPrice = 20,
        weight = 200,
        minQuantity=1,
        maxQuantity=10,
        typicalQuantity=2
    )
)