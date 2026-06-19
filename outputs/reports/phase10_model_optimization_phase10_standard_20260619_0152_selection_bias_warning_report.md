# Phase 10 Selection-Bias Warning Report

Phase 10 used bounded deterministic configuration search because Optuna was not installed in the project `.venv` and modifying `.venv` was prohibited. The search spaces and budgets remained within the signed authorization.

- M1 configs evaluated: 50 / 50 authorized.
- CatBoost configs evaluated: 30 / 30 authorized.
- Objective: fixed-fold OOF ROC-AUC only.
- Auxiliary metrics and slices are diagnostic only.
- No leaderboard feedback, no submission, no final winner.
- Search-space widening after results: not performed.
- Multiplicity warning: HPO reuses the same frozen CV substrate; independent recomputation and Opus strategic review are required before acceptance.

## Secondary Repeated-CV Confirmation For Tuned M1

These splitter seeds are diagnostic only and do not replace the frozen-fold decision substrate.

| candidate | splitter_seed | oof_auc | delta_vs_frozen_fold_m1_tuned | fold_mean_auc | fold_std_auc |
| --- | --- | --- | --- | --- | --- |
| m1_logistic_regression_tuned | 7 | 0.8309333342 | 0.0034514165 | 0.8323617543 | 0.0211945243 |
| m1_logistic_regression_tuned | 2025 | 0.8219911826 | -0.0054907352 | 0.8234111975 | 0.0153217624 |
| m1_logistic_regression_tuned | 90210 | 0.8312418407 | 0.0037599230 | 0.8320475253 | 0.0123910984 |
