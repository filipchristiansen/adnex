""" Module for processing input variables and computing outcome probabilities. """

import numpy as np
import pandas as pd

from adnex_model.variables import get_adnex_model_constants


def transform_input_variables(row: pd.Series) -> pd.Series:
    """
    Transform raw input variables into the features required by the ADNEX model.

    Parameters
    ----------
    row : pd.Series
        A Pandas Series containing the validated raw input variables.

    Returns
    -------
    pd.Series
        Transformed variables aligned with the model's expected coefficients.
    """

    ratio = row['max_solid_component'] / row['max_lesion_diameter']

    transformed = {
        'constant': 1,
        'A': row['age'],
        'Log2(C)': np.log2(row['max_lesion_diameter']),
        'D/C': ratio,
        'D/C^2': ratio**2,
        'E': row['more_than_10_locules'],
        'F': row['number_of_papillary_projections'],
        'G': row['acoustic_shadows_present'],
        'H': row['ascites_present'],
        'I': row['is_oncology_center'],
    }

    if 's_ca_125' in row.index:
        transformed['Log2(B)'] = np.log2(row['s_ca_125'])

    return pd.Series(transformed)


def compute_probabilities(transformed_vars: pd.Series, with_ca125: bool) -> pd.Series:
    """
    Compute the outcome probabilities using the transformed predictors and the ADNEX coefficients.

    Parameters
    ----------
    transformed_vars : pd.Series
        Series of transformed predictors indexed by short variable names.
    with_ca125 : bool
        Whether CA-125 was included in the model.

    Returns
    -------
    pd.Series
        Probabilities for each outcome class and a combined 'Malignant' category.
    """
    # Retrieve model constants
    constants = get_adnex_model_constants(with_ca125)

    # Ensure ordering
    transformed_vars = transformed_vars.reindex(constants.index)

    # Calculate z-values for each non-benign category
    z_values = constants.T @ transformed_vars

    # Compute exp(z) for each category
    exp_z_values = np.exp(z_values)

    # Prepend 1 for the benign category
    exp_z_values = np.insert(exp_z_values, 0, 1)

    # Compute probabilities
    probabilities = exp_z_values / exp_z_values.sum()

    categories = ['Benign', 'Borderline', 'Stage I cancer', 'Stage II-IV cancer', 'Metastatic cancer']
    probabilities_series = pd.Series(probabilities, index=categories)
    probabilities_series['Malignant'] = probabilities_series.sum() - probabilities_series['Benign']

    return probabilities_series
