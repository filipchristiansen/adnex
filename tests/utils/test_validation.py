""" Tests for the validation helper functions in utils/validation.py. """

import numpy as np
import pytest

from utils.validation import (
    _is_binary,
    _is_in_range,
    _is_integer,
    _is_less_than_or_equal_to_max,
    _is_non_negative,
    _is_numeric,
)


class TestValidationHelpersWithValidInput:

    @pytest.mark.parametrize(
        'value, expected',
        [
            (10, True),
            (3.14, True),
            (np.int32(5), True),
            (np.float64(2.0), True),
            ('10', False),
            (None, False),
            (object(), False),
            (complex(1, 2), False),
        ],
    )
    def test_is_numeric(self, value, expected):
        assert _is_numeric(value) == expected

    @pytest.mark.parametrize(
        'value, expected',
        [
            (0, True),
            (5, True),
            (3.14, True),
            (np.int32(10), True),
            (np.float64(1.1), True),
            (-1, False),
            (-3.14, False),
        ],
    )
    def test_is_non_negative(self, value, expected):
        assert _is_non_negative(value) == expected

    @pytest.mark.parametrize(
        'value, expected',
        [
            (0, True),
            (1, True),
            (5, True),
            (-1, True),
            (np.int32(10), True),
            (3.0, True),
            (np.float64(1.0), True),
            (1.1, False),
            (-1.1, False),
            ('1', False),
            ('1.1', False),
            ('a', False),
            (None, False),
            (object(), False),
            (np.nan, False),
            (np.inf, False),
            (-np.inf, False),
            (np.float64(1.1), False),
            (complex(1, 2), False),
        ],
    )
    def test_is_integer(self, value, expected):
        assert _is_integer(value) == expected

    @pytest.mark.parametrize(
        'value, expected',
        [
            (0, True),
            (1, True),
            (1.0, True),
            (np.int64(1), True),
            (2, False),
            ('0', False),
            (None, False),
            (object(), False),
            (np.nan, False),
            (np.inf, False),
            (-np.inf, False),
            (complex(1, 2), False),
            (np.float64(1.1), False),
        ],
    )
    def test_is_binary(self, value, expected):
        assert _is_binary(value) == expected

    @pytest.mark.parametrize(
        'value, min_val, max_val, expected',
        [
            (5, 1, 10, True),
            (1, 1, 10, True),
            (1.1, 1, 10, True),
            (5, -1.1, 7.3, True),
            (10, 1, 10, True),
            (0, 1, 10, False),
            (11, 1, 10, False),
        ],
    )
    def test_in_range(self, value, min_val, max_val, expected):
        assert _is_in_range(value, min_val, max_val) == expected

    @pytest.mark.parametrize(
        'value, max_val, expected',
        [
            (5, 10, True),
            (10, 10, True),
            (-1, 10, True),
            (0, 0, True),
            (-3.7, -1.1, True),
            (-1, 10, True),
            (11, 10, False),
        ],
    )
    def test_is_less_than_or_equal_to_max(self, value, max_val, expected):
        assert _is_less_than_or_equal_to_max(value, max_val) == expected


class TestValidationHelpersWithInvalidInput:

    @pytest.mark.parametrize('value', ['abc', None, object(), complex(1, 2)])
    def test_is_non_negative_raises_type_error(self, value):
        with pytest.raises(TypeError) as exc:
            _is_non_negative(value)
        assert 'Expected a numeric value' in str(exc.value)

    @pytest.mark.parametrize('value', ['abc', None, object(), complex(3, 4)])
    def test_is_in_range_raises_type_error(self, value):
        with pytest.raises(TypeError) as exc:
            _is_in_range(value, 0, 10)
        assert 'Expected a numeric value' in str(exc.value)

    @pytest.mark.parametrize('value', ['abc', None, object(), complex(5, 6)])
    def test_is_less_than_or_equal_to_max_raises_type_error(self, value):
        with pytest.raises(TypeError) as exc:
            _is_less_than_or_equal_to_max(value, 10)
        assert 'Expected a numeric value' in str(exc.value)
