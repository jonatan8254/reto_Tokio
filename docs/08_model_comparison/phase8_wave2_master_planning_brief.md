# Phase 8 Wave 2 Master Planning Brief — External GBDTs

**Phase:** Phase 8 — Model-Family Comparison, **Wave 2 (External GBDTs)**, PLANNING ONLY
**Date:** 2026-06-17
**Planning baseline commit:** `041ba10` (*validation: accept phase 8 wave 1 model comparison*)
**Status:** Planning package. **Wave 2 execution is NOT authorized by this document.** No package install, no environment creation, no model training. Phase 9, Phase 10 and Phase 11 remain locked.

---

## 0. Executive Verdict

**Wave 2 can be planned safely, and execution must remain blocked until an explicit, separate project-director authorization** that covers dependency installation / environment strategy. Every entry gate holds: Phase 7/7B closed (F2 adopted, F4 rejected); **Phase 8 Wave 1 executed, audited, accepted with warnings, and committed in `041ba10`** (current HEAD, the expected hash). Wave 1 closed *only* the sklearn-native comparison and explicitly left Wave 2 "planned, important, and locked behind a separate dependency/environment authorization."

The single fact that governs the entire Wave 2 design: **xgboost, lightgbm and catboost are not installed** in the pinned project venv (verified this session: `importlib.util.find_spec` returns none for all three; Python 3.13.13). Running Wave 2 therefore requires environment mutation, which is the dominant risk — not the modeling. This brief's central recommendation is consequently a **staged, environment-isolated design**: (1) a read-only dependency-check notebook that installs nothing; (2) a *separate* dedicated Wave 2 environment that **mirrors the pinned scientific stack** (scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6) and adds **pinned** GBDT versions, never mutating the `.venv` that produced and must keep reproducing all Phase 6→Wave 1 results; (3) a comparison notebook in which **m0 and m1 are carried over from their persisted Wave 1 OOF files (not retrained)**, so only the external GBDTs train and no sklearn-version drift can disturb the anchors.

Scope recommendation: a **two-sub-wave** registry — Sub-wave 2A = XGBoost + LightGBM (active candidates, identical shared-OHE F2 preprocessing); Sub-wave 2B = CatBoost as a **double-gated** candidate run on the *same pre-encoded numeric F2 matrix* (its native categorical/target-statistic pathway disabled) with an explicit School-exclusion reconfirmation, deferrable if its risk outweighs first-pass value. Deep tabular models stay **blocked**.

**Recommended next step:** project-director review of this package; execution stays blocked until the separate Wave 2 authorization (Option A, §21).

---

## 1. Repository State Verification

Commands run on 2026-06-17 (read-only):

| Check | Expected | Observed | Status |
|---|---|---|---|
| `git rev-parse --short HEAD` | `041ba10` | `041ba10` | PASS |
| Wave 1 closure commit | `041ba10` exists | `041ba10` *validation: accept phase 8 wave 1 model comparison* — commits acceptance + notebook 08 + 5 OOF + model_summary/fold_metrics/slice_report + validation_report + candidate_log + artifact_manifest (13 files) | PASS |
| `git status --short` | no staged, no tracked mods | Only known untracked items (`.claude/`, `.obsidian/`, `CLAUDE.md`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `Sin título.canvas`, plan v1, 2 backup notebooks, `notebooks/_official/`) | PASS |
| `git diff --cached --name-only` | empty | empty | PASS |
| `git diff --check` | clean | clean (exit 0) | PASS |
| Forbidden-paths diff (`data/input`, `notebooks/_official`, `references`, `outputs/submissions`, `logs/experiment_log.csv`, `.vscode/settings.json`) | empty | empty | PASS |
| `git diff -- logs/experiment_log.csv` | unchanged | empty (unchanged) | PASS |
| `git log --oneline -n 8` | Wave 1 closure on top | `041ba10`, `f8c7911`, `7166c2e`, `42ef12a`, `8b21db5`, `c4d5647`, `f1fb717`, `dbc2efc` | PASS |
| Wave 2 previously executed? | No | No `phase8_wave2_*` artifact exists; no `08b`/`08c` notebook; `docs/08_model_comparison/` holds only Wave 1 docs + acceptance | PASS (not executed) |
| External GBDTs in venv | (design input) | **none present** — xgboost / lightgbm / catboost all absent; Python 3.13.13 | PASS, governs §7 |

**Observations (none is a blocker):**

1. **Informational:** untracked editor/workspace items appeared since the Wave 1 audit (`.obsidian/`, `Sin título.canvas`). They are user files outside this work's scope and are not touched.
2. **Informational:** the Wave 1 OOF/validation/report artifacts I independently audited last session (max OOF-AUC recomputation diff ≤ 1.11e-16; manifest hashes verified; leakage pass) are now committed verbatim in `041ba10`, so the Wave 1 evidence base for Wave 2 is commit-anchored and immutable.

---

## 2. Evidence Reviewed: Wave 1 Closure and Methodology

All inspection read-only; no notebook executed. The Wave 1 artifacts were additionally verified by independent recomputation in the prior audit session.

### Wave 1 closure evidence

| Archivo | Disponible | Propósito | Información crítica extraída | Riesgo si falta |
|---|---|---|---|---|
| `docs/08_model_comparison/phase8_acceptance.md` | Sí (committed; read in full) | Wave 1 closure record | ACCEPT WITH WARNINGS; closes Wave 1 only; Wave 2 planned+locked; CatBoost double-gated; m5/SMOTE not run; m1 candidate_with_warning, not submission-ready | Wave 2 could re-litigate closed Wave 1 |
| `docs/08_model_comparison/phase8_master_planning_brief.md` | Sí (committed) | Wave 1 plan; two-wave design origin | Reserved `08b` for env mutation; flag rule 0.005436 + 4/5; F2 frozen; cap; School excluded | Lose two-wave rationale |
| `docs/08_model_comparison/phase8_operator_runbook.md` | Sí (committed) | Wave 1 procedure | Authorization-note pattern; audit procedure; closure criteria (reused here) | Reinvent procedure |
| `docs/08_model_comparison/prompt_codex_phase8_execution_plan.md` | Sí (committed) | Wave 1 executor prompt | Inert-prompt + Fidelity-Contract template proven in execution (reused for Deliverable C) | Weaker Deliverable C |
| `notebooks/08_phase8_model_family_comparison.ipynb` | Sí (committed; static template) | Wave 1 executed notebook | Audited builders: shared F2 `ColumnTransformer`, fold-fit only, `classes_` helper, fold-SHA assert `96937649526bcadb`, flag-sum asserts, pre-write guards, m5-block — **reuse as Wave 2 template** | Rewrite-from-scratch risk |
| `outputs/validation/phase8_model_family_comparison_v1_model_summary.csv` | Sí (committed) | Wave 1 primary numbers | All §3 values; m0/m1 reference vectors source | No comparator baseline |
| `outputs/validation/phase8_model_family_comparison_v1_fold_metrics.csv` | Sí (committed) | Wave 1 per-fold | m0 per-fold AUCs (carry-forward fold baseline) | No paired-delta base |
| `outputs/validation/phase8_model_family_comparison_v1_slice_report.csv` | Sí (committed) | Wave 1 slices | `Age_missing=1` (n=435, 8 pos) escalations; diagnostic-only flags | Lose slice warning continuity |
| `outputs/reports/phase8_model_family_comparison_v1_validation_report.md` | Sí (committed) | Wave 1 full report | Evidence-only framing; integrity records | Secondary (acceptance covers it) |
| `outputs/reports/phase8_model_family_comparison_v1_experiment_log_candidate.csv` | Sí (committed) | Wave 1 candidate log | hpo not_run; submission False; leakage False; v2 schema (reuse) | Schema drift |
| `outputs/reports/phase8_model_family_comparison_v1_artifact_manifest.csv` | Sí (committed) | Wave 1 manifest | path+sha256[:16]+size pattern (reuse); hashes independently verified | Lose manifest pattern |
| `outputs/oof/...m0_random_forest_frozen_oof_predictions.csv` | Sí (committed) | **m0 reference vector** | OOF 0.8116502602456482; = persisted F2 to 6.66e-16; the Wave 2 anchor | Anchor continuity impossible |
| `outputs/oof/...m1_logistic_regression_oof_predictions.csv` | Sí (committed) | **m1 comparator vector** | OOF 0.8270821069632867 (warned candidate) | No demanding comparator |
| `outputs/oof/...m2/m3/m4_..._oof_predictions.csv` | Sí (committed) | Rejected-model OOF | Continuity/traceability only | Low |

