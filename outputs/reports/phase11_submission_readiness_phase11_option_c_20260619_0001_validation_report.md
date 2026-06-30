# Phase 11 Submission Readiness Validation Report

## Executive Summary

Phase 11 generated and validated two candidate submission artifacts under Option C. No upload was performed, no leaderboard feedback was used, and no final winner was declared.

- HEAD: `e5ea4e8029ad0a1eb8cbe7260a0a949b5f4beb48`
- Run ID: `phase11_option_c_20260619_0001`
- Candidate 1: `catboost_tuned` (primary final-refit candidate, warning-heavy, written waiver granted)
- Candidate 2: `m1_logistic_regression_baseline` (fallback/reference candidate)
- Feature set: F2 only; School excluded
- Test inference: transform-only using preprocessing fitted on full train

## Submission Validation

| candidate | submission_rows | min_probability | max_probability | submission_sha256 | validation_status |
| --- | --- | --- | --- | --- | --- |
| catboost_tuned | 696 | 0.0090689208283123 | 0.9668055592272972 | a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8 | pass |
| m1_logistic_regression_baseline | 696 | 0.0010409329561047 | 0.9894261701960908 | 0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640 | pass |

## Warnings Carried Forward

- CatBoost tuned has the best global Phase 10 OOF AUC but does not clear the historical promotion bar over M1 baseline.
- CatBoost tuned has only 3/5 positive folds vs M1 baseline and lacks repeated-CV stability confirmation.
- Slice warnings include Age_missing=1, Position=QB, Year 2011, available_measurement_count=0, OG and OLB.
- Upload order remains a manual project-director decision; last uploaded file determines final ranking.

## Explicit Non-Actions

- No automatic upload.
- No leaderboard use.
- No final winner declared.
- No submission-ready model declared before Opus review and director acceptance.
- No HPO, ensembles, calibration, threshold tuning, external data, or School feature.

Phase 11 execution complete. Submission generated and validated, not uploaded. No final winner declared. Awaiting independent Opus submission review and project-director acceptance. Leaderboard not used for selection.
