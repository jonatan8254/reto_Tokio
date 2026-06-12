# Phase 6A Baseline Reconciliation Report

## Scope

This report reconciles the Phase 2 baseline and the Phase 6 leakage-safe validation harness using variants V0-V7 only.

Boundary checks:

- No V8 was run.
- No HPO was run.
- No submissions were generated.
- No model-family comparison was performed.
- No public leaderboard feedback was used for decisions.
- `logs/experiment_log.csv` was not modified.
- `School` was excluded from every feature matrix.

## Environment

| Item | Value |
|---|---|
| Git status | dbc2efc4ba77cd1e8eac638bb00c4cfd7fa44440 (dirty) |
| Python | 3.13.13 |
| Platform | Windows-11-10.0.26200-SP0 |
| numpy | 2.4.6 |
| pandas | 3.0.3 |
| scikit-learn | 1.9.0 |

## Inputs

| Input | Path |
|---|---|
| Train | `data\input\train.csv` |
| Test | `data\input\test.csv` |
| Sample submission | `data\input\sample_submission.csv` |
| Frozen folds | `outputs\folds\phase6_rf_sanity_baseline_v1_fold_assignments.csv` |
| Phase 6 OOF | `outputs\oof\phase6_rf_sanity_baseline_v1_oof_predictions.csv` |

## Data contract checks

| check | passed | notes |
|---|---|---|
| train_exists | True | data\input\train.csv |
| test_exists | True | data\input\test.csv |
| sample_submission_exists | True | data\input\sample_submission.csv |
| target_in_train | True |  |
| target_not_in_test | True |  |
| id_in_train_test_sample | True |  |
| sample_columns_exact | True | ['Id', 'Drafted'] |
| test_sample_row_count_match | True | test=696 sample=696 |
| test_sample_id_order_match | True |  |
| target_binary | True |  |
| train_rows_expected | True | rows=2781 |
| test_rows_expected | True | rows=696 |

## Bridge check

| Item | Value |
|---|---:|
| Phase 2 CV mean target | 0.812964 |
| V1 fold mean | 0.812964 |
| Absolute difference | 0.000000 |
| Tolerance | 0.005000 |
| Bridge passed | True |

V1 is diagnostic-only and deliberately reproduces Phase 2 global preprocessing leakage. Passing the bridge check does not make V1 eligible as a future anchor.

## Variant summary

| variant_label | variant_id | diagnostic_only | deliberate_leakage | methodologically_acceptable | include_bmi | encoding | imputation | rf_random_state | feature_count | oof_auc | fold_auc_mean | fold_auc_std_population | oof_delta_vs_v0 | phase2_cv_mean_delta | same_sign_positive_folds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V0 | phase6a_v0_phase6_current | False | False | True | False | onehot | median | 42 | 13 | 0.726616 | 0.729253 | 0.027395 | 0.000000 | -0.083711 | 0 |
| V1 | phase6a_v1_phase2_replica | True | True | False | True | global_label_encoder | global_mean | 2025 | 14 | 0.811638 | 0.812964 | 0.025740 | 0.085022 | -0.000000 | 5 |
| V2 | phase6a_v2_replica_no_bmi | True | True | False | False | global_label_encoder | global_mean | 2025 | 13 | 0.810277 | 0.811531 | 0.024991 | 0.083661 | -0.001433 | 5 |
| V3 | phase6a_v3_replica_seed42 | True | True | False | True | global_label_encoder | global_mean | 42 | 14 | 0.808729 | 0.810717 | 0.026798 | 0.082113 | -0.002247 | 5 |
| V4 | phase6a_v4_foldsafe_ordinal_mean_bmi | False | False | True | True | foldsafe_ordinal | foldsafe_mean | 42 | 14 | 0.809010 | 0.812399 | 0.022844 | 0.082393 | -0.000565 | 5 |
| V5 | phase6a_v5_phase6_plus_bmi | False | False | True | True | foldsafe_onehot | foldsafe_median | 42 | 14 | 0.726948 | 0.729105 | 0.024512 | 0.000332 | -0.083859 | 3 |
| V6 | phase6a_v6_phase6_ordinal | False | False | True | False | foldsafe_ordinal | foldsafe_median | 42 | 13 | 0.725812 | 0.728038 | 0.031295 | -0.000804 | -0.084926 | 1 |
| V7 | phase6a_v7_phase6_mean_impute | False | False | True | False | foldsafe_onehot | foldsafe_mean | 42 | 13 | 0.802271 | 0.805851 | 0.024026 | 0.075655 | -0.007113 | 5 |

