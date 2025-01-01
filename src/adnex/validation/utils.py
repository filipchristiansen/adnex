""" Helper functions for validation of input values. """

import pandas as pd


def has_ca125(row: pd.Series) -> bool:
    """
    Check if the input row contains a value for serum CA-125.

    Parameters
    ----------
    row : pd.Series
        Input data row.

    Returns
    -------
    bool
        True if 's_ca_125' is present and not NaN, False otherwise.
    """
    if 's_ca_125' not in row.index or pd.isna(row['s_ca_125']):
        return False

    return True
