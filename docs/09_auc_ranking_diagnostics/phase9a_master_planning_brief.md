# Phase 9A Master Planning Brief — AUC-Oriented Imbalance and Ranking Diagnostics

**Phase:** Phase 9A — AUC-Oriented Imbalance and Ranking Diagnostics, PLANNING ONLY
**Date:** 2026-06-18
**Planning baseline commit:** `4bbcd7a` (*validation: accept phase 8 wave 2 external gbdt comparison*)
**Status:** Planning package. **Phase 9A execution is NOT authorized by this document.** No model training, no HPO, no submissions, no winner declaration. Phase 10 and Phase 11 remain locked.

---

## 0. Executive Verdict

**Phase 9A can be planned safely as a read-only, OOF-based diagnostic phase, and execution must remain blocked until explicit project-director authorization.** Every entry gate holds: Phase 8 Wave 1 accepted with warnings (`041ba10`); Phase 8 Wave 2 planned (`98d8bb9`) and executed+accepted (`4bbcd7a` = current HEAD, the expected hash). No final winner exists; no submission-ready model exists.

Phase 9A's purpose is **diagnostic, not selective**: using only already-persisted OOF predictions, characterize how the Phase 8 candidates behave under complementary ranking/imbalance diagnostics (PR-AUC, top-k/lift/enrichment, fold stability, slice fragility, score distributions, M1↔CatBoost disagreement, diagnostic calibration) so the project director can decide *what questions to answer before Phase 10/11* — without declaring a winner or authorizing a submission.

One load-bearing fact, verified read-only this planning run, governs the entire diagnostic design: the evaluation set is **mildly imbalanced and majority-positive — positive rate 0.6483 (1803 `Drafted=1` of 2781)**. This is *not* a rare-event retrieval problem. PR-AUC, precision@k, lift@k and top-k capture are therefore included as **ranking-characterization diagnostics at the decision-relevant head of the score distribution**, not as rare-class retrieval substitutes for ROC-AUC, and the plan requires any ROC-vs-PR/top-k conclusion conflict to be reported as a warning rather than used to re-rank candidates.

A second governing fact: all five candidate OOF files share an identical, frozen evaluation substrate — 2781 rows, folds 0..4, **zero Id→fold and Id→y_true mismatches against the M0 anchor** — which makes paired per-fold and per-row diagnostics methodologically valid without any retraining.

**Recommended next step:** project-director review of this package; execution stays blocked until a signed Phase 9A authorization (Option A, §21).

---

## 1. Repository State Verification

Commands run on 2026-06-18 (read-only):

| Check | Expected | Observed | Status |
|---|---|---|---|
| `git rev-parse --short HEAD` | `4bbcd7a` | `4bbcd7a` | PASS |
| `git rev-parse HEAD` | `4bbcd7a7b4dbf159b4bd9379104839923999cc15` | identical | PASS |
| `git status --short` | only known untracked items | only `.claude/`, `.obsidian/`, `CLAUDE.md`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `Sin título.canvas`, plan v1, 2 backup notebooks, `notebooks/_official/` | PASS |
| `git diff --check` | clean | clean | PASS |
| `git diff --cached --name-only` | empty | empty | PASS |
| Forbidden-paths diff (`data/input`, `notebooks/_official`, `references`, `outputs/submissions`, `logs/experiment_log.csv`, `.vscode/settings.json`) | empty | empty | PASS |
| `git diff -- logs/experiment_log.csv` | unchanged | empty (unchanged) | PASS |
| `git log --oneline` (top) | Phase 8 Wave 2 closure on top | `4bbcd7a`, `98d8bb9`, `041ba10`, `f8c7911`, `7166c2e`, … | PASS |
| Phase 8 Wave 2 closure commit `4bbcd7a` | accepts Wave 2 | commits `phase8_wave2_acceptance.md` + notebooks 08b/08c + all `phase8_wave2_external_gbdt_v1_*` artifacts (14 files) | PASS |
| Phase 9A previously executed? | No | `docs/09_auc_ranking_diagnostics/` does not exist; no `phase9a_*` artifact anywhere | PASS (not executed) |

No discrepancy was found. Canonical commits confirmed: Wave 1 acceptance `041ba10`, Wave 2 planning `98d8bb9`, Wave 2 execution+acceptance `4bbcd7a`.

---

## 2. Evidence Reviewed

All inspection read-only; no notebook executed. Notebooks consulted only as static evidence.

### Lote 1 — Phase 8 closure and current state

| Archivo | Disponible | Propósito | Información crítica extraída | Riesgo si falta |
|---|---|---|---|---|
| `docs/08_model_comparison/phase8_acceptance.md` | Sí (committed) | Wave 1 closure | m0 reference; m1 candidate_with_warning; m2/m3/m4 rejected; no winner | Re-litigate Wave 1 |
| `docs/08_model_comparison/phase8_wave2_acceptance.md` | Sí (committed `4bbcd7a`) | Wave 2 closure | xgboost/lightgbm no_qualifying_evidence; catboost escalated; no winner; Phase 9 input | Re-litigate Wave 2 |
| `docs/08_model_comparison/phase8_wave2_master_planning_brief.md` | Sí (committed) | Wave 2 design | F2 frozen; flag rule 0.005436+4/5; slice guard; separate-env doctrine | Lose design lineage |
| `docs/08_model_comparison/phase8_wave2_operator_runbook.md` | Sí (committed) | Wave 2 procedure | Authorization-note pattern; audit procedure (reused here) | Reinvent procedure |
| `docs/08_model_comparison/prompt_codex_phase8_wave2_execution_plan.md` | Sí (committed) | Wave 2 executor prompt | Inert-prompt + fidelity-contract template (reused for Deliverable C) | Weaker prompt template |
| `outputs/validation/phase8_wave2_external_gbdt_v1_model_summary.csv` | Sí (committed) | Wave 2 numbers | xgb 0.8113477084 / lgbm 0.8062204891 / cat 0.8202943969; deltas vs M0/M1; slice_guard_triggered | No GBDT evidence base |
| `outputs/validation/phase8_wave2_external_gbdt_v1_fold_metrics.csv` | Sí (committed) | Wave 2 per-fold | per-fold AUC + deltas vs M0/M1 | No paired-delta base |
| `outputs/validation/phase8_wave2_external_gbdt_v1_slice_report.csv` | Sí (committed) | Wave 2 slices | 7 slice dims; CatBoost escalations (Year=2011 −0.045, avail_count=0 −0.065, Age_missing=1 −0.022) | Lose slice continuity |
| `outputs/validation/phase8_model_family_comparison_v1_model_summary.csv` | Sí (committed) | Wave 1 numbers | m0 0.8116502602 / m1 0.8270821070 | No anchor/M1 base |
| `outputs/validation/phase8_model_family_comparison_v1_slice_report.csv` | Sí (committed) | Wave 1 slices | m1 Age_missing=1 collapse 0.5442 vs m0 0.6917 | Lose m1 warning |
| `outputs/oof/...m0_random_forest_frozen_oof_predictions.csv` | Sí (committed) | M0 anchor OOF | reference vector; verified 0.8116502602 | Anchor impossible |
| `outputs/oof/...m1_logistic_regression_oof_predictions.csv` | Sí (committed) | M1 OOF | candidate-with-warning vector; 0.8270821070 | M1 diagnostics impossible |
| `outputs/oof/...wave2..._{xgboost,lightgbm,catboost}_oof_predictions.csv` | Sí (committed) | GBDT OOF | the diagnostic substrate; all 2781 rows, aligned | Phase 9A impossible |
| `Recapitulaciones/Fase 8/recapitulacion_integral_chat_reto_tokio_phase8_wave2_closure_phase9a_ready.md` | Sí (path corrected: under `Recapitulaciones/Fase 8/`) | Session recap | Confirms closure + Phase 9A gate | Narrative only (git suffices) |

