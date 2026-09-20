# ==========================================================
# Module Name         : generate customer master
# Project             : Test Data Generator
# Purpose             : generate customer master data
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from itertools import product
from random import shuffle
from test_data_generator.master_data.customers.names import FIRST_NAMES, LAST_NAMES
from test_data_generator.models.customer import Customer
from test_data_generator.config.project_paths import CUSTOMER_MASTER_FILE
from  pathlib import Path
from csv import DictWriter
from dataclasses import asdict
from test_data_generator.utils.csv_utils import write_dataclass_list_to_csv

CUSTOMER_COUNT = 5000


def generate_name_combinations() -> list[tuple[str,str]]:
    """
    Generate all possible first names and last names combinations

    Result
    ------
        list of tuple of names
    """

    if not FIRST_NAMES:
        raise ValueError("FIRST_NAMES cannot be empty")

    if not LAST_NAMES:
        raise ValueError("LAST_NAMES cannot be empty")

    name_combinations = list(product(FIRST_NAMES, LAST_NAMES))

    shuffle(name_combinations)

    return name_combinations



def build_customers(
        name_combinations: list[tuple[str,str]]
) -> list[Customer]:
    """
    Generate indexed names from first and last name combinations

    Input
    -----
        list of first name, last name
    
    Output
    ------
        Indexed list of customers
    """

    if not name_combinations:
        raise ValueError("Input name combinations cannot be empty")
    

    customers = []

    for index, (first_name, last_name) in enumerate(
        name_combinations,
        start = 1
    ):
        customer = Customer(
            customerId = f"CUS{index:05d}",
            customerName = f"{first_name} {last_name}"
        )
        customers.append(customer)
    
    return customers

def main() -> None:
    """
    main function to create customer master data

    Input
    -----
        none
    
    output
    ------
        none
    """

    name_combinations = generate_name_combinations()

    if CUSTOMER_COUNT > len(name_combinations):
        raise ValueError(
            "Requested customer count exceeds available unique name combinations."
        )

    customers = build_customers(name_combinations[:CUSTOMER_COUNT])

    write_dataclass_list_to_csv(customers, CUSTOMER_MASTER_FILE)
    
    print(f"Customer master written to {CUSTOMER_MASTER_FILE}")


if __name__ == "__main__":
    main()






        
