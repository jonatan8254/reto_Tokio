# Phase 8 Wave 2 External GBDT Validation Report

## Executive Summary

Phase 8 Wave 2 executed the authorized external GBDT registry only. The run compares XGBoost, LightGBM, and CatBoost if gated/importable against persisted M0 and M1 OOF comparators. It does not declare a final winner.

## Scope Guardrails

- Feature set: accepted F2 only.
- Excluded from feature matrices: Id, Drafted, School.
- School used only for diagnostic slices.
- No HPO, no early stopping, no eval_set, no submissions, no leaderboard use, no external data.
- M0 and M1 were loaded from persisted Wave 1 OOF artifacts and were not retrained.
- Phase 9, Phase 10, and Phase 11 remain locked.

## Environment

- Python: `3.13.13`
- numpy: `2.4.6`
- pandas: `3.0.3`
- scikit-learn: imported through sklearn runtime
- xgboost import error: ``
- lightgbm import error: ``
- catboost import error: ``

## Anchor Checks

- M0 OOF ROC-AUC: `0.8116502602456482`
- M1 OOF ROC-AUC: `0.8270821069632867`
- Frozen fold sha256[:16]: `96937649526bcadb`

## Model Summary

| model_key | run_status | oof_auc | delta_vs_m0 | delta_vs_m1 | fold_auc_mean | fold_auc_std | same_sign_positive_folds_vs_m0 | same_sign_positive_folds_vs_m1 | slice_guard_triggered | classification | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | completed | 0.8113477083751576 | -0.0003025518704906638 | -0.015734398588129084 | 0.811975414606499 | 0.02422799473420046 | 1 | 1 | True | no_qualifying_evidence | No winner declared; classification is evidence only. |
| lightgbm | completed | 0.8062204891415921 | -0.00542977110405618 | -0.0208616178216946 | 0.8065149577481392 | 0.022354359986600295 | 1 | 0 | True | no_qualifying_evidence | No winner declared; classification is evidence only. |
| catboost | completed | 0.8202943968641223 | 0.008644136618474074 | -0.006787710099164346 | 0.8214672549892178 | 0.022969379744692993 | 4 | 2 | True | escalated | No winner declared; classification is evidence only. |

## Fold Metrics

| model_key | fold | auc | m0_auc | m1_auc | delta_vs_m0 | delta_vs_m1 |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | 0 | 0.7874809203459777 | 0.7893888857482051 | 0.7975295381310419 | -0.001907965402227374 | -0.010048617785064162 |
| xgboost | 1 | 0.8306555863342566 | 0.8323815611904254 | 0.8502166347041694 | -0.001725974856168766 | -0.019561048369912792 |
| xgboost | 2 | 0.8255415867604233 | 0.825854108956602 | 0.8628169614319199 | -0.0003125221961787217 | -0.03727537467149655 |
| xgboost | 3 | 0.7837585034013606 | 0.7737244897959185 | 0.7986536281179137 | 0.010034013605442094 | -0.014895124716553187 |
| xgboost | 4 | 0.8324404761904761 | 0.8409297052154195 | 0.8291950113378684 | -0.008489229024943423 | 0.0032454648526076824 |
| lightgbm | 0 | 0.7855305557125898 | 0.7893888857482051 | 0.7975295381310419 | -0.0038583300356153094 | -0.011998982418452098 |
| lightgbm | 1 | 0.8200582427729242 | 0.8323815611904254 | 0.8502166347041694 | -0.012323318417501228 | -0.030158391931245254 |
| lightgbm | 2 | 0.8189786206406704 | 0.825854108956602 | 0.8628169614319199 | -0.006875488315931655 | -0.043838340791249486 |
| lightgbm | 3 | 0.779435941043084 | 0.7737244897959185 | 0.7986536281179137 | 0.005711451247165544 | -0.019217687074829737 |
| lightgbm | 4 | 0.8285714285714285 | 0.8409297052154195 | 0.8291950113378684 | -0.012358276643991029 | -0.0006235827664399229 |
| catboost | 0 | 0.8069563005257505 | 0.7893888857482051 | 0.7975295381310419 | 0.01756741477754542 | 0.009426762394708632 |
| catboost | 1 | 0.8446764684991831 | 0.8323815611904254 | 0.8502166347041694 | 0.012294907308757708 | -0.005540166204986319 |
| catboost | 2 | 0.8269053199801122 | 0.825854108956602 | 0.8628169614319199 | 0.0010512110235101346 | -0.035911641451807697 |
| catboost | 3 | 0.7895833333333333 | 0.7737244897959185 | 0.7986536281179137 | 0.015858843537414846 | -0.009070294784580435 |
| catboost | 4 | 0.8392148526077098 | 0.8409297052154195 | 0.8291950113378684 | -0.0017148526077097603 | 0.010019841269841345 |

## Age_missing=1 Slice Tracking

| model_key | slice_name | slice_value | n | n_positive | n_negative | positive_rate | model_auc | m0_auc | m1_auc | delta_vs_m0 | delta_vs_m1 | status | reason_if_skipped | slice_guard_triggered | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | Age_missing | 1 | 435 | 8 | 427 | 0.01839080459770115 | 0.7034543325526932 | 0.6917447306791569 | 0.5442037470725996 | 0.011709601873536313 | 0.15925058548009363 | computed |  | False | Age_missing=1 tracked explicitly |
| lightgbm | Age_missing | 1 | 435 | 8 | 427 | 0.01839080459770115 | 0.7177985948477752 | 0.6917447306791569 | 0.5442037470725996 | 0.026053864168618324 | 0.17359484777517564 | computed |  | False | Age_missing=1 tracked explicitly |
| catboost | Age_missing | 1 | 435 | 8 | 427 | 0.01839080459770115 | 0.6700819672131147 | 0.6917447306791569 | 0.5442037470725996 | -0.021662763466042123 | 0.1258782201405152 | computed |  | True | Age_missing=1 tracked explicitly |

## Leakage Checklist

- All learned preprocessing was fit inside each training fold.
- Test data was not used for fitting, tuning, preprocessing, selection, or inference.
- No target encoding, feature selection, HPO, early stopping, eval_set, submissions, leaderboard use, or external data were used.
- CatBoost, when run, used the same pre-encoded numeric F2 matrix with `cat_features=[]`.
- `logs/experiment_log.csv` was checked byte-identical before and after the run.

## Final Note

Wave 2 produces classified evidence only. Candidate selection, acceptance, and commit remain gated on explicit project director authorization.
