# Phase 10 Acceptance Draft — Standard Model Optimization Review

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Acceptance **draft** for project-director signature (Deliverable D output of the Opus → Codex → Opus separation). Not a signed acceptance.
**Date:** 2026-06-19
**Run reviewed:** `phase10_standard_20260619_0152`
**Authorization commit:** `fc7a625dfd53b08b5e53ee9f1aeae9b47a2ec6a8` (*planning: authorize phase 10 standard execution*)

> This draft interprets Codex's authorized Phase 10 execution after an independent recomputation. It declares **no final winner**, authorizes **no submission**, and opens **no future phase**. Phase 11 remains locked.

---

## 1. Executive Verdict

**Decision (draft): ACCEPT PHASE 10 RESULT WITH WARNINGS — no final winner, no submission.**

Phase 10 ran the authorized Standard-budget bounded HPO on the frozen F2 / frozen-fold substrate. An independent, generator-≠-verifier recomputation **passed** (ROC-AUC max abs diff **1.11e-16**, tolerance ±1e-9; integrity clean; manifest hashes verified). The findings:

- **CatBoost tuned has the best global OOF ROC-AUC** of Phase 10 (`0.8303208581`), beating the M0 anchor by **+0.0186706 across 5/5 folds** — but it is **not a final winner and not submission-ready**. It does **not** clear the pre-registered promotion bar **over M1** (delta vs M1 baseline **+0.0032388 < 0.005436**, only **3/5** folds), its stability was **not** confirmed by repeated-CV (that diagnostic was run for M1 only), and it carries persistent robust-slice warnings.
- **M1 tuning produced no real improvement.** M1 tuned vs M1 baseline is **+0.0003998 (3/5 folds)** — far below the 0.005436 noise floor, and **smaller than the M1 repeated-CV spread (~0.009)**. The defaults should be retained as the reference.
- **M0 remains the anchor; XGBoost and LightGBM were not run and remain dropped** (`no_qualifying_evidence`); no re-promotion is warranted.

No model is declared a winner. CatBoost tuned is at most a **candidate for future Phase 11 planning**; M1 (baseline) remains the simpler **fallback/reference** candidate.

## 2. Authorization and Starting State

- Authorization note: `docs/10_model_optimization/phase10_project_authorization_note.md` (Standard budget; M1 bounded HPO; CatBoost limited HPO conditional on B5; XGB/LGBM/M0 no HPO; gate-5 waiver; Phase 11 locked).
- HEAD at review: `fc7a625` (= authorization commit). No staged files. `git diff --check` clean. No forbidden-path tracked diffs. `logs/experiment_log.csv` unchanged. The only `outputs/submissions/` artifact is the pre-existing Phase 2 baseline — **no Phase 10 submission was created**.
- Frozen fold file SHA256[:16] = `96937649526bcadb` (verified). F2-only; School excluded; all five OOF files aligned to the frozen folds.

## 3. Codex Execution Summary

- Run ID `phase10_standard_20260619_0152`; `experiment_id = phase10_model_optimization_v1`.
- Budget compliance: **M1 = 50/50** configs, **CatBoost = 30/30** configs (verified by row count in `hpo_results.csv`).
- **HPO mechanism deviation (documented, not a blocker):** Optuna was **not** installed in the project `.venv`, and modifying `.venv` was prohibited by the authorization. Codex therefore used a **bounded deterministic configuration search** within the authorized search space rather than Optuna TPE. The search space was not widened after seeing results; the budget caps were respected; no leaderboard feedback was used. This substitution is arguably *more* conservative on selection bias (no adaptive sampling chasing the CV substrate), but it departs from the planned Optuna mechanism and is flagged for director awareness (see §9 and §13).
- B5 CatBoost pre-HPO diagnosis was completed before CatBoost tuning; instability confirmed and treated as a guardrail (the authorized conditional path was honored).
- CatBoost ran in the separate Wave 2 environment; `cat_features=[]`; base `.venv`/`requirements.txt` unchanged.
- Candidate experiment log written only to `outputs/reports/..._experiment_log_candidate.csv`; main log untouched (gate-5 waiver conditions satisfied).

## 4. Independent Recompute Summary

Method: pure-stdlib rank-based ROC-AUC (Mann–Whitney U with tie handling), top-k by independent sort, integrity by direct file parse — independent of Codex's tooling.

