# ==========================================================
# Module Name         : cav_utils
# Project             : Test Data Generator
# Purpose             : Util functions related to csv
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from typing import TypeVar
from pathlib import Path
from dataclasses import asdict
from csv import DictWriter, DictReader

T = TypeVar("T")



def write_dataclass_list_to_csv(
        dataclassList: list[T],
        output_path: Path
) -> None:
    """
    Takes input of list of any dataclass objects and write it to csv

    Input
    -----
        dataclassList: list[T]
        output_path: Path
    Output
    ------
        None
    """

    if not dataclassList:
        raise ValueError("dataclass list cannot be empty")
    
    if output_path.exists():
        raise FileExistsError(f"{output_path} already exists")
    
    output_path.parent.mkdir(
    parents=True,
    exist_ok=True
    )
    
    fieldNames = asdict(dataclassList[0]).keys()

    dataclassDictList = []

    for item in dataclassList:
        dataclassDict = asdict(item) #object.__dict__
        dataclassDictList.append(dataclassDict)
    """
    customer_dicts = [
    asdict(customer)
    for customer in customers
    ]
    """
    
    with open(output_path, mode = 'w', newline = '') as file:
        writer = DictWriter(file, fieldnames = fieldNames)
        writer.writeheader()
        writer.writerows(dataclassDictList)


def load_dataclass_list_from_csv(
        input_path: Path,
        dataclass_type: type[T]
) -> tuple[T, ...]:
    """
    Read data from csv and return dataclass object

    Input
    -----
        input_path - Path
        dataclass_type - type[T]
    Output
    ------
        list[T]
    """

    if not input_path.exists():
        raise FileNotFoundError(f"Input file path {input_path} doesn't exist")
    
    dataclass_list = []

    with open(input_path, mode = 'r', newline = '', encoding="utf-8") as file:
        reader = DictReader(file)
        for row in reader:
            dataclass_list.append(dataclass_type(**row))
        
    
    return tuple(dataclass_list)


    