### Methodology base

| Archivo | Disponible | Principio aplicable | Aplicación a Wave 2 | Riesgo mitigado |
|---|---|---|---|---|
| `docs/05_methodology/phase5_execution_decisions.md` | Sí | Frozen metric/splitter/seed/score-input | ROC-AUC, StratifiedKFold seed 42, positive-proba via `classes_` for every GBDT | Protocol drift |
| `docs/05_methodology/validation_protocol_phase6.md` | Sí | OOF currency; fold integrity | Identical OOF construction for GBDTs; frozen folds loaded+SHA-checked | Invalid comparison |
| `docs/05_methodology/leakage_checklist_phase6.md` | Sí | "If a transform learns from rows, fit inside each training fold"; CatBoost categorical = leakage temptation | GBDTs consume the shared fold-fitted OHE F2 matrix; CatBoost native target-statistic encoding disabled; School excluded | Categorical/target-encoding leakage |
| `docs/00_project_contract/challenge_brief.md` | Sí | Official data only; external data invalidates ranking; audits possible | No external data via any GBDT; reproducible, seed-controlled notebooks | Disqualification |
| `docs/00_project_contract/submission_checklist.md` | Sí | Submission gates | Wave 2 generates none | Submission-policy drift |
| `docs/03_eda/experiment_notes.md` | Sí | Signal families; School + missingness risk | Slice mandate incl. `Age_missing`, completeness, School-diagnostic | Lose subgroup focus |
| `docs/01_project_planning/project_execution_plan_v3.md` | Sí | Phase 8 = fair shortlist comparison; gates | Wave 2 = external-GBDT shortlist under same gates | Phase-boundary drift |
| `docs/01_project_planning/integral_project_review_phase0_phase6.md` | Sí | Project diagnosis / ordering | Wave 2 sits before Phase 9 error analysis | Phase-order drift |
| `AGENTS.md` | Sí | Hard git rules; forbidden paths; phase gates | Selective-commit-only; no `git add .`; protected paths | Git/process violations |

Per the project reading policy, full PDFs were not re-parsed; references are consumed via the committed Phase 4B audit (`pdf_review_audit.md`, `pdf_key_findings.md`) and research notes (`research_notes_tabular_models.md`, `research_notes_hpo.md`, `research_notes_leakage.md`, `research_notes_reproducibility.md` read this session). `/plugin list ecc@ecc` is a CLI user command not invocable from agent context; ECC availability was verified by direct disk inspection (§17).

---

## 3. Numerical Results Validation

All values cross-checked against the committed Wave 1 `model_summary.csv`, `slice_report.csv` and `phase8_acceptance.md`; the OOF AUCs were additionally recomputed independently in the prior audit (stdlib rank AUC, max abs diff ≤ 1.11e-16).

| Evidence item | Expected value | Confirmed value | Source | Status | Impact on Wave 2 |
|---|---|---|---|---|---|
| m0 OOF AUC | 0.8116502602456482 | 0.8116502602456482 | model_summary / acceptance §6 | Confirmed | Wave 2 anchor (M0) |
| m0 delta vs M0 | 0.0 | 0.0 | same | Confirmed | Self-delta sanity |
| m0 classification | reference_reproduced | reference_reproduced | acceptance §6 | Confirmed | Carried as reference comparator |
| m0 vs persisted F2 | ≈ 6.661e-16 | 6.661338147750939e-16 | acceptance §5 / report | Confirmed | Integrity anchor for Wave 2 |
| m1 OOF AUC | 0.8270821069632867 | 0.8270821069632867 | model_summary | Confirmed | Demanding comparator (M1) |
| m1 delta vs M0 | +0.01543184671763842 | +0.01543184671763842 | model_summary | Confirmed | GBDTs must beat a real bar |
| m1 same-sign folds | 4/5 | 4/5 | model_summary | Confirmed | Fold-consistency bar |
| m1 classification | candidate_with_warning | candidate_with_warning | acceptance §6 | Confirmed | Not a winner; warned |
| m2 OOF / delta / folds / class | 0.8055237975335360 / −0.006126462712112257 / 2/5 / reject | identical | model_summary | Confirmed | Context: deeper RF not better |
| m3 OOF / delta / folds / class | 0.7896938413255798 / −0.021956418920068388 / 0/5 / reject | identical | model_summary | Confirmed | Context: ExtraTrees weakest |
| m4 OOF / delta / folds / class | 0.8093293726543015 / −0.002320887591346743 / 1/5 / reject | identical | model_summary | Confirmed | Context: sklearn HGB ties, no edge |
| m1 `Age_missing=1` n / pos | 435 / 8 | 435 / 8 | slice_report / acceptance §8 | Confirmed | Fragile slice GBDTs must be tracked on |
| m1 `Age_missing=1` AUC | 0.5442037470725996 | 0.5442037470725996 | slice_report | Confirmed | Warning baseline to beat |
| M0 `Age_missing=1` AUC | 0.6917447306791569 | 0.6917447306791569 | slice_report | Confirmed | Reference on the fragile slice |
| m1 `Age_missing=1` delta | −0.14754098360655732 | −0.14754098360655732 | slice_report | Confirmed | Explicit Wave 2 slice-tracking target |
| Frozen-fold integrity | 2781 rows, labels 0..4, sha256[:16] `96937649526bcadb` | identical | committed fold file + notebook assert | Confirmed | Same folds for GBDTs |
| F2 feature set | 21 features (13 base + 7 flags + count) | identical | Wave 1 notebook / acceptance §6 | Confirmed | Same matrix for GBDTs |
| Train contract | 2781×16; test 696×15; 1803 drafted / 978 | identical | challenge brief | Confirmed | Same data |
| External GBDTs installed | none | none (Python 3.13.13) | venv check this session | Confirmed | Drives §7 environment gate |

No discrepancy was found between the prompt's claimed values and repository evidence.

---

## 4. Frozen Decisions Preserved

| # | Frozen decision | Wave 2 consequence |
|---|---|---|
| 1 | Primary metric: ROC-AUC on probabilities for `Drafted=1` | Sole primary metric for every GBDT |
| 2 | Positive-class probability via verified `estimator.classes_` | Mandatory per GBDT (XGB/LGBM/CatBoost all expose `classes_`); never blind `[:,1]` |
| 3 | Official data only; no external data; no manual labels/edits | GBDT configs carry no externally derived information |
| 4 | Frozen folds active (sha `96937649526bcadb`) | Loaded + integrity-asserted; never recomputed; identical for every GBDT |
| 5 | OOF ROC-AUC is the primary local comparison currency | Model summary ranks by OOF; fold metrics are diagnostics |
| 6 | **Phase 7 accepted feature set is F2** | Every GBDT consumes exactly the 21 F2 features; no per-model feature engineering |
| 7 | Wave 1 accepted with warnings | This brief does not reopen Wave 1; it extends Phase 8 |
| 8 | m0 = reference_reproduced | Carried into Wave 2 as the M0 anchor (from persisted OOF) |
| 9 | m1 = candidate_with_warning, not winner, not submission-ready | Carried as the M1 comparator; GBDTs compared against both M0 and M1 |
| 10 | m2/m3/m4 rejected | Not re-run; context only |
| 11 | XGBoost/LightGBM/CatBoost not run in Wave 1 | They are exactly Wave 2's subject |
| 12 | **CatBoost requires a special gate (School leakage risk)** | Double-gate (§9); native categorical pathway disabled; School-exclusion reconfirmation required |
| 13 | School excluded unless a later gate authorizes it | Excluded from every GBDT matrix; diagnostic-only slice |
| 14 | Candidate logs separate; `logs/experiment_log.csv` protected | Wave 2 writes one candidate-log row under `outputs/reports/`; main log read-before/assert-after |
| 15 | Public LB never a selection criterion | No LB anywhere in Wave 2 |
| 16 | No HPO in Wave 2 first pass | One pre-registered default-ish config per GBDT; any search = stop condition |
| 17 | No submissions in Wave 2 | No file under `outputs/submissions/`; no inference |
| 18 | No ensembles in Wave 2 first pass | Single-model comparisons only |
| 19 | Phase 9/10/11 locked | §20; dependency notes only |

Honest caveat carried forward: the 0.005436 threshold is RF-seed-noise-derived; in Wave 2 it is a pre-registered **evidence flag**, not an auto-adoption rule. GBDTs have their own (unmeasured) seed/implementation variance; per-family noise calibration is a Phase 9 question, not a Wave 2 tuning license.

---

## 5. References Reviewed and Theory-to-Practice Transfer

