# Validation Protocol for Phase 6

## Purpose

Define the exact validation protocol that Phase 6 must implement before any feature block ablation, model-family comparison, HPO, ensemble, or strategic submission.

## Competition metric

| Item | Decision |
|---|---|
| Task | Binary classification |
| Target | `Drafted` |
| Positive class | `Drafted = 1` |
| Metric | ROC-AUC |
| Metric function | `sklearn.metrics.roc_auc_score` |
| Score input | Positive-class probabilities, not hard labels |

ROC-AUC must evaluate probability ranking quality for `Drafted = 1`.

## Positive-class probability policy

Phase 6 must not blindly assume `predict_proba(X)[:, 1]`.

Required future implementation policy:

1. Fit the estimator only on the training fold.
2. Read `estimator.classes_` after fitting.
3. Locate the class index corresponding to label `1`.
4. Extract probabilities for that class.
5. Fail loudly if class `1` is not present.
6. Compute ROC-AUC from those probabilities and the validation-fold target.

Hard labels must not be used for ROC-AUC.

## CV splitter decision

| Decision item | Value | Status |
|---|---|---|
| Splitter | `StratifiedKFold` | Frozen |
| `n_splits` | `5` | Frozen |
| `shuffle` | `True` | Frozen |
| `random_state` | `PROJECT_SEED = 42` | Frozen |

Rationale:

- 3 folds are simpler but less stable.
- 10 folds are more expensive and create smaller validation folds.
- 5 folds match the Phase 2 baseline context and provide a practical stability/cost balance for 2,781 training rows.
- Stratification protects class balance in a binary task.

## Fold assignment policy

Future Phase 6 implementation should create deterministic fold assignments from the official training data only.

Recommended future artifact:

```text
outputs/folds/{experiment_id}_fold_assignments.csv
```

Required fields:

```text
Id,fold
```

Rules:

- Fold assignments must be reproducible from code.
- The same fold assignments must be reused for Phase 7 feature ablations and Phase 8 model comparison.
- Fold assignments must not use test data.
- If folds are regenerated, the reason must be logged.

## OOF prediction policy

Out-of-fold predictions are required for important Phase 6+ experiments because they support slice diagnostics, error analysis, and future stacking guardrails.

Recommended future artifact:

```text
outputs/oof/{experiment_id}_oof_predictions.csv
```

Required fields:

```text
Id,fold,y_true,y_pred_proba
```

Rules:

- OOF predictions must be generated only for training rows.
- Each OOF prediction must come from a model that did not train on that row.
- OOF predictions must not be used to tune test predictions or public leaderboard submissions.

## Slice diagnostics schema

Mandatory slices:

- `Player_Type`
- `Position_Type`
- `Year`
- measurement completeness
- `Age_missing`
- frequent vs rare `School` groups

Recommended schema:

```text
experiment_id,fold_strategy,slice_name,slice_value,n,n_positive,n_negative,positive_rate,roc_auc,status,reason_if_skipped,notes
```

Allowed `status` values:

| Status | Meaning |
|---|---|
| `computed` | Slice metric was computed. |
| `skipped_too_small` | Slice did not meet minimum support policy. |
| `skipped_one_class` | Slice contained only one target class, so ROC-AUC is undefined. |
| `not_applicable` | Slice was not relevant for that experiment. |

Minimum slice size:

```text
Not confirmed yet until baseline variance under frozen folds is measured.
```

## Public leaderboard policy

The public leaderboard is a sanity check only.

It must not be used for:

- feature selection;
- model selection;
- HPO;
- preprocessing decisions;
- rare grouping decisions;
- choosing which submission to trust;
- repeated optimization loops.

## Grouped and temporal validation policy

| Validation variant | Phase 6 policy | Reason |
|---|---|---|
| `StratifiedGroupKFold` | Conditional, not active | Unit of observation and grouping need are not confirmed. |
| `GroupKFold` | Conditional, not active | Class balance remains important unless grouping becomes dominant. |
| Temporal/year split | Diagnostic only | Year effects exist, but no official temporal validation requirement is confirmed. |

Open questions:

- Unit of observation: Not confirmed yet.
- Need for grouped CV: Not confirmed yet.
- Need for temporal split: Not confirmed yet.

## Validation failure modes

Phase 6 validation harness must fail or mark the result invalid if:

- `Drafted` is missing from train data;
- `Drafted` appears in test data;
- `Id` is missing from train, test, or sample submission;
- fold assignment is not reproducible;
- validation fold contains one class only for global ROC-AUC;
- class `1` cannot be found in `estimator.classes_`;
- predictions contain NaN or infinite values;
- preprocessing is fitted outside the training fold;
- test data is used for fitting, tuning, selection, or preprocessing;
- public leaderboard feedback is used as a decision signal.

## Acceptance criteria for Phase 6 validation harness

Phase 6 validation harness is acceptable only if:

- it uses `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`;
- it computes ROC-AUC from verified positive-class probabilities;
- it produces fold-by-fold ROC-AUC, mean ROC-AUC, and std ROC-AUC;
- it can produce OOF predictions for training rows;
- it reports mandatory slice diagnostics or explicitly marks skipped slices;
- all learned preprocessing is fitted inside training folds;
- no submission is generated;
- no HPO is run;
- no test data is used for fitting, tuning, or model/feature selection;
- results can be logged with the documented experiment schema.
