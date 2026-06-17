# Phase 8 Acceptance — Model-Family Comparison Wave 1

## 0. Executive Decision

Phase 8 Wave 1 is ACCEPTED WITH WARNINGS.

This acceptance closes only the sklearn-native Wave 1 comparison. It does not reject, execute, close, or supersede Wave 2. Wave 2 external GBDTs remain important, planned, and locked behind a separate dependency/environment authorization.

## 1. Scope and Authorization

Wave 1 was executed from the committed Phase 8 planning package at authorized starting hash `f8c7911` and compared only the ratified sklearn-native registry on the frozen F2 feature set from Phase 7/7B.

Authorized Wave 1 models:

- `m0_random_forest_frozen`
- `m1_logistic_regression`
- `m2_random_forest_default`
- `m3_extra_trees_default`
- `m4_hist_gradient_boosting`

Not authorized in this Wave 1 execution:

- `m5_hgb_native_missing`
- `xgboost`
- `lightgbm`
- `catboost`
- deep tabular models
- HPO
- submissions
- ensembles
- leaderboard use
- external data
- package installation
- environment mutation
- Phase 9
- Phase 10
- Phase 11

## 2. Artifacts Reviewed

The following Phase 8 Wave 1 artifacts were reviewed for this acceptance:

- `notebooks/08_phase8_model_family_comparison.ipynb`
- `outputs/validation/phase8_model_family_comparison_v1_model_summary.csv`
- `outputs/validation/phase8_model_family_comparison_v1_fold_metrics.csv`
- `outputs/validation/phase8_model_family_comparison_v1_slice_report.csv`
- `outputs/reports/phase8_model_family_comparison_v1_validation_report.md`
- `outputs/reports/phase8_model_family_comparison_v1_experiment_log_candidate.csv`
- `outputs/reports/phase8_model_family_comparison_v1_artifact_manifest.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m0_random_forest_frozen_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m1_logistic_regression_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m2_random_forest_default_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m3_extra_trees_default_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m4_hist_gradient_boosting_oof_predictions.csv`

## 3. Repository and Safety Status

Repository safety checks at acceptance drafting time:

- HEAD: `f8c7911`
- `git diff --check`: clean
- No staged files
- Forbidden-path diff: empty
- `logs/experiment_log.csv`: unchanged
- No submission artifacts were created

The acceptance drafting step did not modify any forbidden path or open any later phase.

## 4. Independent Audit Summary

The independent Wave 1 audit passed without blockers.

Key findings:

- The frozen Phase 6 folds were used as-is.
- The accepted Phase 7 F2 OOF reference was reproduced by `m0_random_forest_frozen`.
- Positive-class probabilities were extracted with `classes_` verification.
- No HPO, submissions, leaderboard use, external data, or model-family expansion occurred.
- Mandatory slice diagnostics were generated and the warning behavior was preserved in the acceptance record.

## 5. M0 Integrity Gate

M0 integrity gate result: PASS

- `M0 OOF ROC-AUC = 0.8116502602456482`
- `Max abs probability diff vs persisted Phase 7 F2 OOF ≈ 6.661e-16`

The frozen anchor was reproduced to numerical tolerance.

## 6. Model Evidence Table

| model_key | classification | OOF AUC | Delta vs M0 | Same-sign folds | Slice guard | Decision |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `m0_random_forest_frozen` | `reference_reproduced` | `0.8116502602456482` | `0.0000000000000000` | `0/5` | clear | Anchor reproduced |
| `m1_logistic_regression` | `candidate_with_warning` | `0.8270821069632867` | `+0.01543184671763842` | `4/5` | triggered | Carry forward with warning |
| `m2_random_forest_default` | `reject_no_qualifying_evidence` | `0.8055237975335360` | `-0.006126462712112257` | `2/5` | triggered | Rejected |
| `m3_extra_trees_default` | `reject_no_qualifying_evidence` | `0.7896938413255798` | `-0.021956418920068388` | `0/5` | triggered | Rejected |
| `m4_hist_gradient_boosting` | `reject_no_qualifying_evidence` | `0.8093293726543015` | `-0.002320887591346743` | `1/5` | triggered | Rejected |