Sources are those the project's Phase 4B audit marks **Reviewed** (`pdf_review_audit.md` — 26 reviewed; confirmed this session). Compact summaries sufficed; **no full PDF was re-parsed.** References contribute methodology only — **never external data**.

| Fuente / referencia | Evidencia o principio metodológico | Aplicación práctica a Wave 2 | Riesgo que mitiga | Cómo integrarlo al plan |
|---|---|---|---|---|
| `research_notes_tabular_models.md` (project) | "Short shortlist > model zoo"; identical folds/metric/OOF/logging; School & missingness sensitivity in review; missing/categorical handling are *model-specific contracts, not leakage bypasses*; "Phase 8: run fair shortlist comparison" | Two-sub-wave registry (§8); identical F2 matrix; CatBoost categorical handled as a contract, not a shortcut | Model-zoo sprawl; unfair comparison; categorical leakage | §8/§9/§11 |
| `machine_learning_with_lightgbm_python_2023.pdf` (Reviewed) | LightGBM/XGBoost as strong tabular GBDTs; leaf-wise growth; categorical handling requires precise contracts | LightGBM + XGBoost as Sub-wave 2A actives on the shared OHE matrix; deterministic single-thread config noted for reproducibility | Library-specific leakage; nondeterminism | §8 registry; §11 protocol |
| `catboost_unbiased_boosting_categorical_features.pdf` (Reviewed) | Ordered boosting reduces target-statistic leakage in categorical encoding — but the mechanism is *target-aware* by design | CatBoost **double-gated**; run on pre-encoded numeric F2 (`cat_features=[]`), native target-statistic pathway disabled; School excluded | School/target-encoding leakage temptation | §9 double-gate |
| `closer_look_deep_learning_tabular_datasets.pdf` (Reviewed) | Deep tabular rarely beats tuned GBDT on small/medium tabular; high cost | Deep tabular **blocked** for Wave 2; not in registry | Time sink; irreproducibility | §8 registry |
| The Kaggle Book (2nd ed., 2025) (Reviewed) | Trust frozen local CV; LB is noise; pre-register experiments | Frozen folds + pre-registered configs + hard run cap; LB prohibited | Leaderboard chasing; adaptive overfitting | §11; §19 |
| The Kaggle Workbook (2023) (Reviewed) | Change one thing at a time on identical folds | Only varying factor = model family; F2 + folds + comparators constant | Confounded attribution | §11 fair-matrix |
| `research_notes_hpo.md` (project) + Optuna paper | HPO blocked until 7 conditions met (validation frozen, pipeline leakage-safe, feature blocks ablated, 1–3 candidates selected, log schema active, no leakage, no LB dependence) | **No HPO in Wave 2**; default-ish configs only; HPO is Phase 10 | HPO-by-stealth | §4 #16; §11; §19 |
| `research_notes_leakage.md` (project) + leakage/reproducibility-crisis papers | Pipeline-wide leakage taxonomy; "if a transform learns any statistic from rows, fit it inside each training fold" | GBDTs fit only inside training folds via the shared pipeline; per-model leakage checklist (§15) | All taxonomy layers | §15 |
| Cawley & Talbot (Reviewed) | Model selection on the same CV overfits; selection is part of training | Hard cap on trained models; flag-rule ≠ adoption; director decides | Selection bias | §8 cap; §14 |
| `research_notes_reproducibility.md` (project) + Hands-On ML (Reviewed) | Fixed seeds; reproducible from repo root; pin versions; reproducibility failures hide leakage | Separate Wave 2 env mirrors pinned stack + pinned GBDT versions; environment_report recorded; seeds fixed | Irreproducibility; hidden leakage | §7; §13 |
| ISLP (Reviewed) | Selection variance must clear a noise estimate | 0.005436 flag + 4/5 fold rule as evidence flags; per-family noise deferred to Phase 9 | Reading noise as signal | §14 |
| GCI course materials (sesión 7, QA, tutorial) (Reviewed) | Clean, deterministic, seed-controlled, auditable code; external data invalidates ranking | Notebook contract (§12/§13): top-to-bottom, relative paths, seed 42, env+hash recorded | Disqualification / audit failure | §12/§13/§16 |

Note: standalone XGBoost (Chen & Guestrin) and LightGBM (Ke et al.) papers are referenced through the project's `research_notes_tabular_models.md` and the reviewed LightGBM book; the CatBoost paper itself is directly Reviewed. Compact summaries were sufficient for every Wave 2 decision; no directed long-form re-read was required.

---

## 6. Wave 2 Objective and Scope

**Objective:** under identical data, F2 features, frozen folds, metric, and `classes_`-verified positive probabilities, measure whether external GBDTs (XGBoost, LightGBM, optionally CatBoost) produce evidence strong enough — versus the M0 anchor and the M1 warned candidate — to justify carrying any of them into later phases, **without** HPO, submissions, leaderboard use, ensembling, or environment contamination.

**In scope:** XGBoost, LightGBM (Sub-wave 2A); CatBoost double-gated (Sub-wave 2B, deferrable); m0/m1 as carried comparators; dependency/environment safety; fold-safe shared-OHE preprocessing; OOF + fold + slice diagnostics incl. `Age_missing=1`; one candidate-log row; an environment/dependency report.

**Out of scope (locked):** HPO/AutoML, submissions, leaderboard optimization, ensembling/stacking, deep tabular models, SMOTE/resampling, School-as-feature, any new feature engineering, Phase 9/10/11.

**Explicit separation (frozen):** pre-registered default-ish configs = the only permitted comparison mode; search/tuning loops = HPO (Phase 10, blocked); ensembles/stacking = later phase (blocked); submissions = Phase 11 (blocked).

---

## 7. Environment and Dependency Strategy

Wave 2's dominant risk is environment, not modeling: the pinned `.venv` (Python 3.13.13 / scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6) produced **every** committed result from Phase 6 through Wave 1, and M0 reproduces F2 to 6.66e-16 only because that stack is byte-stable. Mutating it risks silently changing M0/M1 and breaking reproducibility of already-accepted work.

| Strategy | Pros | Cons | Reproducibility risk | Operational risk | Codex execution risk | Recommendation |
|---|---|---|---|---|---|---|
| **A. Install into current `.venv`** | Simplest; one env | Mutates the stack that produced all accepted results; GBDT deps may upgrade numpy/scipy transitively | **High** — can change M0/M1 numerically; breaks Wave 1 reproducibility | High (no clean rollback) | High (silent transitive upgrades) | **Reject** |
| **B. Separate Wave 2 env mirroring pinned stack + pinned GBDTs** | `.venv` untouched; Wave 1 stays reproducible; GBDTs isolated; explicit pinned versions | Extra env to create; must mirror sklearn/pandas/numpy exactly | **Low** — comparators carried from persisted OOF; F2 pipeline uses the same pinned sklearn | Medium (one-time setup) | Low (explicit, scripted, pinned) | **Recommended** |
| **C. Block Wave 2 until compatibility confirmed** | Zero risk now | No progress; defers a legitimate, planned comparison indefinitely | None | None | None | Partial — adopt as the *gate*, not the end state |
| **D. Dependency check first, no install** | Records Python/OS/wheel availability and version compatibility before any decision; zero mutation | Not an execution path by itself | None | None | None | **Recommended as the mandatory first step** |

**Recommended strategy: D → B, gated.** First run a **read-only** dependency-check notebook (installs nothing) that records the environment and tests wheel availability/compatibility for pinned XGBoost/LightGBM/CatBoost on Python 3.13. Only if the director then authorizes, create a **separate** environment (e.g., `.venv_wave2`) that pins `scikit-learn==1.9.0`, `pandas==3.0.3`, `numpy==2.4.6` (mirroring `.venv`) and adds **pinned** GBDT versions; run the comparison there. **Comparators m0/m1 are loaded from their persisted Wave 1 OOF files — not retrained** — so no sklearn re-execution and no version-drift can disturb the anchors; the dependency-check + environment_report capture exact versions for audit. The `.venv`, `requirements.txt`, and any dependency lockfiles are **never modified** by this plan.

Hard rules for this run: **no install, no env creation, no `.venv` modification, no dependency-file edits.** Planning only.

---

## 8. Model Candidate Registry

**Two-sub-wave staging.** Sub-wave 2A (XGBoost, LightGBM) carries the primary GBDT comparison; Sub-wave 2B (CatBoost) is double-gated and deferrable. **Hard cap: ≤ 3 trained GBDTs** (XGB, LGBM, +CatBoost only if 2B authorized). m0/m1 are carried comparators (not trained).

