# ==========================================================
# Module Name         : store
# Project             : Test Data Generator
# Purpose             : store model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from dataclasses import dataclass

@dataclass(frozen=True)
class Store:
    """
    Represent a store
    """
    storeId: str
    storeName: str
    city: str
    state: str