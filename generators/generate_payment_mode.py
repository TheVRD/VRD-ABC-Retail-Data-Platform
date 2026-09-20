# ==========================================================
# Module Name         : payment_mode_generator
# Project             : Test Data Generator
# Purpose             : generate payment modes
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================
from models.payment_mode import PaymentMode
from master_data.payment_mode.payment_mode import PAYMENT_MODES
from utils.random_utils import weighted_choice

def generate_payment_mode() -> PaymentMode:
    """
    Generate a random payment mode based on weights

    Returns
    -------
    Randomly selected paymnt mode
    """
    return (weighted_choice(PAYMENT_MODES))