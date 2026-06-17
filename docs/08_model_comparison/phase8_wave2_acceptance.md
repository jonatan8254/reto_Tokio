# Phase 8 Wave 2 Acceptance — External GBDT Comparison

## 0. Executive Decision

Phase 8 Wave 2 is ACCEPTED WITH WARNINGS.

This acceptance closes only the external-GBDT Wave 2 comparison (XGBoost, LightGBM, CatBoost) on the frozen F2 feature set. It does not select a final model, does not authorize a submission, and does not open Phase 9, Phase 10 or Phase 11. It complements — and does not modify or supersede — the Wave 1 acceptance (`docs/08_model_comparison/phase8_acceptance.md`).

Headline result: no external GBDT qualifies for clean promotion. CatBoost is the only external GBDT that beats the M0 anchor and passes the global OOF/fold evidence rule, but it triggers the mandatory slice guard and remains below the M1 comparator; it is carried forward only as a candidate-with-warning for future Phase 9 review. XGBoost and LightGBM show no qualifying evidence.

## 1. Scope and Authorization

Wave 2 was executed from the committed Wave 2 planning package at authorized starting hash `98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e` and compared only the ratified external-GBDT registry on the frozen Phase 7/7B F2 feature set, against the carried Wave 1 comparators m0 (reference) and m1 (candidate-with-warning).

Authorized Wave 2 models:

- `xgboost` (XGBClassifier)
- `lightgbm` (LGBMClassifier)
- `catboost` (CatBoostClassifier) — Sub-wave 2B, double-gated, run with `cat_features=[]`

Carried comparators (loaded from persisted Wave 1 OOF, not retrained):

- `m0_random_forest_frozen` (reference anchor)
- `m1_logistic_regression` (candidate-with-warning)

Not authorized / not performed in this Wave 2 execution: HPO, early stopping, `eval_set`, submissions, ensembles, leaderboard use, external data, deep tabular models, School-as-feature, CatBoost native categorical encoding, modification of `.venv`/requirements, Phase 9, Phase 10, Phase 11.

## 2. Independent Audit Summary

An independent post-run audit (generator ≠ verifier) passed without blockers. Method: OOF ROC-AUC recomputed from each persisted OOF file with a pure-stdlib rank-based (Mann-Whitney) AUC, then compared to the model summary and anchors.

| Check | Result |
| --- | --- |
| HEAD == authorized hash | PASS (`98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e`) |
| No staged files; `git diff --check` clean; forbidden-path diff empty | PASS |
| `logs/experiment_log.csv` unchanged | PASS |
| No Wave 2 submission created; `outputs/submissions/` contained only a pre-existing baseline file, and no Wave 2 submission artifact was generated. | PASS |
| `.venv` still GBDT-free; separate Wave 2 env used; `requirements.txt` unchanged | PASS |
| Frozen-fold SHA256[:16] == `96937649526bcadb` | PASS |
| All OOF files: 2781 rows, folds 0..4, fold-aligned to frozen mapping, finite probabilities in [0,1], no single-class fold | PASS |
| Artifact manifest: 10/10 full-SHA256 hashes verified; no unlisted artifact (manifest self-exclusion is expected) | PASS |
| Static notebook review (08b read-only/no-install; 08c no HPO/early-stopping/eval_set, `cat_features=[]`, School excluded, m0/m1 not retrained) | PASS |

## 3. Anchor Integrity

| Anchor | Expected | Recomputed | Abs diff | Tolerance | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| M0 (m0_random_forest_frozen) | 0.8116502602456482 | 0.8116502602456483 | 1.11e-16 | 1e-9 | PASS |
| M1 (m1_logistic_regression) | 0.8270821069632867 | 0.8270821069632865 | 1.11e-16 | 1e-9 | PASS |

M0 also remains equal to the accepted Phase 7 F2 OOF reference; M1 remains the Wave 1 candidate-with-warning. Both comparators were loaded from persisted Wave 1 OOF and were not retrained.

## 4. Model Evidence Table

Independent recomputation matched the committed `model_summary.csv` to ≤ 1.11e-16 for every model.

| model_key | OOF AUC | Delta vs M0 | Same-sign vs M0 | Delta vs M1 | Same-sign vs M1 | Slice guard | Classification |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `xgboost` | 0.8113477083751576 | −0.0003025518704907 | 1/5 | −0.0157343985881291 | 1/5 | triggered | `no_qualifying_evidence` |
| `lightgbm` | 0.8062204891415921 | −0.0054297711040562 | 1/5 | −0.0208616178216946 | 0/5 | triggered | `no_qualifying_evidence` |
| `catboost` | 0.8202943968641223 | +0.0086441366184741 | 4/5 | −0.0067877100991643 | 2/5 | triggered | `escalated` |

