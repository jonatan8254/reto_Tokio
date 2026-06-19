# Phase 9A AUC/Raking Diagnostics Report

## Executive Summary

Phase 9A executed as a read-only diagnostic pass over persisted OOF predictions. No models were trained, no OOF predictions were edited, no HPO was run, no submissions were generated, and no final winner was selected.

- Authorized HEAD: `020743681e10b94e26631cd4db01d244b45ba0e8`
- Observed HEAD: `020743681e10b94e26631cd4db01d244b45ba0e8`
- Experiment ID: `phase9a_auc_ranking_diagnostics_v1`
- Global positive rate: `0.648328` (1803/2781)
- Main experiment log: read before and verified unchanged after artifact generation.

## Integrity Gates

| model_key | row_count | positive_count | negative_count | positive_rate | passed |
| --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | 2781 | 1803 | 978 | 0.6483279396 | True |
| m1_logistic_regression | 2781 | 1803 | 978 | 0.6483279396 | True |
| xgboost | 2781 | 1803 | 978 | 0.6483279396 | True |
| lightgbm | 2781 | 1803 | 978 | 0.6483279396 | True |
| catboost | 2781 | 1803 | 978 | 0.6483279396 | True |

## AUC Reproduction

| model_key | accepted_auc | recomputed_auc | abs_diff | status |
| --- | --- | --- | --- | --- |
| m0_random_forest_frozen | 0.8116502602 | 0.8116502602 | 0.0000000000 | PASS |
| m1_logistic_regression | 0.8270821070 | 0.8270821070 | 0.0000000000 | PASS |
| xgboost | 0.8113477084 | 0.8113477084 | 0.0000000000 | PASS |
| lightgbm | 0.8062204891 | 0.8062204891 | 0.0000000000 | PASS |
| catboost | 0.8202943969 | 0.8202943969 | 0.0000000000 | PASS |

## Global Metrics

| model_key | source_status | technical_verdict | roc_auc | average_precision | negative_class_average_precision | brier_score | delta_auc_vs_m0 | delta_auc_vs_m1 | same_sign_positive_folds_vs_m0 | same_sign_positive_folds_vs_m1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | reference_anchor | anchor | 0.8116502602 | 0.8638108888 | 0.7787191920 | 0.1586025745 | 0.0000000000 | -0.0154318467 | 0.0000000000 | 1.0000000000 |
| m1_logistic_regression | candidate_with_warning | carry | 0.8270821070 | 0.8741841782 | 0.7904989158 | 0.1414342729 | 0.0154318467 | 0.0000000000 | 4.0000000000 | 0.0000000000 |
| xgboost | no_qualifying_evidence | drop-candidate | 0.8113477084 | 0.8640251038 | 0.7810117011 | 0.1574592320 | -0.0003025519 | -0.0157343986 | 1.0000000000 | 1.0000000000 |
| lightgbm | no_qualifying_evidence | drop-candidate | 0.8062204891 | 0.8581335085 | 0.7770412525 | 0.1664000087 | -0.0054297711 | -0.0208616178 | 1.0000000000 | 0.0000000000 |
| catboost | escalated_candidate_with_warning | observe | 0.8202943969 | 0.8704625840 | 0.7886180141 | 0.1472910331 | 0.0086441366 | -0.0067877101 | 4.0000000000 | 2.0000000000 |

## Top-K And Quantile Diagnostics

The positive class is the majority, so top-k and PR-style metrics are ranking-head diagnostics rather than rare-event retrieval substitutes for ROC-AUC. Random baselines are included in the CSV artifact.

| model_key | cut_label | n_selected | positives_selected | precision | recall_capture | lift_vs_random |
| --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | top_10pct | 278 | 254 | 0.9136690647 | 0.1408763172 | 1.4092699218 |
| m1_logistic_regression | top_10pct | 278 | 263 | 0.9460431655 | 0.1458679978 | 1.4592046828 |
| xgboost | top_10pct | 278 | 259 | 0.9316546763 | 0.1436494731 | 1.4370114557 |
| lightgbm | top_10pct | 278 | 257 | 0.9244604317 | 0.1425402108 | 1.4259148422 |
| catboost | top_10pct | 278 | 258 | 0.9280575540 | 0.1430948419 | 1.4314631489 |

Negative-tail retrieval is also reported because the negative class is the minority side.

