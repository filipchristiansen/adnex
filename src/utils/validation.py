""" Helper functions for validation of input values. """

from typing import Union

import numpy as np


def _is_numeric(value: object) -> bool:
    return isinstance(value, (int, float, np.number))


def _is_non_negative(value: Union[int, float, np.number]) -> bool:
    if not _is_numeric(value):
        raise TypeError(f'Expected a numeric value, got {type(value).__name__}.')
    return bool(value >= 0)


def _is_integer(value: object) -> bool:
    if not _is_numeric(value):
        return False
    if isinstance(value, (int, np.integer)):
        return True
    if isinstance(value, (float, np.floating)) and value.is_integer():
        return True
    return False


def _is_binary(value: int) -> bool:
    return _is_integer(value) and int(value) in {0, 1}


def _is_in_range(value: int, min_value: int, max_value: int) -> bool:
    if not _is_numeric(value):
        raise TypeError(f'Expected a numeric value, got {type(value).__name__}.')
    return min_value <= value <= max_value


def _is_less_than_or_equal_to_max(value: int, max_value: int) -> bool:
    if not _is_numeric(value):
        raise TypeError(f'Expected a numeric value, got {type(value).__name__}.')
    return value <= max_value
