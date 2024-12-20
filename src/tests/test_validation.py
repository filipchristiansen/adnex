""" Tests for the validation module. """

import re

import pandas as pd
import pytest

from adnex_model.validation import (
    MAX_CA_125,
    MIN_AGE,
    _validate_adnex_model_input,
    has_ca125,
    validate_and_filter_input,
)
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


def test_validate_and_filter_input_invalid_ca125(sample_input):
    # Modify the CA-125 to be out of range
    invalid_input = sample_input.copy()
    invalid_input['s_ca_125'] = -1

    with pytest.raises(ValueError, match=f'Must be between 0 and {MAX_CA_125}'):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_invalid_max_solid_component(sample_input):
    # Modify the max_solid_component to be negative
    invalid_input = sample_input.copy()
    invalid_input['max_solid_component'] = -1

    with pytest.raises(ValueError, match='Max solid component=-1 mm cannot be negative.'):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_invalid_max_solid_component_greater_than_max_lesion_diameter(sample_input):
    # Modify the max_solid_component to larger than the maximal lesion diameter
    invalid_input = sample_input.copy()
    invalid_input['max_solid_component'] = invalid_input['max_lesion_diameter'] + 1

    with pytest.raises(
        ValueError,
        match=f"Max solid component={sample_input['max_lesion_diameter'] + 1} mm cannot exceed "
        + f"max lesion diameter={sample_input['max_lesion_diameter']} mm.",
    ):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_invalid_data_type_age(sample_input):
    # Modify the age to be a string
    invalid_input = sample_input.copy()
    invalid_input = invalid_input.drop('age')
    invalid_input['age'] = 'invalid'

    with pytest.raises(ValueError, match='must be numeric'):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_input_invalid_number_of_papillary_projections(sample_input):
    # Modify the number_of_papillary_projections to be out of range
    invalid_input = sample_input.copy()
    invalid_input['number_of_papillary_projections'] = 5

    with pytest.raises(
        ValueError,
        match=re.escape('Number of papillary projections 5 is invalid. Must be 0, 1, 2, 3, or 4. (4 means > 3)'),
    ):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_missing_input(sample_input):
    # Remove the age and max_lesion_diameter columns
    invalid_input = sample_input.drop(['age', 'max_lesion_diameter'])

    with pytest.raises(
        ValueError, match=re.escape("The input row is missing required columns: ['age', 'max_lesion_diameter']")
    ):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_nan_input(sample_input):
    # Replace
    invalid_input = sample_input.copy()
    invalid_input['age'] = None

    with pytest.raises(ValueError, match=re.escape("The following variables are missing (NaN): ['age']")):
        validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_and_filter_extra_input(sample_input):
    # Add an extra column
    invalid_input = sample_input.copy()
    invalid_input['extra_col'] = 1

    # Should not raise any exception
    validate_and_filter_input(invalid_input, ADNEX_MODEL_VARIABLES)


def test_validate_adnex_model_input(sample_input):
    # Should not raise any exception
    _validate_adnex_model_input(sample_input)


def test_validate_adnex_model_input_missing_cols(sample_input):
    # Remove one of the required columns
    invalid_input = sample_input.drop('more_than_10_locules')

    with pytest.raises(ValueError, match="Missing binary predictor: 'more_than_10_locules'"):
        _validate_adnex_model_input(invalid_input)


def test_validate_adnex_model_input_invalid_binary_cols(sample_input):
    # Modify one of the binary columns to be out of range
    invalid_input = sample_input.copy()
    invalid_input['more_than_10_locules'] = 2

    with pytest.raises(ValueError, match="Binary predictor 'more_than_10_locules' must be 0 or 1, got 2."):
        _validate_adnex_model_input(invalid_input)