| model_key | cut_label | n_selected | negatives_selected | precision | recall_capture | lift_vs_random |
| --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | bottom_100 | 100 | 99 | 0.9900000000 | 0.1012269939 | 2.8151226994 |
| m1_logistic_regression | bottom_100 | 100 | 99 | 0.9900000000 | 0.1012269939 | 2.8151226994 |
| xgboost | bottom_100 | 100 | 100 | 1.0000000000 | 0.1022494888 | 2.8435582822 |
| lightgbm | bottom_100 | 100 | 100 | 1.0000000000 | 0.1022494888 | 2.8435582822 |
| catboost | bottom_100 | 100 | 99 | 0.9900000000 | 0.1012269939 | 2.8151226994 |

## Fold-Level Paired Diagnostics

| model_key | fold | roc_auc | average_precision | delta_auc_vs_m0 | delta_auc_vs_m1 |
| --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | 0 | 0.7893888857 | 0.8485105456 | 0.0000000000 | -0.0081406524 |
| m0_random_forest_frozen | 1 | 0.8323815612 | 0.8889674504 | 0.0000000000 | -0.0178350735 |
| m0_random_forest_frozen | 2 | 0.8258541090 | 0.8727891155 | 0.0000000000 | -0.0369628525 |
| m0_random_forest_frozen | 3 | 0.7737244898 | 0.8250906640 | 0.0000000000 | -0.0249291383 |
| m0_random_forest_frozen | 4 | 0.8409297052 | 0.8887534008 | 0.0000000000 | 0.0117346939 |
| m1_logistic_regression | 0 | 0.7975295381 | 0.8559422574 | 0.0081406524 | 0.0000000000 |
| m1_logistic_regression | 1 | 0.8502166347 | 0.9040317547 | 0.0178350735 | 0.0000000000 |
| m1_logistic_regression | 2 | 0.8628169614 | 0.8978196078 | 0.0369628525 | 0.0000000000 |
| m1_logistic_regression | 3 | 0.7986536281 | 0.8522958178 | 0.0249291383 | 0.0000000000 |
| m1_logistic_regression | 4 | 0.8291950113 | 0.8717517255 | -0.0117346939 | 0.0000000000 |
| xgboost | 0 | 0.7874809203 | 0.8388998850 | -0.0019079654 | -0.0100486178 |
| xgboost | 1 | 0.8306555863 | 0.8935563358 | -0.0017259749 | -0.0195610484 |
| xgboost | 2 | 0.8255415868 | 0.8757123412 | -0.0003125222 | -0.0372753747 |
| xgboost | 3 | 0.7837585034 | 0.8341417405 | 0.0100340136 | -0.0148951247 |
| xgboost | 4 | 0.8324404762 | 0.8799468797 | -0.0084892290 | 0.0032454649 |
| lightgbm | 0 | 0.7855305557 | 0.8402287598 | -0.0038583300 | -0.0119989824 |
| lightgbm | 1 | 0.8200582428 | 0.8859541376 | -0.0123233184 | -0.0301583919 |
| lightgbm | 2 | 0.8189786206 | 0.8596726038 | -0.0068754883 | -0.0438383408 |
| lightgbm | 3 | 0.7794359410 | 0.8330380314 | 0.0057114512 | -0.0192176871 |
| lightgbm | 4 | 0.8285714286 | 0.8754285495 | -0.0123582766 | -0.0006235828 |
| catboost | 0 | 0.8069563005 | 0.8610906056 | 0.0175674148 | 0.0094267624 |
| catboost | 1 | 0.8446764685 | 0.8941023378 | 0.0122949073 | -0.0055401662 |
| catboost | 2 | 0.8269053200 | 0.8732721939 | 0.0010512110 | -0.0359116415 |
| catboost | 3 | 0.7895833333 | 0.8423227957 | 0.0158588435 | -0.0090702948 |
| catboost | 4 | 0.8392148526 | 0.8886896101 | -0.0017148526 | 0.0100198413 |

## Slice Diagnostics

Mandatory slice drops greater than 0.02 AUC vs M0 are warnings for strategic review, not leakage findings.