## Fold-by-fold ROC-AUC

| variant_id | fold | roc_auc |
|---|---|---|
| phase6a_v0_phase6_current | 0 | 0.690076 |
| phase6a_v0_phase6_current | 1 | 0.751758 |
| phase6a_v0_phase6_current | 2 | 0.761581 |
| phase6a_v0_phase6_current | 3 | 0.704939 |
| phase6a_v0_phase6_current | 4 | 0.737911 |
| phase6a_v1_phase2_replica | 0 | 0.786138 |
| phase6a_v1_phase2_replica | 1 | 0.835926 |
| phase6a_v1_phase2_replica | 2 | 0.837446 |
| phase6a_v1_phase2_replica | 3 | 0.777615 |
| phase6a_v1_phase2_replica | 4 | 0.827693 |
| phase6a_v2_replica_no_bmi | 0 | 0.790477 |
| phase6a_v2_replica_no_bmi | 1 | 0.830570 |
| phase6a_v2_replica_no_bmi | 2 | 0.832921 |
| phase6a_v2_replica_no_bmi | 3 | 0.772931 |
| phase6a_v2_replica_no_bmi | 4 | 0.830754 |
| phase6a_v3_replica_seed42 | 0 | 0.777835 |
| phase6a_v3_replica_seed42 | 1 | 0.830641 |
| phase6a_v3_replica_seed42 | 2 | 0.834718 |
| phase6a_v3_replica_seed42 | 3 | 0.778033 |
| phase6a_v3_replica_seed42 | 4 | 0.832355 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 0 | 0.784598 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 1 | 0.833213 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 2 | 0.822431 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 3 | 0.785402 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 4 | 0.836352 |
| phase6a_v5_phase6_plus_bmi | 0 | 0.695150 |
| phase6a_v5_phase6_plus_bmi | 1 | 0.746573 |
| phase6a_v5_phase6_plus_bmi | 2 | 0.764969 |
| phase6a_v5_phase6_plus_bmi | 3 | 0.713407 |
| phase6a_v5_phase6_plus_bmi | 4 | 0.725425 |
| phase6a_v6_phase6_ordinal | 0 | 0.689892 |
| phase6a_v6_phase6_ordinal | 1 | 0.749577 |
| phase6a_v6_phase6_ordinal | 2 | 0.774046 |
| phase6a_v6_phase6_ordinal | 3 | 0.698696 |
| phase6a_v6_phase6_ordinal | 4 | 0.727976 |
| phase6a_v7_phase6_mean_impute | 0 | 0.782760 |
| phase6a_v7_phase6_mean_impute | 1 | 0.826500 |
| phase6a_v7_phase6_mean_impute | 2 | 0.817359 |
| phase6a_v7_phase6_mean_impute | 3 | 0.771712 |
| phase6a_v7_phase6_mean_impute | 4 | 0.830924 |

## Paired fold deltas vs V0