| Modelo | Estado propuesto | Motivo | Riesgo metodológico | Riesgo de dependencia | Requisitos antes de ejecutar | Incluir ahora / diferir |
|---|---|---|---|---|---|---|
| XGBClassifier (XGBoost) | **Active Wave 2 candidate** (Sub-wave 2A) | Strong, standard tabular GBDT; pure-numeric on shared OHE F2 | Low if no native categorical/tuning | **Not installed**; needs pinned wheel on Py 3.13 | Dependency check + separate env + registry ratification | **Incluir — 2A** |
| LGBMClassifier (LightGBM) | **Active Wave 2 candidate** (Sub-wave 2A) | Efficient leaf-wise GBDT; pure-numeric on shared OHE F2 | Low if `categorical_feature` unused and deterministic config | **Not installed**; needs pinned wheel; OpenMP runtime on Windows | Dependency check + separate env + registry ratification | **Incluir — 2A** |
| CatBoostClassifier (CatBoost) | **Gated candidate** (Sub-wave 2B, deferrable) | Powerful, but its value is native categorical/ordered-target encoding — the exact School-leakage temptation | **High** — native `cat_features` invites School/target-statistic leakage; neutralized only by running on pre-encoded numeric F2 with `cat_features=[]` | **Not installed**; needs pinned wheel | 2A complete + **double-gate** (§9): School-exclusion reconfirmation + explicit 2B authorization | **Diferir to 2B (or omit)** |
| m0_random_forest_frozen | **Reference comparator** | Continuity anchor = accepted F2 | None (carried from persisted OOF, not retrained) | None (sklearn, pinned) | Carried | **Incluir (comparator)** |
| m1_logistic_regression | **Candidate-with-warning comparator** | Demanding bar; the only Wave 1 challenger with global evidence; warned on `Age_missing=1` | None (carried from persisted OOF) | None | Carried | **Incluir (comparator)** |
| Deep tabular (MLP/TabNet/FT-Transformer/SAINT/NODE) | **Blocked** | Reviewed benchmark: rarely beats GBDT on small tabular; high cost; no plateau evidence | Cost; irreproducibility | Heavy deps | GBDT-plateau evidence + future-phase authorization | **Bloquear** |

**Pre-registered default-ish configs (frozen at ratification; any change after = stop = HPO):**

```text
xgboost   XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1, subsample=1.0,
                        colsample_bytree=1.0, reg_lambda=1.0, random_state=42, n_jobs=1,
                        tree_method="hist", eval_metric="logloss")     # no early stopping, no eval_set
lightgbm  LGBMClassifier(n_estimators=300, num_leaves=31, learning_rate=0.1, subsample=1.0,
                        colsample_bytree=1.0, reg_lambda=1.0, random_state=42, n_jobs=1,
                        deterministic=True, force_col_wise=True, verbose=-1)   # categorical_feature unused
catboost  CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1, random_seed=42,
                        thread_count=1, cat_features=[], verbose=0, allow_writing_files=False)  # 2B only
```

Rationale: these are single, conventional default-ish settings (no search). `n_jobs=1` / `thread_count=1` / `deterministic=True` are pre-registered **reproducibility requirements**, not tuning. `cat_features=[]` is the CatBoost leakage neutralizer. No `eval_set`/early stopping (that would peek at validation folds). These configs are proposals; the director ratifies or amends them at the §20 gate, after which they freeze.

---

## 9. CatBoost Double Gate and School Leakage Control

CatBoost's headline advantage is *ordered target-statistic encoding of categoricals* — which is exactly the mechanism the project forbids, because School (high-cardinality) is excluded precisely to avoid target/category leakage. Running CatBoost in its native categorical mode would re-introduce that risk through the back door.

| Gate | Condition | Why | Enforcement |
|---|---|---|---|
| **Gate 1 — Wave 2 authorization** | The general Wave 2 Project Authorization Note exists (covers 2A) | No external GBDT runs without it | Pre-flight HEAD/note check |
| **Gate 2 — CatBoost-specific authorization** | A separate, explicit line in the note authorizes Sub-wave 2B | CatBoost's risk profile differs from XGB/LGBM | Notebook refuses CatBoost unless the 2B flag is present |
| **School-exclusion reconfirmation** | The note re-affirms School stays excluded; notebook asserts `School ∉ features` | Native categorical mode would tempt School-as-feature | Hard assert (raise on violation) |
| **No native categorical** | CatBoost runs with `cat_features=[]` on the **same pre-encoded numeric F2 matrix** as XGB/LGBM | Preserves fair comparison; disables target-statistic encoding | Config assert: `cat_features == []` |
| **Deferrable** | If 2A already answers the question or 2B risk outweighs value, CatBoost may be **omitted** | First-pass parsimony | Director decision at §20 |

If any gate is unmet, CatBoost is not run; XGBoost + LightGBM (Sub-wave 2A) still constitute a complete, defensible Wave 2.

---

## 10. Proposed Wave 2 Block Architecture

The suggested 12-block skeleton was adapted: the bibliographic transfer is a planning activity (done in §5, not an execution block), and an explicit **dependency/environment gate block** is elevated to first-class status (forced by §7). Net result: 9 blocks, 0–8.

| Block | Nombre | Objetivo | Decisiones que cubre | Evidencia necesaria | Riesgos mitigados | Salida esperada | Condición de avance |
|---|---|---|---|---|---|---|---|
| 0 | Repository, Git & Phase Gate Verification | Prove the session starts from the accepted Wave 1 baseline | None (verification) | HEAD = authorized hash; clean tree; Wave 1 committed; folds sha `96937649526bcadb`; no `phase8_wave2_*` artifacts | Wrong/dirty baseline; double execution | Verification block | All PASS; any FAIL ⇒ stop |
| 1 | Wave 1 Evidence Carryover | Load m0/m1 as comparators from persisted OOF | Comparator vectors; M0 integrity re-check | committed m0/m1 OOF | Retraining drift; anchor loss | Loaded vectors + M0 recheck (0.811650) | m0 recompute == 0.8116502602456482 ± 1e-9 |
| 2 | Current State Freeze | Freeze what every GBDT inherits | F2 (21), exclusions, folds, metric, M0/M1 bars, non-scope | acceptance + F2 builder | Silent policy drift | Frozen-state cell + asserts | Policies restated + asserted |
| 3 | Dependency & Environment Gate | Record env; verify pinned-stack mirror + pinned GBDTs; never mutate `.venv` | Strategy D→B; versions; rollback | dependency-check notebook output | Env contamination; version drift | dependency_report + environment_report | Versions verified; **no install in `.venv`** |
| 4 | External GBDT Registry & Risk Classification | Pre-register GBDTs, configs, statuses | §8 registry; 2A/2B split; cap ≤ 3 | §8 ratified at §20 | Model-zoo creep; informal HPO | Ratified registry | Director ratification |
| 5 | CatBoost Double-Gate & School Control | Enforce §9 gates | 2B authorization; `cat_features=[]`; School assert | §9 | Categorical/School leakage | Gate-checked CatBoost path | Both gates pass or CatBoost skipped |
| 6 | Fair Comparison Protocol & Notebook Blueprint | Guarantee identical conditions; fix notebook structure | §11 matrix; §12 cell-by-cell | §11/§12 | Confounded/rigged comparison | Protocol + blueprint | Independent review passes |
| 7 | Validation, Slice Diagnostics & Acceptance | Classify each GBDT per pre-registered rule | §14 criteria; paired vs M0 & M1; slice guard incl. `Age_missing=1` | §14 tables | Noise as signal; subgroup harm | model_summary + fold_metrics + slice_report + decision table | Every GBDT classified by rule |
| 8 | Project Director Approval Gate & Codex Handoff | Separate decision from execution | Whether to run 2A; whether to run 2B; install authorization | this brief + runbook | Unauthorized execution/installs | Project Authorization Note (runbook §12) | **Explicit director authorization recorded** |

---

## 11. Fair Comparison Protocol

Every Wave 2 GBDT runs under an identical matrix; the only varying factor is the model family. m0/m1 are carried from persisted OOF (not retrained).

