# ==========================================================
# Module Name         : generate_stores
# Project             : Test Data Generator
# Purpose             : generate stores
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from random import choice
from test_data_generator.models.store import Store
from test_data_generator.master_data.stores.stores import STORES


def generate_stores()-> Store:
    
    """
    Generate a random store.

    Returns
    -------
    Store
        Randomly selected store object.
    """

    return choice(STORES)