| variant_id | fold | variant_fold_auc | v0_fold_auc | delta_vs_v0 |
|---|---|---|---|---|
| phase6a_v0_phase6_current | 0 | 0.690076 | 0.690076 | 0.000000 |
| phase6a_v0_phase6_current | 1 | 0.751758 | 0.751758 | 0.000000 |
| phase6a_v0_phase6_current | 2 | 0.761581 | 0.761581 | 0.000000 |
| phase6a_v0_phase6_current | 3 | 0.704939 | 0.704939 | 0.000000 |
| phase6a_v0_phase6_current | 4 | 0.737911 | 0.737911 | 0.000000 |
| phase6a_v1_phase2_replica | 0 | 0.786138 | 0.690076 | 0.096063 |
| phase6a_v1_phase2_replica | 1 | 0.835926 | 0.751758 | 0.084168 |
| phase6a_v1_phase2_replica | 2 | 0.837446 | 0.761581 | 0.075865 |
| phase6a_v1_phase2_replica | 3 | 0.777615 | 0.704939 | 0.072676 |
| phase6a_v1_phase2_replica | 4 | 0.827693 | 0.737911 | 0.089782 |
| phase6a_v2_replica_no_bmi | 0 | 0.790477 | 0.690076 | 0.100401 |
| phase6a_v2_replica_no_bmi | 1 | 0.830570 | 0.751758 | 0.078812 |
| phase6a_v2_replica_no_bmi | 2 | 0.832921 | 0.761581 | 0.071340 |
| phase6a_v2_replica_no_bmi | 3 | 0.772931 | 0.704939 | 0.067992 |
| phase6a_v2_replica_no_bmi | 4 | 0.830754 | 0.737911 | 0.092843 |
| phase6a_v3_replica_seed42 | 0 | 0.777835 | 0.690076 | 0.087759 |
| phase6a_v3_replica_seed42 | 1 | 0.830641 | 0.751758 | 0.078883 |
| phase6a_v3_replica_seed42 | 2 | 0.834718 | 0.761581 | 0.073137 |
| phase6a_v3_replica_seed42 | 3 | 0.778033 | 0.704939 | 0.073094 |
| phase6a_v3_replica_seed42 | 4 | 0.832355 | 0.737911 | 0.094444 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 0 | 0.784598 | 0.690076 | 0.094522 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 1 | 0.833213 | 0.751758 | 0.081455 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 2 | 0.822431 | 0.761581 | 0.060849 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 3 | 0.785402 | 0.704939 | 0.080463 |
| phase6a_v4_foldsafe_ordinal_mean_bmi | 4 | 0.836352 | 0.737911 | 0.098441 |
| phase6a_v5_phase6_plus_bmi | 0 | 0.695150 | 0.690076 | 0.005074 |
| phase6a_v5_phase6_plus_bmi | 1 | 0.746573 | 0.751758 | -0.005185 |
| phase6a_v5_phase6_plus_bmi | 2 | 0.764969 | 0.761581 | 0.003388 |
| phase6a_v5_phase6_plus_bmi | 3 | 0.713407 | 0.704939 | 0.008468 |
| phase6a_v5_phase6_plus_bmi | 4 | 0.725425 | 0.737911 | -0.012486 |
| phase6a_v6_phase6_ordinal | 0 | 0.689892 | 0.690076 | -0.000184 |
| phase6a_v6_phase6_ordinal | 1 | 0.749577 | 0.751758 | -0.002181 |
| phase6a_v6_phase6_ordinal | 2 | 0.774046 | 0.761581 | 0.012465 |
| phase6a_v6_phase6_ordinal | 3 | 0.698696 | 0.704939 | -0.006243 |
| phase6a_v6_phase6_ordinal | 4 | 0.727976 | 0.737911 | -0.009935 |
| phase6a_v7_phase6_mean_impute | 0 | 0.782760 | 0.690076 | 0.092685 |
| phase6a_v7_phase6_mean_impute | 1 | 0.826500 | 0.751758 | 0.074743 |
| phase6a_v7_phase6_mean_impute | 2 | 0.817359 | 0.761581 | 0.055778 |
| phase6a_v7_phase6_mean_impute | 3 | 0.771712 | 0.704939 | 0.066773 |
| phase6a_v7_phase6_mean_impute | 4 | 0.830924 | 0.737911 | 0.093013 |

## Gap decomposition

| factor | estimate | context | decision_use |
|---|---|---|---|
| Total Phase2 mean minus V0 OOF | 0.086348 | Historical Phase 2 vs accepted Phase 6 OOF | Gap size only |
| BMI contribution, leaky context | 0.001433 | V1 fold mean minus V2 fold mean | Diagnostic-only |
| RF seed effect, leaky context | 0.002247 | V1 fold mean minus V3 fold mean | Diagnostic-only |
| Global preprocessing effect in ordinal/mean/BMI family | -0.001682 | V3 fold mean minus V4 fold mean | Leakage inflation estimate |
| BMI contribution, clean context | 0.000332 | V5 OOF minus V0 OOF | Phase 7 Block 0 input only |
| Ordinal encoding contribution, clean context | -0.000804 | V6 OOF minus V0 OOF | Encoding policy input |
| Mean imputation contribution, clean context | 0.075655 | V7 OOF minus V0 OOF | Imputation policy input |