| Dimension | Fixed value for all models |
|---|---|
| Dataset | `data/input/train.csv` only (test only for contract checks; no Wave 2 inference) |
| Feature set | **F2 exactly**: 13 base + 7 missingness flags + `available_measurement_count` (21 features) |
| Exclusions | `Id`, `Drafted`, `School` (asserted) |
| Folds | Frozen file, sha256[:16] `96937649526bcadb`, 2781 rows, labels 0..4; never recomputed |
| Metric | ROC-AUC, positive-class proba via verified `estimator.classes_` |
| Preprocessing | Audited Wave 1 / Phase 7 shared F2 builder: fold-fitted median imputer + most_frequent + OHE(`handle_unknown="ignore"`) in `ColumnTransformer`+`Pipeline`; **GBDTs receive the same all-numeric encoded matrix**; CatBoost `cat_features=[]` |
| Comparators | m0 (reference) and m1 (warned) loaded from persisted Wave 1 OOF; not retrained |
| Seed | 42 everywhere; single-thread/deterministic GBDT settings |
| Artifact naming | `phase8_wave2_external_gbdt_v1_<model_key>_*` with pre-write guards |
| Candidate log | One v2 row under `outputs/reports/`; main log untouched |
| Leakage checks | §15 checklist instantiated per model |
| Leaderboard | Untouched |

**Pre-registered evidence rule (flagging, not auto-adoption):** a GBDT is flagged **"promotable evidence"** if `OOF(model) − OOF(m0) ≥ 0.005436` AND paired fold deltas vs m0 positive in ≥ 4/5 folds AND the slice guard is clear. A **second readout** compares each GBDT to m1 (delta and same-sign folds) — informational, since m1 is itself only a warned candidate. Models below the m0 bar are flagged "no qualifying evidence"; slice-guard trips are "escalated". `Age_missing=1` (n=435, 8 positives) is tracked explicitly for every GBDT against M0's 0.6917 and m1's 0.5442. **Wave 2 produces a classified evidence table — it does not crown a winner.** Candidate selection is a director decision in `phase8_wave2_acceptance.md`.

---

## 12. Notebook / Script Architecture Blueprint

### 12.1 Decision: two notebooks (staged)

**Decision: two notebooks** — a read-only dependency/environment check, then the comparison — because environment mutation must be isolated from comparison logic (the Wave 1 plan already reserved `08b` for exactly this). A single notebook would force install logic and modeling into one artifact, contaminating reproducibility and audit clarity; three+ notebooks would fragment without a control point.

| Notebook | Rol | Por qué separado | Inputs | Outputs | Cuándo se ejecutaría | Riesgo si se fusiona | Riesgo si se separa |
|---|---|---|---|---|---|---|---|
| `08b_phase8_wave2_dependency_environment_check.ipynb` | Read-only env/dependency gate | Install/version decisions must be auditable before any modeling; zero mutation | venv introspection | dependency_report + environment_report | First, after §20 authorization to *check* (still no install) | Install logic mixed with modeling breaks reproducibility | None (it is the safety gate) |
| `08c_phase8_wave2_external_gbdt_comparison.ipynb` | GBDT comparison | Runs only in the authorized separate env after install authorization | train.csv, frozen folds, m0/m1 persisted OOF, F2 builder | all §15.8 comparison artifacts | After dependency check + separate-env + install authorization | — | None |

### 12.2 Mandatory notebook hygiene (both notebooks)

Each notebook must include: a clear title; exact phase (`Phase 8 Wave 2`); objective; authorized scope; explicit "does / does NOT" limits; a short description before each technical block; methodological justification before each critical decision; a validation cell after each critical block; a brief analysis after each important table/metric; an executive conclusion; risks; decisions; next steps; and the literal Phase 9/10/11 lock reminder. It must avoid: unexplained cells, results without interpretation, metrics without context, silent decision changes, outputs without a manifest, ignored warnings, unnecessary hardcoded paths, unverified dependencies, and any mid-notebook scope change.

### 12.3 `08b` dependency/environment check (read-only)

| Sección / celda | Título sugerido | Propósito | Inputs | Outputs | Validaciones obligatorias | Análisis esperado | Riesgos controlados |
|---|---|---|---|---|---|---|---|
| 1 | Title, scope & guardrails | Declare read-only, no-install | — | markdown | — | — | Scope creep |
| 2 | Environment read-only inspection | Record Python/OS/arch, `.venv` path | venv | env dict | Records without mutation | Pinned-stack confirmation | Mutation |
| 3 | Python version check | Confirm 3.13.13 | sys | field | == 3.13.13 | Compatibility note | Wrong interpreter |
| 4 | Installed package check | Snapshot key versions | importlib.metadata | table | sklearn 1.9.0 / pandas 3.0.3 / numpy 2.4.6 | Stack matches pinned | Drift |
| 5 | GBDT availability check | `find_spec` for xgboost/lightgbm/catboost | importlib.util | table | Currently all absent | Confirms install needed | Silent presence |
| 6 | Compatibility risk summary | Wheel/Py3.13/OpenMP notes | static knowledge | dependency_report | Risk levels recorded | Per-library feasibility | Hidden incompatibility |
| 7 | Recommendation | install-separate-env / defer | analysis | report field | Recommends separate env (§7) | Decision support | Wrong env strategy |
| 8 | No-install confirmation | Assert nothing installed | env | assert | No new packages present after run | — | Accidental install |
| 9 | No-model-execution confirmation | Assert no model trained | — | assert | — | — | Scope creep |
| 10 | Executive conclusion | Summarize + lock reminder | — | markdown | Phase 9/10/11 locked stated | — | Overclaim |

This notebook stays **read-only** unless the director later authorizes installs explicitly.

### 12.4 `08c` external GBDT comparison

| Sección / celda | Título sugerido | Propósito | Inputs | Outputs | Validaciones obligatorias | Análisis esperado | Artefactos asociados |
|---|---|---|---|---|---|---|---|
| 1 | Title, scope & guardrails | Phase, experiment_id, non-scope | — | markdown | — | — | — |
| 2 | Imports & dependency checks | Import sklearn/pandas/numpy + authorized GBDTs; record versions | env | env dict | GBDTs importable in the **separate** env; versions pinned | Env readiness | environment_report |
| 3 | Path config & repo-root validation | Relative paths | — | constants | Root markers exist | — | — |
| 4 | Environment record | git HEAD + dirty + versions | git | report fields | HEAD == authorized hash | Provenance | report |
| 5 | Protected-path & no-overwrite checks | Assert no `phase8_wave2_*` exists; main-log checksum | outputs/, logs/ | guard state | Guards armed | — | — |
| 6 | Data loading (official only) | Load train.csv | data/input | DataFrame | 2781×16 | — | — |
| 7 | Data contract checks | 12 contract checks | DataFrame | asserts | dtypes, Id uniqueness, target, missingness counts | Contract intact | report |
| 8 | Frozen folds load + integrity | Load fold file | outputs/folds | fold map | 2781 rows; labels 0..4; Id order; sha `96937649526bcadb` | Fold integrity | report |
| 9 | F2 feature builder | Row-wise flags + count via audited builder | train | X (21), y | Flag sums == known missingness; School/Id/Drafted ∉ X | Feature integrity | — |
| 10 | Exclusion asserts | `Id`/`Drafted`/`School` not in X | X | assert | Raise on violation | — | — |
| 11 | Comparator carryover (m0, m1) | Load persisted OOF; re-verify M0 anchor | Wave 1 OOF | vectors | m0 OOF == 0.8116502602456482 ± 1e-9 | Anchor reproduced | — |
| 12 | Preprocessing protocol | Shared fold-fitted F2 `ColumnTransformer` | X | pipeline factory | Fit only inside folds | Leakage-safe | — |
| 13 | External GBDT registry | §8 configs verbatim; statuses; cap ≤ 3 | — | registry dict | Exactly ratified configs | No creep | report registry |
| 14 | CatBoost double-gate check | Enforce §9 gates | note flags | gate verdict | 2B flag + School reconfirm or skip; `cat_features=[]` | Categorical/School control | report |
| 15 | Model eligibility checks | Importable, `predict_proba`, seed set | registry | table | Eligible or skip+record (never substitute) | — | report |
| 16 | CV/OOF loop | Per GBDT × 5 frozen folds; fit train mask, predict val mask | X, y, folds | per-model OOF | classes_ verified; proba finite [0,1]; no single-class fold; fold map matches | Leakage/class-index control | per-model OOF CSVs |
| 17 | Positive-class proba verification | `classes_` locates label 1 once | models | — | Helper raises otherwise | — | — |
| 18 | Fold-level metrics | Per fold AUC | OOFs | fold_metrics | 5 rows/model | Variance visible | fold_metrics CSV |
| 19 | OOF ROC-AUC | OOF AUC per GBDT | OOFs | summary rows | — | Global standing | model_summary CSV |
| 20 | Paired deltas vs M0 | Per-fold + OOF delta vs m0; same-sign count | OOFs | summary | Flag rule applied | Evidence vs anchor | model_summary CSV |
| 21 | Paired deltas vs M1 | Per-fold + OOF delta vs m1 | OOFs | summary | Informational readout | Evidence vs warned candidate | model_summary CSV |
| 22 | Slice diagnostics | 7 mandatory slices per GBDT | OOFs + slices | slice table | n<50 flagged; >0.02 vs m0 ⇒ escalated | Subgroup robustness | slice_report CSV |
| 23 | `Age_missing=1` comparison | Track GBDT AUC on the fragile slice vs M0 (0.6917) and m1 (0.5442) | slice data | rows | Explicit per-model values | Fragile-slice behavior | slice_report CSV |
| 24 | Model summary table | One row per GBDT + classification | summary | table | Rule applied; no winner language | Standing | model_summary CSV |
| 25 | Artifact writing plan | All §15.8 files with guards | results | files | Guard trip ⇒ stop; manifest row per artifact | — | artifact_manifest CSV |
| 26 | Candidate log row | v2 schema rows | results | log | Main log byte-identical (assert) | — | candidate_log CSV |
| 27 | Leakage checklist | §15 per model | state | table | All pass or stop | All layers | report |
| 28 | Acceptance criteria check | Apply §14 flag rule | summary | decision table | promotable / no_qualifying / escalated / failed_run | Classification | report |
| 29 | Executive conclusion | Classified table + "no winner crowned" | — | markdown | Required statements present | — | report |
| 30 | Stop conditions & next-phase lock | Phase 9/10/11 locked | — | markdown | Lock statements present | — | report |

