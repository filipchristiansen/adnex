# Assessment of Different NEoplasias in the adneXa(ADNEX) model

<a href="https://github.com/psf/black/actions"><img alt="Actions Status" src="https://github.com/psf/black/workflows/Test/badge.svg"></a>
<a href="https://coveralls.io/github/psf/black?branch=main"><img alt="Coverage Status" src="https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_100.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Table of Contents

- [Assessment of Different NEoplasias in the adneXa(ADNEX) model](#assessment-of-different-neoplasias-in-the-adnexaadnex-model)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [References](#references)
  - [Contributing](#contributing)
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

2. `predict_risk_of_cancer`: A function that takes a pandas Series containing the ADNEX variables as input and returns the predicted risk of malignancy (Borderline + Stage I + Stage II-IV + Metastatic).

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

Here is an example of how to use the `predict_risk_of_cancer` function:

```python
import pandas as pd
import adnex

data = ... # Create a pandas Series with the ADNEX variables (see above)

risk = adnex.predict_risk_of_cancer(data)

print(risk)
```

Output:

```bash
0.387119
```

## References

- [Van Calster B, et al. *BMJ* (2014)](https://doi.org/10.1136/bmj.g5920)
- [Landolfo C, et al. *Ultrasound Obstet Gynecol* (2022)](https://doi.org/10.1002/uog.26080)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact the author at [filip.christiansen.2@ki.se](mailto:filip.christiansen.2@ki.se) with the subject line "GitHub adnex: [Your Subject]".
