# ==========================================================
# Module Name         : customer
# Project             : Test Data Generator
# Purpose             : Customer model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from dataclasses import dataclass

@dataclass(frozen=True)
class Customer:
    """
    Represents a retail customer
    """
    customerId: str
    customerName: str