### 12.5 Model registry architecture

| model_key | Modelo | Estado | Dependencia | Preprocessing requerido | Config inicial pre-registrada | Riesgo | Condición de inclusión |
|---|---|---|---|---|---|---|---|
| `xgboost` | XGBClassifier | Active Wave 2 candidate | xgboost (pinned, **not installed**) | Shared OHE F2 | `n_estimators=300, max_depth=6, lr=0.1, reg_lambda=1.0, random_state=42, n_jobs=1, tree_method="hist"` | Env; determinism | 2A authorization |
| `lightgbm` | LGBMClassifier | Active Wave 2 candidate | lightgbm (pinned, **not installed**) | Shared OHE F2 | `n_estimators=300, num_leaves=31, lr=0.1, reg_lambda=1.0, random_state=42, n_jobs=1, deterministic=True, force_col_wise=True` | Env; OpenMP; determinism | 2A authorization |
| `catboost` | CatBoostClassifier | Gated candidate | catboost (pinned, **not installed**) | Shared OHE F2, `cat_features=[]` | `iterations=300, depth=6, lr=0.1, random_seed=42, thread_count=1, cat_features=[], allow_writing_files=False` | School/categorical leakage; env | 2B double-gate (§9) |
| `m0_random_forest_frozen` | RandomForestClassifier | Reference comparator | sklearn (installed) | carried OOF (not retrained) | from Wave 1 | None | Always |
| `m1_logistic_regression` | LogisticRegression | Candidate-with-warning comparator | sklearn (installed) | carried OOF (not retrained) | from Wave 1 | None | Always |

### 12.6 Preprocessing architecture per model

| Modelo | Numeric preprocessing | Categorical preprocessing | Missing-value strategy | Scaling needed | School policy | Riesgo de leakage | Diseño recomendado |
|---|---|---|---|---|---|---|---|
| xgboost | fold-fitted median impute | fold-fitted most_frequent + OHE(ignore) | median + 7 flags + count (F2) | No | Excluded | Low (shared builder) | Reuse F2 pipeline; numeric matrix to XGB |
| lightgbm | same | same | same | No | Excluded | Low; **`categorical_feature` unused** | Same shared pipeline; no native categorical |
| catboost | same | same | same | No | **Excluded — hard gate** | Native target-statistic encoding is the risk | `cat_features=[]` on the pre-encoded matrix; School-reconfirm |
| m0 / m1 | n/a (carried OOF) | n/a | n/a | n/a | Excluded | None | Load persisted OOF; do not retrain |

Invariants: same F2 features for all; no per-model feature engineering; all fitting inside training folds; no global statistics; no tuning; no target encoding; no external data.

### 12.7 Validation architecture

| Componente | Diseño esperado | Evidencia requerida | Stop condition |
|---|---|---|---|
| Frozen fold loading | Load committed file; assert count/labels/order/sha | sha256[:16] `96937649526bcadb` | Any mismatch |
| M0 anchor recheck | recompute m0 persisted OOF AUC | == 0.8116502602456482 ± 1e-9 | Mismatch ⇒ baseline drift |
| ROC-AUC per fold | `roc_auc_score` on val-fold proba | fold_metrics CSV | NaN/undefined |
| OOF ROC-AUC | full-vector AUC per GBDT | model_summary CSV | — |
| `estimator.classes_` | label 1 located once before proba | helper raises | Helper raises |
| Probability validity | finite, [0,1], no NaN | per-model asserts | Any violation |
| Paired fold deltas vs M0 | model − m0 per fold; same-sign | model_summary | — |
| Paired fold deltas vs M1 | model − m1 per fold; same-sign | model_summary | — |
| Paired OOF comparison | vs M0 (flag) and M1 (informational) | decision table | — |
| Slice diagnostics | 7 mandatory dims; n≥50 policy | slice_report CSV | escalation = flag, not auto-decide |
| `Age_missing=1` tracking | per-GBDT AUC vs M0 0.6917 / m1 0.5442 | slice_report rows | — |
| Model summary table | one row per GBDT + classification | model_summary CSV | — |
| Leakage checklist per model | §15 instantiated | report | any failure ⇒ stop |
| Artifact manifest | path + sha256 + rows per artifact | artifact_manifest CSV | guard trip |

### 12.8 Artifact architecture (namespace `phase8_wave2_external_gbdt_v1`)

| Artifact | Path pattern | Producer section | Purpose | Overwrite policy | Required before acceptance |
|---|---|---|---|---|---|
| Per-model OOF | `outputs/oof/phase8_wave2_external_gbdt_v1_<model_key>_oof_predictions.csv` | 16/25 | Independent recomputation currency | Never (guard) | Yes |
| Model summary | `outputs/validation/phase8_wave2_external_gbdt_v1_model_summary.csv` | 24/25 | Primary comparison table | Never | Yes |
| Fold metrics | `outputs/validation/phase8_wave2_external_gbdt_v1_fold_metrics.csv` | 18/25 | Fold-level diagnostics | Never | Yes |
| Slice report | `outputs/validation/phase8_wave2_external_gbdt_v1_slice_report.csv` | 22/25 | Subgroup robustness incl. `Age_missing=1` | Never | Yes |
| Dependency report | `outputs/validation/phase8_wave2_external_gbdt_v1_dependency_report.csv` | 08b | Wheel/version/compat record | Never | Yes |
| Validation report | `outputs/reports/phase8_wave2_external_gbdt_v1_validation_report.md` | 29 | Full narrative + tables + leakage checklists | Never | Yes |
| Candidate log | `outputs/reports/phase8_wave2_external_gbdt_v1_experiment_log_candidate.csv` | 26 | v2-schema rows; main log untouched | Never | Yes |
| Artifact manifest | `outputs/reports/phase8_wave2_external_gbdt_v1_artifact_manifest.csv` | 25 | Path + sha256 + rows per artifact | Never | Yes |
| Environment report | `outputs/reports/phase8_wave2_external_gbdt_v1_environment_report.md` | 08b/08c | Exact env + GBDT versions | Never | Yes |
| Acceptance record | `docs/08_model_comparison/phase8_wave2_acceptance.md` | post-run, director | Closure decision (candidate(s) or null) | Human-authored | Yes (at closure) |

### 12.9 Opus → Codex fidelity contract (traceability)

