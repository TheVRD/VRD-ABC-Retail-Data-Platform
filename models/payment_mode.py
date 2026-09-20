# ==========================================================
# Module Name         : paymentMode
# Project             : Test Data Generator
# Purpose             : Payment mmode model
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from dataclasses import dataclass

@dataclass(frozen=True)
class PaymentMode:
    """
    Represent Payment Modes
    """
    name: str
    weight: int