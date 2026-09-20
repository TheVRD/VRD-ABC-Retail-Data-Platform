# ==========================================================
# Module Name         : generate sales record
# Project             : Test Data Generator
# Purpose             : generate sales record
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.customer import Customer
from test_data_generator.models.product import Product
from test_data_generator.models.store import Store
from test_data_generator.models.sales_record import SalesRecord
from test_data_generator.generators.generate_customers import generate_customer
from test_data_generator.generators.generate_product import generate_product
from test_data_generator.generators.generate_stores import generate_stores
from test_data_generator.generators.generate_quantity import generate_quantity
from test_data_generator.generators.generate_unit_price import generate_unit_price
from test_data_generator.generators.calculate_sales_amount import calculate_sales_amount
from test_data_generator.generators.generate_payment_mode import generate_payment_mode
from test_data_generator.generators.generate_timestamp import generate_timestamp
from test_data_generator.utils.id_generator import generateID
from test_data_generator.config.generator_config import SALE_ID_PREFIX, ID_PADDING


def generate_sales_record(
        sale_number: int,
        customers: tuple[Customer, ...],
    ) -> SalesRecord:
    """
    Create and return one SalesRecord object

    Input:
        sale_number: int,
        customers: tuple[Customer, ...],
    
    Output:
    ------
        SalesRecord class object
    """

    if sale_number <= 0:
        raise ValueError("sale_number cannot be 0 or lesst than 0")
    
    if not isinstance(customers, tuple):
        raise TypeError("customers should be tuple")
    
    if not customers:
        raise ValueError("customers tuple cannot be empty")
    
    customer = generate_customer(customers)
    product = generate_product()
    quantity = generate_quantity(product)
    unit_price = generate_unit_price(product)
    total_amount = calculate_sales_amount(quantity, unit_price)
    store = generate_stores()
    payment_mode = generate_payment_mode()
    timestamp = generate_timestamp()
    saleId = generateID(SALE_ID_PREFIX, sale_number, ID_PADDING)

    return SalesRecord(
        saleId = saleId,
        customerId = customer.customerId,
        productId = product.productId,
        customerName = customer.customerName,
        productName = product.name,
        category = product.category,
        unitPrice = unit_price,
        quantity = quantity,
        totalAmount = total_amount,
        paymentMode = payment_mode.name,
        saleTimeStamp = timestamp,
        storeId = store.storeId,
        storeCity = store.city
    )


    