| Decisión de Claude Opus | Sección del notebook | Instrucción correspondiente para Codex | Cómo verificar fidelidad |
|---|---|---|---|
| Two notebooks; install isolated | 08b / 08c split | "Run 08b read-only first; 08c only in the authorized separate env" | Two-file structure; no install in 08b |
| Separate env, `.venv` untouched | 08c cell 2 | "Import GBDTs from the separate env; never modify `.venv`/requirements" | environment_report; `.venv` unchanged |
| Comparators carried, not retrained | 08c cell 11 | "Load m0/m1 from persisted OOF; re-verify M0; do not retrain" | M0 recompute == 0.811650; no RF/LR fit |
| F2 frozen, School excluded | 08c cells 9/10/14 | "Build F2; assert feature list + exclusions + flag sums" | Assert output |
| Frozen folds, sha-checked | 08c cell 8 | "Load fold file; assert sha/rows/labels/order; never recompute" | Assert output |
| Registry of ≤3 GBDTs, configs frozen | 08c cell 13 | "Implement exactly the ratified registry; no add/substitute/alter" | Registry diff vs §8 |
| CatBoost double-gate, `cat_features=[]` | 08c cell 14 | "Run CatBoost only if 2B authorized + School reconfirmed; `cat_features=[]`" | Gate verdict; config assert |
| No HPO / no eval_set | 08c cell 13/16 | "Single config per family; no search; no early stopping / eval_set" | Config inspection |
| Flag rule, paired vs M0 & M1, no winner | 08c cells 20/21/28 | "Classify per rule; selection language prohibited" | Decision-table wording |
| Slice guard incl. `Age_missing=1` | 08c cells 22/23 | "All 7 slices; n≥50; >0.02 ⇒ escalated; track Age_missing=1" | slice_report |
| Pre-write guards + manifest | 08c cell 25 | "Fail-if-exists on every path; write manifest" | Manifest vs filesystem |
| Main log protected | 08c cells 5/26 | "Read-before/assert-after byte-identical" | Checksum asserts |
| No submissions/LB/Phase 9+ | 08c cells 1/30 | Stop rules + closing statements | Report closing section |

---

## 13. Fold-Safe Implementation Design, if Later Authorized

No notebook is created now. The future `08c` is bound by the §12 blueprint plus: runs top-to-bottom from repo root; relative paths; `PROJECT_SEED = 42`; executed headless in the **separate authorized Wave 2 env** (mirroring scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6 + pinned GBDTs); records env + `git rev-parse HEAD` + dirty flag + exact GBDT versions; reuses the audited Wave 1 / Phase 7 F2 builders and shared `ColumnTransformer`; comparators loaded from persisted OOF (not retrained); two-role verification after the run (independent stdlib rank-AUC recomputation of every OOF file — the proven 6A/7/Wave-1 pattern). **Forbidden inside the notebook:** test-data fitting; submissions; HPO/early-stopping/eval_set; School in features; CatBoost native categorical; `logs/experiment_log.csv` writes; `.venv`/requirements modification; Phase 9/10/11 work.

---

## 14. Validation, Slice Reports and Acceptance Criteria

### 14.1 Acceptance of the planning package (level A)

| Criterion | Condition | Evidence source | What happens if it fails |
|---|---|---|---|
| Repository state verified | §1 all PASS at `041ba10` | §1 | Re-verify; stop if HEAD/forbidden differ |
| Wave 1 closure verified | acceptance committed (`041ba10`) | §1/§2 | Wave 2 stays blocked |
| Wave 2 not previously executed | no `phase8_wave2_*` artifacts | §1 | Treat as collision; investigate |
| F2 verified | OOF 0.811650; 21 features | §3 | Mark Not confirmed yet; block |
| XGB/LGBM/CatBoost named & classified | §8 registry | §8 | Amend |
| CatBoost double gate included | §9 | §9 | Amend |
| References reviewed / deferred | §5 (compact summaries sufficed) | §5 | Targeted review |
| Theory→practice transfer | §5 | §5 | Amend |
| Dependency/env strategy | §7 (D→B recommended) | §7 | Amend |
| Notebook blueprint | §12 cell-by-cell, 2 notebooks | §12 | Amend |
| Opus→Codex fidelity contract | §12.9 + Deliverable C | §12.9 | Amend |
| Metric & folds verified | §3/§4 | §3 | Block |
| Protected paths + prohibited actions listed | §15/§19 + runbook | this brief | Amend |
| HPO / submissions / LB blocked; School explicit | §4, §9, §19 | this brief | Block |
| Artifacts & logs policy explicit | §16 | §16 | Amend |
| Director approval required before execution | §20 | §20 | Absolute |
| Phase 9/10/11 locked | §20 | this brief | Absolute |

### 14.2 Acceptance of a future authorized execution (level B)

| Criterion | Condition | Evidence source | What happens if it fails |
|---|---|---|---|
| Identical folds & F2 for all models | fold sha + feature asserts pass | notebook asserts | Stop run |
| M0 anchor recheck | m0 persisted OOF == 0.8116502602456482 ± 1e-9 | report + recompute | Stop; baseline drift |
| No model-specific feature leakage | shared builder; checklist per model | §15 | Stop |
| No HPO | configs byte-identical to ratified registry; no eval_set | registry diff | Stop |
| No submissions; no LB | no `outputs/submissions/`; no LB refs | git status + report | Stop |
| No env contamination | `.venv`/requirements unchanged; GBDTs only in separate env | git + environment_report | Stop |
| OOF validity | finite, [0,1], no NaN, no single-class fold, fold map matches | per-model asserts | Stop |
| `classes_` verified | label 1 once per fit | helper | Stop |
| Fold-level metrics saved | fold_metrics complete | artifact | Block acceptance |
| OOF ROC-AUC + paired deltas vs M0 & M1 | model_summary complete | artifact | Block acceptance |
| Slice diagnostics + min-n + `Age_missing=1` | slice_report complete; escalations listed | artifact | Block acceptance |
| Dependency + environment reports | both generated | artifacts | Block acceptance |
| Artifact manifest | rows == written files, sha-matched | manifest | Block acceptance |
| Candidate log separate; main log untouched | byte-identical assert | checksum | Stop |
| Validation report generated | complete with leakage checklists | artifact | Block acceptance |
| Independent recomputation matches | ≤ 1e-9 per OOF file | audit | Block acceptance until resolved |
| No forbidden diffs; only expected new untracked artifacts | post-run git checks | runbook §14 | Stop |
| Phase 9/10/11 locked | closing statements present | report | Block acceptance |

**Pre-registered edge cases:** GBDT fails to import / converge / errors ⇒ record `failed_run`, never substitute a config, continue remaining registry, report; AUC undefined on a slice ⇒ flag non-evaluable; escalated slice ⇒ director review with the slice table (the m1 `Age_missing=1` pattern); guard trip / HEAD mismatch / fold mismatch / proba invalid / `classes_` failure / env contamination / mid-run config change ⇒ **stop the run**.

---

## 15. Leakage Control Strategy

Instantiates `leakage_checklist_phase6.md` for external GBDTs:

| Layer | Wave 2 control |
|---|---|
| Data / external | Official CSVs only; references = methodology only; GBDT configs carry no external info |
| Test-to-train | Test rows only for contract checks; **no Wave 2 fitting touches test; no inference; no submission** |
| Preprocessing / imputation / encoding | Shared fold-fitted F2 pipeline; GBDTs receive the same encoded matrix; fit only on training mask |
| Feature computation | F2 frozen; **no per-model feature engineering** |
| Target encoding | Absent; **CatBoost native target-statistic encoding disabled (`cat_features=[]`)** |
| Feature selection / dim reduction / rare grouping | Absent |
| Role statistics | Only fold-fitted OHE of raw categoricals |
| HPO / model selection | Frozen registry; run cap ≤ 3; flag rule ≠ adoption; **search / early-stopping / eval_set = stop condition** |
| Model-specific shortcuts | LightGBM `categorical_feature` unused; CatBoost `cat_features=[]`; School excluded everywhere |
| Leaderboard | Untouched |
| Confound/group | Folds frozen; grouped CV dormant (refined D2); new duplication evidence = stop |
| Diagnostic-only variables | `frequent_vs_rare_school_group`, `measurement_completeness_group` stay out of all feature matrices (assert) |
| Environment | `.venv`/requirements untouched; GBDTs isolated in a separate env; versions recorded |
| Verification doctrine | Two-role rule: in-notebook self-checks **plus** post-run independent OOF recomputation by a different role/session |

---

## 16. Artifact, Documentation and Git Plan

**Created/updated in this planning run (authorized set only):**

```text
docs/08_model_comparison/phase8_wave2_master_planning_brief.md   (this file)
docs/08_model_comparison/phase8_wave2_operator_runbook.md
docs/08_model_comparison/prompt_codex_phase8_wave2_execution_plan.md
```

**Future artifacts if execution is authorized (names reserved; NOT created now):** the §12.8 table — notebooks `08b`/`08c`, ≤3 per-model OOF files, model_summary, fold_metrics, slice_report, dependency_report, validation_report, experiment_log_candidate, artifact_manifest, environment_report, and `docs/08_model_comparison/phase8_wave2_acceptance.md` at closure. The orientative separate `phase8_wave2_execution_plan.md` / `phase8_wave2_model_registry.md` / `phase8_wave2_validation_and_acceptance_criteria.md` are **subsumed by §§8–14 of this brief** (separate near-duplicate files create drift); extractable verbatim later if preferred.

