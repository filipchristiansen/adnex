""" Tests for the validation module. """

import re

import pytest

from adnex.exceptions import MissingColumnsError, ValidationError
from adnex.validation.core import validate_input
from adnex.validation.variables import MAX_AGE, MIN_AGE


def test_validate_input_valid(sample_input):
    validate_input(sample_input)


def test_validate_input_missing_cols(sample_input):
    # Remove one of the required columns
    var_name = 'age'
    invalid_input = sample_input.drop(var_name)

    with pytest.raises(MissingColumnsError, match=f"The input row is missing required columns: '{var_name}'."):
        validate_input(invalid_input)


def test_validate_input_invalid_age(sample_input):
    # Modify the age to be out of range
    var_name = 'age'
    value = MIN_AGE - 1
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(
        ValidationError,
        match=f'{var_name}={value} is out of range. Must be between {MIN_AGE} and {MAX_AGE}.',
    ):
        validate_input(invalid_input)


def test_validate_input_invalid_ca125(sample_input):
    # Modify the CA-125 to be negative
    var_name = 's_ca_125'
    value = -1
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(ValidationError, match=f'{var_name}={value} cannot be negative.'):
        validate_input(invalid_input)


def test_validate_input_invalid_max_solid_component(sample_input):
    # Modify the max_solid_component to be negative
    var_name = 'max_solid_component'
    value = -1
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(ValidationError, match=f'{var_name}={value} cannot be negative.'):
        validate_input(invalid_input)


def test_validate_input_invalid_max_solid_component_greater_than_max_lesion_diameter(sample_input):
    # Modify the max_solid_component to larger than the maximal lesion diameter
    var_name = 'max_solid_component'
    value = sample_input['max_lesion_diameter'] + 1
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(
        ValidationError,
        match=f"{var_name}={value} cannot exceed max_lesion_diameter={sample_input['max_lesion_diameter']}.",
    ):
        validate_input(invalid_input)


def test_validate_input_invalid_data_type_age(sample_input):
    # Modify the age to be a string
    var_name = 'age'
    invalid_input = sample_input.copy()
    del invalid_input[var_name]
    invalid_input[var_name] = 'invalid'

    with pytest.raises(ValidationError, match=f"Invalid type for '{var_name}': expected integer, got str."):
        validate_input(invalid_input)


def test_validate_input_invalid_number_of_papillary_projections(sample_input):
    # Modify the number_of_papillary_projections to be out of range
    var_name = 'number_of_papillary_projections'
    value = 5
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(
        ValidationError,
        match=re.escape(f'{var_name}={value} is invalid. Must be 0, 1, 2, 3, or 4 (4 means > 3).'),
    ):
        validate_input(invalid_input)


def test_validate_and_missing_cols(sample_input):
    # Remove the age and max_lesion_diameter columns
    invalid_input = sample_input.drop(['age', 'max_lesion_diameter'])

    with pytest.raises(
        MissingColumnsError,
        match="The input row is missing required columns: {'age', 'max_lesion_diameter'}.",
    ):
        validate_input(invalid_input)


def test_validate_nan_input(sample_input):
    # Set the age to NaN
    var_name = 'age'
    invalid_input = sample_input.copy()
    invalid_input[var_name] = None

    with pytest.raises(
        ValidationError,
        match=re.escape(f"The following variables are missing (NaN): ['{var_name}']"),
    ):
        validate_input(invalid_input)


def test_validate_extra_input(sample_input):
    # Add an extra column
    invalid_input = sample_input.copy()
    invalid_input['extra_col'] = 1

    # Should not raise any exception
    validate_input(invalid_input)


def test_validate_adnex_model_input_without_ca125(sample_input):
    # Should not raise any exception
    valid_input = sample_input.copy()
    del valid_input['s_ca_125']
    validate_input(valid_input)


def test_validate_adnex_model_input_with_float_ca125(sample_input):
    # Should not raise any exception
    var_name = 's_ca_125'
    valid_input = sample_input.copy()
    s_ca_125 = valid_input[var_name]
    del valid_input[var_name]
    valid_input[var_name] = float(s_ca_125)
    validate_input(valid_input)


def test_validate_adnex_model_input_invalid_binary_cols(sample_input):
    # Modify one of the binary columns to be out of range
    var_name = 'more_than_10_locules'
    value = 2
    invalid_input = sample_input.copy()
    invalid_input[var_name] = value

    with pytest.raises(ValidationError, match=f"Invalid value for '{var_name}': expected 0 or 1, got {value}."):
        validate_input(invalid_input)