| model | recomputed ROC-AUC | reported ROC-AUC | abs diff |
|---|---:|---:|---:|
| m0_random_forest_frozen | 0.8116502602456483 | 0.8116502602456482 | 1.11e-16 |
| m1_logistic_regression_baseline | 0.8270821069632865 | 0.8270821069632867 | 1.11e-16 |
| catboost_baseline | 0.8202943968641222 | 0.8202943968641223 | 1.11e-16 |
| m1_logistic_regression_tuned | 0.8274819177762126 | 0.8274819177762125 | 1.11e-16 |
| catboost_tuned | 0.8303208581017549 | 0.8303208581017550 | 1.11e-16 |

- **M0 anchor** reproduces the persisted Phase 7/8 F2 value (≤1e-9). **M1 baseline = 0.8270821069632867** confirmed.
- Top-k independently reproduced: M1 tuned top-500 = **460** positives; CatBoost tuned top-500 = **461**; both match `topk_quantile.csv` exactly.
- Positive rate independently = **0.6483279396** across all five OOF files.

**Independent recompute verdict: PASS — no blockers.**

## 5. Artifact Integrity Review

- OOF integrity (all 5 files): schema `Id,fold,y_true,y_pred_proba`; **2781 rows**; folds **0..4**; no NaN/inf; range **[0,1]**; no duplicate `(Id,fold)`; **0 `y_true` mismatches** across files.
- Artifact manifest: **11/12 entries hash-verified, 0 mismatches, 0 missing**; the manifest's self-entry is `self_excluded_until_after_write` (expected).
- All 13 contract artifacts present (notebook + 2 OOF + 6 validation + 4 reports). Paths contract-named with `run_id`. No overwrite collisions.

## 6. Model Performance Summary

| model_key | OOF ROC-AUC | AP | neg-AP | Brier | Δ vs M0 | Δ vs M1 base | +folds vs M0 | +folds vs M1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| m0_random_forest_frozen (anchor) | 0.8116503 | 0.8638109 | 0.7787192 | 0.1586026 | — | −0.0154318 | — | 1/5 |
| m1_logistic_regression_baseline | 0.8270821 | 0.8741842 | 0.7904989 | 0.1414343 | +0.0154318 | — | 4/5 | — |
| catboost_baseline | 0.8202944 | 0.8704626 | 0.7886180 | 0.1472910 | +0.0086441 | −0.0067877 | 4/5 | 2/5 |
| **m1_logistic_regression_tuned** | 0.8274819 | 0.8750674 | 0.7904326 | 0.1525661 | +0.0158317 | **+0.0003998** | 4/5 | **3/5** |
| **catboost_tuned** | **0.8303209** | **0.8806016** | **0.7934551** | **0.1404953** | **+0.0186706** | **+0.0032388** | **5/5** | **3/5** |

Pre-registered promotion bar (inherited): delta ≥ **0.005436** AND same-sign positive folds ≥ **4/5** AND mandatory-slice guard clear.

- **CatBoost tuned vs M0:** +0.0186706, **5/5** → clears the bar **against the anchor**.
- **CatBoost tuned vs M1 baseline:** +0.0032388 (**< 0.005436**), **3/5** → does **not** clear the bar against M1.
- **M1 tuned vs M1 baseline:** +0.0003998 (**< 0.005436**), **3/5** → does **not** clear the bar; consistent with noise.
- CatBoost tuned has the best AP, neg-AP, and Brier as well — the global lenses agree on ordering, but ordering alone does not promote a candidate over M1 under the pre-registered rule.

## 7. Fold-Level Stability Review

Per-fold OOF ROC-AUC (independently recomputed):

| model | f0 | f1 | f2 | f3 | f4 |
|---|---:|---:|---:|---:|---:|
| m0 | 0.7894 | 0.8324 | 0.8259 | 0.7737 | 0.8409 |
| m1 baseline | 0.7975 | 0.8502 | 0.8628 | 0.7987 | 0.8292 |
| m1 tuned | 0.7970 | 0.8501 | 0.8635 | 0.7997 | 0.8315 |
| catboost tuned | 0.8057 | 0.8589 | 0.8514 | 0.7897 | 0.8516 |

- **M1 tuned ≈ M1 baseline fold-by-fold** (differences in the 3rd–4th decimal). The tuning is effectively a no-op on ranking.
- **Repeated-CV (M1 tuned only, diagnostic):** seed 7 → 0.8309, seed 2025 → **0.8220**, seed 90210 → 0.8312. The spread (~**0.009**) is an order of magnitude larger than the M1 tuned-vs-baseline gain (0.0004), confirming the M1 tuning gain is **within noise**.
- **Repeated-CV was NOT run for CatBoost** — CatBoost tuned's stability under resampling is **unconfirmed**, a gap that must be closed before any Phase 11 reliance.

