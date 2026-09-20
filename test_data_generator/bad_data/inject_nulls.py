# ==========================================================
# Module Name         : inject_nulls
# Project             : Test Data Generator
# Purpose             : Inject Null values
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.sales_record import SalesRecord
from test_data_generator.config.bad_data_config import NULL_PERCENTAGE, NULLABLE_FIELDS
from random import sample, choice
from dataclasses import replace



def inject_nulls(
        sales_records: list[SalesRecord],
        modified_sale_ids: set[str]
) -> tuple[list[SalesRecord], set[str]]:
    """
    Inject null values at random places in sales data

    Input
    -----
        sales_records: list[SalesRecord]
    
    Output
    ------
        list[SalesRecord]
    """

    if not isinstance(sales_records, list):
        raise TypeError("sales records type shuold be list")
    
    if not sales_records:
        raise ValueError("sales record doesn't exist")
    
    if not 0 <= NULL_PERCENTAGE <= 1:
        raise ValueError("null percentage must be between 0 and 1")
    if not isinstance(modified_sale_ids, set):
        raise TypeError("modified sales ids should of type set")
    
    corrupted_records = sales_records.copy()
    
    null_count = int(
        len(sales_records) * NULL_PERCENTAGE
    )

    available_records = [
        record
        for record in sales_records
        if record.saleId not in modified_sale_ids
    ]

    null_count = min(
        null_count,
        len(available_records)
    )



    records_to_insert_null = set(sample(available_records, null_count))

    for i in range(len(corrupted_records)):
        if corrupted_records[i] in records_to_insert_null:
            field_to_null = choice(NULLABLE_FIELDS)
            null_record = replace(
               corrupted_records[i],
               **{
                   field_to_null: None
               } 
            )
            corrupted_records[i] = null_record
            modified_sale_ids.add(corrupted_records[i].saleId)
    
    return corrupted_records, modified_sale_ids




    
