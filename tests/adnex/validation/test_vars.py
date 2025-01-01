""" Tests for the validation module. """

import pytest

from adnex.validation.variables import (
    MAX_AGE,
    MAXIMAL_LESION_DIAMETER,
    MIN_AGE,
    _validate_age,
    _validate_max_lesion_diameter,
    _validate_max_solid_component,
    _validate_number_of_papillary_projections,
    _validate_s_ca_125,
)
from utils.exceptions import ValidationError


def test_validate_age_valid_integer():
    """
    Test that _validate_age does not raise an exception for valid integer ages within range.
    """
    valid_ages = [MIN_AGE, (MIN_AGE + MAX_AGE) // 2, MAX_AGE]
    for age in valid_ages:
        _validate_age(age)


@pytest.mark.parametrize('age', ['25', 25.1, None, [25], {'age': 25}])
def test_validate_age_invalid_type(age):
    """
    Test that _validate_age raises ValidationError for invalid types.
    """
    with pytest.raises(ValidationError, match=f"Invalid type for 'age': expected integer, got {type(age).__name__}."):
        _validate_age(age)


@pytest.mark.parametrize('age', [-1, -10, -MIN_AGE])
def test_validate_age_negative(age):
    """
    Test that _validate_age raises ValidationError for negative ages.
    """
    var_name = 'age'
    with pytest.raises(ValidationError, match=f'{var_name}={age} cannot be negative.'):
        _validate_age(age)


@pytest.mark.parametrize('age', [MAX_AGE + 1, MIN_AGE - 1])
def test_validate_age_above_max(age):
    """
    Test that _validate_age raises ValidationError for ages autside the range [MIN_AGE, MAX_AGE].
    """
    with pytest.raises(ValidationError, match=f'age={age} is out of range. Must be between {MIN_AGE} and {MAX_AGE}.'):
        _validate_age(age)


def test_validate_max_lesion_diameter_valid():
    """
    Test that _validate_max_lesion_diameter does not raise an exception for valid inputs within range.
    """
    valid_values = [0, 1, 10, MAXIMAL_LESION_DIAMETER]
    for value in valid_values:
        _validate_max_lesion_diameter(value)


@pytest.mark.parametrize(
    'invalid_value',
    [
        '25',  # String
        25.5,  # Float
        None,  # NoneType
        [25],  # List
        {'value': 25},  # Dictionary
    ],
)
def test_validate_max_lesion_diameter_invalid_type(invalid_value):
    """
    Test that _validate_max_lesion_diameter raises ValidationError for invalid types.
    """
    var_name = 'max_lesion_diameter'
    with pytest.raises(
        ValidationError,
        match=f"Invalid type for '{var_name}': expected integer, got {type(invalid_value).__name__}.",
    ):
        _validate_max_lesion_diameter(invalid_value)


def test_validate_max_lesion_diameter_negative():
    """
    Test that _validate_max_lesion_diameter raises ValidationError for negative values.
    """
    var_name = 'max_lesion_diameter'
    value = -1
    with pytest.raises(ValidationError, match=f'{var_name}={value} cannot be negative.'):
        _validate_max_lesion_diameter(value)


def test_validate_max_lesion_diameter_above_max():
    """
    Test that _validate_max_lesion_diameter raises ValidationError for values exceeding MAXIMAL_LESION_DIAMETER.
    """
    var_name = 'max_lesion_diameter'
    value = MAXIMAL_LESION_DIAMETER + 1
    with pytest.raises(
        ValidationError,
        match=f'{var_name}={value} is out of range. Must not exceed {MAXIMAL_LESION_DIAMETER}.',
    ):
        _validate_max_lesion_diameter(value)


def test_validate_max_solid_component_valid():
    """
    Test that _validate_max_solid_component does not raise an exception for valid inputs within range.
    """
    valid_max_lesion_diameters = [50, 100, MAXIMAL_LESION_DIAMETER]
    valid_max_solid_components = [0, 10, MAXIMAL_LESION_DIAMETER - 1]

    for max_lesion_diameter, max_solid_component in zip(valid_max_lesion_diameters, valid_max_solid_components):
        _validate_max_solid_component(max_solid_component, max_lesion_diameter)


@pytest.mark.parametrize(
    'invalid_value',
    [
        '25',  # String
        25.5,  # Float
        None,  # NoneType
        [25],  # List
        {'value': 25},  # Dictionary
    ],
)
def test_validate_max_solid_component_invalid_type(invalid_value):
    """
    Test that _validate_max_solid_component raises ValidationError for invalid types.
    """
    var_name = 'max_solid_component'
    max_lesion_diameter = MAXIMAL_LESION_DIAMETER  # Assuming a valid max lesion diameter

    with pytest.raises(
        ValidationError,
        match=f"Invalid type for '{var_name}': expected integer, got {type(invalid_value).__name__}.",
    ):
        _validate_max_solid_component(invalid_value, max_lesion_diameter)


@pytest.mark.parametrize(
    ('var_name', 'func'),
    [
        ('age', _validate_age),
        ('s_ca_125', _validate_s_ca_125),
        ('max_lesion_diameter', _validate_max_lesion_diameter),
        ('number_of_papillary_projections', _validate_number_of_papillary_projections),
    ],
)
def test_validate_negative(var_name, func):
    """
    Test that _validate_* functions raise ValidationError for negative values.
    """
    value = -1
    with pytest.raises(ValidationError, match=f'{var_name}={value} cannot be negative.'):
        func(value)


def test_validate_max_solid_component_negative():
    """
    Test that _validate_max_solid_component raises ValidationError for negative values.
    """
    var_name = 'max_solid_component'
    value = -1
    max_lesion_diameter = MAXIMAL_LESION_DIAMETER  # Assuming a valid max lesion diameter

    with pytest.raises(ValidationError, match=f'{var_name}={value} cannot be negative.'):
        _validate_max_solid_component(value, max_lesion_diameter=max_lesion_diameter)


def test_validate_max_solid_component_above_max():
    """
    Test that _validate_max_solid_component raises ValidationError for values exceeding MAXIMAL_LESION_DIAMETER.
    """
    var_name = 'max_solid_component'
    value = MAXIMAL_LESION_DIAMETER + 1
    max_lesion_diameter = MAXIMAL_LESION_DIAMETER  # Using the maximum allowed lesion diameter

    with pytest.raises(
        ValidationError,
        match=(f'{var_name}={value} cannot exceed max_lesion_diameter={max_lesion_diameter}.'),
    ):
        _validate_max_solid_component(value, max_lesion_diameter=max_lesion_diameter)