## Proposed anchor candidate

The best methodologically acceptable variant in this run is:

| Field | Value |
|---|---|
| variant_id | `phase6a_v4_foldsafe_ordinal_mean_bmi` |
| OOF ROC-AUC | `0.809010` |
| fold mean ROC-AUC | `0.812399` |
| diagnostic_only | `False` |
| deliberate_leakage | `False` |

This is a recommendation for human review only. The definitive anchor must be ratified in a Phase 6A acceptance record.

## Encoding policy evidence

V6 minus V0 OOF delta: `-0.000804`.

One-hot remains the leading tree-categorical policy candidate, pending human ratification.

## BMI disposition

Clean-context BMI delta, V5 minus V0 OOF: `0.000332`.

BMI was measured only. Adoption remains a human Phase 7 Block 0 decision unless explicitly ratified in Phase 6A acceptance.

## Imputation evidence

Clean-context mean-imputation delta, V7 minus V0 OOF: `0.075655`.

This informs imputation policy but does not authorize feature blocks, HPO, or submissions.

## Ablation threshold

Not confirmed yet: V0-V7 were run, but the D1 seed-sweep noise-floor diagnostic was not part of this authorized V0-V7-only execution.

## Unit-of-observation / D2 status

D2 was not executed in this V0-V7-only run. Unit of observation remains `Not confirmed yet`; grouped CV remains dormant unless a later approved diagnostic escalates it.

## Leakage labels

| Variants | Status |
|---|---|
| V1-V3 | Diagnostic-only; deliberate leakage by design; not eligible as future anchor. |
| V0, V4-V7 | Methodologically acceptable constructions; still require human ratification before policy adoption. |

## Artifact list

| Artifact | Path |
|---|---|
| Fixed folds copy | `outputs\folds\phase6a_fixed_fold_assignments.csv` |
| Variant summary | `outputs\validation\phase6a_baseline_reconciliation_variant_summary.csv` |
| Candidate log | `outputs\reports\phase6a_baseline_reconciliation_experiment_log_candidate.csv` |
| Report | `outputs\reports\phase6a_baseline_reconciliation_report.md` |

OOF artifacts:

| variant_id | path |
|---|---|
| phase6a_v0_phase6_current | outputs\oof\phase6a_v0_phase6_current_oof_predictions.csv |
| phase6a_v1_phase2_replica | outputs\oof\phase6a_v1_phase2_replica_oof_predictions.csv |
| phase6a_v2_replica_no_bmi | outputs\oof\phase6a_v2_replica_no_bmi_oof_predictions.csv |
| phase6a_v3_replica_seed42 | outputs\oof\phase6a_v3_replica_seed42_oof_predictions.csv |
| phase6a_v4_foldsafe_ordinal_mean_bmi | outputs\oof\phase6a_v4_foldsafe_ordinal_mean_bmi_oof_predictions.csv |
| phase6a_v5_phase6_plus_bmi | outputs\oof\phase6a_v5_phase6_plus_bmi_oof_predictions.csv |
| phase6a_v6_phase6_ordinal | outputs\oof\phase6a_v6_phase6_ordinal_oof_predictions.csv |
| phase6a_v7_phase6_mean_impute | outputs\oof\phase6a_v7_phase6_mean_impute_oof_predictions.csv |

## Main experiment log

`logs/experiment_log.csv` was intentionally left unchanged. Phase 6A wrote only a candidate log row under `outputs/reports/`.

## Phase 6A closure status

Phase 6A V0-V7 execution is ready for human review. Phase 6A is not formally closed until a human acceptance record ratifies the anchor, encoding policy, BMI disposition, and whether the ablation threshold remains `Not confirmed yet` or requires D1.

## Next gate

Do not start Phase 7 until Phase 6A is reviewed and accepted.
