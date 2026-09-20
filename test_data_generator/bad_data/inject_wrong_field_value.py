# ==========================================================
# Module Name         : inject_wrong_field_value
# Project             : Test Data Generator
# Purpose             : Inject bad data in fields
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.sales_record import SalesRecord
from test_data_generator.config.bad_data_config import WRONG_FIELD_VALUE_PERCENTAGE, WRONG_VALUE_FIELDS, WRONG_VALUES
from random import sample, choice
from dataclasses import replace


def inject_wrong_field_value(
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
) -> tuple[list[SalesRecord], set[str]]:
    """
    Injecting wrong values in the specified columns

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
    
    if not 0 <= WRONG_FIELD_VALUE_PERCENTAGE <= 1:
        raise ValueError(f"{WRONG_FIELD_VALUE_PERCENTAGE} that is negative value percentage must be between 0 adn 1")
    
    if not sales_records:
        raise ValueError("sales_records must not be empty")
    
    corrupted_records = sales_records.copy()

    wrong_value_count = int(
        len(sales_records) * WRONG_FIELD_VALUE_PERCENTAGE
    )

    available_records = [
        record
        for record in sales_records
        if record.saleId not in modified_sale_ids
    ]
    
    wrong_value_count = min(
        wrong_value_count,
        len(available_records)
    )

    records_to_insert_negative = set(sample(available_records, wrong_value_count))

    for i in range(len(corrupted_records)):
        if corrupted_records[i] in records_to_insert_negative:
            field_to_insert_wrong_value = choice(WRONG_VALUE_FIELDS)
            wrong_val = choice(WRONG_VALUES)
            wrong_value_record = replace(
                corrupted_records[i],
                **{
                    field_to_insert_wrong_value: wrong_val
                }
                )
            corrupted_records[i] = wrong_value_record
            modified_sale_ids.add(corrupted_records[i].saleId)
    
    return corrupted_records, modified_sale_ids