**Git policy:** this run stages and commits **nothing** (`git add .` / `git commit -a` permanently forbidden). Recommended future sequencing: (1) selectively commit the three planning docs (one explicit instruction, individual `git add` per file) so the execution session verifies a planning-inclusive hash; (2) after execution + audit + signed acceptance, a second selective commit of notebooks + artifacts + acceptance, hash recorded back (the `041ba10` pattern). Notebooks, reports, prompts and acceptance docs must not be mixed into one undifferentiated commit without that declared strategy. Main log untouched; v2 migration separately gated.

---

## 17. ECC Agents and Skills Plan

`/plugin list ecc@ecc` is a CLI user command not invocable from agent context; availability verified by direct disk inspection: **10 agents** in `.claude/agents/`, **21 skills** in `.claude/skills/`. No new installation recommended (no Wave-2 capability gap). Anything toward HPO/AutoML/submissions/LB/scraping/external-data/deployment/autonomous-loops is prohibited regardless of tool.

| Etapa o necesidad | Agente/skill sugerido | Uso propuesto | Riesgo mitigado | Condición de activación |
|---|---|---|---|---|
| Block 0 pre-flight | repo-scan + gateguard | Verify HEAD, clean tree, gates, no `phase8_wave2_*` artifacts | Wrong baseline; double execution | Start of any Wave 2 session |
| Dependency/env planning | docs-lookup / documentation-lookup | Confirm pinned XGB/LGBM/CatBoost versions + Py 3.13 wheels | Broken env; irreproducibility | Reviewing §7 / before install authorization |
| Plan re-validation | planner / plan-orchestrate | Re-check this package vs repo state | Stale plan | Before §20 gate |
| Registry/protocol review | mle-reviewer + mle-workflow | Validate fair-matrix, configs, fold use, OOF + CatBoost gate | Methodological defects | Before authorization |
| Evaluation design | eval-harness | OOF / fold-metrics / paired-deltas / slice design of `08c` | Metric corruption | Notebook draft review |
| Static code review (two-role) | code-reviewer + python-reviewer + python-patterns | Independent review of `08b`/`08c`; generator ≠ verifier | Leakage/code defects | After draft, before execution |
| Silent-failure pass | silent-failure-hunter | `classes_` paths, NaN handling, install/import failures, guard trips | Silent corruption | Same gate |
| Environment safety | build-error-resolver | **Only if** an authorized install fails (wheel/OpenMP/Py3.13) | Broken env | After install authorization, on failure |
| Execution session guard | gateguard + safety-guard | Block HPO/submissions/LB/installs-into-`.venv`/Phase 9+ mid-run | Scope creep; env contamination | During authorized execution |
| Post-run verification | verification-loop + independent stdlib AUC recompute | Recompute every OOF AUC from persisted files; git/forbidden-path checks | Self-reported-only results | Immediately after execution |
| Selective commit | git-workflow | Stage explicit file list only; record hash | `git add .` accidents | **Only after explicit director instruction** |
| Long-session hygiene | context-budget / token-budget-advisor | Keep sessions within budget | Context-degradation errors | If sessions grow long |

Classification: **(1) Active in planning** — repo-scan, gateguard, planner, mle-reviewer, mle-workflow, eval-harness, code-reviewer, python-reviewer, python-patterns, silent-failure-hunter, verification-loop, doc-updater (3 docs only); **(2) On need** — architect, code-explorer, docs-lookup, documentation-lookup, build-error-resolver (install-failure only), git-workflow (post-authorization commit), safety-guard, context-budget, token-budget-advisor, architecture-decision-records; **(3) Not for Wave 2** — agent-eval, agent-architecture-audit, automation-audit-ops, codebase-onboarding, code-tour; **(4) Risky/prohibited use** — any tool aimed at HPO/AutoML/submissions/LB/scraping/external-data/deployment/autonomous loops.

---

## 18. Risks, Failure Modes and Mitigations

| Risk | Failure mode | Mitigation |
|---|---|---|
| Environment mutation breaks Wave 1 reproducibility | Install into `.venv` upgrades numpy/sklearn; M0 ≠ F2 | Separate env mirroring pinned stack; comparators carried from persisted OOF; `.venv` untouched (§7) |
| Wave 2 drifts into HPO | "Try a few depths/learning rates / early stopping" | Frozen single config per family; cap ≤ 3; no eval_set; config change = stop; HPO is Phase 10 |
| CatBoost School/target-encoding leakage | Native `cat_features` re-introduces excluded School signal | Double-gate; `cat_features=[]`; School assert; deferrable (§9) |
| Unfair preprocessing advantage | Per-model pipeline tweaks / native categorical | Shared audited F2 pipeline for all; LightGBM `categorical_feature` unused |
| GBDT nondeterminism | Threaded/leaf-wise nondeterminism makes results irreproducible | `n_jobs=1`/`thread_count=1`/`deterministic=True`; seed 42; env+versions recorded |
| Winner-crowning by max-picking | Top OOF treated as selection | Flag rule + "no winner" language; selection only in acceptance by director |
| Slice harm hidden by global gains | `Age_missing=1` regression masked | Mandatory slice guard incl. explicit `Age_missing=1` tracking vs M0/m1 |
| Threshold misapplied across families | 0.005436 is RF-noise-derived | Documented limitation; flag-not-adopt; per-family noise = Phase 9 |
| Dependency wheel/Py3.13 incompatibility | Install fails or pulls incompatible transitive deps | Read-only dependency check first; pinned versions; build-error-resolver only on failure |
| Artifact overwrite / unanchored results | Lost audit trail | Pre-write guards; sha256 manifest; selective-commit + hash-record |
| Generator-verifier collusion | Unreviewed defects | Two-role rule: independent static review + independent OOF recomputation |
| Phase 9/10/11 pull | "Tune / ensemble / submit the winner" | gateguard + locks (§20); refusal wired into Deliverable C |

---

## 19. Explicit Non-Actions

This planning run did **not**: install any package; create or modify any environment or `.venv`/requirements; execute or create any notebook; train any model; run XGBoost, LightGBM or CatBoost; run any model-family comparison; run HPO; generate any OOF/validation/report/submission artifact; consult the leaderboard; modify Wave 1 artifacts, `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `docs/08_model_comparison/phase8_acceptance.md`, `notebooks/08_phase8_model_family_comparison.ipynb`, or any tracked file; stage anything; commit anything; push anything; open Phase 9/10/11. The only filesystem writes were the three authorized documents under `docs/08_model_comparison/`.

---

## 20. Required Project Director Authorization Before Execution

Wave 2 execution may begin only after the project director explicitly and in writing:

1. Approves this brief and the runbook (or records amendments, which then freeze).
2. **Authorizes the environment strategy** (§7 D→B): permits the read-only dependency check, and separately permits creating a dedicated Wave 2 env with named, pinned GBDT versions — explicitly **not** mutating `.venv`/requirements.
3. **Ratifies the §8 registry**: model list, exact configs, statuses, the cap (≤ 3 trained GBDTs), and the Sub-wave 2A/2B split.
4. **Decides CatBoost (§9)**: authorize Sub-wave 2B with School-exclusion reconfirmation, or defer/omit CatBoost.
5. Confirms thresholds: flag rule 0.005436 + ≥ 4/5 same-sign vs M0; slice guard (n ≥ 50, 0.02 escalation); M0 anchor tolerance ± 1e-9.
6. Confirms the §12.8/§16 artifact names and the no-commit-without-instruction policy.
7. Records the authorized starting commit hash (currently `041ba10`; advances if these planning docs are committed first — recommended).
8. Issues an explicit "execute Phase 8 Wave 2" instruction referencing `prompt_codex_phase8_wave2_execution_plan.md` with the signed note (runbook §12 format).

Absent any item: **planned, not executable.**

---

## 21. Recommended Next Step

**Option A — Review the generated Wave 2 planning package; execution remains blocked until explicit project director authorization.**

Concretely: (1) read this brief top-to-bottom; (2) decide the environment strategy (§7) and ratify/amend the §8 registry, the §9 CatBoost gate, and §20's parameters; (3) decide whether to selectively commit the three planning docs first (recommended); (4) when ready, authorize per §20 using Deliverable C — first the read-only dependency check, then (separately) the dependency install + comparison. **Phase 9, Phase 10 and Phase 11 remain locked throughout. Future phases remain locked.**
