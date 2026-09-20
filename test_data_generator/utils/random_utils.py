# ==========================================================
# Module Name         : random_utils
# Project             : Test Data Generator
# Purpose             : Util functions for other generators
# Author              : TheVRD
# Created Date        : 2026-07-04
# Version             : 1.0
# ==========================================================

from typing import TypeVar
from random import choices

T = TypeVar("T")


def weighted_choice(
        population: tuple[T, ...],
) -> T:
    """
    
    Parameters
    ----------
    population : tuple[T, ...]
        Collection of weighted objects.

    Returns
    -------
    T
    """

    weights = []

    #Validation Tests
    for obj in population:
        if not hasattr(obj, "weight"):
            raise AttributeError("Missing weight in object")
        
        if obj.weight < 0:
            raise ValueError("Value of weight cannot be negative")
        
        weights.append(obj.weight)


    #returning choosen object
    #choices always returns a list thus [0]
    return choices(
        population = population, weights = tuple(weights), k = 1
    )[0]