## 8. Slice and Warning Review

Robust-size warning slices (n≥50, drop >0.02 AUC vs M0): m0 **0**, m1 baseline **6**, catboost baseline **7**, **m1 tuned 4**, **catboost tuned 3** (robust-only counts; total n≥50 drops: m1 tuned 5, catboost tuned 4 — matches the execution report).

Key fragile / robust slices (independently confirmed):

| slice | n / n_pos | m1 baseline | m1 tuned | catboost tuned |
|---|---|---:|---:|---:|
| `Age_missing=1` (fragile, 8 pos) | 435 / 8 | 0.5442 | **0.5404** (worse) | **0.6253** (worse than cat base 0.6701) |
| `Position=QB` (robust) | 162 / 101 | 0.7716 | **0.7703** (worse, drop) | **0.7969** (now a drop vs M0) |
| `Position=SS` (robust) | 87 / 57 | 0.7064 | 0.7070 | **0.7427** (no longer a drop; improved) |

B5-diagnosed CatBoost robust instabilities **persist after tuning**: `Year=2011` (−0.045 vs M0), `available_measurement_count=0` (−0.0649), `Position=OG` (−0.051), `Position=OLB` (−0.027), `Year=2009` (−0.025).

Reading:
- **HPO did not relieve M1's inherited warnings** — `Age_missing=1` and `Position=QB` got marginally *worse*, not better. Tuning was not used to hide a slice problem, but it also did not fix one.
- **CatBoost tuning is a mixed slice picture:** it reduced the total warning-slice count and improved some slices (e.g., SS), but **worsened `Age_missing=1` and `Position=QB`** and **retained the robust B5 instabilities**. Global gain came with localized slice trade-offs.
- The fragile `Age_missing=1` slice (8 positives) is high-variance and must not, alone, decide anything; the robust QB drop is the more decision-relevant warning.

## 9. Selection-Bias and Overfitting Review

- Search executed entirely on the frozen-fold OOF substrate; **objective = fixed-fold OOF ROC-AUC only**; auxiliary metrics/slices diagnostic only; **no search-space widening after results**; **no leaderboard feedback**; **no submission**.
- Configs evaluated: **M1 50/50, CatBoost 30/30** (within authorization).
- **Multiplicity:** 80 tuned variants share the same frozen CV substrate; the executor correctly flagged `warning_hpo_same_cv_substrate` and deferred acceptance to this independent review.
- **M1 over-tuning is ruled out** by the flat tuned-vs-baseline delta and the larger repeated-CV spread (the search did not buy a real CV-overfit gain either).
- **CatBoost over-tuning cannot be ruled in or out** — no repeated-CV diagnostic was run for it; its +0.0100 over its own baseline plus retained robust-slice instabilities means caution is required.
- **Mechanism note:** Optuna-TPE-as-planned was replaced by a bounded deterministic config search due to the `.venv` prohibition (see §3). This is a documented deviation, not a leakage/scope breach; the director should decide whether a future Optuna-based confirmation run is desired (would require an environment decision).

## 10. Candidate Recommendation Matrix

| Recommendation ID | Recommendation | Evidence from Phase 10 | Comparison baseline | Methodological support | Risk | Required next gate | Priority |
|---|---|---|---|---|---|---|---|
| R1 | **Accept Phase 10 result with warnings** (Cat. 1) | Independent recompute PASS (1.11e-16); integrity + manifest verified; budget-compliant | All baselines | Cawley & Talbot; reproducibility notes | Treating a passing diagnostic as a promotion | Director sign-off on this draft | **High** |
| R2 | **Accept CatBoost tuned as a candidate for Phase 11 *planning*, not submission** (Cat. 2) | Best global OOF (0.8303); +0.0187 vs M0 (5/5) | M0 anchor | research_notes_hpo; ranking-metric primacy | Mistaking "best OOF" for "winner/submission-ready" | Phase 11 authorization (separate) | **Medium** |
| R3 | **Reject the M1 *tuned* variant; keep M1 baseline** (Cat. 3) | +0.0004 (3/5), < 0.005436; repeated-CV spread ~0.009 ≫ gain | M1 baseline | ISLP; Cawley & Talbot (noise floor) | Shipping complexity for no gain | None to record; keep defaults | **High** |
| R4 | **Keep CatBoost tuned under observation** (Cat. 4) | +0.0032 vs M1 (3/5) below bar; retained robust-slice instability (Year 2011, avail_count 0, OG/OLB); Age_missing/QB worsened | M1 baseline; CatBoost baseline | Kuhn & Johnson (subgroup divergence) | Promoting on global gain despite slice trade-offs | Slice-robustness review | **Medium** |
| R5 | **Request additional audit before Phase 11: run repeated-CV / stability for CatBoost tuned** (Cat. 5) | Repeated-CV run for M1 only; CatBoost stability unconfirmed | CatBoost tuned vs itself across seeds | research_notes_validation (stability) | Relying on a single-substrate CatBoost result | Phase 11 planning gate | **Medium** |
| R6 | **Keep M0 as anchor; keep XGBoost/LightGBM dropped** (Cat. 6 for XGB/LGBM) | Not run in Phase 10; no new evidence | — | Kaggle Book (diversity ≠ count) | Re-promoting weak models without evidence | Written justification (none exists) | **Low** |
| R7 | **No submission / no threshold / no ensemble / no calibration as executed actions** (Cat. 7) | None performed; ranking metric is threshold-free | — | challenge brief; submission checklist | Leaderboard chasing / gate jumping | Phase 11 authorization | **Prohibited (now)** |

