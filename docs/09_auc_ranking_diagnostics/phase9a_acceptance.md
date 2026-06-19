# Phase 9A Acceptance — AUC-Oriented Imbalance and Ranking Diagnostics

**Decision:** ACCEPT (DIAGNOSTIC) WITH WARNINGS
**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-18
**Authorized starting commit hash:** `0207436` (*planning: refine phase 9a diagnostics package* — planning-inclusive)
**Selective-closure commit hash:** ____ (to be recorded by the project director after selective commit)

> Draft acceptance record for project-director review. It is not signed acceptance, does not open Phase 10 or Phase 11, does not declare a final winner, does not authorize a submission, and does not authorize any commit or staging by itself.

---

## 0. Executive Decision

Phase 9A — a read-only, OOF-based AUC/ranking/imbalance diagnostic pass over the five Phase 8 candidates — is **accepted with warnings**. It trained nothing, edited no predictions, ran no HPO, generated no submission, and selected no final winner. An independent post-Codex recomputation (verifier ≠ generator) passed without blockers. The diagnostics **confirm** the Phase 8 ordering under complementary ranking/imbalance lenses and convert the findings into a phase-gated improvement backlog. M0 remains the anchor; M1 carries as a candidate-with-warning; CatBoost remains under observation; XGBoost and LightGBM remain without qualifying evidence.

## 1. Scope and Authorization

Executed by Codex from the committed Phase 9A planning package at authorized hash `0207436`, then independently reviewed by Opus (this record). Read-only over persisted OOF predictions for: `m0_random_forest_frozen`, `m1_logistic_regression`, `xgboost`, `lightgbm`, `catboost`. Not authorized / not performed: training/retraining, HPO, ensembles/blending/stacking, calibration fitting, threshold tuning, submissions, leaderboard use, external data, School-as-feature, winner/submission-ready declaration, Phase 10/11.

## 2. Independent Audit Summary

Method: pure-stdlib recomputation from raw OOF files, compared to Codex artifacts.

| Check | Result |
| --- | --- |
| HEAD == authorized hash; clean tree; no staged files; forbidden-path diff empty | PASS (`0207436`) |
| `logs/experiment_log.csv` unchanged | PASS |
| No submission created (`outputs/submissions/` holds only the pre-existing Phase 2 baseline) | PASS |
| OOF integrity (5 files): schema, 2781 rows, range [0,1], no NaN/inf, no duplicate (Id,fold), **0 fold/y_true mismatches vs M0**, positive rate 0.6483279396 | PASS (matches Codex integrity report) |
| ROC-AUC reproduction vs accepted Phase 8 (±1e-9) | PASS — independent max abs diff **1.11e-16** |
| Average Precision vs Codex global metrics | PASS — independent max abs diff **1.4e-15** |
| Top-k cross-check (top-500 positive head, exact integer counts) | PASS — m0 450 / m1 460 / xgb 455 / lgbm 450 / cat 455 (exact) |
| Artifact manifest (11 entries) | hashes present; self-exclusion of the manifest is expected |

**Audit verdict: PASS — no blockers.**

## 3. Reproduced Numbers (independent)

| model | ROC-AUC | PR-AUC (AP) | neg-class AP | Brier | folds + vs M0 | folds + vs M1 | technical verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m0_random_forest_frozen | 0.8116502602 | 0.8638108888 | 0.7787191920 | 0.1586025745 | — | 1/5 | anchor |
| m1_logistic_regression | 0.8270821070 | 0.8741841782 | 0.7904989158 | 0.1414342729 | 4/5 | — | carry |
| catboost | 0.8202943969 | 0.8704625840 | 0.7886180141 | 0.1472910331 | 4/5 | 2/5 | observe |
| xgboost | 0.8113477084 | 0.8640251038 | 0.7810117011 | 0.1574592320 | 1/5 | 1/5 | drop-candidate |
| lightgbm | 0.8062204891 | 0.8581335085 | 0.7770412525 | 0.1664000087 | 1/5 | 0/5 | drop-candidate |

