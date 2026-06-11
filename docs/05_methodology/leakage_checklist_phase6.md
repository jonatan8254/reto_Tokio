# Leakage Checklist for Phase 6

## Purpose

Convert the project leakage rules into an executable checklist for the Phase 6 validation harness and preprocessing workflow.

Phase 6 may implement validation and leakage-safe preprocessing only. It must not implement feature block ablations, model comparison, HPO, ensembles, or submissions.

## Allowed row-wise transformations

Allowed row-wise transformations learn no statistics from other rows and use only values in the current row.

| Item | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Missingness indicator from a current-row field | Allowed | row-wise | Phase 6+ | Column exists in official train/test files. |
| `available_measurement_count` from current-row missingness | Allowed | row-wise | Phase 7, not selected in Phase 6 baseline | Defined from official row values only. |
| Simple arithmetic ratios from same-row numeric values | Conditional | row-wise | Phase 7 | Predeclared feature block and no external data. |
| Boolean flags based only on current-row values | Conditional | row-wise | Phase 7 | Predeclared feature block and validation ablation. |

## Learned transformations and fit scope

Any transformation that learns from data rows must be fitted inside each training fold during CV.

| Item | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Numeric imputation | Conditional | fold during CV; final-train-only for final model | Phase 6 | Imputer fitted only on training fold. |
| Categorical imputation | Conditional | fold during CV; final-train-only for final model | Phase 6 | Imputer fitted only on training fold. |
| One-hot encoding | Conditional | fold during CV; final-train-only for final model | Phase 6 | Encoder fitted only on training fold; unknown handling defined. |
| Ordinal encoding | Conditional | fold during CV; final-train-only for final model | Phase 6 | Encoder fitted only on training fold; ordering not target-derived. |
| Scaling | Conditional | fold during CV; final-train-only for final model | Phase 6 for linear models; optional for trees | Scaler fitted only on training fold. |
| Rare grouping | Conditional | fold during CV; final-train-only for final model | Phase 7 | Mapping learned only from training fold; no target use. |
| Role mean/std statistics | Conditional | fold during CV; final-train-only for final model | Phase 7 | Statistics learned only from training fold. |
| Role z-scores or percentiles | Conditional | fold during CV; final-train-only for final model | Phase 7 | Role statistics learned only from training fold. |

## Blocked transformations

| Item | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Global imputation before CV | Blocked | blocked | Never | Not applicable. |
| Global encoding before CV | Blocked | blocked | Never | Not applicable. |
| Global scaling before CV | Blocked | blocked | Never | Not applicable. |
| Global rare grouping before CV | Blocked | blocked | Never | Not applicable. |
| Global feature selection before CV | Blocked | blocked | Never | Not applicable. |
| Target encoding | Blocked in Phase 6 | blocked | Phase 7+ only if justified | Strict OOF implementation and prior stable School ablations. |
| Dimensionality reduction | Blocked in Phase 6 | blocked | Later only if justified | Fold-safe implementation and documented purpose. |
| HPO/model selection | Blocked in Phase 6 | blocked | Phase 10 after gates | Frozen validation, leakage-safe pipeline, feature ablations, candidate models. |

## Test-data use policy

| Test-data use | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Column and shape checks | Allowed | row-wise/descriptive | Phase 0+ | No target use and no learned transform. |
| Submission row/order checks | Allowed | descriptive | Submission phases only | Uses `sample_submission.csv` and `test.csv` IDs only. |
| Train/test drift diagnostics | Conditional | descriptive only | Phase 3+ | Must not choose preprocessing or models from drift alone. |
| Final inference | Conditional | final-train-only | Final model phases | Final model trained after validation decision. |
| Fitting imputers/encoders/scalers | Blocked | blocked | Never | Not applicable. |
| Feature selection/model selection/HPO | Blocked | blocked | Never | Not applicable. |

## Public leaderboard policy

| Use | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Sanity check after logged submission | Conditional | not a fit scope | Phase 11 | Submission generated from a logged reproducible experiment. |
| Feature selection | Blocked | blocked | Never | Not applicable. |
| Model selection | Blocked | blocked | Never | Not applicable. |
| HPO/tuning | Blocked | blocked | Never | Not applicable. |
| Choosing among repeated submissions | Blocked | blocked | Never | Not applicable. |

