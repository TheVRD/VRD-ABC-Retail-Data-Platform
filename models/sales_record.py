# ==========================================================
# Module Name         : sales record
# Project             : Test Data Generator
# Purpose             : Sales record model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SalesRecord:
    """
    Represent Sales Record
    """
    saleId: str
    customerId: str
    productId: str
    customerName: str | None
    productName: str | None
    category: str | None
    unitPrice: int
    quantity: int
    totalAmount: int
    paymentMode: str | None
    saleTimeStamp: datetime
    storeId: str
    storeCity: str | None