### Lote 2 — frozen methodology and governing rules

| Archivo | Disponible | Principio aplicable | Aplicación a Phase 9A | Riesgo mitigado |
|---|---|---|---|---|
| `docs/01_project_planning/project_execution_plan_v3.md` | Sí | Phase ordering; gates | Phase 9 = error/diagnostic review before Phase 10 HPO | Phase-boundary drift |
| `docs/05_methodology/phase5_execution_decisions.md` | Sí | ROC-AUC, StratifiedKFold seed 42, positive-proba via `classes_` | Reproduce ROC-AUC; metrics from OOF; folds frozen | Protocol drift |
| `docs/05_methodology/validation_protocol_phase6.md` | Sí | OOF currency; fold-by-fold mean/std AUC; **"optimize ranking quality, not threshold accuracy"; "binary and not extremely imbalanced"** | Ranking diagnostics, not threshold tuning; mild-imbalance framing (§6) | Metric misuse |
| `docs/05_methodology/leakage_checklist_phase6.md` | Sí | Fold-safe; no test fitting; no leaderboard label | OOF read-only; no test; no LB; integrity before metrics | Leakage |
| `docs/07_feature_engineering/phase7_acceptance.md` | Sí | F2 adopted; `Age_missing=1` fragility | Slice plan tracks Age_missing=1 (n=435, 8 pos) | Lose fragile-slice focus |
| `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md` | Sí | F4 rejected (role interaction) | No role-interaction re-promotion | Re-litigate 7B |
| `docs/00_project_contract/challenge_brief.md` | Sí | Official data only; ROC-AUC; no external data; audits possible | No external data; reproducible diagnostics | Disqualification |
| `docs/00_project_contract/submission_checklist.md` | Sí | Submission gates | Phase 9A generates none | Submission drift |
| `docs/03_eda/experiment_notes.md` | Sí | Signal families; School/missingness risk | Slice dims; School diagnostic-only | Lose subgroup focus |

### Lote 3 — expanded Phase 7/7B/8 evidence (read-only integrity)