`m1_logistic_regression` is not a final winner and is not selected for submission. It is only carried forward as a warned candidate for future analysis.

## 7. Fold-Level Evidence

| model_key | fold 0 | fold 1 | fold 2 | fold 3 | fold 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `m0_random_forest_frozen` | `0.7893888857482051` | `0.8323815611904254` | `0.8258541089566020` | `0.7737244897959185` | `0.8409297052154195` |
| `m1_logistic_regression` | `0.7975295381310419` | `0.8502166347041694` | `0.8628169614319199` | `0.7986536281179137` | `0.8291950113378684` |
| `m2_random_forest_default` | `0.7903782011419527` | `0.8415796576461397` | `0.8222743092549187` | `0.7645762471655329` | `0.8116921768707483` |
| `m3_extra_trees_default` | `0.7546215161965062` | `0.8268627033169970` | `0.8118261240144896` | `0.7650935374149660` | `0.7933673469387755` |
| `m4_hist_gradient_boosting` | `0.7988439142970207` | `0.8252574756729882` | `0.8188791817600682` | `0.7670493197278911` | `0.8359835600907030` |

Fold deltas versus M0 were positive in `4/5` folds for `m1`, `2/5` for `m2`, `0/5` for `m3`, and `1/5` for `m4`.

## 8. Slice-Level Evidence and Escalations

Mandatory slices were reviewed for `Player_Type`, `Position_Type`, `Year`, `Age_missing`, `available_measurement_count`, `measurement_completeness_group`, and frequent-vs-rare `School` groups.

The most important warning is the `Age_missing = 1` slice:

- `n = 435`
- `positives = 8`
- `m1 AUC = 0.5442037470725996`
- `M0 AUC = 0.6917447306791569`
- `delta vs M0 = -0.14754098360655732`

That slice is statistically fragile because it has only 8 positives, but the degradation is too large to accept `m1_logistic_regression` cleanly.

Other mandatory-slice escalations remained warnings, not leakage findings. The slice guard is a robustness warning, not evidence of fit-scope contamination or data leakage.

## 9. LogisticRegression Candidate-With-Warning Rationale

LogisticRegression is the only challenger with global promotable evidence, but it is not cleanly accepted because the mandatory slice guard triggered, especially on `Age_missing = 1`.

The global evidence is strong:

- `m1_logistic_regression OOF AUC = 0.8270821069632867`
- `Delta vs M0 = +0.01543184671763842`
- `Same-sign positive folds = 4/5`
- `Classification = candidate_with_warning`

That is sufficient to keep it in the evidence set, but not sufficient to treat it as a final winner or a submission-ready choice.

## 10. Rejected Models and Rationale

`m2_random_forest_default`:

- `OOF AUC = 0.8055237975335360`
- `Delta vs M0 = -0.006126462712112257`
- `Same-sign folds = 2/5`
- `Decision = reject_no_qualifying_evidence`

`m3_extra_trees_default`:

- `OOF AUC = 0.7896938413255798`
- `Delta vs M0 = -0.021956418920068388`
- `Same-sign folds = 0/5`
- `Decision = reject_no_qualifying_evidence`

`m4_hist_gradient_boosting`:

- `OOF AUC = 0.8093293726543015`
- `Delta vs M0 = -0.002320887591346743`
- `Same-sign folds = 1/5`
- `Decision = reject_no_qualifying_evidence`

None of these models met the pre-registered Wave 1 acceptance rule.

## 11. Wave 2 Status and Next Gate

Wave 2 remains planned but not executed.

XGBoost, LightGBM and CatBoost were not installed in the pinned Wave 1 environment and were intentionally deferred. They require a separate Wave 2 Project Authorization Note covering dependency installation or environment strategy, pinned versions, compatibility checks with Python 3.13, pre-registered configs, artifact namespace, and stop rules.

CatBoost remains double-gated because its native categorical workflow could tempt School-as-feature leakage. Any future CatBoost execution must explicitly reconfirm that School remains excluded from all feature matrices.

Wave 2 should be considered after Wave 1 is accepted, selectively committed, hash-recorded, and reviewed by the project director.

This acceptance does not authorize:

- xgboost installation
- lightgbm installation
- catboost installation
- Wave 2 execution
- HPO
- submissions
- leaderboard use
- Phase 9
- Phase 10
- Phase 11

