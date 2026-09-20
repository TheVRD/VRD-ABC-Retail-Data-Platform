# ==========================================================
# Module Name         : inject_invalid_valid
# Project             : Test Data Generator
# Purpose             : Inject Invalid Data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.sales_record import SalesRecord
from config.bad_data_config import INVALID_DATA_PERCENTAGE, INVALID_FIELDS
from utils.corruption_utils import corrupt_field
from random import sample, choice
from dataclasses import replace


def inject_invalid_values(
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
) -> tuple[list[SalesRecord], set[str]]:
    """
    Injects invalid values in sales data

    Input:
    -----
        sales_records: list[SalesRecord]
    
    Output:
    -------
        list[SalesRecord]
    """

    if not isinstance(sales_records, list):
        raise TypeError("sales records must be a list")
    
    if not sales_records:
        raise ValueError("sales records cannot be empty")
    
    if not 0 <= INVALID_DATA_PERCENTAGE <= 1:
        raise ValueError("INVALID_DATA_PERCENTAGE must be between 0 and 1")
    
    if not INVALID_FIELDS:
        raise ValueError("INVALID_FIELDS cannot be empty")
    
    if not isinstance(modified_sale_ids, set):
        raise TypeError("modified_sale_ids must be a set")
    
    corrupted_records = sales_records.copy()

    invalid_data_count = int(
        len(sales_records) * INVALID_DATA_PERCENTAGE
    )

    available_records = [
        record
        for record in sales_records
        if record.saleId not in modified_sale_ids
    ]

    invalid_data_count = min(
        invalid_data_count,
        len(available_records)
    )

    records_to_invalidate = set(sample(available_records, invalid_data_count))

    for i in range(len(corrupted_records)):
        if corrupted_records[i] in records_to_invalidate:
            field_to_corrupt = choice(INVALID_FIELDS)
            current_value = getattr(
                corrupted_records[i],
                field_to_corrupt
            )
            corrupted_value = corrupt_field(
                field_name = field_to_corrupt,
                value = current_value
            )
            invalid_record = replace(
                corrupted_records[i],
                **{
                    field_to_corrupt: corrupted_value
                }

            )
            corrupted_records[i] = invalid_record
            modified_sale_ids.add(corrupted_records[i].saleId)
    
    return corrupted_records, modified_sale_ids

