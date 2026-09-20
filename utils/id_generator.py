# ==========================================================
# Module Name         : id_generator
# Project             : Test Data Generator
# Purpose             : Generate id value per requirement
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

def generateID(
        prefix: str,
        number: int,
        length: int
) -> str:
    if not prefix:
        raise ValueError("prefix cannot be empty")
    
    if not prefix.isalpha():
        raise ValueError("Prefix should be string")
    
    if not isinstance(number, int):
        raise ValueError("number should always be integer")
    
    numberLength = len(str(number))
    
    if number < 0:
        raise ValueError("Number or Length must be non negative")
    
    #if numberLength > length:
    #    raise ValueError("length of number should not be greater than length")
    
    if length <= 0:
        raise ValueError("legnth should not be zero or negative")
    
    prefix = prefix.strip().upper()

    paddedNumber = str(number).zfill(length)

    resultId = f"{prefix}{paddedNumber}"

    return resultId
    

    

