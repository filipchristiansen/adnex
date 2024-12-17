""" Tests for the validation module. """

import pandas as pd
import pytest

from adnex_model.validation import MIN_AGE, has_ca125, validate_and_filter_input
from adnex_model.variables import ADNEX_MODEL_VARIABLES


@pytest.mark.parametrize(
    'input_data,expected',
    [
        ({'s_ca_125': 50}, True),
        ({'s_ca_125': 0}, False),
        ({}, False),
        ({'s_ca_125': None}, False),
        ({'s_ca_125': -1}, False),
    ],
)
def test_has_ca125(input_data, expected):
    row = pd.Series(input_data)
    assert has_ca125(row) == expected


def test_validate_and_filter_input_valid(sample_input):
    # Should not raise any exception
    validate_and_filter_input(sample_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_missing_cols(sample_input):
    # Remove one of the required columns
    invalid_input = sample_input.drop('age')

    with pytest.raises(ValueError, match='missing required columns'):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_invalid_age(sample_input):
    # Modify the age to be out of range
    invalid_input = sample_input.copy()
    invalid_input['age'] = MIN_AGE - 1

    with pytest.raises(ValueError, match=f'Must be between {MIN_AGE} and'):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)
