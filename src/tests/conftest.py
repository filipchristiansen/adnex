""" Pytest fixtures for the tests. """

import pandas as pd
import pytest


@pytest.fixture
def sample_input():
    return pd.Series(
        {
            'age': 46,
            's_ca_125': 68,
            'max_lesion_diameter': 88,
            'max_solid_component': 50,
            'more_than_10_locules': 0,
            'number_of_papillary_projections': 2,
            'acoustic_shadows_present': 1,
            'ascites_present': 1,
            'is_oncology_center': 0,
        }
    )


@pytest.fixture
def expected_output():
    # Expected output based on https://www.evidencio.com/models/show/946
    return pd.Series(
        {
            'Benign': 0.613,
            'Borderline': 0.082,
            'Malignant': 0.387,
            'Stage I cancer': 0.112,
            'Stage II-IV cancer': 0.168,
            'Metastatic cancer': 0.025,
        }
    )