## 11. Explicit Non-Decisions

- **No final winner selected.** **No submission-ready model designated.** **No submission created.**
- No model trained or retrained by this review (all values read from persisted OOF and independently recomputed).
- No HPO, ensemble, blending, stacking, calibration fitting, or threshold tuning performed.
- No leaderboard use; no external data; School never used as a feature.
- `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.venv`, `requirements.txt`, `.vscode/settings.json`, and the Codex artifacts were not modified by this review.
- No staging, commit, or push performed.
- Phase 11 not opened.

## 12. Phase 11 Handoff Without Opening Phase 11

Phase 11 **remains locked.** This acceptance records, for *future Phase 11 planning only*:

- **Primary candidate for Phase 11 planning:** `catboost_tuned` — best global OOF ranker — **with the explicit caveats** that it does not clear the promotion bar over M1, its repeated-CV stability is unconfirmed, and it carries robust-slice warnings (Year 2011, avail_count 0, OG/OLB, plus worsened Age_missing/QB).
- **Fallback / reference candidate:** `m1_logistic_regression` **baseline** (defaults) — simpler, well-characterized, statistically indistinguishable from its tuned variant.
- **Phase 11 planning must explicitly:** (a) run the missing CatBoost stability/repeated-CV audit (R5); (b) decide the final refit + single-test-inference protocol (v3 §14); (c) apply the submission-readiness gates (v3 §16.7) and the submission checklist; (d) decide whether an Optuna-based confirmation run is warranted given the §3/§9 mechanism deviation. None of this is authorized here.

Phase 11 creates the only `outputs/submissions/` artifact and the only leaderboard sanity-check — **neither occurs in or after Phase 10 without separate authorization.**

## 13. Required Next Gate

Project-director review of this draft. If accepted: authorize a **selective** commit of the Phase 10 execution artifacts (§14) and record the resulting hash into §15. The recommended *safe* next work is **Phase 11 *planning*** (not execution), beginning with the CatBoost stability audit (R5) and a director decision on the Optuna mechanism deviation (§3/§9). Phase 11 execution and any submission remain locked behind their own authorization.

## 14. Files Recommended for Selective Commit

Recommended (do **not** commit without explicit instruction; selective per-file `git add`):

```text
notebooks/10_phase10_model_optimization.ipynb
outputs/oof/phase10_model_optimization_phase10_standard_20260619_0152_m1_logistic_regression_tuned_oof_predictions.csv
outputs/oof/phase10_model_optimization_phase10_standard_20260619_0152_catboost_tuned_oof_predictions.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_hpo_results.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_model_summary.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_fold_metrics.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_slice_report.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_topk_quantile.csv
outputs/validation/phase10_model_optimization_phase10_standard_20260619_0152_score_distribution.csv
outputs/reports/phase10_model_optimization_phase10_standard_20260619_0152_selection_bias_warning_report.md
outputs/reports/phase10_model_optimization_phase10_standard_20260619_0152_validation_report.md
outputs/reports/phase10_model_optimization_phase10_standard_20260619_0152_experiment_log_candidate.csv
outputs/reports/phase10_model_optimization_phase10_standard_20260619_0152_artifact_manifest.csv
docs/10_model_optimization/phase10_acceptance.md
```

Must **not** be included: `logs/experiment_log.csv`, `outputs/submissions/`, `data/input/`, `notebooks/_official/`, `references/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`.

## 15. Project Director Signature

- Decision:
- Authorized by:
- Date:
- Acceptance commit hash:
