# Phase 6 Validation Harness Report

## Purpose

Implement and verify a leakage-safe local validation harness. This is not a competitive modeling report.

## Data contract checks

- Train shape: `(2781, 16)`
- Test shape: `(696, 15)`
- Sample submission shape: `(696, 2)`
- Contract passed: `True`
- Unit of observation: `Not confirmed yet`

| check | passed | notes |
|---|---|---|
| train_csv_exists | True | data\input\train.csv |
| test_csv_exists | True | data\input\test.csv |
| sample_submission_csv_exists | True | data\input\sample_submission.csv |
| target_exists_in_train | True |  |
| target_absent_from_test | True |  |
| id_exists_in_train | True |  |
| id_exists_in_test | True |  |
| id_exists_in_sample_submission | True |  |
| sample_submission_columns | True | ['Id', 'Drafted'] |
| test_rows_match_sample_submission | True | test=696 sample=696 |
| test_ids_match_sample_submission_order | True |  |
| train_duplicate_full_rows | True | duplicates=0 |
| test_duplicate_full_rows | True | duplicates=0 |
| target_is_binary | True | values=[0.0, 1.0] |
| positive_class_exists | True | values=[0.0, 1.0] |
| test_columns_match_train_without_target | True |  |

## Feature set used

| Category | Columns | Notes |
|---|---|---|
| numeric_features | Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle | Used as model features. |
| categorical_role_features | Player_Type, Position_Type, Position | Fold-safe encoded role categoricals. |
| excluded | Id, Drafted, School | Excluded from feature matrix. |

## Diagnostic-only variables

| Variable | Purpose | Confirmed not used as feature? |
|---|---|---|
| Age_missing | Age missingness slice | True |
| physical_missing_count | Physical test missingness support | True |
| available_measurement_count | Measurement completeness slice | True |
| measurement_completeness_group | Completeness grouping slice | True |
| frequent_vs_rare_school_group | School frequency slice with threshold `< 5` | True |

Diagnostic notes:

```text
{'Age_missing': 'computed from Age.isna(); diagnostic-only', 'missing_physical_test_columns': [], 'frequent_vs_rare_school_group': 'diagnostic-only train threshold: rare if School count < 5; frequent otherwise'}
```

## Phase 3 EDA risks carried into Phase 6

- School high-cardinality/rare-category risk.
- Age_missing strong train-only association but not yet accepted as feature.
- Measurement availability as future Phase 7 hypothesis.
- special_teams as important Player_Type slice.
- Year/cohort effects as diagnostic only.
- Role-dependent physical interpretation.
- Unit of observation: Not confirmed yet.

The `special_teams` slice status is `computed`. Notes: computed.

## Preprocessing summary

- Numeric features: `SimpleImputer(strategy="median")`, fitted inside each training fold.
- Role categorical features: `SimpleImputer(strategy="most_frequent")` plus `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`, fitted inside each training fold.
- No global preprocessing was fitted before cross-validation.
- No scaling was used because the Phase 6 sanity model is a RandomForest classifier.

## Model used

- Model: `RandomForestClassifier`
- Purpose: Phase 6 validation harness sanity baseline only.
- Parameters: `n_estimators=100`, `max_depth=5`, `random_state=42`, `n_jobs=-1`.
- No model-family comparison was performed.

## Fold strategy

- Splitter: `StratifiedKFold`
- `n_splits`: `5`
- `shuffle`: `True`
- `random_state`: `42`
- Fold labels: `0..4`

| fold | n | n_positive | n_negative | positive_rate |
|---|---|---|---|---|
| 0.0 | 557.0 | 361.0 | 196.0 | 0.6481149012567325 |
| 1.0 | 556.0 | 361.0 | 195.0 | 0.6492805755395683 |
| 2.0 | 556.0 | 361.0 | 195.0 | 0.6492805755395683 |
| 3.0 | 556.0 | 360.0 | 196.0 | 0.6474820143884892 |
| 4.0 | 556.0 | 360.0 | 196.0 | 0.6474820143884892 |

## Fold metrics

