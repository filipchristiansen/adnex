""" Test cases for the adnex_model function. """

import pytest

from adnex_model.model import adnex_model


def test_adnex_model_output(sample_input, expected_output):
    calculated_output = adnex_model(sample_input)

    for key in expected_output.index:
        expected_value = expected_output[key]
        calculated_value = calculated_output[key]

        assert calculated_value == pytest.approx(expected_value, abs=0.02), (
            f"Mismatch for '{key}': calculated {calculated_value}, " f'expected {expected_value}'
        )


def test_adnex_model_output_keys(sample_input):
    probabilities = adnex_model(sample_input)
    assert 'Benign' in probabilities.index
    assert 'Malignant' in probabilities.index
    assert 'Borderline' in probabilities.index
    assert 'Stage I cancer' in probabilities.index
    assert 'Stage II-IV cancer' in probabilities.index
    assert 'Metastatic cancer' in probabilities.index


def test_adnex_model_output_sum(sample_input):
    probabilities = adnex_model(sample_input)

    assert probabilities['Malignant'] == pytest.approx(
        probabilities['Borderline']
        + probabilities['Stage I cancer']
        + probabilities['Stage II-IV cancer']
        + probabilities['Metastatic cancer']
    )

    assert pytest.approx(probabilities.sum()) == 1.0 + probabilities['Malignant']
    assert pytest.approx(probabilities['Benign']) == 1.0 - 2 * probabilities['Malignant']


def test_adnex_model_with_null_ca_125(sample_input):
    input_data = sample_input.copy()
    input_data['s_ca_125'] = None
    adnex_model(input_data)


def test_adnex_model_without_ca_125(sample_input):
    input_data = sample_input.copy()
    del input_data['s_ca_125']
    adnex_model(input_data)
