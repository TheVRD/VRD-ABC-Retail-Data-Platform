# ==========================================================
# Module Name         : inject_negative_values
# Project             : Test Data Generator
# Purpose             : Inject bad number values to respected columns
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from models.sales_record import SalesRecord
from config.bad_data_config import NEGATIVE_FIELDS, NEGATIVE_VALUE_PERCENTAGE, MIN_NEGATIVE_VALUE, MAX_NEGATIVE_VALUE
from random import sample, choice, randint
from dataclasses import replace


def inject_negative_values(
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
) -> tuple[list[SalesRecord], set[str]]:
    """
    Injecting negative values in the specified columns

    Input: 
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
    Output:
       tuple[list[SalesRecord], set[str]] 
    """

    if not isinstance(sales_records, list):
        raise TypeError("sales_records must be list")
    if not isinstance(modified_sale_ids, set):
        raise TypeError("modified sale ids must be a set")
    if not all(
        isinstance(record, SalesRecord)
        for record in sales_records
    ):
        raise TypeError("every record of sales_records must be a SalesRecord")
    
    if not 0 <= NEGATIVE_VALUE_PERCENTAGE <= 1:
        raise ValueError(f"{NEGATIVE_VALUE_PERCENTAGE} that is negative value percentage must be between 0 adn 1")
    
    if not sales_records:
        raise ValueError("sales_records must not be empty")
    
    corrupted_records = sales_records.copy()

    negative_count = int(
        len(sales_records) * NEGATIVE_VALUE_PERCENTAGE
    )

    available_records = [
        record
        for record in sales_records
        if record.saleId not in modified_sale_ids
    ]
    
    negative_count = min(
        negative_count,
        len(available_records)
    )

    records_to_insert_negative = set(sample(available_records, negative_count))

    for i in range(len(corrupted_records)):
        if corrupted_records[i] in records_to_insert_negative:
            field_to_negate = choice(NEGATIVE_FIELDS)
            negative_val = randint(MIN_NEGATIVE_VALUE, MAX_NEGATIVE_VALUE)
            negative_record = replace(
                corrupted_records[i],
                **{
                    field_to_negate: negative_val
                }
                )
            corrupted_records[i] = negative_record
            modified_sale_ids.add(corrupted_records[i].saleId)
    
    return corrupted_records, modified_sale_ids


