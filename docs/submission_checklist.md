# Submission Checklist

Phase: 0 - Rules, Intake, and Competition Contract

Use this checklist before generating or submitting any candidate file. Phase 0 does not generate a submission.

## Official Data

- [ ] Data is loaded only from `data/input/train.csv`, `data/input/test.csv`, and `data/input/sample_submission.csv`.
- [ ] No external athlete, school, conference, ranking, geography, draft-history, or sports-outcome data is used.
- [ ] No similar online or externally sourced dataset is used, even if it appears to match the competition data.
- [ ] No examples are manually labeled.
- [ ] Official notebooks under `notebooks/_official/` are not modified.

## Required Columns

- [ ] Target column is exactly `Drafted`.
- [ ] ID column is exactly `Id`.
- [ ] `train.csv` contains `Drafted`.
- [ ] `test.csv` does not contain `Drafted`.
- [ ] `test.csv` columns match `train.csv` after removing `Drafted`.
- [ ] `sample_submission.csv` columns are exactly `Id`, `Drafted`.

## Validation

- [ ] ROC-AUC is used as the primary local validation metric.
- [ ] Predictions used for ROC-AUC are positive-class probabilities, not hard class labels.
- [ ] Stratified validation is used for binary classification unless a later documented validation design justifies otherwise.
- [ ] Public leaderboard score is not used as the main validation system.

## Leakage Prevention

- [ ] Test data is used only for structural checks and final inference.
- [ ] Imputation is fitted only on training folds or the final training data, never on test data.
- [ ] Encoding is fitted only on training folds or the final training data, never on test data.
- [ ] Scaling is fitted only on training folds or the final training data, never on test data.
- [ ] Feature selection is fitted only on training folds or the final training data, never on test data.
- [ ] Target encoding, if ever used, is implemented fold-aware and never fit using validation or test labels.
- [ ] Model selection and hyperparameter tuning do not use test data.

## Submission Format

- [ ] Submission columns are exactly `Id`, `Drafted`.
- [ ] Submission row count is 696.
- [ ] Submission row count matches both `test.csv` and `sample_submission.csv`.
- [ ] Submission `Id` order matches `sample_submission.csv`.
- [ ] Submission `Id` order matches `test.csv`.
- [ ] `Drafted` values are numeric probabilities.
- [ ] `Drafted` values are finite.
- [ ] `Drafted` values contain no missing values.
- [ ] `Drafted` values are within `[0, 1]`.
- [ ] Predictions are generated automatically by code.
- [ ] Prediction values are not manually edited after generation.
- [ ] The submitted file can be traced back to the notebook/code that generated it.

## Reproducibility

- [ ] Random seeds are fixed wherever randomness is used.
- [ ] Code is deterministic enough to rerun for audit.
- [ ] The notebook that generated the submission is saved.
- [ ] The notebook runs from top to bottom from a clean kernel.
- [ ] The submission is saved under `outputs/submissions/`.
- [ ] Important experiments are logged in `logs/experiment_log.csv`.
- [ ] The exact model, parameters, validation score, and submission path are recorded.
- [ ] If code is requested for audit, it matches the submitted predictions and documented experiment.

## Pre-Submission Stop Checks

- [ ] No Phase 0-only documentation has been mistaken for a modeling result.
- [ ] No submission is created before baseline reproduction is approved and executed in Phase 1 or later.
- [ ] Any PDF-only fact that could not be reliably extracted locally is marked `Not confirmed yet`.
- [ ] Any conflict between course PDFs and the official README is resolved in favor of the official README unless later official guidance supersedes it.
