# ==========================================================
# Module Name         : inject_duplicates
# Project             : Test Data Generator
# Purpose             : Inject duplicate values
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.sales_record import SalesRecord
from config.bad_data_config import DUPLICATE_PERCENTAGE
from random import sample, randint
from dataclasses import replace 


def inject_duplicates(
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
) -> tuple[list[SalesRecord], set[str]]:
    """
    Inject duplicates rows in Sales data

    Input
    -----
        sales_records: list[SalesRecord]
    
    Output
    ------
        list[SalesRecord]
    """

    if not isinstance(sales_records, list):
        raise TypeError("sales records input should be list")
    
    if not sales_records:
        raise ValueError("sales record doesn't exist")
    
    if not 0 <= DUPLICATE_PERCENTAGE <= 1:
        raise ValueError("DUPLICATE_PERCENTAGE must be between 0 and 1")
    

    corrupted_records = sales_records.copy()

    duplicate_count = int(
        len(sales_records) * DUPLICATE_PERCENTAGE
    )

    available_records = [
        record
        for record in sales_records
        if record.saleId not in modified_sale_ids
    ]

    duplicate_count = min(
        duplicate_count,
        len(available_records)
    )

    records_to_duplicate = sample(available_records, duplicate_count)

    for record in records_to_duplicate:
        duplicate_record = replace(record)
        index = randint(0, len(corrupted_records))
        corrupted_records.insert(index, duplicate_record)
        modified_sale_ids.add(record.saleId)
    
    return corrupted_records, modified_sale_ids



