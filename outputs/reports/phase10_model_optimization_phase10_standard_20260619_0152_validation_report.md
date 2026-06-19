# Phase 10 Model Optimization Validation Report

## Executive Summary

Phase 10 executed the authorized Standard-budget bounded HPO. No final winner was selected and no submission was authorized.

- HEAD: `fc7a625dfd53b08b5e53ee9f1aeae9b47a2ec6a8`
- Run ID: `phase10_standard_20260619_0152`
- M1 baseline AUC: `0.827082106963`
- M1 tuned AUC: `0.827481917776`
- CatBoost baseline AUC: `0.820294396864`
- CatBoost tuned AUC: `0.830320858102`
- M0 anchor AUC: `0.811650260246`

## Model Summary

| model_key | run_status | oof_auc | delta_vs_m0 | delta_vs_m1 | fold_mean_auc | fold_std_auc | same_sign_positive_folds_vs_m0 | same_sign_positive_folds_vs_m1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m0_random_forest_frozen | baseline_loaded | 0.8116502602 | 0.0000000000 | -0.0154318467 | 0.8124557502 | 0.0261515233 | 0.0000000000 | 1.0000000000 |
| m1_logistic_regression_baseline | baseline_loaded | 0.8270821070 | 0.0154318467 | 0.0000000000 | 0.8276823547 | 0.0264438341 | 4.0000000000 | 0.0000000000 |
| catboost_baseline | baseline_loaded | 0.8202943969 | 0.0086441366 | -0.0067877101 | 0.8214672550 | 0.0205444378 | 4.0000000000 | 2.0000000000 |
| m1_logistic_regression_tuned | tuned | 0.8274819178 | 0.0158316575 | 0.0003998108 | 0.8283660466 | 0.0265558341 | 4.0000000000 | 3.0000000000 |
| catboost_tuned | tuned | 0.8303208581 | 0.0186705979 | 0.0032387511 | 0.8314775456 | 0.0281535613 | 5.0000000000 | 3.0000000000 |

## Secondary Repeated-CV Confirmation

Repeated-CV confirmation was run for tuned M1 only as a selection-bias diagnostic; it is not a replacement for frozen-fold OOF scoring.

| candidate | splitter_seed | oof_auc | delta_vs_frozen_fold_m1_tuned | fold_mean_auc | fold_std_auc |
| --- | --- | --- | --- | --- | --- |
| m1_logistic_regression_tuned | 7 | 0.8309333342 | 0.0034514165 | 0.8323617543 | 0.0211945243 |
| m1_logistic_regression_tuned | 2025 | 0.8219911826 | -0.0054907352 | 0.8234111975 | 0.0153217624 |
| m1_logistic_regression_tuned | 90210 | 0.8312418407 | 0.0037599230 | 0.8320475253 | 0.0123910984 |

## B5 CatBoost Diagnosis

B5 diagnosis completed; CatBoost instability is confirmed and will be treated as a guardrail. No leakage or data-integrity blocker was found, so limited secondary HPO may proceed under the authorization note.

| slice_name | slice_value | n | n_positive | catboost_auc | catboost_delta_vs_m0 |
| --- | --- | --- | --- | --- | --- |
| Year | 2009 | 253 | 160 | 0.7939516129 | -0.0247311828 |
| Year | 2011 | 278 | 188 | 0.7484633570 | -0.0449763593 |
| available_measurement_count | 0 | 56 | 39 | 0.8190045249 | -0.0648567119 |
| available_measurement_count | 4 | 269 | 166 | 0.8455374898 | -0.0253830857 |
| measurement_completeness_group | none | 56 | 39 | 0.8190045249 | -0.0648567119 |
| Position | OG | 151 | 97 | 0.7502863688 | -0.0507827415 |
| Position | OLB | 191 | 145 | 0.7289355322 | -0.0265367316 |

## Scope And Leakage

- F2 only.
- School excluded from all feature matrices.
- All learned preprocessing fitted inside each training fold.
- No external data, no leaderboard, no submissions, no Phase 11.
- `logs/experiment_log.csv` was read before execution and verified unchanged after artifact writing.

Phase 10 execution complete. No final winner selected, no submission authorized. Candidates remain phase-gated. Awaiting independent recomputation and Opus strategic review. Phase 11 remains locked.
