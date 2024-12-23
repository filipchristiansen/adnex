""" Test cases for the adnex function. """

from unittest.mock import patch

import pytest

from adnex.exceptions import ADNEXModelError
from adnex.model import adnex


def test_adnex_model_with_nan_ca125(sample_input):
    """Test that adnex runs with NaN CA-125 value."""
    valid_input = sample_input.copy()
    valid_input = valid_input.drop('s_ca_125')
    valid_input['s_ca_125'] = None
    adnex(valid_input)


def test_adnex_model_output(sample_input, expected_output):
    """Test that adnex returns expected probabilities for valid input."""

    calculated_output = adnex(sample_input)

    for key in expected_output.index:
        expected_value = expected_output[key]
        calculated_value = calculated_output[key]

        assert calculated_value == pytest.approx(
            expected_value, abs=0.02
        ), f"Mismatch for '{key}': calculated {calculated_value}, expected {expected_value}"


def test_adnex_model_output_keys(sample_input):
    """Test that adnex returns all required probability keys."""
    probabilities = adnex(sample_input)
    required_keys = [
        'Benign',
        'Malignant',
        'Borderline',
        'Stage I cancer',
        'Stage II-IV cancer',
        'Metastatic cancer',
    ]
    for key in required_keys:
        assert key in probabilities.index, f"Missing key '{key}' in output probabilities."


def test_adnex_model_output_sum(sample_input):
    """Test that the probabilities sum correctly."""
    probabilities = adnex(sample_input)

    # Malignant should be the sum of its subcategories
    assert probabilities['Malignant'] == pytest.approx(
        probabilities['Borderline']
        + probabilities['Stage I cancer']
        + probabilities['Stage II-IV cancer']
        + probabilities['Metastatic cancer']
    ), 'Malignant probability does not match the sum of its subcategories.'

    # Total sum should be 1 + Malignant
    assert probabilities.sum() == pytest.approx(1.0 + probabilities['Malignant']), ()

    # Benign + Malignant should be 1
    assert probabilities['Benign'] + probabilities['Malignant'] == pytest.approx(
        1.0
    ), 'Sum of Benign and Malignant probabilities does not equal 1.'


def test_adnex_unexpected_error(sample_input):
    # Mock the transformation function to raise an exception to simulate an unexpected error
    with patch('adnex.model.transform_input_variables') as mock_transform:
        mock_transform.side_effect = Exception('Unexpected error during transformation')

        # Check that the model raises an ADNEXModelError
        with pytest.raises(ADNEXModelError, match='An unexpected error occurred while processing the ADNEX model.'):
            adnex(sample_input)