AP baseline = positive rate **0.6483** (majority-positive); neg-class AP baseline = 0.3517. Rank correlations: M1↔CatBoost 0.818; XGB↔LGBM 0.952 (near-duplicate).

## 4. Candidate Diagnostic Verdicts (no winner)

| model | Verdict | Rationale |
| --- | --- | --- |
| `m0_random_forest_frozen` | **anchor** (unchanged) | Reference for all paired deltas |
| `m1_logistic_regression` | **carry** (candidate-with-warning) | Strongest on ROC, PR-AUC, neg-class AP, Brier, and top-k capture; 4/5 folds vs M0; **not a winner** — concentrated `Age_missing=1` warning + a robust-size QB-slice loss; lead stability unconfirmed |
| `catboost` | **observe** (escalated / candidate-with-warning) | Genuine second-best; beats M0 (+0.0086, 4/5) but trails M1 on ROC/PR/Brier and 2/5 vs M1; more robust-slice instability (8 warnings) |
| `xgboost` | **drop-candidate** | no_qualifying_evidence confirmed (≈M0, below M0); near-duplicate of LightGBM |
| `lightgbm` | **drop-candidate** | Weakest global; most slice warnings (13) |

**No final winner is selected; no submission-ready model is designated.** Across all of Phase 8 + 9A, M1 remains the strongest local ranker and a candidate-with-warning only.

## 5. Imbalance-Aware Reading

The evaluation set is mildly imbalanced and **majority-positive (positive rate 0.6483)**. PR-AUC, top-k, and lift were reported strictly as diagnostics with baselines shown. Important negative result: **the complementary imbalance metrics confirmed the ROC-AUC ordering — no ROC-vs-PR/top-k conflict forced a re-ranking.** Negative-class AP (minority side, baseline 0.352) is the lower/harder region for every model (~0.78), with M1 again leading.

## 6. Slice Findings (incl. `Age_missing=1`)

- `Age_missing=1` (n=435, **8 positives — fragile**): M1 AUC 0.5442 (≈ random, −0.1475 vs M0, warning + fragile); CatBoost 0.6701 (−0.0217, warning); XGB 0.7035 (+0.0117) and LGBM 0.7178 (+0.0261) *beat* M0 here. On the large `Age_missing=0` slice (n=2346), M1 is the **best** model (+0.0281 vs M0). M1's weakness is localized to the fragile slice.
- Warning-slice counts (n≥50, >0.02 AUC drop vs M0): m0 0, **m1 6**, catboost 8, xgboost 9, lightgbm 13. M1's robust-size warnings of note: `Position=QB` (n=162, −0.046), `Year=2011` (−0.021). CatBoost's robust-size warnings: `Year=2011` (−0.045), `Year=2009` (−0.025), `Position=OG/OLB`.

## 7. Warnings

- M1's `Age_missing=1` collapse is real but on a statistically fragile slice (8 positives) — important, high-variance; not by itself decisive. Tracked as backlog B1.
- M1's `Position=QB` underperformance is a robust-size warning worth a Phase 9B look (B2).
- CatBoost's robust-slice instability must be understood before any tuning (B5).
- The 0.005436 flag threshold is RF-seed-noise-derived; M1's lead stability under resampling is unconfirmed (B3).
- Multiplicity: many slice/metric comparisons were reported in full (no cherry-picking); single large slice movements are hypotheses, not conclusions.

## 8. Backlog Summary

The phase-gated improvement backlog is recorded in `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md` (11 items, each classified into exactly one of the 7 categories with a priority). Highest-value *safe* next questions: **B1** (M1 Age_missing=1 characterization), **B3** (M1 lead stability under resampling), **B10** (negative-class retrieval) — all Phase 9B diagnostic. Everything touching HPO (B5/B8 → Phase 10), ensembling (B7 → future ensemble phase), calibration fitting (B11), thresholds, or submissions (B9 → Phase 11) is **future-locked**.

