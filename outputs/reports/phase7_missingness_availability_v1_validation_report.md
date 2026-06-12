# Phase 7 Validation Report - phase7_missingness_availability_v1

## Scope

This run executed only the pre-registered missingness / measurement availability feature block. It did not generate submissions, run HPO, compare model families, use public leaderboard feedback, use external data, use School as a model feature, modify `logs/experiment_log.csv`, or open Phase 8.

## Environment and Integrity Gates

- Git HEAD: `8b21db5`
- Git status label: `dirty_untracked_only`
- Python: `3.13.13`
- numpy: `2.4.6`
- pandas: `3.0.3`
- scikit-learn: `1.9.0`
- Frozen fold sha256[:16]: `96937649526bcadb`
- Main experiment log unchanged: `true`
- F0 reference max absolute probability delta vs Phase 6 OOF: `0.000000000000`

## Variant Summary

| variant_id | run_status | classification | oof_auc | delta_vs_f0_oof | fold_mean_auc | fold_std_auc | same_sign_positive_folds | slice_guard_triggered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase7_f0_anchor_recheck | trained | anchor_recheck | 0.726616 | 0.000000 | 0.729253 | 0.030629 | 0 | False |
| phase7_f1_median_flags | trained | escalated | 0.811568 | 0.084952 | 0.813093 | 0.034002 | 5 | True |
| phase7_f5_mean_flags | trained | escalated | 0.813066 | 0.086450 | 0.813652 | 0.033866 | 5 | True |
| phase7_f2_median_flags_count | trained | adopted | 0.811650 | 0.085034 | 0.812456 | 0.029238 | 5 | False |
| phase7_f3_median_flags_count_bins | trained | escalated | 0.810606 | 0.083989 | 0.812605 | 0.028212 | 5 | True |
| phase7_f6_mean_flags_count | not_run_gated | not_run |  |  |  |  | 0 | False |

## Fold Scores

| variant_id | fold | n_valid | n_positive | n_negative | positive_rate | roc_auc |
| --- | --- | --- | --- | --- | --- | --- |
| phase7_f0_anchor_recheck | 0 | 557 | 361 | 196 | 0.648115 | 0.690076 |
| phase7_f0_anchor_recheck | 1 | 556 | 361 | 195 | 0.649281 | 0.751758 |
| phase7_f0_anchor_recheck | 2 | 556 | 361 | 195 | 0.649281 | 0.761581 |
| phase7_f0_anchor_recheck | 3 | 556 | 360 | 196 | 0.647482 | 0.704939 |
| phase7_f0_anchor_recheck | 4 | 556 | 360 | 196 | 0.647482 | 0.737911 |
| phase7_f1_median_flags | 0 | 557 | 361 | 196 | 0.648115 | 0.785841 |
| phase7_f1_median_flags | 1 | 556 | 361 | 195 | 0.649281 | 0.827658 |
| phase7_f1_median_flags | 2 | 556 | 361 | 195 | 0.649281 | 0.834377 |
| phase7_f1_median_flags | 3 | 556 | 360 | 196 | 0.647482 | 0.768920 |
| phase7_f1_median_flags | 4 | 556 | 360 | 196 | 0.647482 | 0.848668 |
| phase7_f5_mean_flags | 0 | 557 | 361 | 196 | 0.648115 | 0.789403 |
| phase7_f5_mean_flags | 1 | 556 | 361 | 195 | 0.649281 | 0.830925 |
| phase7_f5_mean_flags | 2 | 556 | 361 | 195 | 0.649281 | 0.823979 |
| phase7_f5_mean_flags | 3 | 556 | 360 | 196 | 0.647482 | 0.769615 |
| phase7_f5_mean_flags | 4 | 556 | 360 | 196 | 0.647482 | 0.854337 |
| phase7_f2_median_flags_count | 0 | 557 | 361 | 196 | 0.648115 | 0.789389 |
| phase7_f2_median_flags_count | 1 | 556 | 361 | 195 | 0.649281 | 0.832382 |
| phase7_f2_median_flags_count | 2 | 556 | 361 | 195 | 0.649281 | 0.825854 |
| phase7_f2_median_flags_count | 3 | 556 | 360 | 196 | 0.647482 | 0.773724 |
| phase7_f2_median_flags_count | 4 | 556 | 360 | 196 | 0.647482 | 0.840930 |
| phase7_f3_median_flags_count_bins | 0 | 557 | 361 | 196 | 0.648115 | 0.790350 |
| phase7_f3_median_flags_count_bins | 1 | 556 | 361 | 195 | 0.649281 | 0.828688 |
| phase7_f3_median_flags_count_bins | 2 | 556 | 361 | 195 | 0.649281 | 0.835542 |
| phase7_f3_median_flags_count_bins | 3 | 556 | 360 | 196 | 0.647482 | 0.774532 |
| phase7_f3_median_flags_count_bins | 4 | 556 | 360 | 196 | 0.647482 | 0.833914 |

