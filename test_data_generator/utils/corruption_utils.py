# ==========================================================
# Module Name         : corruption_utils
# Project             : Test Data Generator
# Purpose             : Util functions corrupting sales values
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from random import randint, choice
from test_data_generator.config.bad_data_config import INVALID_FIELDS, NULLABLE_FIELDS

def swap_adjacent_characters(
        value: str
)-> str:
    """
    swap adjacent characters of string value

    Input:
    -----
        value: str
    Output:
    ------
        str
    """

    if not isinstance(value, str):
        raise TypeError("value must be string type")
    
    if not value:
        raise ValueError("value cannot be empty")
    
    if not len(value) >= 2:
        return value
    
    swap_index = randint(0, len(value) - 2)
    char_value = list(value)

    char_value[swap_index], char_value[swap_index + 1] = char_value[swap_index + 1], char_value[swap_index]

    return "".join(char_value)

    

    


def duplicate_random_character(
        value: str
) -> str:
    """
    Duplicate random character of value string and return corrupted value

    Input
    -----
        value: str
    
    Output:
    ------
        str
    """

    if not isinstance(value, str):
        raise TypeError("value must be string type")
    
    if not value:
        raise ValueError("value cannot be empty")
    
    duplication_index = randint(0, len(value) - 1)

    return (value[:duplication_index+1] + value[duplication_index] + value[duplication_index+1:])


def remove_random_character(
        value: str
) -> str:
    """
    Remove random character from value string and return corrupted value

    Input:
    -----
        value: str
    Output:
    ------
        str
    """

    if not isinstance(value, str):
        raise TypeError("value must be string type")
    
    if not value:
        raise ValueError("value cannot be empty")
    
    if len(value) < 2:
        return value
    
    removal_index = randint(0, len(value) - 1)

    return (
        value[:removal_index]
        + value[removal_index + 1:]
    )


def corrupt_field(
        *,
        field_name: str,
        value: str
) -> str:
    """
    A generic corruption function that corrupts fields and return corrupted value

    Input
    -----
        field
    """

    if not isinstance(value, str):
        raise TypeError("value should be string type")
    
    if not isinstance(field_name, str):
        raise TypeError("field name should be string type")
    
    if not field_name:
        raise ValueError("field name should not be empty")
    
    if not value:
        raise ValueError("value should not be empty")
    
    if field_name not in INVALID_FIELDS:
        raise ValueError(f"{field_name} is not configured as a corruptible field")
    
    strategies = (
        swap_adjacent_characters,
        duplicate_random_character,
        remove_random_character
    )

    strategy = choice(strategies)

    return strategy(value)
    

    