## 9. Artifacts Reviewed

`outputs/validation/phase9a_auc_ranking_diagnostics_v1_{oof_integrity_report, auc_reproduction, global_metrics, topk_quantile, fold_paired, slice_report, score_distribution, disagreement}.csv`; `outputs/reports/phase9a_auc_ranking_diagnostics_v1_{validation_report.md, artifact_manifest.csv, experiment_log_candidate.csv}`; `notebooks/09a_auc_ranking_diagnostics.ipynb` (static); context: both Phase 8 acceptance records and the Phase 9A master brief.

## 10. Leakage and Scope Verdict

Leakage verdict: **pass**. Scope: Phase 9A diagnostic only. Read-only over accepted OOF; no test fitting; no training/retraining; no HPO; no ensembles; no recalibration; no threshold tuning; no submissions; no leaderboard; no external data; School appeared only as a diagnostic slice dimension, never as a feature; `logs/experiment_log.csv` read before and verified unchanged after.

## 11. Acceptance Metadata

| Field | Value |
| --- | --- |
| experiment_id | `phase9a_auc_ranking_diagnostics_v1` |
| authorized starting hash | `0207436` |
| audit status | `passed` (no blockers) |
| ROC-AUC reproduced (±1e-9) | yes (independent max diff 1.11e-16) |
| candidate verdicts | m0 anchor; m1 carry (candidate-with-warning); catboost observe; xgboost/lightgbm drop-candidate |
| final winner | **none** |
| submission status | **none created** |
| main log status | **unchanged** |
| backlog produced and phase-gated | yes (11 items) |
| Phase 10 / Phase 11 | **locked** |

Files prepared for future selective commit after project-director approval:

- `notebooks/09a_auc_ranking_diagnostics.ipynb`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_oof_integrity_report.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_auc_reproduction.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_global_metrics.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_topk_quantile.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_fold_paired.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_slice_report.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_score_distribution.csv`
- `outputs/validation/phase9a_auc_ranking_diagnostics_v1_disagreement.csv`
- `outputs/reports/phase9a_auc_ranking_diagnostics_v1_validation_report.md`
- `outputs/reports/phase9a_auc_ranking_diagnostics_v1_artifact_manifest.csv`
- `outputs/reports/phase9a_auc_ranking_diagnostics_v1_experiment_log_candidate.csv`
- `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md`
- `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md`

## 12. Explicit Non-Actions

- No model was trained, retrained, or executed by this review (all values read from persisted artifacts and independently recomputed).
- No HPO, ensemble, blending, stacking, calibration fitting, or threshold tuning.
- No submission created; no leaderboard used; no external data; no School-as-feature.
- No final winner declared; no submission-ready model designated.
- `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, and the Codex-generated artifacts were not modified.
- No commit, stage, or push was performed by this review step.
- Phase 10 and Phase 11 were not opened.

## 13. Decision for Future Phases Without Opening Them

```text
Phase 10 remains locked.
Phase 11 remains locked.
No final winner selected.
No submission-ready model.
Future phases remain locked.
```

## 14. Required Next Step

Project-director review of this acceptance record and the backlog. If approved: authorize a selective commit of the Phase 9A notebook, artifacts, validation report, backlog, and this acceptance record (the `4bbcd7a` closure pattern: selective `git add` per file, then record the resulting hash into the "Selective-closure commit hash" field above). The recommended *safe* next work is Phase 9B diagnostics (backlog B1/B3/B10), which requires its own authorization. Phase 10 and Phase 11 remain locked.

**Decision:** ACCEPT (DIAGNOSTIC) WITH WARNINGS — M1 carries as candidate-with-warning; CatBoost observed; XGBoost/LightGBM drop-candidate; no final winner; no submission.

Signature (project director): ____
