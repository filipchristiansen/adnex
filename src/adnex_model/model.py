""" This module contains the main function to apply the ADNEX model to a single patient data row. """

import pandas as pd

from adnex_model.processing import compute_probabilities, transform_input_variables
from adnex_model.validation import has_ca125, validate_and_filter_input
from adnex_model.variables import ADNEX_MODEL_VARIABLES


def adnex_model(row: pd.Series) -> pd.Series:
    """
    Apply the ADNEX model to a single patient data row.

    Parameters
    ----------
    row : pd.Series
        A pandas Series containing the necessary predictors with the expected column names.

    Returns
    -------
    pd.Series
        A pandas Series with probabilities for each outcome category:
        ['Benign', 'Borderline', 'Stage I cancer', 'Stage II-IV cancer', 'Metastatic cancer', 'Malignant'].
        The 'Malignant' category is the sum of the last four categories.
    """
    with_ca125 = has_ca125(row)

    # Adjust the variables to use
    adnex_model_variables_to_use = ADNEX_MODEL_VARIABLES.copy()
    if not with_ca125:
        adnex_model_variables_to_use.pop('B')

    # Validate and filter input data
    validate_and_filter_input(row, adnex_model_variables_to_use)

    # Transform the input variables
    transformed_vars = transform_input_variables(row)

    # Compute probabilities
    probabilities = compute_probabilities(transformed_vars, with_ca125)

    return probabilities
