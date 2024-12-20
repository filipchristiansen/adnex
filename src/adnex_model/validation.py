""" Module for input validation and filtering for the ADNEX model. """

from collections.abc import Iterable

import numpy as np
import pandas as pd

MIN_AGE = 10
MAX_AGE = 110
MAX_CA_125 = 10_000
MAXIMAL_LESION_DIAMETER = 300


def validate_and_filter_input(row: pd.Series, variables_to_use: dict) -> None:
    """
    Validate that the input row contains all necessary columns, and
    that the values conform to the expected constraints.

    Parameters
    ----------
    row : pd.Series
        Input data row.
    variables_to_use : dict
        Dictionary of variable short names to long names required by the model.

    Raises
    ------
    ValueError
        If required columns are missing or input validation fails.
    """
    if not _contains_all_columns(row, variables_to_use.values()):
        missing = [col for col in variables_to_use.values() if col not in row.index]
        raise ValueError(f'The input row is missing required columns: {missing}')

    # Keep only necessary columns
    filtered_row = _filter_input(row, variables_to_use)

    # Validate the input data
    _validate_adnex_model_input(filtered_row)


def has_ca125(row: pd.Series) -> bool:
    """
    Determine whether CA-125 is present and > 0.

    Parameters
    ----------
    row : pd.Series
        Input data row.

    Returns
    -------
    bool
        True if CA-125 is present and > 0, False otherwise.
    """
    return 's_ca_125' in row.index and pd.notna(row['s_ca_125']) and row['s_ca_125'] > 0


def _contains_all_columns(series: pd.Series, columns: Iterable[str]) -> bool:
    """
    Check if the series contains all columns.

    Parameters
    ----------
    series : pd.Series
        Input data row.
    columns : Iterable[str]
        Column names to check for.

    Returns
    -------
    bool
        True if all columns are present, False otherwise.
    """
    return all(column in series.index for column in columns)


def _filter_input(row: pd.Series, variables_to_use: dict) -> pd.Series:
    """
    Filter the input data to keep only the necessary columns.

    Parameters
    ----------
    row : pd.Series
        Input data row.
    variables_to_use : dict
        Dictionary of variable short names to long names required by the model.

    Returns
    -------
    pd.Series
        Filtered input data row.
    """
    filtered_row = row.drop(index=[var for var in row.index if var not in variables_to_use.values()])
    return filtered_row


def _validate_adnex_model_input(row: pd.Series) -> None:
    """
    Validate input data for the ADNEX model.

    Checks:
    - No missing or NaN values.
    - Age in correct range.
    - CA-125 (if present) in correct range.
    - max lesion diameter, max solid component, and papillary projections in valid range.
    - Binary predictors are strictly 0 or 1.

    Parameters
    ----------
    row : pd.Series
        Input data row.

    Raises
    ------
    ValueError
        If any of the validation checks fail.
    """

    # Check for missing values
    if row.isna().any():
        missing_vars = row.index[row.isna()].tolist()
        raise ValueError(f'The following variables are missing (NaN): {missing_vars}')

    def _check_numeric(name: str) -> None:
        if not isinstance(row[name], (int, float, np.number)):
            raise ValueError(f"'{name}' must be numeric, got {type(row[name])}.")

    def _check_range(name: str, low: float, high: float, unit: str = '', extra_note: str = '') -> None:
        val = row[name]
        if not low <= val <= high:
            unit_str = f' {unit}' if unit else ''
            raise ValueError(
                f"'{name}'={val}{unit_str} is out of range. Must be between {low} and {high}{unit_str}. {extra_note}"
            )

    # Validate age
    _check_numeric('age')
    _check_range('age', low=MIN_AGE, high=MAX_AGE, extra_note='(years)')

    # Validate CA-125 if present
    if 's_ca_125' in row.index:
        _check_numeric('s_ca_125')
        if not 0 < row['s_ca_125'] < MAX_CA_125:
            raise ValueError(
                f"Serum CA-125={row['s_ca_125']} U/mL is out of range. Must be between 0 and {MAX_CA_125}."
            )

    # Validate lesion diameters
    _check_numeric('max_lesion_diameter')
    _check_range('max_lesion_diameter', low=0, high=MAXIMAL_LESION_DIAMETER, unit='mm')

    _check_numeric('max_solid_component')
    if row['max_solid_component'] < 0:
        raise ValueError(f"Max solid component={row['max_solid_component']} mm cannot be negative.")
    if row['max_solid_component'] > row['max_lesion_diameter']:
        raise ValueError(
            f"Max solid component={row['max_solid_component']} mm cannot exceed "
            f"max lesion diameter={row['max_lesion_diameter']} mm."
        )

    # Validate number of papillary projections
    if not (
        isinstance(row['number_of_papillary_projections'], (int, np.number))
        and row['number_of_papillary_projections'] in {0, 1, 2, 3, 4}
    ):
        raise ValueError(
            f'Number of papillary projections {row["number_of_papillary_projections"]} is invalid. '
            'Must be 0, 1, 2, 3, or 4. (4 means > 3)'
        )

    # Validate binary variables
    binary_vars = ['more_than_10_locules', 'acoustic_shadows_present', 'ascites_present', 'is_oncology_center']
    for predictor in binary_vars:
        if predictor not in row.index:
            raise ValueError(f"Missing binary predictor: '{predictor}'")
        if row[predictor] not in {0, 1}:
            raise ValueError(f"Binary predictor '{predictor}' must be 0 or 1, got {row[predictor]}.")
