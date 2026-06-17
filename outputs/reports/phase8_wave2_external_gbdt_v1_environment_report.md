# Phase 8 Wave 2 Environment Report

## Scope
Separate environment dependency report for `phase8_wave2_external_gbdt_v1`.

## Repository
- Authorized HEAD: `98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e`
- Observed HEAD: `98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e`
- Repository root: `C:\GitHub\reto_Tokio`

## Base Environment
- Base Python executable: `C:\GitHub\reto_Tokio\.venv\Scripts\python.exe`
- Base Python: `3.13.13`
- Base numpy: `2.4.6`
- Base pandas: `3.0.3`
- Base scikit-learn: `1.9.0`
- Base GBDT availability: `{'xgboost': False, 'lightgbm': False, 'catboost': False}`

## Separate Wave 2 Environment
- Path: `C:\tmp\reto_tokio_phase8_wave2_env`
- Python: `3.13.13`
- Required imports OK: `True`
- CatBoost import OK: `True`

## Install Groups
- core_plus_wave2a: returncode=0; required=True
- catboost_wave2b: returncode=0; required=False

## Dependency Table
| package | required_version | installed_version | import_status | install_status | required |
|---|---:|---:|---|---|---|
| numpy | 2.4.6 | 2.4.6 | ok | ok | yes |
| pandas | 3.0.3 | 3.0.3 | ok | ok | yes |
| sklearn | 1.9.0 | 1.9.0 | ok | ok | yes |
| xgboost | 3.2.0 | 3.2.0 | ok | ok | yes |
| lightgbm | 4.6.0 | 4.6.0 | ok | ok | yes |
| catboost | 1.2.10 | 1.2.10 | ok | ok | conditional |

## Guardrails
- The existing project `.venv` was not installed into or modified by this notebook.
- `requirements.txt`, lockfiles, `logs/experiment_log.csv`, official data, references, and submissions were not modified by this notebook.
- Phase 9, Phase 10, and Phase 11 remain locked.
