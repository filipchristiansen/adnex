# Assessment of Different NEoplasias in the adneXa(ADNEX) model

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/filipchristiansen/adnex/actions/workflows/ci.yml/badge.svg)](https://github.com/filipchristiansen/adnex/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/filipchristiansen/adnex/graph/badge.svg?token=kUQsPQBVL3)](https://codecov.io/gh/filipchristiansen/adnex)
[![PyPI version](https://badge.fury.io/py/adnex.svg)](https://badge.fury.io/py/adnex)

## Table of Contents

- [Assessment of Different NEoplasias in the adneXa(ADNEX) model](#assessment-of-different-neoplasias-in-the-adnexaadnex-model)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [References](#references)
    - [ADNEX model](#adnex-model)
    - [Simple Rules model](#simple-rules-model)
    - [Simple Rules Risk model](#simple-rules-risk-model)
  - [Contributing](#contributing)
    - [Open an Issue on GitHub to report a bug](#open-an-issue-on-github-to-report-a-bug)
    - [Open an Issue on GitHub to request a new feature](#open-an-issue-on-github-to-request-a-new-feature)
    - [Create a Pull Request on GitHub to contribute code](#create-a-pull-request-on-github-to-contribute-code)
  - [License](#license)
  - [Contact](#contact)

## Dependencies

- Python 3.8+
- pandas
- numpy

## Description

This is an unofficial Python implementation of the **Assessment of Different NEoplasias in the adneXa (ADNEX)** model developed by the **International Ovarian Tumor Analysis (IOTA) group** for the preoperative assessment of adnexal masses ([Van Calster et al. (2014)](https://doi.org/10.1136/bmj.g5920)).

The model is used to predict the risk of malignancy, as well as to differentiate between benign, borderline, early and advanced stage invasive, and secondary metastatic tumours.

The model is based on logistic regression and uses the following ultrasound and clinical variables:

- [A] **age** (years)
- [B] **serum CA-125** (U/ml)
- [C] **maximal lesion diameter** (mm)
- [D] **maximal diameter of largest solid component** (mm)
- [E] **more than 10 cyst locules** (1 for yes, 0 for no)
- [F] **number of papillary projections** (0, 1, 2, 3, or 4, where 4 indicates > 3)
- [G] **acoustic shadows** (1 for yes, 0 for no)
- [H] **ascites** (1 for yes, 0 for no)
- [I] **type of centre** (1 for oncology centre, 0 for other)

The model is available in two versions, with and without CA-125. If CA-125 is available and not 'NaN', the model uses the version with CA-125. Otherwise, it uses the version without CA-125.

The model provides the predicted probabilities of the different types of neoplasias (Benign, Borderline, Stage I, Stage II-IV, Metastatic) and the predicted risk of malignancy (Borderline + Stage I + Stage II-IV + Metastatic).

## Installation

You can install the package using `pip`:

```bash
pip install adnex
```

Alternatively, install it from the source:

```bash
git clone https://github.com/filipchristiansen/adnex.git
cd adnex
pip install -e .
```

## Usage

The package provides two functions:

1. `predict_risks`: A function that takes a pandas Series containing the ADNEX variables as input and returns a pandas Series with the predicted probabilities of the different types of neoplasias (Benign, Borderline, Stage I, Stage II-IV, Metastatic).

2. `predict_cancer_risk`: A function that takes a pandas Series containing the ADNEX variables as input and returns the predicted risk of malignancy (Borderline + Stage I + Stage II-IV + Metastatic).

Here is an example of how to use the `predict_risks` function:

```python
import pandas as pd
import adnex

# Create a pandas Series with the ADNEX variables
data = pd.Series(
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

# Get the predicted probabilities
probs = adnex.predict_risks(data)
print(probs)
```

Output:

``` bash
Benign                0.612881
Borderline            0.081589
Stage I cancer        0.111828
Stage II-IV cancer    0.168236
Metastatic cancer     0.025466
dtype: float64
```

Here is an example of how to use the `predict_cancer_risk` function:

```python
import pandas as pd
import adnex

data = ... # Create a pandas Series with the ADNEX variables (see above)

# Get the predicted risk of cancer
risk = adnex.predict_cancer_risk(data)

print(risk)
```

Output:

```bash
0.387119
```

Here is an example of how to use the `predict_cancer_risk` function for multiple observations:

```python
import numpy as np
import pandas as pd
import adnex

# Create the DataFrame with the ADNEX variables for multiple observations
data = pd.DataFrame(
    {
      'age': [46, 52, 38, 29, 60, 45, 50, 33, 61, 40],
      's_ca_125': [68, np.nan, 120, np.nan, 85, 90, 55, np.nan, 100, 75],
      'max_lesion_diameter': [88, 45, 70, 100, 55, 60, 72, 80, 65, 50],
      'max_solid_component': [50, 25, 35, 60, 30, 40, 25, 50, 35, 20],
      'more_than_10_locules': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      'number_of_papillary_projections': [2, 4, 1, 3, 0, 1, 2, 3, 4, 0],
      'acoustic_shadows_present': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
      'ascites_present': [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      'is_oncology_center': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
  }
)

# Get the predicted risk of cancer for each observation
data['predicted_risk'] = data.apply(calculate_risk, axis=1)

print(data['predicted_risk'])
```

Output:

```bash
0    0.387119
1    0.986933
2    0.102789
3    0.983853
4    0.102129
5    0.637533
6    0.412924
7    0.831998
8    0.874002
9    0.289273
Name: predicted_risk, dtype: float64
```

## References

### ADNEX model

- [Van Calster B, et al. *BMJ* (2014)](https://doi.org/10.1136/bmj.g5920)
- [Landolfo C, et al. *Ultrasound Obstet Gynecol* (2022)](https://doi.org/10.1002/uog.26080)

### Simple Rules model

- [Timmerman, D. et al. *Ultrasound Obstet Gynecol* (2008)](https://doi.org/10.1002/uog.5365)

### Simple Rules Risk model

- [Timmerman, D. et al. *Am J Obstet Gynecol* (2016)](https://doi.org/10.1016/j.ajog.2016.01.007)

## Contributing

Contributions are welcome! Here are a few ways you can help:

### Open an Issue on GitHub to report a bug

- Please provide a detailed description of the bug, including the steps to reproduce it.
- If possible, provide a minimal code example that reproduces the bug.
- If you have a suggestion for how to fix the bug, please include that as well.

### Open an Issue on GitHub to request a new feature

- Please provide a detailed description of the feature you would like to see.
- If possible, provide a use case for the feature and any relevant examples.

### Create a Pull Request on GitHub to contribute code

1. Fork the repository.
2. Make your changes, add and run tests, and update the documentation if relevant.
3. Open a Pull Request with a detailed description of your changes.
4. Your Pull Request will be reviewed by the maintainers, and you may be asked to make changes before it is accepted.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact the author at [filip.christiansen.2@ki.se](mailto:filip.christiansen.2@ki.se) with the subject line "GitHub adnex: [Your Subject]".