## Drift diagnostics policy

Train/test drift diagnostics are descriptive only.

They may identify risk, but must not determine:

- feature selection;
- model selection;
- clipping or winsorization;
- rare grouping;
- imputation strategy;
- encoding strategy;
- sample weighting;
- submission choice.

Adversarial validation, if ever used, is diagnostic only and cannot become a model-selection or preprocessing-selection target without a separate methodology review.

## School-specific leakage risks

| Strategy | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| No `School` baseline | Allowed | blocked for `School` use | Phase 6 | First baseline excludes `School`. |
| `School` frequency/count encoding | Conditional | fold during CV | Phase 7 | Counts learned only from training fold; no target use. |
| Rare grouping | Conditional | fold during CV | Phase 7 | Threshold/mapping learned only from training fold. |
| Unknown/test-only handling | Conditional | fold/final-train-only | Phase 7 | Unknown category policy documented. |
| OOF target encoding | Blocked in Phase 6 | fold/OOF only | Phase 7+ only if justified | Prior School encodings stable; strict OOF logic. |
| CatBoost native categorical handling | Blocked in Phase 6 | fold during CV | Phase 8+ only after model-comparison gates | Same folds, slice diagnostics, and School ablation. |

## Role-statistics leakage risks

Role-aware features can leak if role statistics are computed globally.

| Role-statistic use | Allowed / Blocked / Conditional | Fit scope | Phase where allowed | Required evidence before use |
|---|---|---|---|---|
| Raw role categoricals | Conditional | fold-fitted encoding | Phase 6 | Encoder fitted inside training folds. |
| Role interactions | Conditional | row-wise or fold-safe | Phase 7 | Predeclared block and fixed-fold ablation. |
| Role mean/std normalization | Conditional | fold during CV | Phase 7 | Statistics learned only from training folds. |
| Within-role ranks/percentiles | Conditional | fold during CV | Phase 7 | Mapping learned only from training folds. |
| Role-specific outlier flags | Conditional | fold during CV if thresholds are learned | Phase 7 | Threshold policy documented and fold-safe. |

## Preprocessing contract

| Area | Phase 6 policy |
|---|---|
| Numeric columns | Use official numeric columns only; impute inside folds if required by the model. |
| Categorical role columns | Encode `Player_Type`, `Position_Type`, and `Position` inside folds. |
| `School` | Exclude from first Phase 6 baseline. |
| Unknown categories | Must have explicit handling before any encoder is used. |
| Missing values | Imputation must be fitted inside folds; missingness features are not selected in Phase 6 baseline. |
| Scaling | Required for linear models, optional for trees; if used, fit inside folds. |
| Tree models | May not require scaling; still require fold-safe imputation/encoding if the estimator does not handle missing/categorical inputs natively. |
| Linear models | Require imputation, encoding, and likely scaling inside folds. |
| Implementation form | Use `Pipeline`/`ColumnTransformer` or equivalent fold-aware implementation. |

## Phase 6 baseline leakage checklist

Before treating a Phase 6 harness result as valid, verify:

- `Id`, `Drafted`, and `School` are excluded from the first baseline features.
- `Year` is used as a raw numeric feature and diagnostic slice, not as a temporal split driver.
- Role categoricals are encoded inside folds.
- Numeric imputation is fitted inside folds.
- Categorical imputation/encoding is fitted inside folds.
- Positive-class probabilities are extracted by verified class index.
- ROC-AUC is computed on validation folds only.
- OOF predictions are generated only from models that did not train on those rows.
- Test data is not used for fitting, tuning, feature selection, or model selection.
- No public leaderboard result is used for any Phase 6 decision.

## Pre-submission leakage checklist

Submissions are blocked in Phase 6. For later phases, before any submission:

- Experiment is logged.
- Notebook/script can regenerate predictions.
- Test data is used only for final inference.
- Submission columns are exactly `Id`, `Drafted`.
- Row count is 696.
- ID order matches `sample_submission.csv` and `test.csv`.
- Predictions are numeric, finite, non-missing probabilities in `[0, 1]`.
- Prediction values are not manually edited.
- Public leaderboard is treated only as a sanity check.
