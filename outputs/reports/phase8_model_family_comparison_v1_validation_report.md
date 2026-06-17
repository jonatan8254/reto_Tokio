# Phase 8 Wave 1 Validation Report

## Executive Summary

Phase 8 Wave 1 executed the authorized sklearn-native model-family comparison on the accepted Phase 7/7B F2 feature set. This report is evidence only: candidate selection, acceptance, and commit remain gated on explicit project director authorization.

- Experiment ID: `phase8_model_family_comparison_v1`
- Start HEAD: `f8c791103adc4a259e68a9fff2ccd3e43166801c`
- Environment: Python 3.13.13, pandas 3.0.3, scikit-learn 1.9.0, numpy 2.4.6
- M0 OOF ROC-AUC: `0.8116502602456482`
- Persisted F2 OOF ROC-AUC: `0.8116502602456482`
- M0 max absolute probability difference vs persisted F2: `6.661338147750939e-16`

## Authorized Scope

- Authorized models: m0, m1, m2, m3, m4.
- Not authorized: m5, xgboost, lightgbm, catboost, deep tabular models, HPO, submissions, ensembles, leaderboard use, external data, package installation, environment mutation, Phase 9, Phase 10, Phase 11.
- School remained excluded from all feature matrices.

## Model Summary

| model_key | run_status | classification | oof_auc | delta_vs_m0_oof | fold_mean_auc | fold_std_auc | same_sign_positive_folds | slice_guard_triggered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | trained | reference_reproduced | 0.811650260246 | 0.000000000000 | 0.812455750181 | 0.029238291859 | 0 | False |
| m1_logistic_regression | trained | escalated | 0.827082106963 | 0.015431846718 | 0.827682354745 | 0.029565105317 | 4 | True |
| m2_random_forest_default | trained | no_qualifying_evidence | 0.805523797534 | -0.006126462712 | 0.806100118416 | 0.029677785621 | 2 | True |
| m3_extra_trees_default | trained | no_qualifying_evidence | 0.789693841326 | -0.021956418920 | 0.790354245576 | 0.030487370975 | 0 | True |
| m4_hist_gradient_boosting | trained | no_qualifying_evidence | 0.809329372654 | -0.002320887591 | 0.809202690310 | 0.027169912118 | 1 | True |

## Fold-Level Metrics

| model_key | fold | n_valid | n_positive | n_negative | roc_auc | delta_vs_m0_fold_auc |
| --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | 0 | 557 | 361 | 196 | 0.789388885748 | 0.000000000000 |
| m0_random_forest_frozen | 1 | 556 | 361 | 195 | 0.832381561190 | 0.000000000000 |
| m0_random_forest_frozen | 2 | 556 | 361 | 195 | 0.825854108957 | 0.000000000000 |
| m0_random_forest_frozen | 3 | 556 | 360 | 196 | 0.773724489796 | 0.000000000000 |
| m0_random_forest_frozen | 4 | 556 | 360 | 196 | 0.840929705215 | 0.000000000000 |
| m1_logistic_regression | 0 | 557 | 361 | 196 | 0.797529538131 | 0.008140652383 |
| m1_logistic_regression | 1 | 556 | 361 | 195 | 0.850216634704 | 0.017835073514 |
| m1_logistic_regression | 2 | 556 | 361 | 195 | 0.862816961432 | 0.036962852475 |
| m1_logistic_regression | 3 | 556 | 360 | 196 | 0.798653628118 | 0.024929138322 |
| m1_logistic_regression | 4 | 556 | 360 | 196 | 0.829195011338 | -0.011734693878 |
| m2_random_forest_default | 0 | 557 | 361 | 196 | 0.790378201142 | 0.000989315394 |
| m2_random_forest_default | 1 | 556 | 361 | 195 | 0.841579657646 | 0.009198096456 |
| m2_random_forest_default | 2 | 556 | 361 | 195 | 0.822274309255 | -0.003579799702 |
| m2_random_forest_default | 3 | 556 | 360 | 196 | 0.764576247166 | -0.009148242630 |
| m2_random_forest_default | 4 | 556 | 360 | 196 | 0.811692176871 | -0.029237528345 |
| m3_extra_trees_default | 0 | 557 | 361 | 196 | 0.754621516197 | -0.034767369552 |
| m3_extra_trees_default | 1 | 556 | 361 | 195 | 0.826862703317 | -0.005518857873 |
| m3_extra_trees_default | 2 | 556 | 361 | 195 | 0.811826124014 | -0.014027984942 |
| m3_extra_trees_default | 3 | 556 | 360 | 196 | 0.765093537415 | -0.008630952381 |
| m3_extra_trees_default | 4 | 556 | 360 | 196 | 0.793367346939 | -0.047562358277 |
| m4_hist_gradient_boosting | 0 | 557 | 361 | 196 | 0.798843914297 | 0.009455028549 |
| m4_hist_gradient_boosting | 1 | 556 | 361 | 195 | 0.825257475673 | -0.007124085517 |
| m4_hist_gradient_boosting | 2 | 556 | 361 | 195 | 0.818879181760 | -0.006974927197 |
| m4_hist_gradient_boosting | 3 | 556 | 360 | 196 | 0.767049319728 | -0.006675170068 |
| m4_hist_gradient_boosting | 4 | 556 | 360 | 196 | 0.835983560091 | -0.004946145125 |