Pre-registered evidence rule (vs M0): promote only if `OOF − OOF(M0) ≥ 0.005436` AND same-sign positive folds ≥ 4/5 AND slice guard clear.

- `xgboost`: OOF delta below threshold and negative; 1/5 folds. Fails the rule → `no_qualifying_evidence`.
- `lightgbm`: OOF delta below threshold and negative; 1/5 folds. Fails the rule → `no_qualifying_evidence`.
- `catboost`: OOF delta `+0.008644` clears `0.005436` and folds are `4/5` positive vs M0 — it passes the global evidence rule — **but** the mandatory slice guard triggered, so it is `escalated`, not promoted. It is also `−0.006788` below M1, so it does not surpass the Wave 1 candidate-with-warning.

No external GBDT is a final winner, and none is submission-ready.

## 5. CatBoost Escalation Detail

CatBoost passes the global rule but escalates on the mandatory slice guard. Slices with n ≥ 50 degrading by more than 0.02 AUC versus M0:

| Slice | Value | n | Delta vs M0 | Note |
| --- | --- | ---: | ---: | --- |
| `available_measurement_count` | 0 | 56 | −0.0649 | mirrors `measurement_completeness_group = none` |
| `measurement_completeness_group` | none | 56 | −0.0649 | diagnostic-only dimension |
| `Year` | 2011 | 278 | −0.0450 | robust-size slice |
| `available_measurement_count` | 4 | 269 | −0.0254 | robust-size slice |
| `Year` | 2009 | 253 | −0.0247 | robust-size slice |
| `Age_missing` | 1 | 435 | −0.0217 | fragile slice (only 8 positives) |

The escalation is methodologically genuine: it is driven not only by the fragile `Age_missing = 1` slice (8 positives, high variance) but by robust-size slices (`Year = 2011`, `available_measurement_count` groups). This is a robustness warning, not a leakage finding.

## 6. `Age_missing = 1` Slice Tracking

Explicit per-model tracking on the fragile slice (n = 435, 8 positives; M0 = 0.6917447306791569, m1 = 0.5442037470725996):

| model_key | model AUC | Delta vs M0 | Guard |
| --- | ---: | ---: | --- |
| `xgboost` | 0.7034543325526932 | +0.0117 | clear |
| `lightgbm` | 0.7177985948477752 | +0.0261 | clear |
| `catboost` | 0.6700819672131147 | −0.0217 | triggered |

XGBoost and LightGBM improve on this slice versus M0; CatBoost degrades on it. All three are far above the m1 value on this slice, but the slice is statistically fragile and is not by itself decisive.

## 7. Environment and Dependency Verdict

| Item | Value |
| --- | --- |
| Authorized HEAD == observed HEAD | `98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e` |
| Base `.venv` Python / numpy / pandas / sklearn | 3.13.13 / 2.4.6 / 3.0.3 / 1.9.0 |
| Base `.venv` GBDT availability | xgboost False, lightgbm False, catboost False (untouched) |
| Separate Wave 2 env | `C:\tmp\reto_tokio_phase8_wave2_env`, Python 3.13.13 (pinned-stack mirror) |
| Installed GBDT versions (separate env) | xgboost 3.2.0, lightgbm 4.6.0, catboost 1.2.10 |
| `.venv` / `requirements.txt` / lockfiles modified | No |

The dependency strategy was executed exactly as planned (D → B): a read-only dependency check, then a separate environment mirroring the pinned scientific stack plus pinned GBDTs. The pinned `.venv` that produces all accepted results was not contaminated.

## 8. Leakage and Scope Verdict

Leakage verdict: pass. Scope verdict: Wave 2 only.

Confirmed: all learned preprocessing fit inside training folds; test used only for contract checks (no inference, no submission); no target encoding (CatBoost `cat_features=[]`); no feature selection, dimensionality reduction, rare grouping, or learned role statistics; no leaderboard; no external data; School excluded from every feature matrix (loaded only to build the diagnostic `frequent_vs_rare_school_group` slice, with a raise-on-violation assert); positive-class probabilities extracted only after verifying `estimator.classes_` contains label 1 exactly once; `logs/experiment_log.csv` byte-identical before and after; m0/m1 loaded from persisted OOF and not retrained.

## 9. Limitations

