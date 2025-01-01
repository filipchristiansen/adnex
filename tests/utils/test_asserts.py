""" Tests for the 'ensure_*' functions in utils/asserts.py. """

import numpy as np
import pytest

from utils.asserts import (
    _ensure_binary,
    _ensure_in_range,
    _ensure_integer,
    _ensure_less_than_or_equal_to_max,
    _ensure_non_negative,
)
from utils.exceptions import ValidationError


class TestValidationAssertsSuccess:

    @pytest.mark.parametrize('value', [0, 5, 3.14, np.int32(10), np.float64(1.1)])
    def test_ensure_non_negative(self, value):
        _ensure_non_negative(value, 'amount')

    @pytest.mark.parametrize('value', [0, 1, 5, -1, np.int32(10), 3.0, np.float64(1.0)])
    def test_ensure_integer(self, value):
        _ensure_integer(value, 'my_var')

    @pytest.mark.parametrize('value', [0, 1, 1, 0, np.int32(1), np.int64(0)])
    def test_ensure_binary(self, value):
        _ensure_binary(value, 'flag')

    @pytest.mark.parametrize(
        'value, min_val, max_val',
        [
            (5, 1, 10),
            (1, 1, 10),
            (1.1, 1, 10),
            (5, -1.1, 7.3),
            (10, 1, 10),
        ],
    )
    def test_ensure_in_range(self, value, min_val, max_val):
        _ensure_in_range(value, min_val, max_val, 'limit')

    @pytest.mark.parametrize(
        'value, max_val',
        [
            (5, 10),
            (10, 10),
            (-1, 10),
            (0, 0),
            (-3.7, -1.1),
            (-1, 10),
        ],
    )
    def test_ensure_less_than_or_equal_to_max(self, value, max_val):
        _ensure_less_than_or_equal_to_max(value, max_val, 'score')


class TestValidationAssertsFailure:

    @pytest.mark.parametrize('value', [-1, -3.14])
    def test_ensure_non_negative(self, value):
        with pytest.raises(ValidationError):
            _ensure_non_negative(value, 'amount')

    @pytest.mark.parametrize('value', [3.14, '10', None, 'abc', complex(1, 2), object()])
    def test_ensure_integer(self, value):
        with pytest.raises(ValidationError):
            _ensure_integer(value, 'my_var')

    @pytest.mark.parametrize('value', [2, -1, '0'])
    def test_ensure_binary(self, value):
        with pytest.raises(ValidationError):
            _ensure_binary(value, 'flag')

    @pytest.mark.parametrize('value, max_val', [(11, 10), (999, 100)])
    def test_ensure_upper_bounded(self, value, max_val):
        with pytest.raises(ValidationError):
            _ensure_less_than_or_equal_to_max(value, max_val, 'score')

    @pytest.mark.parametrize('value, min_val, max_val', [(-1, 0, 10), (11, 0, 10)])
    def test_ensure_in_range(self, value, min_val, max_val):
        with pytest.raises(ValidationError):
            _ensure_in_range(value, min_val, max_val, 'limit')


class TestValidationAssertsTypeErrors:

    invalid_types = ['abc', None, complex(1, 2), object()]

    @pytest.mark.parametrize('value', invalid_types)
    def test_ensure_non_negative_type_error(self, value):
        with pytest.raises(TypeError):
            _ensure_non_negative(value, 'my_var')

    @pytest.mark.parametrize('value', invalid_types)
    def test_ensure_in_range_type_error(self, value):
        with pytest.raises(TypeError):
            _ensure_in_range(value, 0, 10, 'my_var')

    @pytest.mark.parametrize('value', invalid_types)
    def test_ensure_less_than_or_equal_to_max_type_error(self, value):
        with pytest.raises(TypeError):
            _ensure_less_than_or_equal_to_max(value, 10, 'my_var')
