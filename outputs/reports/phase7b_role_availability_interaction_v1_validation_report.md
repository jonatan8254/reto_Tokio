# Phase 7B Validation Report - phase7b_role_availability_interaction_v1

## Executive Summary

F4 classification: `rejected`.
F2 OOF ROC-AUC: `0.811650260246`.
F4 OOF ROC-AUC: `0.809369070182`.
OOF delta F4 - F2: `-0.002281190064`.
Same-sign fold count: `1/5`.
Slice guard triggered: `False`.

## Authorized Hypothesis

`available_measurement_count x Player_Type` is evaluated as the only F4 addition over F2. F4 is compared against persisted F2 OOF predictions, not against F0.

## Environment and Contract

- Git HEAD: `8b21db5`
- Python: `3.13.13`
- pandas: `3.0.3`
- scikit-learn: `1.9.0`
- numpy: `2.4.6`
- Frozen fold sha256[:16]: `96937649526bcadb`
- Main experiment log unchanged: `true`

## F4 Implementation

The interaction is implemented inside a scikit-learn transformer. `Player_Type` one-hot categories are fit only on each training fold, validation rows are transformed with `handle_unknown="ignore"`, and the resulting one-hot columns are multiplied by the row-wise `available_measurement_count`.

## Fold-Level Evidence

| fold | n_valid | n_positive | n_negative | f2_auc | f4_auc | delta_f4_minus_f2 | sign |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 557 | 361 | 196 | 0.789389 | 0.786025 | -0.003364 | non_positive |
| 1 | 556 | 361 | 195 | 0.832382 | 0.827928 | -0.004453 | non_positive |
| 2 | 556 | 361 | 195 | 0.825854 | 0.838923 | 0.013069 | positive |
| 3 | 556 | 360 | 196 | 0.773724 | 0.767900 | -0.005825 | non_positive |
| 4 | 556 | 360 | 196 | 0.840930 | 0.837018 | -0.003912 | non_positive |

## Slice Report Summary

| slice_name | slice_value | n | f2_auc | f4_auc | delta_f4_minus_f2 | status |
| --- | --- | --- | --- | --- | --- | --- |
| Player_Type | special_teams | 95 | 0.799429 | 0.829714 | 0.030286 | computed |
| Year | 2013 | 256 | 0.744324 | 0.765019 | 0.020695 | computed |
| Position_Type | kicking_specialist | 82 | 0.814988 | 0.834504 | 0.019516 | computed |
| available_measurement_count | 0 | 56 | 0.883861 | 0.865762 | -0.018100 | computed |
| measurement_completeness_group | 0 | 56 | 0.883861 | 0.865762 | -0.018100 | computed |
| Year | 2017 | 274 | 0.814151 | 0.799089 | -0.015062 | computed |
| Year | 2011 | 278 | 0.793440 | 0.782683 | -0.010757 | computed |
| Year | 2016 | 260 | 0.810326 | 0.799922 | -0.010404 | computed |
| available_measurement_count | 3 | 137 | 0.820767 | 0.830467 | 0.009700 | computed |
| Year | 2014 | 260 | 0.718358 | 0.709986 | -0.008372 | computed |
| Position_Type | offensive_lineman | 435 | 0.785870 | 0.778239 | -0.007631 | computed |
| Position_Type | line_backer | 309 | 0.741640 | 0.749259 | 0.007619 | computed |
| available_measurement_count | 5 | 454 | 0.795698 | 0.788187 | -0.007511 | computed |
| available_measurement_count | 1 | 240 | 0.835308 | 0.828096 | -0.007212 | computed |
| available_measurement_count | 2 | 236 | 0.772804 | 0.766585 | -0.006219 | computed |

## Leakage Checklist

- No test fitting, tuning, preprocessing, feature selection, final inference, or submission occurred.
- No global preprocessing was used for the F4 interaction.
- `School` was not used as a feature; it was used only for the diagnostic frequent-vs-rare slice.
- No external data, leaderboard data, HPO, model-family comparison, BMI, completeness bins as features, or extra interactions were used.
- Positive-class probabilities were extracted only after verifying `estimator.classes_` contained label `1` exactly once.
- Phase 8 remains locked.

## Final Recommendation

OOF gain and/or same-sign fold criterion did not pass.