- The 0.005436 OOF-gain threshold is an evidence-flagging rule inherited from prior RandomForest seed-noise analysis. It structures the comparison but does not replace project-director judgment, and it does not describe per-family (XGBoost/LightGBM/CatBoost) seed/implementation variance, which was not measured here.
- The `Age_missing = 1` slice has only 8 positives, making its per-model AUC high variance for all models.
- This Wave 2 used single, pre-registered default-ish configurations with no tuning. The result characterizes default external GBDTs on F2, not their tuned ceiling — which is a Phase 10 question and remains locked.
- This document closes only the external-GBDT Wave 2 comparison. It makes no claim about a final model or submission.

## 10. Decision Record

| model_key | Decision |
| --- | --- |
| `xgboost` | `no_qualifying_evidence` — not carried forward |
| `lightgbm` | `no_qualifying_evidence` — not carried forward |
| `catboost` | `escalated` — carried forward only as a candidate-with-warning for future Phase 9 review |

- No final winner is selected.
- No submission-ready model is designated.
- Across all of Phase 8 (Wave 1 + Wave 2), the strongest global OOF remains the Wave 1 `m1_logistic_regression` (0.8270821069632867, itself a candidate-with-warning); no external GBDT surpassed it.
- Phase 9, Phase 10 and Phase 11 remain locked.

## 11. Decision for Future Phases Without Opening Them

Phase 9 remains locked.
Phase 10 remains locked.
Phase 11 remains locked.
Future phases remain locked.

Open questions routed forward as names only, no experiments: per-family seed-noise calibration before any final selection (Phase 9); error analysis of where CatBoost, m1 and m0 disagree, including the CatBoost slice escalations (Phase 9); whether any carried candidate merits tuning (Phase 10, only after its documented conditions); submissions (Phase 11). None of these is authorized by this acceptance.

## 12. Acceptance Metadata

| Field | Value |
| --- | --- |
| experiment_id | `phase8_wave2_external_gbdt_v1` |
| authorized starting hash | `98d8bb9bc0cc2cccd0c3722a9efebf56ab63021e` |
| audit status | `passed` (no blockers) |
| accepted Wave | `Wave 2 only` |
| anchors | `m0 = 0.8116502602456482 (reference)`, `m1 = 0.8270821069632867 (candidate-with-warning)` |
| classifications | `xgboost: no_qualifying_evidence`, `lightgbm: no_qualifying_evidence`, `catboost: escalated` |
| final winner | `none` |
| submission status | `none created` |
| `.venv` status | `unchanged (separate Wave 2 env used)` |
| main log status | `unchanged` |
| leakage verdict | `pass` |

Files prepared for future selective commit after project-director approval (Wave 1 `phase8_acceptance.md` is NOT to be modified):

- `notebooks/08b_phase8_wave2_dependency_environment_check.ipynb`
- `notebooks/08c_phase8_wave2_external_gbdt_comparison.ipynb`
- `outputs/oof/phase8_wave2_external_gbdt_v1_xgboost_oof_predictions.csv`
- `outputs/oof/phase8_wave2_external_gbdt_v1_lightgbm_oof_predictions.csv`
- `outputs/oof/phase8_wave2_external_gbdt_v1_catboost_oof_predictions.csv`
- `outputs/validation/phase8_wave2_external_gbdt_v1_dependency_report.csv`
- `outputs/validation/phase8_wave2_external_gbdt_v1_model_summary.csv`
- `outputs/validation/phase8_wave2_external_gbdt_v1_fold_metrics.csv`
- `outputs/validation/phase8_wave2_external_gbdt_v1_slice_report.csv`
- `outputs/reports/phase8_wave2_external_gbdt_v1_environment_report.md`
- `outputs/reports/phase8_wave2_external_gbdt_v1_validation_report.md`
- `outputs/reports/phase8_wave2_external_gbdt_v1_experiment_log_candidate.csv`
- `outputs/reports/phase8_wave2_external_gbdt_v1_artifact_manifest.csv`
- `docs/08_model_comparison/phase8_wave2_acceptance.md`

## 13. Explicit Non-Actions

- No model was retrained or executed by this audit (comparators and GBDTs were read from persisted artifacts only).
- No HPO, early stopping, or `eval_set` was run.
- No submission was created; no leaderboard feedback was used.
- No external data was used; School was not used as a feature.
- `.venv`, `requirements.txt`, `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, and the Wave 1 acceptance record were not modified.
- No commit, stage, or push was performed by this audit.
- Phase 9, Phase 10 and Phase 11 were not opened.

## 14. Required Next Step

Project-director review of this acceptance record. If approved, authorize a selective commit of the Wave 2 notebooks, artifacts, reports and this acceptance record (the `041ba10` pattern: selective `git add` per file, then record the resulting hash back into this document). Phase 9, Phase 10 and Phase 11 remain locked.

ACCEPT WITH WARNINGS — CatBoost escalated as candidate-with-warning; XGBoost and LightGBM rejected; no final winner.
