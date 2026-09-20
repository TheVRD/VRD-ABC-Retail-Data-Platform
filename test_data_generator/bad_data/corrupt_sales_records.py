# ==========================================================
# Module Name         : corrupt_sales_records
# Project             : Test Data Generator
# Purpose             : Corrupt Sales Records
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.models.sales_record import SalesRecord
from test_data_generator.bad_data.inject_duplicates import inject_duplicates
from test_data_generator.bad_data.inject_invalid_values import inject_invalid_values
from test_data_generator.bad_data.inject_nulls import inject_nulls
from test_data_generator.bad_data.inject_negative_values import inject_negative_values
from test_data_generator.bad_data.inject_wrong_field_value import inject_wrong_field_value
from test_data_generator.bad_data.inject_wrong_amount import inject_wrong_amount_value
from test_data_generator.config.bad_data_config import ENABLE_DUPLICATES, ENABLE_INVALID_VALUES, ENABLE_NULLS, ENABLE_NEGATIVE_VALUES, ENABLE_WRONG_VALUES, ENABLE_WRONG_AMOUNT


def corrupt_sales_records(
        sales_records: list[SalesRecord]
) -> list[SalesRecord]:
    """
    Corrupt sales records by applying all enabled bad-data injectors.

    Input:
    -----
        sales_record: SalesRecord
    Output:
    ------
        SalesRecord
    """

    if not isinstance(sales_records, list):
        raise TypeError("sales_records should be of list type")
    
    if not sales_records:
        raise ValueError("sales_records cannot be empty")
    
    modified_sale_ids: set[str] = set()
    corrupted_records = sales_records.copy()


    if ENABLE_DUPLICATES:
        corrupted_records, modified_sale_ids = inject_duplicates(
            corrupted_records,
            modified_sale_ids
        )

    if ENABLE_NULLS:
        corrupted_records, modified_sale_ids = inject_nulls(
            corrupted_records,
            modified_sale_ids
        )
    
    if ENABLE_INVALID_VALUES:
        corrupted_records, modified_sale_ids = inject_invalid_values(
            corrupted_records,
            modified_sale_ids
        )
    
    if ENABLE_NEGATIVE_VALUES:
        corrupted_records, modified_sale_ids = inject_negative_values(
            corrupted_records,
            modified_sale_ids
        )
    
    if ENABLE_WRONG_VALUES:
        corrupted_records, modified_sale_ids = inject_wrong_field_value(
            corrupted_records,
            modified_sale_ids
        )
    
    if ENABLE_WRONG_AMOUNT:
        corrupted_records, modified_sale_ids = inject_wrong_amount_value(
            corrupted_records,
            modified_sale_ids
        )

    


    return corrupted_records



    
    