## Slice Diagnostics Summary

The following mandatory slice guard rows triggered escalation:

| model_key | slice_name | slice_value | n | n_positive | n_negative | roc_auc | m0_slice_auc | delta_vs_m0_slice_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m1_logistic_regression | Year | 2011 | 278 | 188 | 90 | 0.772695035461 | 0.793439716312 | -0.020744680851 |
| m1_logistic_regression | Age_missing | 1 | 435 | 8 | 427 | 0.544203747073 | 0.691744730679 | -0.147540983607 |
| m1_logistic_regression | available_measurement_count | 0 | 56 | 39 | 17 | 0.858220211161 | 0.883861236802 | -0.025641025641 |
| m1_logistic_regression | available_measurement_count | 4 | 269 | 166 | 103 | 0.842613171131 | 0.870920575506 | -0.028307404375 |
| m1_logistic_regression | measurement_completeness_group | 0 | 56 | 39 | 17 | 0.858220211161 | 0.883861236802 | -0.025641025641 |
| m2_random_forest_default | Position_Type | defensive_lineman | 391 | 277 | 114 | 0.761131167268 | 0.793226296789 | -0.032095129521 |
| m2_random_forest_default | Position_Type | kicking_specialist | 82 | 21 | 61 | 0.787275565964 | 0.814988290398 | -0.027712724434 |
| m2_random_forest_default | Year | 2011 | 278 | 188 | 90 | 0.762115839243 | 0.793439716312 | -0.031323877069 |
| m2_random_forest_default | Year | 2014 | 260 | 173 | 87 | 0.694073483489 | 0.718357584214 | -0.024284100724 |
| m2_random_forest_default | Age_missing | 1 | 435 | 8 | 427 | 0.626756440281 | 0.691744730679 | -0.064988290398 |
| m2_random_forest_default | available_measurement_count | 0 | 56 | 39 | 17 | 0.827300150830 | 0.883861236802 | -0.056561085973 |
| m2_random_forest_default | available_measurement_count | 1 | 240 | 127 | 113 | 0.794369730332 | 0.835307644067 | -0.040937913734 |
| m2_random_forest_default | available_measurement_count | 2 | 236 | 148 | 88 | 0.742667383292 | 0.772804054054 | -0.030136670762 |
| m2_random_forest_default | measurement_completeness_group | 0 | 56 | 39 | 17 | 0.827300150830 | 0.883861236802 | -0.056561085973 |
| m2_random_forest_default | measurement_completeness_group | 1 | 613 | 356 | 257 | 0.786025007651 | 0.811584619420 | -0.025559611769 |
| m3_extra_trees_default | Player_Type | defense | 1241 | 867 | 374 | 0.784925892345 | 0.813868894522 | -0.028943002177 |
| m3_extra_trees_default | Player_Type | offense | 1445 | 911 | 534 | 0.770263158977 | 0.790484177983 | -0.020221019006 |
| m3_extra_trees_default | Player_Type | special_teams | 95 | 25 | 70 | 0.728285714286 | 0.799428571429 | -0.071142857143 |
| m3_extra_trees_default | Position_Type | defensive_lineman | 391 | 277 | 114 | 0.731949458484 | 0.793226296789 | -0.061276838305 |
| m3_extra_trees_default | Position_Type | kicking_specialist | 82 | 21 | 61 | 0.754098360656 | 0.814988290398 | -0.060889929742 |
| m3_extra_trees_default | Position_Type | offensive_lineman | 435 | 289 | 146 | 0.761387875053 | 0.785870028914 | -0.024482153861 |
| m3_extra_trees_default | Year | 2009 | 253 | 160 | 93 | 0.779469086022 | 0.818682795699 | -0.039213709677 |
| m3_extra_trees_default | Year | 2010 | 262 | 172 | 90 | 0.791537467700 | 0.821834625323 | -0.030297157623 |
| m3_extra_trees_default | Year | 2011 | 278 | 188 | 90 | 0.745005910165 | 0.793439716312 | -0.048433806147 |
| m3_extra_trees_default | Year | 2012 | 261 | 169 | 92 | 0.766047080010 | 0.788461538462 | -0.022414458451 |
| m3_extra_trees_default | Year | 2016 | 260 | 169 | 91 | 0.771148969374 | 0.810325768906 | -0.039176799532 |
| m3_extra_trees_default | Year | 2017 | 274 | 185 | 89 | 0.767810507136 | 0.814151229882 | -0.046340722745 |
| m3_extra_trees_default | Year | 2018 | 250 | 153 | 97 | 0.843137254902 | 0.866787952294 | -0.023650697392 |
| m3_extra_trees_default | Age_missing | 0 | 2346 | 1795 | 551 | 0.632157788574 | 0.669830493051 | -0.037672704478 |
| m3_extra_trees_default | Age_missing | 1 | 435 | 8 | 427 | 0.643442622951 | 0.691744730679 | -0.048302107728 |
| m3_extra_trees_default | available_measurement_count | 0 | 56 | 39 | 17 | 0.787330316742 | 0.883861236802 | -0.096530920060 |
| m3_extra_trees_default | available_measurement_count | 1 | 240 | 127 | 113 | 0.784022019371 | 0.835307644067 | -0.051285624695 |
| m3_extra_trees_default | available_measurement_count | 2 | 236 | 148 | 88 | 0.722934582310 | 0.772804054054 | -0.049869471744 |
| m3_extra_trees_default | available_measurement_count | 3 | 137 | 81 | 56 | 0.782407407407 | 0.820767195767 | -0.038359788360 |
| m3_extra_trees_default | available_measurement_count | 4 | 269 | 166 | 103 | 0.838051234062 | 0.870920575506 | -0.032869341443 |
| m3_extra_trees_default | measurement_completeness_group | 0 | 56 | 39 | 17 | 0.787330316742 | 0.883861236802 | -0.096530920060 |
| m3_extra_trees_default | measurement_completeness_group | 1 | 613 | 356 | 257 | 0.765378393739 | 0.811584619420 | -0.046206225681 |
| m3_extra_trees_default | measurement_completeness_group | 2 | 723 | 453 | 270 | 0.802841141362 | 0.823399558499 | -0.020558417137 |
| m3_extra_trees_default | frequent_vs_rare_school_group | frequent | 2559 | 1682 | 877 | 0.783184553872 | 0.806773917135 | -0.023589363263 |
| m4_hist_gradient_boosting | Position_Type | offensive_lineman | 435 | 289 | 146 | 0.756102763426 | 0.785870028914 | -0.029767265488 |
| m4_hist_gradient_boosting | Year | 2011 | 278 | 188 | 90 | 0.732505910165 | 0.793439716312 | -0.060933806147 |
| m4_hist_gradient_boosting | Year | 2016 | 260 | 169 | 91 | 0.789128031732 | 0.810325768906 | -0.021197737174 |
| m4_hist_gradient_boosting | Year | 2017 | 274 | 185 | 89 | 0.742241117522 | 0.814151229882 | -0.071910112360 |
| m4_hist_gradient_boosting | Age_missing | 1 | 435 | 8 | 427 | 0.583138173302 | 0.691744730679 | -0.108606557377 |
| m4_hist_gradient_boosting | available_measurement_count | 0 | 56 | 39 | 17 | 0.819004524887 | 0.883861236802 | -0.064856711916 |
| m4_hist_gradient_boosting | measurement_completeness_group | 0 | 56 | 39 | 17 | 0.819004524887 | 0.883861236802 | -0.064856711916 |

## Leakage Checklist

- Official train/test/sample CSVs only; test used only for contract checks.
- Frozen folds loaded from file and SHA-checked; folds were not recomputed.
- F2 features are row-wise and fixed; no per-model feature engineering was introduced.
- All learned preprocessing was fitted inside fold-specific sklearn pipelines.
- Positive-class probabilities were extracted only after verifying `estimator.classes_` contains label `1` exactly once.
- No target encoding, feature selection, dimensionality reduction, HPO, ensemble, submission, public leaderboard use, or external data was used.
- `logs/experiment_log.csv` remained byte-identical; candidate log was written separately under `outputs/reports/`.

## Threshold Interpretation

The OOF gain threshold `0.005436` and same-sign fold rule `4/5` are evidence flags, not an automatic winner-selection mechanism. The threshold was inherited from prior RF seed-noise analysis and may not fully describe per-family variance.

## Phase Locks

Phase 9 remains locked.
Phase 10 remains locked.
Phase 11 remains locked.