## F1 vs F5 vs V7 Reference

- F0 OOF ROC-AUC: `0.726616`.
- Phase 6A V7 reference OOF ROC-AUC: `0.802271`.
- F1 OOF ROC-AUC: `0.811568`.
- F5 OOF ROC-AUC: `0.813066`.
- F5 - F1 OOF delta: `0.001498`.
- F6 run: `False`.
The V7 reference is used only as historical context for how much of the mean-imputation signal is recovered by explicit row-wise availability features.

## Slice Findings

| variant_id | slice_name | slice_value | n | roc_auc | delta_vs_f0 | status |
| --- | --- | --- | --- | --- | --- | --- |
| phase7_f3_median_flags_count_bins | Player_Type | special_teams | 95 | 0.826286 | 0.221714 | computed |
| phase7_f1_median_flags | Player_Type | special_teams | 95 | 0.821714 | 0.217143 | computed |
| phase7_f1_median_flags | Position_Type | kicking_specialist | 82 | 0.843091 | 0.216237 | computed |
| phase7_f3_median_flags_count_bins | available_measurement_count | 0 | 56 | 0.895928 | 0.214178 | computed |
| phase7_f3_median_flags_count_bins | measurement_completeness_group | 0 | 56 | 0.895928 | 0.214178 | computed |
| phase7_f5_mean_flags | available_measurement_count | 0 | 56 | 0.894419 | 0.212670 | computed |
| phase7_f5_mean_flags | measurement_completeness_group | 0 | 56 | 0.894419 | 0.212670 | computed |
| phase7_f3_median_flags_count_bins | Position_Type | kicking_specialist | 82 | 0.838407 | 0.211553 | computed |
| phase7_f5_mean_flags | Player_Type | special_teams | 95 | 0.808000 | 0.203429 | computed |
| phase7_f2_median_flags_count | available_measurement_count | 0 | 56 | 0.883861 | 0.202112 | computed |
| phase7_f2_median_flags_count | measurement_completeness_group | 0 | 56 | 0.883861 | 0.202112 | computed |
| phase7_f1_median_flags | available_measurement_count | 0 | 56 | 0.879336 | 0.197587 | computed |
| phase7_f1_median_flags | measurement_completeness_group | 0 | 56 | 0.879336 | 0.197587 | computed |
| phase7_f2_median_flags_count | Player_Type | special_teams | 95 | 0.799429 | 0.194857 | computed |
| phase7_f5_mean_flags | Position_Type | kicking_specialist | 82 | 0.821233 | 0.194379 | computed |

## Leakage Checklist

- All preprocessing was fitted inside each training fold through `Pipeline` / `ColumnTransformer`.
- Test data was used only for contract checks; no test fitting, tuning, selection, final inference, or submission occurred.
- `School` was excluded from every model feature matrix and used only for the diagnostic frequent-vs-rare slice.
- No target encoding, feature selection, dimensionality reduction, HPO, ensembles, model-family comparison, or leaderboard feedback was used.
- Positive-class probabilities were extracted only after verifying `estimator.classes_` contained label `1` exactly once.
- Report language is associative and predictive only, not causal.

## Warnings and Decision State

- Classification counts: `{'escalated': 3, 'anchor_recheck': 1, 'adopted': 1, 'not_run': 1}`.
- Escalated variants: `['phase7_f1_median_flags', 'phase7_f5_mean_flags', 'phase7_f3_median_flags_count_bins']`.
- F4 was not authorized and was not executed. Any F4 activation requires a new Project Authorization Note and run_id.
- Acceptance and commit remain gated on explicit user/project director authorization.
- Phase 8 remains locked.