| model_key | slice_name | slice_value | n | n_positive | roc_auc | delta_auc_vs_m0 | fragile_positive_support_lt_20 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| catboost | available_measurement_count | 0 | 56 | 39 | 0.8190045249 | -0.0648567119 | False |
| catboost | measurement_completeness_group | none | 56 | 39 | 0.8190045249 | -0.0648567119 | False |
| catboost | Position | OG | 151 | 97 | 0.7502863688 | -0.0507827415 | False |
| catboost | Year | 2011 | 278 | 188 | 0.7484633570 | -0.0449763593 | False |
| catboost | Position | OLB | 191 | 145 | 0.7289355322 | -0.0265367316 | False |
| catboost | available_measurement_count | 4 | 269 | 166 | 0.8455374898 | -0.0253830857 | False |
| catboost | Year | 2009 | 253 | 160 | 0.7939516129 | -0.0247311828 | False |
| catboost | Age_missing | 1 | 435 | 8 | 0.6700819672 | -0.0216627635 | True |
| lightgbm | Position | OG | 151 | 97 | 0.6981672394 | -0.1029018709 | False |
| lightgbm | available_measurement_count | 0 | 56 | 39 | 0.8235294118 | -0.0603318250 | False |
| lightgbm | measurement_completeness_group | none | 56 | 39 | 0.8235294118 | -0.0603318250 | False |
| lightgbm | Year | 2011 | 278 | 188 | 0.7391252955 | -0.0543144208 | False |
| lightgbm | Year | 2017 | 274 | 185 | 0.7673246280 | -0.0468266019 | False |
| lightgbm | Position | TE | 162 | 113 | 0.7487809283 | -0.0449702005 | False |
| lightgbm | Position | OLB | 191 | 145 | 0.7212893553 | -0.0341829085 | False |
| lightgbm | available_measurement_count | 1 | 240 | 127 | 0.8087938123 | -0.0265138318 | False |
| lightgbm | Position | DE | 191 | 134 | 0.7889499869 | -0.0252029327 | False |
| lightgbm | Position_Type | offensive_lineman | 435 | 289 | 0.7615537754 | -0.0243162535 | False |
| lightgbm | available_measurement_count | 4 | 269 | 166 | 0.8482863493 | -0.0226342262 | False |
| lightgbm | Position | WR | 395 | 235 | 0.7580851064 | -0.0220744681 | False |
| lightgbm | Position | CB | 328 | 227 | 0.8614733720 | -0.0212413312 | False |
| m1_logistic_regression | Age_missing | 1 | 435 | 8 | 0.5442037471 | -0.1475409836 | True |
| m1_logistic_regression | Position | QB | 162 | 101 | 0.7716279825 | -0.0464210355 | False |
| m1_logistic_regression | available_measurement_count | 4 | 269 | 166 | 0.8426131711 | -0.0283074044 | False |
| m1_logistic_regression | available_measurement_count | 0 | 56 | 39 | 0.8582202112 | -0.0256410256 | False |
| m1_logistic_regression | measurement_completeness_group | none | 56 | 39 | 0.8582202112 | -0.0256410256 | False |
| m1_logistic_regression | Year | 2011 | 278 | 188 | 0.7726950355 | -0.0207446809 | False |
| xgboost | available_measurement_count | 0 | 56 | 39 | 0.8069381599 | -0.0769230769 | False |
| xgboost | measurement_completeness_group | none | 56 | 39 | 0.8069381599 | -0.0769230769 | False |
| xgboost | Position | OG | 151 | 97 | 0.7273768614 | -0.0736922489 | False |
| xgboost | Year | 2011 | 278 | 188 | 0.7454491726 | -0.0479905437 | False |
| xgboost | Year | 2017 | 274 | 185 | 0.7682963863 | -0.0458548436 | False |
| xgboost | available_measurement_count | 4 | 269 | 166 | 0.8409170663 | -0.0300035092 | False |
| xgboost | Position | TE | 162 | 113 | 0.7643128048 | -0.0294383240 | False |
| xgboost | Position | OLB | 191 | 145 | 0.7341829085 | -0.0212893553 | False |
| xgboost | Position | WR | 395 | 235 | 0.7600000000 | -0.0201595745 | False |

`School` was used only for the diagnostic frequent-vs-rare slice and never as a feature.

## Score Distribution And Diagnostic Calibration

Score quantiles, Brier score, and calibration deciles were computed descriptively. No calibration model was fitted.

