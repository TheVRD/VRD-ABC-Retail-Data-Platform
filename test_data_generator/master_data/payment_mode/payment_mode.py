# ==========================================================
# Module Name         : paymentMode
# Project             : Test Data Generator
# Purpose             : Payment Mode master data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.payment_mode import PaymentMode

PAYMENT_MODES = (
    PaymentMode(
        name="UPI",
        weight=60
    ),
    PaymentMode(
        name="Credit Card",
        weight=20
    ),
    PaymentMode(
        name="Debit Card",
        weight=10
    ),
    PaymentMode(
        name="Cash",
        weight=8
    ),
    PaymentMode(
        name="Gift Card",
        weight=3
    ),
    PaymentMode(
        name="Net Banking",
        weight=2
    )
)
