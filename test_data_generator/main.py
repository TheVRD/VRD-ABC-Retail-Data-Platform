# ==========================================================
# Module Name         : main
# Project             : Test Data Generator
# Purpose             : main function of the test data generator
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from test_data_generator.config.project_paths import CLEAN_SALES_DATA_PATH, CORRUPT_SALES_DATA_PATH
from test_data_generator.config.bad_data_config import ENABLE_BAD_DATA
from test_data_generator.generators.build_sales_records import build_sales_records
from test_data_generator.bad_data.corrupt_sales_records import corrupt_sales_records
from test_data_generator.utils.csv_utils import write_dataclass_list_to_csv
from test_data_generator.config.generator_config import RANDOM_SEED
from random import seed

def main() -> None:
    """
    Main function of the entire project Test Data Generators

    """
    if RANDOM_SEED is not None:
        seed(RANDOM_SEED)

    seperator = "=" * 70

    print(seperator)

    # Generate clean sales records

    print("Generating Clean Sales Data")

    clean_sales_data = build_sales_records()

    print(f"{len(clean_sales_data)} rows of clean sales data generated")

    # Write clean dataset

    print("Writing Clean Sales Data")

    write_dataclass_list_to_csv(
        clean_sales_data,
        CLEAN_SALES_DATA_PATH
    )

    print(f"Successfully written clean sales data at {CLEAN_SALES_DATA_PATH}")

    print(seperator)

    # Generate corrupted dataset (optional)

    if ENABLE_BAD_DATA:

        print("Corrupting Sales Data")

        corrupted_sales_data = corrupt_sales_records(
            clean_sales_data
        )

        print(f"Corrupted {len(corrupted_sales_data)} rows of sales data")

        print("Writing Sales Data")

        write_dataclass_list_to_csv(
            corrupted_sales_data,
            CORRUPT_SALES_DATA_PATH
        )

        print(f"Successfully written sales data at {CORRUPT_SALES_DATA_PATH}")

    print(seperator)

    print(" ")

    print("Test Data Generated Succesfully")

    print(" ")

    print(seperator)

if __name__ == "__main__":
    main()