## 12. Deferred / Not Authorized Items

`m5_hgb_native_missing` was not authorized in this execution and remains deferred as an optional diagnostic. It is not required for Phase 8 Wave 1 closure.

SMOTE, oversampling, undersampling, resampling and imbalance-focused interventions were not run in Phase 8 Wave 1. Any future imbalance or slice-risk analysis must be handled as a separately authorized diagnostic or future phase, not as part of this closure.

XGBoost, LightGBM, CatBoost and deep tabular models remain deferred/locked and require separate future authorization.

## 13. Leakage and Scope Verdict

Leakage verdict: pass.

Scope verdict: Wave 1 only.

The acceptance is limited to the sklearn-native Wave 1 comparison. No test fitting, no target encoding, no feature selection, no HPO, no public leaderboard use, no submissions, and no external data were used. The `Age_missing = 1` slice warning is a robustness issue, not a leakage issue.

## 14. Limitations

The pre-registered OOF gain threshold is an evidence-flagging rule inherited from prior RF seed-noise analysis. It is useful for structured comparison, but it does not replace project director judgment.

The mandatory slice guard is especially sensitive on `Age_missing = 1`, where the slice has only 8 positives. That makes the warning important, but also high variance.

This document closes only the Wave 1 comparison. It does not close the broader Phase 8 roadmap, and it does not make any claim about Wave 2 candidates.

## 15. Decision for Future Phases Without Opening Them

Phase 9 remains locked.
Phase 10 remains locked.
Phase 11 remains locked.
Future phases remain locked.

## 16. Acceptance Metadata

| Field | Value |
| --- | --- |
| experiment_id | `phase8_model_family_comparison_v1` |
| authorized starting hash | `f8c791103adc4a259e68a9fff2ccd3e43166801c` |
| audit status | `passed` |
| accepted Wave | `Wave 1 only` |
| Wave 2 status | `planned, important, and locked behind separate authorization` |
| accepted model classification | `m1_logistic_regression: candidate_with_warning` |
| anchor status | `m0_random_forest_frozen: reference_reproduced` |
| rejected models | `m2_random_forest_default`, `m3_extra_trees_default`, `m4_hist_gradient_boosting` |
| leakage verdict | `pass` |
| submission status | `none created` |
| main log status | `unchanged` |

Recommended files for future selective commit after project-director approval:

- `notebooks/08_phase8_model_family_comparison.ipynb`
- `outputs/oof/phase8_model_family_comparison_v1_m0_random_forest_frozen_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m1_logistic_regression_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m2_random_forest_default_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m3_extra_trees_default_oof_predictions.csv`
- `outputs/oof/phase8_model_family_comparison_v1_m4_hist_gradient_boosting_oof_predictions.csv`
- `outputs/validation/phase8_model_family_comparison_v1_model_summary.csv`
- `outputs/validation/phase8_model_family_comparison_v1_fold_metrics.csv`
- `outputs/validation/phase8_model_family_comparison_v1_slice_report.csv`
- `outputs/reports/phase8_model_family_comparison_v1_validation_report.md`
- `outputs/reports/phase8_model_family_comparison_v1_experiment_log_candidate.csv`
- `outputs/reports/phase8_model_family_comparison_v1_artifact_manifest.csv`
- `docs/08_model_comparison/phase8_acceptance.md`

## 17. Explicit Non-Actions

- No HPO was run.
- No submissions were created.
- No leaderboard feedback was used.
- No external data was used.
- No XGBoost, LightGBM, CatBoost or deep tabular model was run.
- No `m5_hgb_native_missing` diagnostic was run.
- No SMOTE, oversampling, undersampling or resampling method was run.
- No forbidden paths were modified.
- `logs/experiment_log.csv` was not modified.
- No commit, stage or push was performed by this acceptance-drafting step.

## 18. Required Next Step

Project director review of `docs/08_model_comparison/phase8_acceptance.md`. If approved, authorize a selective commit of the Phase 8 Wave 1 notebook, artifacts, reports and acceptance record. After that, prepare a separate Phase 8 Wave 2 planning addendum for external GBDTs. Phase 9, Phase 10 and Phase 11 remain locked.
