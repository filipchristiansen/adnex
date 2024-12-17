"""
This package implements the ADNEX model for predicting malignancy in adnexal masses.

The ADNEX model uses the following predictors (units in parentheses):

    [A] age (years)
    [B] serum CA-125 (U/mL)
    [C] maximal diameter of lesion (mm)
    [D] maximal diameter of largest solid component (mm)
    [E] more than 10 cyst locules (1 for yes, 0 for no)
    [F] number of papillary structures (0, 1, 2, 3, or 4, where 4 indicates >3)
    [G] acoustic shadows (1 for yes, 0 for no)
    [H] ascites (1 for yes, 0 for no)
    [I] type of centre (1 for oncology centre, 0 for other)

The model can be run with or without CA-125:
- If CA-125 is available and > 0, it is included.
- Otherwise, the model uses the version without CA-125.

References:
- Van Calster B, et al. (2014). BMJ, https://doi.org/10.1136/bmj.g5920
- Landolfo C, et al. (2022). Ultrasound Obstet Gynecol, https://doi.org/10.1002/uog.26080
"""
