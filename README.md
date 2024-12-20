# Assessment of Different NEoplasias in the adneXa(ADNEX) model

## Description

This is an unofficial python implementation of the **Assessment of Different NEoplasias in the adneXa (ADNEX)** model developed by the **International Ovarian Tumor Analysis (IOTA) group**. The model is used to predict the risk of malignancy in adnexal masses based on ultrasound findings and clinical data. The model is based on logistic regression and uses the following predictors (units in parentheses):

- [A] **age** (years)
- [B] **serum CA-125** (U/mL)
- [C] **maximal lesion diameter** (mm)
- [D] **maximal diameter of largest solid component** (mm)
- [E] **more than 10 cyst locules** (1 for yes, 0 for no)
- [F] **number of papillary projections** (0, 1, 2, 3, or 4, where 4 indicates >3)
- [G] **acoustic shadows** (1 for yes, 0 for no)
- [H] **ascites** (1 for yes, 0 for no)
- [I] **type of centre** (1 for oncology centre, 0 for other)

The ADNEX model is available in two versions, with and without CA-125. If CA-125 is available and greater than 0 U/mL, the model uses the version with CA-125. Otherwise, it uses the version without CA-125.

## References

- [Van Calster B, et al. *BMJ* (2014)](https://doi.org/10.1136/bmj.g5920)
- [Landolfo C, et al. *Ultrasound Obstet Gynecol* (2022)](https://doi.org/10.1002/uog.26080)