| model_key | mean_pred | std_pred | p10 | p50 | p90 | brier_score |
| --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | 0.6477413560 | 0.1738273670 | 0.2928992237 | 0.7011245581 | 0.7944214301 | 0.1586025745 |
| m1_logistic_regression | 0.6484366261 | 0.3006498314 | 0.0173409450 | 0.7667965387 | 0.9100841609 | 0.1414342729 |
| xgboost | 0.6707461908 | 0.3508523899 | 0.0037877886 | 0.8253129721 | 0.9853762984 | 0.1574592320 |
| lightgbm | 0.6845624406 | 0.3680914340 | 0.0020735092 | 0.8831963860 | 0.9942452951 | 0.1664000087 |
| catboost | 0.6661682933 | 0.3289654795 | 0.0171341449 | 0.8063512702 | 0.9654249735 | 0.1472910331 |

## Disagreement Diagnostics

Rank disagreement is diagnostic only. It does not authorize blending, stacking, ensembles, manual edits, or submissions.

| model_a | model_b | metric | value |
| --- | --- | --- | --- |
| m1_logistic_regression | catboost | spearman_rank_corr | 0.8177728584 |
| m1_logistic_regression | catboost | kendall_rank_corr | 0.6374581888 |
| m1_logistic_regression | catboost | pearson_score_corr | 0.9177132654 |
| m1_logistic_regression | m0_random_forest_frozen | spearman_rank_corr | 0.8194614735 |
| m1_logistic_regression | m0_random_forest_frozen | kendall_rank_corr | 0.6373153790 |
| m1_logistic_regression | m0_random_forest_frozen | pearson_score_corr | 0.9418280088 |
| catboost | m0_random_forest_frozen | spearman_rank_corr | 0.8349208431 |
| catboost | m0_random_forest_frozen | kendall_rank_corr | 0.6525756686 |
| catboost | m0_random_forest_frozen | pearson_score_corr | 0.9128321480 |
| xgboost | lightgbm | spearman_rank_corr | 0.9518900703 |
| xgboost | lightgbm | kendall_rank_corr | 0.8166360116 |
| xgboost | lightgbm | pearson_score_corr | 0.9646720423 |

## Technical Verdicts

- `m0_random_forest_frozen`: anchor/reference.
- `m1_logistic_regression`: carry as candidate-with-warning for project-director review; no final winner selected.
- `catboost`: observe as candidate-with-warning; global signal exists but Phase 8 slice escalation remains material.
- `xgboost`: drop-candidate for now; no qualifying evidence preserved.
- `lightgbm`: drop-candidate for now; no qualifying evidence preserved.

## Technical Backlog Seed

This is a technical backlog seed only. Codex did not create `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md`; final strategic prioritization belongs to post-Codex review and the project director.

| ID | Hypothesis | Evidence | Future phase |
| --- | --- | --- | --- |
| H1 | Review M1 vs CatBoost disagreement cases before any future ensemble discussion. | Phase 9A rank disagreement diagnostics. | Phase 9B or later diagnostic; ensembles remain locked. |
| H2 | Investigate Age_missing=1 separately due tiny positive support and repeated warning behavior. | Age_missing=1 has n=435 and 8 positives; m1 and CatBoost warnings originate here in prior phases. | Phase 9B diagnostic only. |
| H3 | Use top-k and negative-tail retrieval as supporting evidence, not selection criteria. | Global positive rate is 0.6483; negatives are the minority side. | Project-director strategic review. |
| H4 | Defer all tuning/calibration/threshold/submission ideas until explicit Phase 10/11 authorization. | Phase 9A is diagnostics only. | Phase 10/11 locked. |

## Leakage And Scope Verdict

Leakage verdict: pass for Phase 9A read-only diagnostics. No test fitting, no preprocessing fitting, no target encoding, no feature selection, no model training, no HPO, no leaderboard use, no external data, and no submissions occurred.

## Explicit Non-Actions

- No model was trained or retrained.
- No notebook outside `notebooks/09a_auc_ranking_diagnostics.ipynb` was created or executed.
- No HPO, ensemble, blending, stacking, calibration fitting, threshold tuning, or submission was run.
- `logs/experiment_log.csv` was not modified.
- Phase 10 and Phase 11 remain locked.

Phase 9A diagnostics complete; this is technical evidence only. No final winner was selected and no submission was authorized. Strategic prioritization and acceptance remain for the project director. Phase 10 and Phase 11 remain locked.