All Lote-3 OOF and report artifacts present and committed. The five candidate OOF files were integrity-verified read-only this run (§3). Phase 7/7B variant summaries, slice reports, validation reports, and the frozen-fold file (`outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, sha256[:16] `96937649526bcadb`) are all present. Notebooks `08b`/`08c` reviewed statically in the prior Wave 2 audit; not executed. **No Lote-3 file is missing → no future-execution blocker flagged at planning time.**

`/plugin list ecc@ecc` is a CLI user command not invocable from agent context; ECC availability verified by direct disk inspection (§16). Full PDFs not re-parsed; references consumed via committed Phase 4B summaries and `docs/04_research/research_notes_*` (§5).

---

## 3. Numerical Results and OOF Integrity Validation

Read-only verification this planning run (pure-stdlib rank AUC recomputation from each persisted OOF; no training).

| Evidence item | Expected | Recomputed / Observed | Status | Impact on Phase 9A |
|---|---|---|---|---|
| M0 OOF ROC-AUC | 0.8116502602456482 | 0.8116502602… (match <1e-9) | Confirmed | Anchor for paired deltas |
| M1 OOF ROC-AUC | 0.8270821069632867 | 0.8270821070… (match <1e-9) | Confirmed | Strongest global; demanding comparator |
| XGBoost OOF ROC-AUC | 0.8113477084 | 0.8113477084 (match <1e-9) | Confirmed | no_qualifying_evidence (Wave 2) |
| LightGBM OOF ROC-AUC | 0.8062204891 | 0.8062204891 (match <1e-9) | Confirmed | no_qualifying_evidence (Wave 2) |
| CatBoost OOF ROC-AUC | 0.8202943969 | 0.8202943969 (match <1e-9) | Confirmed | escalated / candidate-with-warning |
| OOF schema (all 5) | `Id,fold,y_true,y_pred_proba` | exact match | Confirmed | Schema gate passes |
| OOF row count (all 5) | 2781 | 2781 | Confirmed | Row-count gate passes |
| Unique (Id) per file | 2781 | 2781 (no duplicate Id/fold) | Confirmed | Duplicate gate passes |
| Probability range | [0,1] | all in [0,1] | Confirmed | Range gate passes |
| NaN / infinite | none | none | Confirmed | Finite gate passes |
| Fold set | {0,1,2,3,4} | {0,1,2,3,4} | Confirmed | Fold gate passes |
| Id→fold mismatch vs M0 | 0 | 0 (all 5) | Confirmed | **Paired diagnostics valid** |
| Id→y_true mismatch vs M0 | 0 | 0 (all 5) | Confirmed | Shared label substrate |
| **Positive rate** | n/a | **0.6483 (1803/2781) — majority-positive** | Confirmed | **Governs imbalance framing (§6)** |
| Frozen folds sha256[:16] | `96937649526bcadb` | `96937649526bcadb` | Confirmed | Same folds throughout |

No discrepancy. Every numerical claim in the source prompt is confirmed against repository evidence. The integrity result is strong enough that Phase 9A's first execution gate (artifact integrity) is *pre-validated* at planning time — but the runbook still requires Codex to re-verify it independently before any metric is computed.

---

## 4. Frozen Decisions Preserved

| # | Frozen decision | Phase 9A consequence |
|---|---|---|
| 1 | Primary metric: ROC-AUC on positive-class probabilities (`Drafted=1`) | ROC-AUC stays the official primary; all else is diagnostic |
| 2 | Positive-class probability via verified `estimator.classes_` | Not applicable in Phase 9A (no estimator touched); OOF `y_pred_proba` is already positive-class proba |
| 3 | Official data only; no external data; no manual labels/edits | No external data; no manual prediction edits |
| 4 | Frozen folds active (sha `96937649526bcadb`) | OOF fold column is authoritative; never recomputed |
| 5 | OOF ROC-AUC is the primary local comparison currency | Diagnostics computed from persisted OOF only |
| 6 | F2 is the accepted feature set; F4 rejected | No feature work; no role-interaction re-promotion |
| 7 | m0 = reference anchor | Preserved as anchor; never re-promoted/retrained |
| 8 | m1 = strongest global OOF, candidate-with-warning (not winner, not submission-ready) | Diagnosed, never crowned |
| 9 | catboost = escalated / candidate-with-warning | Diagnosed as candidate-with-warning, never cleanly promoted |
| 10 | xgboost, lightgbm = no_qualifying_evidence | Diagnostic-only; not reinterpreted as strong without new accepted evidence |
| 11 | School excluded from features | Diagnostic-only slice; never a feature |
| 12 | Candidate logs separate; `logs/experiment_log.csv` protected | Phase 9A writes candidate-log rows under `outputs/`; main log read-before/assert-after |
| 13 | Public LB never a criterion | No LB anywhere |
| 14 | No HPO / no submissions / no ensembles | All locked; backlog items only (§15) |
| 15 | Phase 10 / 11 locked | §20; dependency notes only |

Honest caveat carried forward: the 0.005436 flag threshold is RF-seed-noise-derived; in Phase 9A it appears only as historical context for interpreting Wave 1/2 deltas, never as a Phase 9A adoption rule (Phase 9A adopts nothing).

---

## 5. Scientific and Methodological Evidence Transfer

Sources are those the project's Phase 4B audit marks **Reviewed** (`docs/04_research/pdf_review_audit.md`) plus the project research notes (`research_notes_validation.md`, `research_notes_leakage.md`, `research_notes_reproducibility.md`, `research_notes_tabular_models.md`, `research_notes_hpo.md` read this run). Compact summaries sufficed; **no full PDF re-parsed.** References contribute methodology only — **never external data**.

| Source / Reference | Methodological principle | Phase 9A practical decision | Diagnostic artifact affected | Risk mitigated | Limitation / caution |
|---|---|---|---|---|---|
| `research_notes_validation.md` (project) | "Optimize ranking quality: probability ordering for `Drafted=1`, not threshold accuracy"; "binary and not extremely imbalanced"; report fold-by-fold mean/std AUC | ROC-AUC primary; PR/top-k strictly diagnostic; per-fold AUC + std reported | Global metrics; fold diagnostics | Threshold-accuracy misuse | Mild imbalance ≠ rare-event; frame top-k as ranking-head characterization |
| ISLP | ROC vs PR trade-offs; selection variance must clear noise | Report both ROC-AUC and PR-AUC; flag ROC↔PR conclusion conflicts as warnings | Global metrics; warning synthesis | Reading noise as signal | Single OOF realization; no per-family noise model |
| The Kaggle Book (2nd ed., 2025) | Trust frozen local CV; LB is noise; pre-register; top-k/lift are competition-utility lenses | Pre-registered diagnostic set; LB prohibited; top-decile/quintile capture + lift reported | Top-k/quantile diagnostics | Leaderboard chasing; adaptive overfitting | Utility framing is descriptive, not a selection rule |
| The Kaggle Workbook (2023) | One-factor-at-a-time on identical folds; paired comparison | Paired per-fold deltas vs M0 and vs M1 on the shared fold substrate | Fold paired diagnostics | Confounded attribution | Paired deltas describe, do not select |
| Kuhn & Johnson, *Feature Engineering and Selection* | Subgroup performance can diverge from global; calibration is a diagnostic lens | Slice-level AUC with n≥50; diagnostic calibration curve + Brier (no recalibration) | Slice + calibration diagnostics | Hidden subgroup failure | Small-n slices high variance; calibration is diagnostic only |
| Cawley & Talbot, *On Over-fitting in Model Selection* | Repeated selection on the same CV biases estimates; selection is part of training | Phase 9A selects nothing; multiple diagnostics ⇒ multiplicity warnings, not re-ranking | Warning synthesis; backlog | Selection bias disguised as diagnosis | Many metrics increase cherry-pick risk → explicit multiplicity caution |
| Leakage & reproducibility-crisis papers (`research_notes_leakage.md`) | Pipeline-wide leakage taxonomy; integrity precedes interpretation | OOF integrity gate **before** any metric; no test fitting; no LB label | OOF inventory/integrity | All leakage layers | Read-only ≠ leakage-proof if alignment unchecked → mandatory alignment checks |
| `research_notes_hpo.md` (project) + Optuna | HPO blocked until 7 conditions; HPO ≠ diagnosis | Any tuning idea → backlog as future-locked (Phase 10) | Hypothesis backlog | HPO-by-stealth | Diagnostics may *suggest* HPO but cannot authorize it |
| `research_notes_reproducibility.md` (project) + Hands-On ML | Fixed seeds; reproducible from repo root; recompute and cross-check against accepted reports | `PROJECT_SEED`; reproduce accepted ROC-AUC; environment + hash recorded | Reproduction report; manifest | Irreproducibility hides errors | Reproduction tolerance must be explicit (≤1e-9) |
| Competition-overfitting / holdout-reuse papers | Adaptive test-set reuse inflates scores | Zero submissions; LB untouched; private LB never inferred | Non-actions | Adaptive overfitting | — |
| GCI course materials (model evaluation, EDA, workflow) | Clean, deterministic, auditable; ranking-oriented evaluation | Notebook-as-report standard (§14); positive-rate reporting global/fold/slice | Notebook; imbalance reporting | Audit failure | — |

Explicit separation maintained throughout: **(1) project evidence** (accepted reports/OOF/fold/slice), **(2) scientific/methodological evidence** (the table above), **(3) inference** (my planning judgment), **(4) Not confirmed yet** (nothing in this run — all referenced artifacts exist).

---

## 6. Class Imbalance and Ranking Utility Framing

**Verified fact:** positive rate = **0.6483** (1803 `Drafted=1` / 2781). The positive class is the **majority**; imbalance is **mild and majority-positive**, consistent with the project note "binary and not extremely imbalanced."

Design consequences (mandatory in any future execution):

- **ROC-AUC remains primary and sufficient as the official metric.** It measures ranking separation over all positive–negative pairs and is base-rate invariant.
- **PR-AUC / Average Precision are diagnostic, with a high baseline (≈0.6483).** Because positives dominate, a naive classifier already achieves high precision; PR-AUC here characterizes ranking behavior in the *precision-relevant region*, not rare-class retrieval. The plan requires reporting the PR-AUC baseline alongside the values so they are never over-read.
- **Top-k / precision@k / lift@k / top-decile & top-quintile capture** characterize the **confident head** of the ranking ("which players the model is most sure are drafted"). With a 0.648 base rate, lift ceilings are compressed (max lift ≈ 1/0.648 ≈ 1.54); the plan requires reporting the random-baseline capture/lift so enrichment is interpreted correctly.
- **The negative class (35.2%) is the harder retrieval target.** The plan requires Codex to additionally report negative-oriented framing (e.g., bottom-decile capture of negatives / how cleanly each model isolates the not-drafted minority), because that is where ranking utility is most discriminating here.
- **Positive rate must be reported at global, fold, and slice level** so every top-k/PR number is read against its local base rate. Fold positive rates are expected near 0.648 by stratification; slice positive rates vary widely (e.g., `Age_missing=1` had only 8 positives in 435 → positive rate ≈ 0.018, an inverted, fragile regime).
- **ROC-vs-(PR/top-k) conclusion conflicts are warnings, never re-ranking triggers.** No imbalance metric may declare a winner or a submission-ready model.

This framing is the single most important way Phase 9A differs from a naive "add more metrics" pass: it ties every complementary metric to the verified 0.648 base rate and forbids treating any of them as a selection rule.

---

## 7. Phase 9A Objective, Scope and Diagnostic Questions

**Objective.** Using only persisted OOF predictions, determine whether the Phase 8 candidates are robust, useful, reliable *rankers* under local OOF analysis — before any HPO, final selection, or submission — and convert that understanding into a classified backlog of future questions. Phase 9A **adopts nothing and crowns nobody.**

**In scope:** OOF integrity verification; ROC-AUC reproduction; global complementary metrics (PR-AUC, Brier-diagnostic); top-k/quantile/lift/enrichment + cumulative gains; fold-level paired deltas vs M0 and M1; slice-level AUC (n≥50) + slice positive rates; score-distribution diagnostics; M1↔CatBoost rank-correlation/disagreement; diagnostic calibration (no recalibration); warning synthesis; improvement-hypothesis backlog.

**Out of scope (locked):** training/retraining, HPO, model-family re-comparison, ensembling/blending/stacking, calibration *fitting*, threshold tuning for submission, submissions, leaderboard use, external data, School-as-feature, winner/submission-ready declarations, Phase 10/11.

**Diagnostic questions (the deliverable answers *characterize*, never *select*):**
1. Does M1 retain superiority beyond global ROC-AUC — in top-k ranking utility and fold stability?
2. Does CatBoost offer *complementary* signal vs M1, or only local gains with warnings?
3. Do candidates rank positives well at the confident head (top decile/quintile)?
4. What happens on critical slices — Age_missing, Year, measurement completeness, role groups?
5. Are any score distributions degenerate, over-compressed, or unstable?
6. Are fold-level differences consistent enough to be trusted?
7. Which candidates merit carrying into a future decision phase, and which should be observed or dropped?
8. Which diagnostics must be mandatory *before* any Phase 10 HPO or Phase 11 submission?
9. What M1↔CatBoost disagreement suggests future hypotheses — *without* authorizing an ensemble?
10. Where do warnings suggest the next step is *better auditing*, not optimization?

---

## 8. Metrics and Diagnostics Catalogue

Primary frozen metric: **ROC-AUC** on positive-class probabilities. Everything below is **diagnostic** and may not select a model.

| Metric / diagnostic | What it measures | Value to 9A | Methodological support | Over-interpretation risk → control | OOF labels? | Probs? | Fold-level? | Scope | Min condition | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| ROC-AUC (reproduce) | Pairwise ranking separation | Anchor + reproduction gate | validation note; phase5 | Treated as confirmation, not new ranking | Yes | Yes | Yes | global+slice | reproduces accepted ±1e-9 | **Mandatory** |
| PR-AUC / Average Precision | Precision–recall ranking, base-rate sensitive | Ranking at precision-relevant head | ISLP; Kaggle Book | Report baseline 0.6483 alongside | Yes | Yes | Yes | global(+slice if n≥50) | report PR baseline | **Mandatory** |
| Positive rate (global/fold/slice) | Local base rate | Context for every top-k/PR number | §6; validation note | Always shown beside the metric | Yes | No | Yes | all | — | **Mandatory** |
| Precision@k / Recall@k | Quality/coverage in top-k | Confident-head utility | Kaggle Book | Report random baseline | Yes | Yes | optional | global | k grid pre-registered | **Mandatory** |
| Lift@k / Enrichment by quantile | Top-k vs random enrichment | Competition-utility lens | Kaggle Book/Workbook | Report lift ceiling (≈1.54) | Yes | Yes | optional | global | quantile grid pre-registered | **Mandatory** |
| Top-decile / top-quintile capture | Positives captured in head | Ranking-head capture | Kaggle Book | Compare to base-rate capture | Yes | Yes | optional | global | — | **Mandatory** |
| Cumulative gains | Capture vs population fraction | Visual/tabular ranking curve | Kaggle Book | Tabular first; plot optional | Yes | Yes | no | global | — | Mandatory (table), Optional (plot) |
| Negative-class retrieval (bottom-k) | How cleanly minority negatives isolate | The harder retrieval here | §6 inference | Diagnostic only | Yes | Yes | optional | global | — | **Mandatory** |
| Fold paired deltas vs M0 / vs M1 | Per-fold model−comparator gap; same-sign count | Stability/consistency | Kaggle Workbook | Same-sign reported with magnitude | Yes | Yes | Yes | fold | aligned folds (verified) | **Mandatory** |
| Slice ROC-AUC (n≥50) | Subgroup ranking | Subgroup fragility | Kuhn & Johnson | n<50 flagged non-evaluable | Yes | Yes | no | slice | n≥50 | **Mandatory** |
| Slice top-k/lift | Subgroup head utility | Deep subgroup view | Kaggle Book | Only where n sufficient | Yes | Yes | no | slice | n≥ (pre-registered, e.g. 100) | Optional |
| Score distribution (quantiles, separation by y_true) | Shape/compression/degeneracy | Detect pathological scores | Hands-On ML | Describe, don't rank | No | Yes | optional | global+by-class | — | **Mandatory** |
| Rank correlation (Spearman/Kendall) M1↔CatBoost (and vs M0) | Ranking agreement | Complementarity signal | Kaggle Book | Diagnostic only; no ensemble | Yes(order) | Yes | no | global | — | **Mandatory** |
| Disagreement analysis (M1-high/Cat-low and inverse) | Where rankings diverge | Hypothesis seeds | Kaggle Book | No blending implied | Yes | Yes | no | global+slice | — | **Mandatory** |
| Brier score (diagnostic) | Probability accuracy | Calibration context | Kuhn & Johnson | Labeled "diagnostic, not official" | Yes | Yes | optional | global | — | Optional (diagnostic) |
| Calibration curve (diagnostic) | Reliability of probs | Calibration context | Kuhn & Johnson | **No recalibration**; describe only | Yes | Yes | no | global | bins pre-registered | Optional (diagnostic) |
| Bootstrap CIs | Sampling uncertainty of AUC/PR | Uncertainty bands | ISLP | Not a sole criterion; seed fixed | Yes | Yes | optional | global | seed + n_boot pre-registered | Optional |

**Prohibited in Phase 9A:** leaderboard score, public/private LB inference, threshold optimization for submission, manual prediction edits, HPO objective, model re-ranking using test data, submission simulation, external-data validation.

---

## 9. Proposed Phase 9A Block Architecture

The suggested 14-block skeleton was adopted with light compaction: calibration and score-distribution diagnostics merge into one block (both are distributional, read-only, and share inputs), and reference review folds into Block 0/1 rather than standing as an execution block (it is a planning activity, done in §5). Net: 11 blocks (0–10), each mandatory unless noted.

| Block | Nombre | Objetivo | Evidencia necesaria | Referencia metodológica | Diagnósticos cubiertos | Riesgos mitigados | Salida esperada | Condición de avance |
|---|---|---|---|---|---|---|---|---|
| 0 | Repo/Git/Phase-Gate & Environment Verification | Start from accepted baseline, read-only | HEAD `4bbcd7a`; clean tree; folds sha; pinned env | reproducibility note | none (verification) | Wrong/dirty baseline | Verification block | All PASS or stop |
| 1 | OOF Artifact Inventory & Integrity | Prove every OOF is valid before any metric | 5 OOF files; fold file | leakage note | schema, rows, range, NaN, duplicates, **Id/fold/y_true alignment**, positive rate | Metrics on broken data | Integrity report (pass/fail per file) | All files pass or block |
| 2 | Accepted ROC-AUC Reproduction | Re-derive accepted scores from OOF | OOF + accepted summaries | reproducibility; validation | ROC-AUC per model vs accepted (±1e-9) | Silent metric drift | Reproduction report | All within tolerance or stop |
| 3 | Global Ranking & Imbalance Metrics | Characterize global behavior beyond ROC | OOF | ISLP; Kaggle Book; §6 | ROC-AUC, PR-AUC(+baseline), Brier-diag, positive rate, negative-retrieval | Base-rate misread | Global metrics table | Computed + baselines shown |
| 4 | Top-K / Quantile / Lift / Enrichment | Confident-head utility | OOF | Kaggle Book/Workbook | precision@k, recall@k, lift@k, top-decile/quintile capture, cumulative gains, enrichment | Lift over-read | Top-k/quantile tables | Random baselines reported |
| 5 | Fold-Level Stability & Paired Comparison | Consistency vs M0 and M1 | OOF (aligned folds) | Kaggle Workbook | fold AUC/PR, paired deltas vs M0 & M1, same-sign | Single-number illusion | Fold paired table | Folds aligned (verified §3) |
| 6 | Slice-Level Risk Diagnostics | Subgroup fragility | OOF + slice dims | Kuhn & Johnson | slice AUC (n≥50) + slice positive rate; optional slice top-k | Cherry-picking; small-n | Slice diagnostic table | Min-n + multiplicity caution applied |
| 7 | Score Distribution & Calibration (diagnostic) | Detect degenerate/uncalibrated scores | OOF | Hands-On ML; Kuhn & Johnson | quantiles, separation by y_true, compression flags, Brier, calibration curve | False precision; recalibration temptation | Distribution/calibration tables | No recalibration performed |
| 8 | Candidate Complementarity & Disagreement | M1↔CatBoost (and M0) divergence | OOF | Kaggle Book | rank correlation; high/low disagreement cases | Implicit ensemble | Disagreement table | Diagnostic-only; no blending |
| 9 | Warning Synthesis & Diagnostic Verdict | Consolidate conflicts & fragilities | Blocks 1–8 | Cawley & Talbot | global-vs-slice, ROC-vs-top-k, fold instability, small-n, multiplicity | Hidden warnings | Warning report + per-candidate diagnostic verdict (carry/observe/drop-candidate, no winner) | Every candidate classified |
| 10 | Improvement-Hypothesis Backlog & Closure | Future questions, phase-gated | Blocks 1–9 + references | hpo note; Cawley & Talbot | backlog (§15), artifact manifest, candidate log, acceptance draft | Phase-gate jumping; selection bias | Backlog + manifest + acceptance template | Backlog classified; locks restated |

---

## 10. Candidate Model Diagnostic Scope

| Candidate | Phase 8 status | Phase 9A role | Justification |
|---|---|---|---|
| `m0_random_forest_frozen` | reference_reproduced | **Mandatory — anchor** | Reference for all paired deltas; never re-promoted/retrained |
| `m1_logistic_regression` | candidate_with_warning (strongest global OOF) | **Mandatory — primary diagnostic focus** | Most ranking utility to characterize; Age_missing=1 warning to probe; not a winner |
| `catboost` | escalated / candidate_with_warning | **Mandatory — primary diagnostic focus** | Beats M0 globally but slice-escalated and below M1; complementarity vs M1 is a key question |
| `xgboost` | no_qualifying_evidence | **Diagnostic-only (optional depth)** | Included for completeness/disagreement context; **not** reinterpreted as strong; below M0 |
| `lightgbm` | no_qualifying_evidence | **Diagnostic-only (optional depth)** | Same; weakest global; full slice depth optional |

Separation: **mandatory** = m0, m1, catboost; **diagnostic-only / optional** = xgboost, lightgbm; **excluded** = none (all five are cheap to analyze read-only); **carried-with-warnings** = m1, catboost; **not eligible for promotion in 9A** = all (Phase 9A promotes nothing). XGBoost/LightGBM may be dropped from *deep* slice/top-k passes if they add no diagnostic value, with justification recorded — but they remain in the global table and disagreement context.

---

## 11. Slice Diagnostic Plan

Reuse the seven established Phase 7/8 slice dimensions (already in the committed slice reports). Minimum slice size **n ≥ 50** (initial threshold; stricter where noted). School stays a **diagnostic-only** dimension, never a feature.

| Slice | Include | Phase 7/8 motivation | Methodological caution | Min n | Metric | Multiplicity / cherry-pick control |
|---|---|---|---|---|---|---|
| `Age_missing` | **Yes** | Phase 7 fragile slice; m1 collapse (0.5442 vs m0 0.6917); CatBoost −0.0217 | Only 8 positives at `=1` (pos rate ≈0.018) | report all, **flag n_pos<20 as fragile** | slice AUC + positive rate | report alongside global; never decisive alone |
| `Year` | **Yes** | CatBoost escalations (2011 −0.045, 2009 −0.025) | many levels → multiplicity | 50 | slice AUC + positive rate | Bonferroni-style caution noted; report all levels |
| `available_measurement_count` | **Yes** | CatBoost escalation (0 −0.065, 4 −0.025) | ordinal; small extreme bins | 50 | slice AUC + positive rate | report full ladder |
| `measurement_completeness_group` | **Yes** | mirrors avail_count; CatBoost (none −0.065) | diagnostic-only group | 50 | slice AUC + positive rate | flag as diagnostic mirror |
| `Player_Type` | **Yes** | role-aware signal (Phase 3/7) | few levels | 50 | slice AUC + positive rate | report all |
| `Position_Type` | **Yes** | role-aware; kicking_specialist instability seen | rare roles | 50 | slice AUC + positive rate | rare levels flagged |
| `Position` | **Optional** | finest role granularity | high cardinality → many tiny slices | **100** (stricter) | slice AUC | only levels with n≥100; else aggregate |
| `frequent_vs_rare_school_group` | **Yes (diagnostic-only)** | School-risk monitor | **never a feature** | 50 | slice AUC + positive rate | explicit "diagnostic-only, not a feature" note |

For every slice: report n, n_positive, positive_rate, model AUC, delta vs M0, delta vs M1, and a guard flag (>0.02 AUC drop vs M0 on n≥50 ⇒ flagged warning). Cherry-pick control: report **all** levels meeting min-n (no selective reporting), state the number of comparisons, and treat any single large slice movement as a hypothesis, not a conclusion.

---

## 12. Notebook / Script Architecture Blueprint

### 12.1 Decision: one integral, heavily-documented notebook

**Decision: a single notebook** `notebooks/09a_auc_ranking_diagnostics.ipynb` (`experiment_id = phase9a_auc_ranking_diagnostics_v1`). Justification: every diagnostic reads from the *same* five OOF files on the *same* frozen fold substrate; the work is entirely read-only (no env mutation, no training, no install) so there is no isolation boundary to enforce by splitting; a single linear artifact maximizes reproducibility, audit simplicity, and Codex fidelity; the integrity gate (Block 1) is a shared precondition for all later blocks and belongs in one place. Splitting would duplicate the OOF-loading/integrity foundation across files without adding a control gate. (If the score-distribution/disagreement plots make the notebook heavy, plotting may be delegated to an optional appendix section — but not a separate notebook.)

### 12.2 Mandatory notebook hygiene

Notebook-first, reproducible, audit-ready. It must read like an executable technical report, not a code dump. Required: clear title; exact phase; objective; explicit scope ("what it does / does NOT do"); clean imports; centralized paths; `PROJECT_SEED` (even though nothing is trained — for any bootstrap/sampling); explicit `experiment_id`/`run_id`; data loaded only from official paths + accepted OOF; data/artifact contract checks before metrics; frozen-fold load if used; ROC-AUC recomputed from OOF; **no test fitting, no training, no HPO, no submission**; versioned artifact names; no overwrite without `experiment_id`/`run_id`; `logs/experiment_log.csv` untouched; final executive-summary cell (confirmed / uncertain / blocked / for-Opus-review).

### 12.3 Per-cell documentation standard (mandatory)

Each important code block is preceded by a Markdown cell:

```markdown
## <N>. <Analytical title>
**Objetivo.** What is computed/verified.
**Inputs.** Files / DataFrames / columns used.
**Método.** Brief technical logic.
**Output esperado.** Table / validation / plot / artifact produced.
**Riesgo controlado.** Which methodological risk it controls (leakage, OOF misalignment, interpretive overfitting, selection bias, metric misuse, …).
```

Each code cell opens with a numbered comment (e.g. `# 4.2 Validate OOF schema and row counts`). Each results cell is followed by a Markdown **Interpretation** cell: *Resultado principal* / *Lectura metodológica* / *Riesgo o warning* / *Decisión diagnóstica (pass / warning / blocks the phase)*. Style: professional, analytical, audit-ready, no over-claiming, **no winner language, no unjustified causal language.**

### 12.4 Cell-by-cell coverage map

| Sección | Título | Propósito | Inputs | Output | Validación / Riesgo controlado |
|---|---|---|---|---|---|
| 0 | Title, scope & explicit non-actions | Declare phase, experiment_id, locks | — | markdown | scope creep |
| 1 | Git / repo / path / environment checks | Read-only baseline | git, env | env block + HEAD record | wrong baseline |
| 2 | Artifact inventory | List + existence of 5 OOF + fold file | outputs/ | inventory table | missing artifact ⇒ block |
| 3 | OOF schema validation | `Id,fold,y_true,y_pred_proba` per file | OOF | per-file schema verdict | schema drift |
| 4 | OOF row-count validation | 2781 per file | OOF | row-count verdict | truncation |
| 5 | Id/fold/y_true alignment across all 5 | shared substrate vs M0 | OOF | alignment matrix (0 mismatch expected) | misalignment ⇒ block |
| 6 | Probability range + missing checks | [0,1], no NaN/inf | OOF | range/NaN verdict | invalid probs ⇒ block |
| 7 | Duplicate row checks | unique (Id,fold) | OOF | duplicate verdict | duplicates ⇒ block |
| 8 | Positive-rate reporting | global + fold + (slice later) | OOF | base-rate table (≈0.6483) | base-rate context |
| 9 | Accepted ROC-AUC recomputation | reproduce accepted scores | OOF + summaries | reproduction table (±1e-9) | metric drift ⇒ stop |
| 10 | Global metrics | ROC-AUC, PR-AUC(+baseline), Brier-diag, neg-retrieval | OOF | global table | base-rate misread |
| 11 | Top-k / quantile / lift / enrichment / gains | confident-head utility | OOF | top-k tables (+random baselines) | lift over-read |
| 12 | Fold-level paired diagnostics | fold AUC/PR, deltas vs M0 & M1, same-sign | OOF | fold paired table | single-number illusion |
| 13 | Slice diagnostics | 7 established Phase 7/8 slice dimensions + `Position` as optional fine-grained diagnostic slice (n≥50; `Position` n≥100), slice positive rate | OOF + slice dims | slice table + warning flags | cherry-picking; small-n |
| 14 | Score distribution & calibration (diagnostic) | quantiles, separation, Brier, calibration curve | OOF | distribution/calibration tables | recalibration temptation (forbidden) |
| 15 | M1↔CatBoost disagreement | rank corr; divergence cases | OOF | disagreement table | implicit ensemble |
| 16 | Warning synthesis | consolidate conflicts | cells 10–15 | warning report | hidden warnings |
| 17 | Per-candidate diagnostic verdict | carry / observe / drop-candidate (no winner) | cells 10–16 | verdict table | winner declaration (forbidden) |
| 18 | Improvement-hypothesis seed | evidence-based future ideas | cells 10–17 | backlog seed (classified) | phase-gate jumping |
| 19 | Artifact writing (versioned) + manifest + candidate log | persist outputs with guards | results | files + manifest + log row | overwrite; main-log touch |
| 20 | Executive conclusion | confirmed/uncertain/blocked/for-Opus | all | markdown + Phase 10/11 lock restated | over-claim |

### 12.5 Visualizations

Plots are **optional**; tables are the audit-of-record. If included (score histograms by model, cumulative-gains/lift/top-k-capture curves, fold bar charts, slice degradation table/heatmap, M1-vs-CatBoost rank scatter), they must be reproducible and saved only if they add diagnostic value. If excluded, the notebook must state that the tables are self-sufficient. No plot may imply a winner.

### 12.6 Prohibitions (notebook)

No training/retraining; no HPO; no submissions; no leaderboard; no external data; no ensembles/blending/stacking; no calibration *fitting*; no threshold tuning for submission; no winner / submission-ready declaration.

---

## 13. Artifact Architecture Plan

Namespace: `phase9a_auc_ranking_diagnostics_v1`. Names are proposals (the director may amend); all writes are guarded (fail-if-exists; no overwrite without a new `run_id`).

| Artifact family | Proposed file(s) | Purpose | Required inputs | Required checks | Produced by | Must exist before closure? | Notes |
|---|---|---|---|---|---|---|---|
| 1. OOF inventory & integrity | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_oof_integrity_report.csv` | Per-file schema/rows/range/NaN/dupes/alignment/positive-rate | 5 OOF + fold file | all integrity gates pass | notebook cells 2–8 | **Yes** | first gate |
| 2. ROC-AUC reproduction | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_auc_reproduction.csv` | Accepted-vs-recomputed AUC (±1e-9) | OOF + accepted summaries | within tolerance | cell 9 | **Yes** | reproduction gate |
| 3. Global metrics | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_global_metrics.csv` | ROC/PR/Brier/neg-retrieval + baselines | OOF | base rates attached | cell 10 | **Yes** | — |
| 4. Top-k/quantile | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_topk_quantile.csv` | precision@k/recall@k/lift@k/capture/gains/enrichment | OOF | random baselines attached | cell 11 | **Yes** | k/quantile grids recorded |
| 5. Fold paired | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_fold_paired.csv` | fold AUC/PR + deltas vs M0/M1 + same-sign | OOF | folds aligned | cell 12 | **Yes** | — |
| 6. Slice diagnostics | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_slice_report.csv` | slice AUC + positive rate + warning flags (n≥50) | OOF + slice dims | min-n enforced | cell 13 | **Yes** | mirrors Phase 8 schema |
| 7. Score distribution | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_score_distribution.csv` | quantiles/separation/compression + Brier + calibration bins | OOF | no recalibration | cell 14 | **Yes** | calibration diagnostic-only |
| 8. Disagreement | `outputs/validation/phase9a_auc_ranking_diagnostics_v1_disagreement.csv` | rank corr + divergence cases (M1↔CatBoost, vs M0) | OOF | diagnostic-only | cell 15 | **Yes** | no blending |
| 9. Warning report | `outputs/reports/phase9a_auc_ranking_diagnostics_v1_validation_report.md` | Human-readable synthesis + per-candidate verdict | cells 1–17 | every candidate classified | cells 16–17,20 | **Yes** | no winner |
| 10. Hypothesis backlog | `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md` | Classified future hypotheses | cells 10–18 + refs | each item phase-gated | cell 18 + Opus review | **Yes** | future-locked items flagged |

The final `phase9a_improvement_backlog.md` is produced only by the post-Codex Opus strategic review, not by Codex. Codex may produce only a technical backlog seed inside the validation report or candidate log. Codex must not create the final improvement backlog document.
| 11. Artifact manifest | `outputs/reports/phase9a_auc_ranking_diagnostics_v1_artifact_manifest.csv` | path + sha256 + rows per artifact | all artifacts | hashes non-empty | cell 19 | **Yes** | self-exclusion ok |
| 12. Candidate log | `outputs/reports/phase9a_auc_ranking_diagnostics_v1_experiment_log_candidate.csv` | v2-schema diagnostic rows; main log untouched | results | main log byte-identical | cell 19 | **Yes** | separate from main log |
| 13. Validation report | (= family 9) | — | — | — | — | — | combined with warning report |
| 14. Acceptance draft | `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md` | Closure decision template (director-signed) | all artifacts + audit | independent audit passed | post-run (Opus review → director) | **Yes (at closure)** | acceptance template provided in runbook |

Families 9 and 13 are intentionally combined (one human-readable report). Optional plot files (`outputs/figures/phase9a_*`) may be added if §12.5 plots are produced.

---

## 14. Validation, Acceptance and Stop Rules

### 14.1 Acceptance of the planning package (level A)

| Criterion | Condition | Evidence | If it fails |
|---|---|---|---|
| Repository state verified | §1 PASS at `4bbcd7a` | §1 | re-verify; stop if HEAD/forbidden differ |
| Phase 8 closure verified | Wave 1 + Wave 2 committed | §1/§2 | block |
| Phase 9A not previously executed | no `phase9a_*` artifacts | §1 | investigate collision |
| OOF integrity pre-validated | 5 files pass; 0 misalignment | §3 | mark Not confirmed yet; block |
| Metrics catalogue + imbalance framing | §6/§8 complete | §6/§8 | amend |
| References transfer | §5 table | §5 | targeted review |
| Block architecture + notebook blueprint | §9/§12 | §9/§12 | amend |
| Artifact plan covers all 14 families | §13 | §13 | amend |
| Backlog design + Opus/Codex/Opus split | §15/§17 | §15/§17 | amend |
| ECC plan | §16 | §16 | amend |
| Locks restated (no HPO/submissions/winner/Phase 10/11) | §4/§19/§20 | this brief | absolute |

### 14.2 Acceptance of a future authorized execution (level B)

| Criterion | Condition | Evidence | If it fails |
|---|---|---|---|
| OOF loaded read-only, accepted files only | no other data source | report | stop |
| Row alignment by Id/fold/target | 0 mismatch across 5 files | integrity report | **block — do not compute metrics** |
| OOF = train rows only; probs in [0,1]; no NaN/inf; no dupes | all gates pass | integrity report | block |
| Accepted ROC-AUC reproduced | within ±1e-9 of accepted summaries | reproduction report | stop (drift) |
| M0 anchor / M1 / CatBoost roles preserved | no re-promotion | verdict table | stop |
| xgboost/lightgbm kept no_qualifying_evidence | not reinterpreted promotionally | verdict table | stop |
| No winner / no submission / no training / no HPO | absent | git + report | stop |
| Main log untouched; artifacts versioned + guarded | byte-identical; no overwrite | manifest + checksum | stop |
| Independent recomputation matches | ≤1e-9 per metric | audit | block acceptance |
| Phase 10/11 locked; backlog phase-gated | statements present | report/backlog | block acceptance |

### 14.3 Edge-case stop/branch rules (future execution)

| Situation | Action |
|---|---|
| OOF AUC ≠ accepted report | **Stop** — reproduction gate failed; do not interpret downstream |
| Misaligned rows / missing OOF / probs out of range / NaN/inf / duplicates | **Stop** — integrity gate failed; block before metrics |
| Complementary metric favors a different model than ROC-AUC | Report as **warning** (ROC↔PR/top-k conflict); never re-rank |
| Model better at top-k but fails critical slices | Report as **warning**; carry-with-warning at most |
| Model better globally but degrades fold/slice stability | Report as **warning**; not a promotion |
| CatBoost shows complementarity with M1 | Record as **future hypothesis (ensemble-locked)**; no implementation |
| M1 dominates globally but persistent warnings | Keep candidate-with-warning; do **not** crown |
| XGBoost/LightGBM show partial good diagnostic | Record as observation; **not** re-promotion without new accepted evidence |
| Results suggest ensemble/blending | **Backlog only, future-locked**; no implementation |
| Submission temptation detected | **Stop/refuse**; submissions are Phase 11-locked |
| HEAD ≠ expected | **Stop** before any compute |
| Artifact name could overwrite | **Stop**; require new `run_id` |

---

## 15. Diagnostic-Driven Improvement Hypothesis Backlog (Design)

Phase 9A produces a **non-executive** backlog. Each item derives only from accepted artifacts / OOF / fold & slice reports / Phase 7-8 evidence / repository references / (later) Phase 9A diagnostics. **Nothing is implemented.** Each item is classified into exactly one category and given a priority.

Categories: **(1)** Safe diagnostic recommendation for Phase 9A execution; **(2)** Hypothesis for Phase 9B/later diagnostic phase; **(3)** Hypothesis for Phase 10 HPO (locked); **(4)** Hypothesis for future ensemble/blending (locked); **(5)** Hypothesis for Phase 11 submission strategy (locked); **(6)** Deferred — insufficient evidence; **(7)** Prohibited under current rules.
Priority: High / Medium / Low / Deferred / Prohibited. Expected AUC/ranking rationale is **qualitative** unless backed by accepted evidence (no invented numeric gains).

Seed backlog (illustrative; the executed notebook + Opus review will finalize):

| ID | Hypothesis | Evidence motivating it | Methodological support | Expected AUC/ranking rationale | Required future phase | Required artifacts | Main risk | Gate before execution | Priority | Category |
|---|---|---|---|---|---|---|---|---|---|---|
| H1 | Quantify M1↔CatBoost ranking complementarity before any combination idea | CatBoost beats M0 globally (+0.0086) but trails M1; different families | Kaggle Book (diversity) | Qualitative: complementarity *may* exist but is unproven | Phase 9B diagnostic | disagreement + rank-corr artifacts | mistaking diagnosis for ensemble license | none to *diagnose*; ensemble locked | Medium | 2 |
| H2 | Characterize `Age_missing=1` regime separately (inverted base rate, n_pos=8) | m1 collapse 0.5442; CatBoost −0.0217 | Kuhn & Johnson | Qualitative: fragile; may need separate handling | Phase 9B / future FE | slice + score-dist on the slice | over-reading 8 positives | min-n / fragility flag | High | 2 |
| H3 | Confirm ROC-AUC vs top-k agreement for M1 and CatBoost | unknown until computed | Kaggle Book; ISLP | Qualitative: agreement strengthens trust | Phase 9A execution | top-k + global tables | conflict ignored | report as warning | High | 1 |
| H4 | Defer any CatBoost tuning until slice escalations are understood | CatBoost escalated on robust slices (Year 2011, avail_count 0) | hpo note; Cawley & Talbot | Qualitative: tuning before understanding risks overfitting | Phase 10 (locked) | slice + fold artifacts | HPO-by-stealth | Phase 10 authorization | Medium | 3 |
| H5 | Score-distribution audit for degeneracy/compression in any candidate | not yet computed | Hands-On ML | Qualitative: degeneracy would invalidate ranking trust | Phase 9A execution | score-dist artifact | false precision | diagnostic-only | High | 1 |
| H6 | Negative-class (minority) retrieval study | positive rate 0.6483 → negatives are the rarer/harder side | §6 inference | Qualitative: where ranking utility concentrates | Phase 9A execution | neg-retrieval table | over-interpretation | diagnostic-only | Medium | 1 |
| H7 | No ensemble/blending/stacking now | CatBoost+M1 divergence | hpo/leakage notes | n/a | future ensemble phase (locked) | — | gate jumping | explicit future authorization | Deferred | 4 |
| H8 | No submission / threshold strategy now | no winner exists | challenge brief | n/a | Phase 11 (locked) | — | leaderboard chasing | Phase 11 authorization | Prohibited (now) | 5 |

Reminders embedded in the backlog: M1 stays candidate-with-warning; CatBoost stays escalated/candidate-with-warning; XGBoost/LightGBM stay no_qualifying_evidence; any ensemble/blending/HPO/calibration/threshold/submission item is future-locked.

---

## 16. ECC Agents and Skills Plan

Verified by disk inspection: **10 agents** in `.claude/agents/`, **21 skills** in `.claude/skills/`. No new installation recommended (no Phase-9A capability gap; everything for planning, ML-diagnostic review, leakage/integrity audit, gate enforcement, and verification is present). Any tool applied toward HPO/AutoML/submissions/LB/training/ensembling/scraping/external-data/deployment is prohibited regardless of tool.

| Etapa o necesidad | Agente/skill sugerido | Uso propuesto | Riesgo mitigado | Condición de activación |
|---|---|---|---|---|
| Block 0 pre-flight | repo-scan + gateguard | Verify HEAD, clean tree, gates, no `phase9a_*` artifacts | Wrong baseline; double execution | Start of any 9A session |
| Phase coherence review | architect | Sanity-check phase limits (diagnostic-only) | Scope creep into selection | Before authorization |
| Plan re-validation | planner / plan-orchestrate | Re-check this package vs repo | Stale plan | Before §20 gate |
| Static inspection | code-explorer / codebase-onboarding | Read-only structure/artifact review | Accidental modification | During planning/review |
| Docs/refs | docs-lookup / documentation-lookup | Internal docs + reference principles | Mis-citation | §5 / backlog |
| ML-diagnostic validity | mle-reviewer / mle-workflow | Ensure diagnostics ≠ selection bias; folds/metric/leakage sound | Selection bias; metric misuse | Notebook design review |
| Eval design | eval-harness | OOF checks, metric, fold-level comparison design | Metric corruption | Notebook draft review |
| Silent-failure pass | silent-failure-hunter | Row alignment, probability ranges, metric direction, OOF reuse, artifact overwrite | Silent corruption | Code review gate |
| Gate enforcement | gateguard + safety-guard | Keep Phase 10/11, HPO, submissions, forbidden paths blocked | Scope creep | During authorized execution |
| Post-run verification | verification-loop + independent recompute | Recompute metrics from persisted files; git checks | Self-reported-only results | After execution |
| Selective commit | git-workflow | Stage explicit files only; record hash | `git add .` accidents | **Only after explicit director instruction** |
| Context hygiene | context-budget / token-budget-advisor | Keep long diagnostic sessions in budget | Context degradation | If sessions grow long |
| Doc creation | doc-updater | Only the authorized planning/diagnostic docs | Unauthorized edits | This planning run |
| Future code review | python-reviewer / python-patterns / python-testing | Review `09a` notebook design (not execute) | Code defects | Only if implementation authorized |

Classification: **(1) Active in 9A planning** — repo-scan, gateguard, planner, architect, mle-reviewer, eval-harness, silent-failure-hunter, verification-loop, doc-updater, docs-lookup; **(2) On need** — plan-orchestrate, mle-workflow, code-explorer, codebase-onboarding, documentation-lookup, safety-guard, security-review, context-budget, token-budget-advisor, git-workflow (post-auth), python-reviewer/python-patterns/python-testing (only if implementing); **(3) Not for 9A (future phases)** — agent-eval, agent-architecture-audit, automation-audit-ops, code-tour; **(4) Risky/prohibited use** — any tool aimed at HPO/AutoML/submissions/LB/training/ensembling/scraping/external-data/deployment. No gap found → no install recommended.

---

## 17. Opus → Codex → Opus Separation

| Stage | Actor | Does | Does NOT |
|---|---|---|---|
| Now | Opus 4.8 (planner/auditor) | Plan Phase 9A; review project + reference evidence; theory→practice; design diagnostics, notebook, artifacts; write runbook + Codex prompt + post-exec Opus prompt | Execute; train; compute production metrics; select |
| After | Codex (executor) | Execute read-only OOF diagnostics; verify artifacts; recompute metrics; produce the heavily-documented notebook, reports, tables, manifests, candidate log | Interpret strategically beyond technical report; propose HPO as action; ensemble; submit; declare winner |
| After Codex | Opus 4.8 (strategic reviewer) | Read Codex outputs; interpret; prioritize hypotheses; classify by future phase; draft acceptance for director | Execute; train; select winner; authorize next phase |

This separation is encoded in Deliverables B (runbook workflow), C (Codex execution prompt — technical-only), and D (post-execution Opus strategic-review prompt).

---

## 18. Risks, Failure Modes and Mitigations

| Risk | Failure mode | Mitigation |
|---|---|---|
| Diagnostics become covert model selection | "PR-AUC says X wins" | Phase 9A adopts nothing; verdicts are carry/observe/drop, never winner; §6/§14 |
| Multiplicity / cherry-picking across many metrics & slices | A favorable slice over-read | Report all min-n slices; state comparison count; multiplicity caution (Cawley & Talbot) |
| Base-rate misread (0.6483 majority-positive) | PR-AUC/top-k over-interpreted | Report baselines beside every metric; §6 framing mandatory |
| Metrics computed on broken/misaligned OOF | Garbage diagnostics | Integrity gate (Block 1) **before** metrics; 0-mismatch requirement |
| Reproduction drift | Wrong scores trusted | ROC-AUC reproduced ±1e-9 vs accepted; stop on mismatch |
| Implicit ensemble from disagreement analysis | Blending sneaks in | Disagreement is diagnostic-only; ensembles future-locked (backlog cat 4) |
| Calibration temptation | Recalibration performed | Calibration is describe-only; recalibration forbidden |
| Phase-gate jumping | HPO/submission "just to try" | Backlog phase-gated; gateguard; §20 |
| Fragile-slice over-reading (Age_missing=1, 8 pos) | Strong claim from 8 positives | n_pos fragility flag; never decisive alone |
| Artifact overwrite / main-log touch | Lost audit trail / log corruption | Versioned names + pre-write guards; main-log read-before/assert-after |
| Generator-verifier collusion | Unreviewed defects | Two-role rule: Codex executes, Opus reviews, independent recompute |

---

## 19. Explicit Non-Actions

This planning run did **not**: execute Phase 9A or any notebook; train or retrain any model (m0/m1/xgboost/lightgbm/catboost or other); run HPO; compute production metrics for selection; create ensembles/blends/stacks; calibrate or threshold-tune; generate submissions; consult the leaderboard; declare a winner or submission-ready model; change any Phase 8 decision; use external data; use School as a feature; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`, existing outputs, or any tracked file; stage, commit, or push; open Phase 10 or Phase 11. The only filesystem writes are the four authorized planning documents under `docs/09_auc_ranking_diagnostics/`.

---

## 20. Required Project Director Authorization Before Execution

Phase 9A execution may begin only after the project director explicitly and in writing:

1. Approves this brief, the runbook, and the two prompts (or records amendments, which then freeze).
2. Ratifies the metrics catalogue (§8), the imbalance framing (§6), and the k/quantile/min-n grids.
3. Ratifies the block architecture (§9), the single-notebook decision (§12), and the artifact namespace (§13).
4. Confirms the candidate scope (§10) and slice plan (§11), including School-diagnostic-only.
5. Confirms the no-winner / no-submission / no-HPO / no-ensemble / no-calibration-fitting / no-threshold-tuning rules and the Phase 10/11 locks.
6. Records the authorized starting commit hash (currently `4bbcd7a`; advances if the planning docs are committed first — recommended).
7. Issues an explicit "execute Phase 9A" instruction referencing `prompt_codex_phase9a_execution_plan.md` with a signed authorization note (runbook format).

Absent any item: **planned, not executable.**

---

## 21. Recommended Next Step

**Option A — Review the generated Phase 9A planning package; execution remains blocked until explicit project-director authorization.**

Concretely: (1) read this brief; (2) ratify or amend §6/§8 (metrics + imbalance), §9/§12 (architecture + notebook), §10/§11 (candidates + slices), and §20's parameters; (3) optionally instruct a selective commit of the four planning docs first (recommended, so the execution session verifies a planning-inclusive hash); (4) when ready, authorize per §20 using Deliverable C; after Codex executes and an independent recomputation passes, run Deliverable D (Opus strategic review) to produce the classified backlog and the acceptance draft for signature. **Phase 9A selects no winner and authorizes no submission. Phase 10 and Phase 11 remain locked. Future phases remain locked.**
