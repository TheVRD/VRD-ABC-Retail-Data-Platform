# ==========================================================
# Module Name         : generate sales records
# Project             : Test Data Generator
# Purpose             : generate sales records
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.config.generator_config import SALES_RECORD_COUNT
from test_data_generator.loaders.load_customers import load_customers
from test_data_generator.models.sales_record import SalesRecord
from test_data_generator.generators.generate_sales_record import generate_sales_record

def build_sales_records() -> list[SalesRecord]:
    """
    Final Orchastration function to generate sales records as per requirement

    Input:
    ------
        None
    Output:
    ------
        None
    """

    customers = load_customers()
    
    #Collection of sales records
    sales_records: list[SalesRecord] = []

    #Generating sales records
    for sale_number in range(1, SALES_RECORD_COUNT + 1):
        sales_record = generate_sales_record(
            sale_number,
            customers
        )
        sales_records.append(sales_record)

    return sales_records



def main() -> None:
    build_sales_records()


if __name__ == "__main__":
    main()

    