| fold | roc_auc | n | n_positive | n_negative | positive_rate | status |
|---|---|---|---|---|---|---|
| 0 | 0.6900757532930069 | 557 | 361 | 196 | 0.6481149012567325 | computed |
| 1 | 0.7517579373535053 | 556 | 361 | 195 | 0.6492805755395683 | computed |
| 2 | 0.7615810782015768 | 556 | 361 | 195 | 0.6492805755395683 | computed |
| 3 | 0.704939058956916 | 556 | 360 | 196 | 0.6474820143884892 | computed |
| 4 | 0.7379109977324262 | 556 | 360 | 196 | 0.6474820143884892 | computed |

Mean fold ROC-AUC: `0.729253`

Std fold ROC-AUC: `0.030629`

## OOF metrics

OOF ROC-AUC: `0.726616`

OOF rows: `2781`

OOF predictions are finite, non-missing, and within `[0, 1]`.

## Slice diagnostics summary

| slice_name | status | count |
|---|---|---|
| Age_missing | computed | 2 |
| Player_Type | computed | 3 |
| Position_Type | computed | 7 |
| Year | computed | 11 |
| available_measurement_count | computed | 7 |
| frequent_vs_rare_school_group | computed | 2 |
| measurement_completeness_group | computed | 3 |

Full slice diagnostics are saved to `outputs\validation\phase6_rf_sanity_baseline_v1_slice_report.csv`.

Slice diagnostics are reporting-only and must not be used for Phase 6 feature selection, model selection, preprocessing selection, HPO, or submission strategy.

## Leakage checklist result

| check | passed | evidence |
|---|---|---|
| Feature matrix excludes Id | True | ['Year', 'Age', 'Height', 'Weight', 'Sprint_40yd', 'Vertical_Jump', 'Bench_Press_Reps', 'Broad_Jump', 'Agility_3cone', 'Shuttle', 'Player_Type', 'Position_Type', 'Position'] |
| Feature matrix excludes Drafted | True | ['Year', 'Age', 'Height', 'Weight', 'Sprint_40yd', 'Vertical_Jump', 'Bench_Press_Reps', 'Broad_Jump', 'Agility_3cone', 'Shuttle', 'Player_Type', 'Position_Type', 'Position'] |
| Feature matrix excludes School | True | ['Year', 'Age', 'Height', 'Weight', 'Sprint_40yd', 'Vertical_Jump', 'Bench_Press_Reps', 'Broad_Jump', 'Agility_3cone', 'Shuttle', 'Player_Type', 'Position_Type', 'Position'] |
| Preprocessing fitted inside each fold | True | Pipeline constructed and fitted inside CV loop |
| Positive class probability verified via estimator.classes_ | True | get_positive_class_proba helper |
| No test data fitting/tuning/selection | True | test used only in contract checks |
| No submissions generated | True | no write to outputs/submissions |
| No HPO run | True | single fixed RandomForestClassifier |
| Main experiment log unchanged by notebook | True | candidate log written separately |

## Test-data use statement

Test data was used only for data-contract structure checks and sample-submission alignment. It was not used for fitting, tuning, preprocessing, feature selection, model selection, HPO, or submission generation.

## Public leaderboard statement

No public leaderboard feedback was used in Phase 6.

## Experiment log handling

`logs/experiment_log.csv` was intentionally left unchanged. A candidate log row was written to `outputs\reports\phase6_rf_sanity_baseline_v1_experiment_log_candidate.csv`. Main experiment log migration/update remains deferred.

## Known limitations

- Minimum slice size remains `Not confirmed yet`; one-class slices are skipped and small slices are reported with caution.
- This sanity baseline is not a final model and is not a model-family comparison.
- `School`, `Age_missing`, and measurement-completeness diagnostics are not model features.

## Provisional decisions remaining

- Exact feature-block acceptance threshold remains unresolved until Phase 7.
- Final School encoding strategy remains unresolved until staged ablations.
- Measurement-completeness cutoffs remain diagnostic only.

## Not confirmed yet items

- Unit of observation: Not confirmed yet.
- Need for grouped CV: Not confirmed yet.
- Minimum slice-size threshold: Not confirmed yet.

## Phase 6 acceptance status

Ready for manual review.

## Next recommended step

Review Phase 6 artifacts manually. Do not start Phase 7 until Phase 6 is accepted.

## Boundary statements

- No submissions were generated.
- No HPO was run.
- No feature blocks were tested.
- No model-family comparison was performed.
- No public leaderboard feedback was used.
- Test data was not used for fitting, tuning, preprocessing, feature selection, or model selection.
- No causal interpretation is made; results are associated with validation ranking performance only.
