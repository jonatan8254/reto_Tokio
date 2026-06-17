# Phase 8 Master Planning Brief — Reto Tokio / GCI World NFL Draft Prediction

**Phase:** Phase 8 — Model-Family Comparison, PLANNING ONLY
**Date:** 2026-06-12
**Planning baseline commit:** `7166c2e` (*docs: record phase 7 closure hash*)
**Status:** Planning package. **Phase 8 execution is NOT authorized by this document.** Phase 9, Phase 10 and Phase 11 remain locked.

---

## 0. Executive Verdict

**Phase 8 can be planned safely, and execution must remain blocked until explicit project director authorization.** Every entry gate holds: Phase 5 frozen (`35852e9`); Phase 6 accepted with warnings (`d3b0aed`/`dbc2efc`); Phase 6A executed, audited, accepted, commit-anchored (`f1fb717`/`c4d5647`); Phase 7 executed, audited, **accepted with warnings** and commit-anchored; Phase 7B executed, audited, and **F4 rejected** by the pre-registered rule — both closed in `42ef12a` with the closure hash recorded in `7166c2e` (current HEAD, aligned with `origin/master`). No Phase 8 artifact exists anywhere in the repository: Phase 8 has not been executed.

The accepted post-Phase-7/7B feature set is **F2** (`phase7_f2_median_flags_count`): the 13 Phase 6 base features + 7 row-wise missingness flags + `available_measurement_count`, median imputation, fold-safe one-hot encoding, School excluded. F2's OOF ROC-AUC is **0.811650** on the frozen folds (+0.085034 vs the 0.726616 anchor, 5/5 same-sign folds, slice guard clear — the only Phase 7 variant that also *improved* the fragile `Age_missing = 1` slice).

Phase 8's core question: **under identical data, F2 features, frozen folds, and metric, do other model families produce evidence strong enough to justify selecting 1–3 candidates for later phases — without turning the comparison into HPO or leaderboard chasing?**

One load-bearing environment finding shapes the whole design: the pinned project venv (Python 3.13.13 / scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6) has **no xgboost, no lightgbm, no catboost installed**. Therefore this plan proposes a **two-wave staged architecture**: Wave 1 compares sklearn-native families with zero new dependencies; Wave 2 (external GBDTs) stays **gated behind a separate dependency/environment authorization**. Deep tabular models are blocked for initial Phase 8.

**Recommended next step:** project director review of this package, then explicit execution authorization per §17 — or continued lock.

---

## 1. Repository State Verification

Commands run on 2026-06-12 (read-only):

| Check | Expected | Observed | Status |
|---|---|---|---|
| `git rev-parse --short HEAD` | `7166c2e` | `7166c2e` | PASS |
| Branch / remote | `master`, aligned with `origin/master` | `## master...origin/master` (no ahead/behind) | PASS |
| `git status --short` | no staged files, no tracked modifications | Only the known untracked items (`.claude/`, `CLAUDE.md`, `Libros/`, `Prompts/`, `Recapitulaciones/`, plan v1, 2 backup notebooks, `notebooks/_official/`) | PASS |
| `git diff --check` | clean | clean (exit 0) | PASS |
| `git diff --cached --name-only` | empty | empty | PASS |
| Forbidden-paths diff (`data/input`, `notebooks/_official`, `references`, `outputs/submissions`, `logs/experiment_log.csv`, `.vscode/settings.json`) | empty | empty | PASS |
| `git log --oneline -n 10` | Phase 7/7B closure sequence on top | `7166c2e`, `42ef12a`, `8b21db5`, `c4d5647`, `f1fb717`, `dbc2efc`, `18f0a12`, `d3b0aed`, `35852e9`, `8305950` | PASS |
| Phase 7 planning commit | `8b21db5` exists | Commits the 3 Phase 7 planning docs (795 insertions) | PASS |
| Phase 7/7B closure commit | `42ef12a` exists | Commits both acceptance records, notebooks 07/07b, 6 OOF files, both variant summaries, both slice reports, both validation reports, both candidate logs (18 files) | PASS |
| Phase 7 hash-record commit | `7166c2e` exists | Adds `Selective closure commit: 42ef12a` + hash-record status to both acceptance records only | PASS |
| Phase 8 previously executed? | No | No `phase8_*` artifact exists under `outputs/` or `notebooks/`; `docs/08_model_comparison/` did not exist before this run | PASS (not executed) |
| Environment (`.venv\Scripts\python.exe`) | pinned versions | Python 3.13.13, scikit-learn 1.9.0, numpy 2.4.6, pandas 3.0.3; **xgboost NOT installed; lightgbm NOT installed; catboost NOT installed** | PASS, with design consequence (§7/§8) |

**Observations (none is a blocker):**

1. **Informational:** both Phase 7/7B acceptance records describe themselves in body text as "draft acceptance record … not signed acceptance", while ending in explicit verdicts (`ACCEPT WITH WARNINGS`, `REJECT F4 — KEEP F2`) and being commit-anchored through the project's established closure pattern (selective commit `42ef12a` → hash record `7166c2e`, identical to the 6A `f1fb717` → `c4d5647` pattern, executed on project director instruction). This brief treats Phase 7/7B as **closed by commit-anchored acceptance**; if the project director wants the "draft" self-descriptions tightened, that is a separate, explicitly authorized doc edit.
2. **Informational:** external GBDT libraries are absent from the venv (see §0). This is a fact to design around, not an error.

---

## 2. Evidence Reviewed: Lote 1 and Lote 2

All inspection read-only; no notebook executed in this run. Notebooks were audited statically in prior committed audits; their numbers are consumed via the commit-anchored acceptance records.

### Lote 1 — essential post-Phase-7/7B context

| Archivo | Disponible | Propósito | Información crítica extraída | Riesgo si falta |
|---|---|---|---|---|
| `AGENTS.md` | Sí (repo root) | Agent operating rules | Hard git rules, forbidden paths, phase gates | Agent misbehavior |
| `outputs/validation/phase7b_role_availability_interaction_v1_variant_summary.csv` | Sí (committed) | 7B primary numbers | F4 OOF 0.809369, Δ −0.002281 vs F2, 1/5 same-sign, slice clear, rejected | No 7B evidence base |
| `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md` | Sí (committed; read in full) | 7B closure record | REJECT F4 — KEEP F2; fold table (only fold 2 positive); localized `special_teams`/`kicking_specialist` signal noted but insufficient | Phase 8 could re-litigate F4 |
| `docs/01_project_planning/project_execution_plan_v3.md` | Sí (committed `18f0a12`) | Master phase plan | Phase 8 = fair shortlist comparison; gates and artifact contracts | Phase-boundary drift |
| `docs/07_feature_engineering/prompt_codex_phase7_execution_plan.md` | Sí (committed `8b21db5`) | Phase 7 executor prompt | Template proven in execution: preconditions, frozen design, stop rules | Weaker Deliverable C template |
| `Recapitulaciones/Fase 7/recapitulacion_integral_chat_reto_tokio_phase7_phase7b_closure_phase8_ready_v3.md` | Sí (path correction: under `Recapitulaciones/Fase 7/`) | Session recap | Confirms closure sequence, push to `origin/master`, F2 adoption, Phase 8 gate | Lost narrative continuity (git evidence suffices) |
| `docs/00_project_contract/submission_checklist.md` | Sí | Submission gates | Phase 8 generates no submissions | Submission-policy drift |
| `docs/05_methodology/validation_protocol_phase6.md` | Sí (committed) | Frozen validation protocol | StratifiedKFold(5, shuffle, seed 42); OOF currency; `classes_` policy | Protocol drift |
| `docs/00_project_contract/challenge_brief.md` | Sí (read in full) | Competition contract | Target `Drafted`, ROC-AUC, 696-row submission, external data prohibited, audits possible | Rule violations |
| `docs/05_methodology/leakage_checklist_phase6.md` | Sí (committed) | Leakage taxonomy | Fold-fit-only transforms; blocked-global list; diagnostic-only variables | Leakage controls weaken |
| `docs/05_methodology/phase5_execution_decisions.md` | Sí (committed) | Frozen Phase 5 decisions | Metric, splitter, seed, score-input policy | Re-litigating closed decisions |
| `docs/06_validation/phase6_acceptance.md` | Sí (committed) | Phase 6 closure | Anchor 0.726616; frozen folds ratified | Anchor ambiguity |
| `docs/06_validation/phase6a_acceptance.md` | Sí (committed) | Phase 6A closure | Threshold 0.005436 + 4/5; slice n ≥ 50; V7 diagnostic; grouped CV dormant | Threshold ambiguity |
| `docs/07_feature_engineering/phase7_acceptance.md` | Sí (committed; read in full) | Phase 7 closure | F2 adopted; F1/F5/F3 escalated on `Age_missing = 1`; F6 gate closed (F5−F1 = 0.001498); mean imputation NOT adopted; independent recomputation max diff 0.0 | Feature-set ambiguity |
| `docs/07_feature_engineering/phase7_master_planning_brief.md` | Sí (committed) | Phase 7 plan | Pre-registered ladder pattern; authorization-note mechanism (reused here) | Lose proven planning pattern |
| `outputs/validation/phase7_missingness_availability_v1_slice_report.csv` | Sí (committed; key rows read) | Phase 7 slices | `Age_missing = 1`: n = 435, only 8 positives; F2 +0.020785 vs F0; F1 −0.044204; F5 −0.043033; F3 −0.077869 | Lose the central slice warning |
| `outputs/reports/phase7_missingness_availability_v1_validation_report.md` | Sí (committed) | Phase 7 full report | Summarized and audited in `phase7_acceptance.md` §H | Secondary (acceptance record covers it) |
| `outputs/validation/phase7_missingness_availability_v1_variant_summary.csv` | Sí (committed; read in full) | Phase 7 primary numbers | All F0–F6 values in §3; per-fold scores and deltas | No Phase 7 evidence base |
| `docs/07_feature_engineering/phase7_operator_runbook.md` | Sí (committed) | Phase 7 procedure | Project Authorization Note format; audit procedure; closure criteria (reused here) | Reinvent procedure |
| `outputs/validation/phase7b_role_availability_interaction_v1_slice_report.csv` | Sí (committed) | 7B slices | Slice guard clear; localized positive movement in `special_teams` (+0.030) | Lose 7B slice context |
| `outputs/reports/phase7b_role_availability_interaction_v1_validation_report.md` | Sí (committed) | 7B full report | Summarized and audited in `phase7b_role_interaction_acceptance.md` | Secondary |

### Lote 2 — extended executive evidence

| Archivo | Disponible | Propósito | Información crítica extraída | Riesgo si falta |
|---|---|---|---|---|
| `outputs/oof/phase7_missingness_availability_v1_phase7_f0_anchor_recheck_oof_predictions.csv` | Sí (committed, 2781 rows) | F0 anchor OOF | Matches Phase 6 OOF (max abs diff 5.55e-16 per acceptance audit) | Anchor-continuity check impossible |
| `..._phase7_f1_median_flags_oof_predictions.csv` | Sí (committed) | F1 OOF | 0.811568 (recomputed independently, diff 0.0) | — |
| `..._phase7_f2_median_flags_count_oof_predictions.csv` | Sí (committed) | **F2 OOF — Phase 8 reference vector** | 0.8116502602456482; per-fold 0.789389/0.832382/0.825854/0.773724/0.840930 | Phase 8 paired deltas impossible |
| `..._phase7_f3_median_flags_count_bins_oof_predictions.csv` | Sí (committed) | F3 OOF | 0.810606 | — |
| `..._phase7_f5_mean_flags_oof_predictions.csv` | Sí (committed) | F5 OOF | 0.813066 (diagnostic only; mean not adopted) | — |
| `outputs/reports/phase7b_role_availability_interaction_v1_experiment_log_candidate.csv` | Sí (committed; read) | 7B candidate log | rejected; hpo_run False; submission_created False; leakage_warning False | Traceability gap |
| `outputs/oof/phase7b_role_availability_interaction_v1_phase7b_f4_role_count_player_type_oof_predictions.csv` | Sí (committed) | F4 OOF | 0.809369 | — |
| `docs/01_project_planning/project_execution_plan_v2_context_efficient.md` | Sí | Historical plan | Superseded by v3; consistent gates | Low |
| `notebooks/07_phase7_missingness_availability_feature_block.ipynb` | Sí (committed; static template) | Phase 7 executed notebook | Audited builders: fold-safe pipelines, F-gates, pre-write guards — **reuse as Phase 8 template** | Rewrite-from-scratch risk |
| `notebooks/07b_phase7b_role_availability_interaction_probe.ipynb` | Sí (committed; static template) | 7B executed notebook | Pattern for comparing against a persisted OOF baseline without retraining it | — |
| `docs/03_eda/experiment_notes.md` | Sí | Phase 3 EDA notes | Signal families; School risk; missingness hypotheses (now confirmed) | Low (superseded by Phase 7 evidence) |
| `docs/01_project_planning/integral_project_review_phase0_phase6.md` | Sí | Project diagnosis | Phase ordering rationale | Low |
| `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md` | Sí (committed) | Phase 6 harness report | Anchor provenance | Low |
| `outputs/reports/phase6a_baseline_reconciliation_report.md` | Sí (committed) | 6A V0–V7 report | Gap decomposition (imputation statistic +0.0757) | Low |
| `outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv` | Sí (committed) | 6A numbers | V4 0.809010; V7 0.802271 | — |
| `outputs/reports/phase6a_d1_d2_diagnostics_report.md` | Sí (committed) | D1/D2 report | Seed-noise floor 0.002718 → threshold 0.005436 | Threshold provenance lost |
| `outputs/validation/phase6a_d1_seed_sweep_summary.csv` | Sí (committed) | D1 numbers | v0median std 0.002718; v7mean std 0.001097 | — |
| `outputs/reports/phase6a_d2_refined_probe_report.md` | Sí (committed) | Refined D2 | Escalation cleared; grouped CV dormant | — |
| `outputs/validation/phase6a_d2_refined_tier_summary.csv` | Sí (committed) | D2 tiers | T4/T4b = 0 genuine duplicates | — |
| `outputs/reports/phase7_missingness_availability_v1_experiment_log_candidate.csv` | Sí (committed) | Phase 7 candidate log | `leakage_checks_passed = False` is escalation metadata, not leakage (per acceptance audit) | Metadata-warning context lost |

OOF files were used **only** to verify continuity, traceability and documented metrics — not to select any model in this run.

---

## 3. Numerical Results Validation

All values checked this session against committed artifacts (variant summaries read directly; acceptance records read in full; slice rows read directly).

| Quantity | Value | Source | Status |
|---|---|---|---|
| Phase 6 anchor OOF ROC-AUC | 0.726616 (0.7266161714116555) | Phase 7 variant summary (F0), `phase6_acceptance.md` | Confirmed |
| Phase 6 fold mean ± std | 0.729253 ± 0.030629 | same | Confirmed |
| 6A V0 OOF | 0.726616 | 6A variant summary | Confirmed |
| 6A V4 OOF | 0.809010 | same | Confirmed |
| 6A V7 OOF (mean-impute diagnostic) | 0.802271 | same | Confirmed |
| D1 seed-noise std (v0median) | 0.002718 | D1 sweep summary | Confirmed |
| Feature-block threshold | OOF gain ≥ 0.005436 AND same-sign ≥ 4/5 | `phase6a_acceptance.md` §5 | Confirmed (ratified) |
| Minimum slice size | n ≥ 50 | same | Confirmed (ratified) |
| Grouped CV | dormant; StratifiedKFold frozen folds retained | refined D2 report + acceptance | Confirmed (ratified) |
| Phase 7 F0 anchor recheck OOF | 0.7266161714116555; reproduces Phase 6 OOF to 5.55e-16 | Phase 7 variant summary + acceptance §H | Confirmed |
| Phase 7 F1 OOF | 0.8115677460991508 (+0.084952; 5/5; slice guard TRIGGERED) | variant summary | Confirmed |
| Phase 7 F2 OOF | **0.8116502602456482** (+0.085034; 5/5; slice guard CLEAR) | variant summary | Confirmed |
| Phase 7 F2 fold mean ± std | 0.8124557501813141 ± 0.029238 | variant summary | Confirmed |
| Phase 7 F2 per-fold AUC | 0.789389 / 0.832382 / 0.825854 / 0.773724 / 0.840930 | variant summary | Confirmed |
| Phase 7 F3 OOF | 0.8106056481642162 (+0.083989; 5/5; TRIGGERED) | variant summary | Confirmed |
| Phase 7 F5 OOF | 0.8130660442094350 (+0.086450; 5/5; TRIGGERED; mean not adopted) | variant summary | Confirmed |
| F6 gate | not run; F5−F1 = 0.001498 < 0.005436 | variant summary | Confirmed |
| **F2 accepted** | adopted by rule; commit-anchored | acceptance + `42ef12a`/`7166c2e` | Confirmed |
| Phase 7 warnings | `Age_missing = 1` degradation for F1 (−0.044204), F5 (−0.043033), F3 (−0.077869); F2 **+0.020785**; candidate-log `leakage_checks_passed = False` = escalation metadata | acceptance §F + slice report rows | Confirmed |
| `Age_missing = 1` slice composition | n = 435, positives = 8 (high-variance slice) | slice report | Confirmed |
| Phase 7B F4 OOF | 0.8093690701818260 | 7B variant summary | Confirmed |
| Phase 7B F2 comparison OOF | 0.8116502602456482 (loaded from persisted OOF, not retrained) | same | Confirmed |
| Delta F4 − F2 | −0.0022811900638222 | same | Confirmed |
| Same-sign positive folds | 1/5 (only fold 2 positive: +0.013069) | same + acceptance §D | Confirmed |
| **F4 rejected; final feature set remains F2** | rejected by pre-registered rule; slice guard clear; leakage pass | 7B acceptance | Confirmed |
| Frozen folds integrity | `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`: 2781 rows, labels 0..4, sha256[:16] `96937649526bcadb` | committed file + acceptance audits | Confirmed |
| Train/test contract | train 2781×16 (1803 drafted / 978 not); test 696×15; submission 696 rows | challenge brief | Confirmed |
| Environment | Python 3.13.13 / sklearn 1.9.0 / pandas 3.0.3 / numpy 2.4.6; **xgboost, lightgbm, catboost NOT installed** | direct venv check this session | Confirmed |

No discrepancy was found between the prompt's claimed values and repository evidence.

---

## 4. Frozen Decisions Preserved

This plan preserves all of the following; none of the evidence reviewed justifies reopening any of them.

| # | Frozen decision | Phase 8 consequence |
|---|---|---|
| 1 | Primary metric: ROC-AUC on probabilities for `Drafted = 1` | Sole primary comparison metric for every family |
| 2 | Positive-class probability verified via `estimator.classes_` | Mandatory per model; never blind `[:, 1]` (HGB/LR/ET included) |
| 3 | Official data only; no external data of any kind; no manual labels/edits | Registry configs contain no externally derived information |
| 4 | Frozen folds remain active (sha `96937649526bcadb`) | Loaded + integrity-asserted; never recomputed; identical for every model |
| 5 | OOF ROC-AUC is the primary local comparison currency | Model summary ranks by OOF; fold metrics are diagnostics |
| 6 | **Phase 7 accepted feature set is F2** | Every Phase 8 model consumes exactly F2 (21 features); no per-model feature engineering |
| 7 | **F4 (7B) is rejected** | No role-interaction features re-enter through any model config |
| 8 | School remains excluded (diagnostic-only slice) | Includes a hard consequence: CatBoost's native-categorical use of School is **blocked**; CatBoost itself stays deferred+gated (§8) |
| 9 | Candidate logs separate; `logs/experiment_log.csv` protected | Phase 8 writes one candidate-log row under `outputs/reports/`; main log read-before/assert-after |
| 10 | Public leaderboard never a selection criterion | Zero LB consultation in Phase 8 |
| 11 | **No HPO in Phase 8** | One pre-registered config per family (plus the frozen continuity config); no search loops, no "informal trying a few values"; any config change after ratification = stop condition |
| 12 | No submissions in Phase 8 | No file under `outputs/submissions/`; no final inference |
| 13 | No ensembles in initial Phase 8 | Single-model comparisons only; ensembling is a later locked phase |
| 14 | Phase 9 / 10 / 11 remain locked | §18 of the planning prompt; dependency notes only |

Honest caveats carried forward (from the 6A/7 acceptance records):

- The threshold 0.005436 was derived from **RF seed noise** (2 × 0.002718). Other families have unmeasured seed noise; in Phase 8 the threshold serves as a pre-registered **evidence-flagging rule**, not an auto-adoption rule — final candidate selection is a project director decision at acceptance. Per-family seed sweeps, if ever needed, are a Phase 9 question.
- The depth-5 RF caveat ("no qualifying gain under the frozen model configuration" ≠ "no value") was explicitly routed to Phase 8 by the Phase 6A/7 records; §8 resolves it with one pre-registered default-parameter RF config — an enumerated config, not a search.

---

## 5. References Reviewed and Theory-to-Practice Transfer

Sources are those the project's Phase 4B audit marks **Reviewed** (`docs/04_research/pdf_review_audit.md`, `pdf_key_findings.md` — path corrections for the prompt's `key_findings.md` / `pdf_audit.md`). Compact project summaries sufficed; **no full PDF was re-parsed in this run** (project reading policy). `docs/04_research/research_notes_tabular_models.md` and `research_notes_hpo.md` were read in full this session — the tabular-models note pre-registers essentially the §8 shortlist and explicitly assigns "fair shortlist comparison" to Phase 8. References contribute **methodology only — never external data** (no athletes, schools, conferences, rankings, geography, NFL history, draft outcomes).

| Fuente / referencia | Principio metodológico | Aplicación práctica a Phase 8 | Riesgo que mitiga | Cómo integrarlo al plan |
|---|---|---|---|---|
| `research_notes_tabular_models.md` (project) | Short shortlist > model zoo; identical folds/metric/OOF/logging; School & missingness sensitivity in review | Two-wave registry (§8); slice diagnostics mandatory per model | Model-zoo sprawl; unfair comparison | §8 registry; §9 protocol |
| The Kaggle Book (2nd ed., 2025) | Trust frozen local CV; LB is noise; pre-register experiments | Frozen folds + pre-registered registry + hard run cap; LB prohibited | Leaderboard chasing; adaptive overfitting | §9; §16 non-actions |
| The Kaggle Workbook (2023) | Change one thing at a time on identical folds | Single varying factor = model family; F2 and folds constant | Confounded attribution | §9 fair-matrix |
| ISLP | Selection variance is real; effects must clear noise | 0.005436 flag threshold + 4/5 fold-sign rule as evidence flags | Reading noise as signal | §12 criteria |
| Hands-On ML (sklearn/PyTorch, 2026) | `Pipeline`/`ColumnTransformer` idiom; verify estimator internals; sklearn HGB as strong native tabular learner | Reuse audited Phase 7 builders; HGB as Wave 1 active candidate; `classes_` check everywhere | Fit-scope drift; class-index bugs | §10/§11 |
| Kuhn & Johnson | Preprocessing requirements differ per model family and must be explicit | Per-model preprocessing matrix (§10.5): LR gets fold-fitted scaling as a *requirement*, not an advantage | Silent preprocessing unfairness | §10.5 table |
| XGBoost paper (Chen & Guestrin) | GBDT strength on tabular; regularized boosting | XGBoost named, classified **Deferred — Wave 2** (not installed; install = gated env mutation) | Premature dependency risk | §8 registry |
| LightGBM paper + ML with LightGBM & Python (2023) | Efficient GBDT; leaf-wise growth; categorical handling is a contract, not magic | LightGBM **Deferred — Wave 2**; categorical handling via the same F2 OHE matrix if ever run | Library-specific leakage shortcuts | §8; §13 |
| CatBoost paper | Ordered boosting reduces target leakage in categorical encoding | CatBoost **Deferred + additionally gated**: its native categorical pathway invites School-as-feature, which is frozen-excluded | School leakage temptation | §8 registry gate |
| Deep-tabular benchmark (`closer_look_deep_learning_tabular_datasets.pdf`) | Deep tabular rarely beats tuned GBDT on small/medium tabular; cost is high | Deep tabular (MLP/TabNet/FT-Transformer/SAINT/NODE) **Blocked** for initial Phase 8 | Time sink; reproducibility burden | §8 registry |
| Optuna paper | HPO is powerful and dangerous post-validation | Confirms **HPO stays blocked until Phase 10** with its 7 activation conditions (`research_notes_hpo.md`) | HPO-by-stealth | §4 item 11; §16 |
| Cawley & Talbot | Model selection on the same CV is itself subject to overfitting | Hard run cap; pre-registered configs; flagging-rule ≠ auto-adoption; director decides | Selection bias | §8 cap; §12 |
| Leakage & reproducibility-crisis papers | Pipeline-wide leakage taxonomy | Per-model leakage checklist instantiated (§13) | All taxonomy layers | §13 |
| GCI course materials (sesión 7, QA, tutorial) | Clean, deterministic, seed-controlled, auditable code; external data invalidates ranking | Notebook contract (§10/§11): seeds fixed, environment + hash recorded, top-to-bottom | Disqualification / audit failure | §10/§11/§14 |

---

## 6. ECC Agents and Skills Plan

`/plugin list ecc@ecc` is a CLI user command not invocable from agent context; availability was verified by **direct disk inspection** this session.

**Agents — 10/11 expected present** in `.claude/agents/`: architect, build-error-resolver, code-explorer, code-reviewer, doc-updater, docs-lookup, mle-reviewer, planner, python-reviewer, silent-failure-hunter. `security-reviewer`: **Not confirmed yet** (absent as an agent; the `security-review` *skill* exists and covers the need).

**Skills — 21/27 expected present** in `.claude/skills/`: agent-architecture-audit, agent-eval, architecture-decision-records, automation-audit-ops, code-tour, codebase-onboarding, context-budget, documentation-lookup, eval-harness, gateguard, git-workflow, mle-workflow, plan-orchestrate, python-patterns, python-testing, repo-scan, safety-guard, security-review, security-scan, token-budget-advisor, verification-loop. **Not confirmed yet** (absent): ai-regression-testing, search-first, strategic-compact, production-audit, nutrient-document-processing, scientific-thinking-literature-review.

**No new installation is recommended.** The absent items cover no capability Phase 8 needs: planning, ML review, leakage review, gate enforcement, verification and selective-commit support are all present. Installing more tools adds surface without mitigating any identified risk. (Per-recommendation gap table therefore intentionally empty — no concrete gap found.)

**Classification:**

1. **Use actively in Phase 8 Planning/Execution:** planner, plan-orchestrate, repo-scan, gateguard, mle-reviewer, mle-workflow, eval-harness, code-reviewer, python-reviewer, python-patterns, silent-failure-hunter, verification-loop, doc-updater (the three authorized docs only), git-workflow (selective commit, post-authorization only).
2. **Available, invoke on need:** architect, code-explorer, docs-lookup, documentation-lookup, codebase-onboarding, code-tour, context-budget, token-budget-advisor, safety-guard, security-review, security-scan, architecture-decision-records (ADR if a model-policy decision at closure merits it), build-error-resolver (**only** if a Wave-2 dependency install is later authorized and fails).
3. **Not for Phase 8 (future phases):** agent-eval, agent-architecture-audit, automation-audit-ops.
4. **Risky/prohibited uses:** no installed item is inherently prohibited, but any agent/skill applied toward HPO, AutoML, submissions, leaderboard optimization, ensembling/stacking, autonomous loops, scraping, external sports data, deployment, or DB/frontend work is prohibited in Phase 8 regardless of the tool.

| Etapa o necesidad | Agente/skill sugerido | Uso propuesto | Riesgo mitigado | Condición de activación |
|---|---|---|---|---|
| Block 0 pre-flight | repo-scan + gateguard | Verify HEAD, clean tree, gates, no `phase8_*` artifacts | Wrong baseline; double execution | Start of any Phase 8 session |
| Plan re-validation | planner / plan-orchestrate | Re-check this package vs repo state before authorization | Stale plan | Before §17 gate |
| Registry/protocol review | mle-reviewer + mle-workflow | Validate fair-matrix, configs, fold use, OOF design | Methodological defects | Before authorization |
| Evaluation design | eval-harness | OOF / fold-metrics / paired-deltas / slice-report design of notebook 08 | Metric corruption | Notebook draft review |
| Static code review (two-role rule) | code-reviewer + python-reviewer + python-patterns | Independent review of notebook 08 draft; generator ≠ verifier | Leakage/code defects | After draft, before execution |
| Silent-failure pass | silent-failure-hunter | `classes_` paths, NaN handling, swallowed exceptions, guard trips | Silent corruption | Same gate |
| Execution session guard | gateguard + safety-guard | Block HPO/submissions/LB/Phase-9+ mid-run | Scope creep | During authorized execution |
| Post-run verification | verification-loop + independent stdlib AUC recompute | Recompute every OOF AUC from persisted files (6A/7 pattern) | Self-reported-only results | Immediately after execution |
| Selective commit | git-workflow | Stage explicit file list only; record hash | `git add .` accidents | **Only after explicit project director instruction** |
| Dependency decision support (Wave 2, future) | docs-lookup / documentation-lookup + build-error-resolver | Version/compatibility check for xgboost/lightgbm/catboost on Python 3.13 | Broken env; irreproducibility | Only if Wave 2 is separately authorized |

---

## 7. Proposed Phase 8 Block Architecture

The suggested 9-block architecture was evaluated and **adapted**: the suggested "Block 3 — Methodological Theory-to-Practice Transfer" is a planning-time activity already completed in §5 of this brief (keeping it as an execution block would add ceremony without a control point), and a **new Environment & Dependency Audit block** is inserted — forced by the verified absence of xgboost/lightgbm/catboost, which makes dependency status a first-class gate rather than a footnote. Net result: 9 blocks, 0–8.

| Block | Nombre | Objetivo | Decisiones que cubre | Evidencia necesaria | Riesgos mitigados | Salida esperada | Condición de avance |
|---|---|---|---|---|---|---|---|
| 0 | Repository, Git & Phase Gate Verification | Prove the session starts from the authorized baseline | None (verification only) | HEAD = authorized hash; clean tree; acceptance records committed; folds sha `96937649526bcadb`; no pre-existing `phase8_*` artifacts | Wrong/dirty baseline; double execution | Verification table in notebook + report | All PASS; any FAIL ⇒ stop |
| 1 | Current State Freeze | Freeze what every model inherits | F2 (21 features); exclusions Id/Drafted/School; frozen folds; ROC-AUC; F2 OOF 0.811650 as reference; non-scope list | `phase7_acceptance.md`; `phase7b_role_interaction_acceptance.md`; F2 OOF file | Silent policy drift | Frozen-state cell with assertions | Policies restated + asserted in code |
| 2 | Environment & Dependency Audit | Record exactly what the pinned env can run | Wave 1 = sklearn-only (no installs); Wave 2 = gated external GBDTs | Direct venv import checks (this session: xgboost/lightgbm/catboost absent) | Mid-run installs; version drift; irreproducible env | Environment record + Wave 1/2 boundary | Versions match pinned set; **no install occurs in Wave 1** |
| 3 | Model Candidate Registry & Risk Classification | Pre-register every model, config and status | §8 registry: model_keys, exact constructor params, statuses, gates | §8 ratified at §17 | Model-zoo creep; informal HPO; CatBoost/School shortcut | Ratified registry table | Project director ratification |
| 4 | Fair Comparison Protocol Design | Guarantee identical comparison conditions | §9 fair-matrix; paired deltas vs M0; flagging rule | §9 of this brief | Confounded or rigged comparison | Protocol section, then notebook cells | Independent review passes |
| 5 | Notebook / Script Architecture Blueprint | Fix the future notebook structure cell-by-cell | §10 blueprint; one notebook for Wave 1; reserved Wave 2 names | §10 of this brief; notebook 07 as audited template | Improvised implementation; Codex drift | §10 blueprint + fidelity contract (§10.8) | Blueprint ratified with the registry |
| 6 | Artifact Architecture & Git Policy | Keep results traceable and commit-anchorable | §14 artifact names; manifest; candidate log; selective-commit list | §14 | Overwrites; unanchored results; log corruption | All §14 artifacts (future); guards | Pre-write guards held; post-run git checks clean |
| 7 | Validation, Slice Diagnostics & Acceptance Criteria | Classify each model's evidence per pre-registered rule | §12 criteria + edge cases; slice guard; escalations | §12 tables | Noise read as signal; subgroup harm hidden | Model summary + fold metrics + slice report + decision table | Every model classified by rule |
| 8 | Project Director Approval Gate & Executor Handoff | Separate decision from implementation | Whether to execute at all; Wave 2 separately; candidate selection at closure | This brief + runbook reviewed | Unauthorized execution; unauthorized installs | Project Authorization Note (runbook §10) | **Explicit project director authorization recorded** |

Block 8 is logically *before* execution of Blocks 4–7; operational ordering is in the runbook.

---

## 8. Model Candidate Registry

**Staged two-wave decision (the central strategic choice of this plan):** Phase 8 should **not** compare all historically named models at once. Wave 1 compares sklearn-native families with **zero new dependencies** in the proven pinned environment. Wave 2 (external GBDTs) requires environment mutation (installs on Python 3.13), which is a separate, explicitly gated authorization — it must never happen silently mid-run. This keeps the core comparison reproducible today, isolates dependency risk, and prevents Phase 8 from sprawling.

**Hard cap: ≤ 6 trained model-runs in Wave 1** (5 core + 1 gated diagnostic). No additional run without a new recorded authorization.

| Modelo | Estado propuesto | Motivo | Riesgo metodológico | Requisitos antes de ejecutar | Incluir ahora / diferir |
|---|---|---|---|---|---|
| RandomForestClassifier (frozen config, depth 5) | **Reference** (M0 integrity gate) | Continuity anchor; must reproduce F2 OOF 0.811650 ± 1e-6 | None (verification) | Authorization note | **Incluir — Wave 1** |
| RandomForestClassifier (library-default depth) | **Active candidate** | Resolves the documented depth-5 caveat routed to Phase 8 by the 6A/7 records; enumerated config, not a search | Misread as HPO if not pre-registered (it is pre-registered, single config) | Registry ratification | **Incluir — Wave 1** |
| LogisticRegression | **Active candidate** | Linear/interpretable floor; separability diagnostic | Convergence/scaling pitfalls (handled by pre-registered pipeline) | Registry ratification | **Incluir — Wave 1** |
| HistGradientBoostingClassifier | **Active candidate** | Strongest sklearn tabular family; bridge before external GBDTs; native-missing question deferred by Phase 7 records lands here | Early-stopping nondeterminism (disabled by config); native-NaN mode breaks strict fairness (gated as diagnostic) | Registry ratification | **Incluir — Wave 1** |
| ExtraTreesClassifier | **Optional candidate** | Cheap randomized-trees contrast to RF | Low marginal information | Registry ratification; fits within cap | **Incluir — Wave 1** (drop first if the director wants a smaller wave) |
| XGBClassifier / XGBoost | **Deferred — Wave 2** | Strong GBDT, but **not installed** in the pinned venv | Env mutation; version pin; Python 3.13 compatibility unverified | Separate Wave 2 authorization + dependency check + pinned install | **Diferir** |
| LGBMClassifier / LightGBM | **Deferred — Wave 2** | Same as XGBoost | Same | Same | **Diferir** |
| CatBoostClassifier / CatBoost | **Deferred — Wave 2, additionally gated** | Not installed; its native-categorical pathway is precisely the School-as-feature temptation that is frozen-excluded | School leakage shortcut; categorical contract complexity | Wave 2 authorization **plus** an explicit School-policy reconfirmation gate | **Diferir (doble gate)** |
| Deep tabular (MLP / TabNet / FT-Transformer / SAINT / NODE) | **Blocked** for initial Phase 8 | Reviewed benchmark evidence: rarely beats GBDT on small tabular; high cost; no plateau evidence yet | Time sink; irreproducibility; dependency sprawl | GBDT plateau evidence + strong justification + project director authorization (future phase) | **Bloquear** |

**Pre-registered exact configs (frozen at ratification; any change after = stop condition):**

```text
m0_random_forest_frozen      RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, n_jobs=-1)        [GATE: OOF == 0.8116502602456482 ± 1e-6]
m1_logistic_regression       LogisticRegression(max_iter=1000, random_state=42)                                       [pipeline adds fold-fitted StandardScaler on numeric features]
m2_random_forest_default     RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1)
m3_extra_trees_default       ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1)
m4_hist_gradient_boosting    HistGradientBoostingClassifier(random_state=42, early_stopping=False)
m5_hgb_native_missing        same as m4, numeric imputation REMOVED (NaNs passed through)                             [GATED diagnostic — runs only if explicitly authorized in the Project Authorization Note]
```

`max_iter=1000` for LR is a pre-registered convergence requirement (documented as such), not tuning. `early_stopping=False` for HGB is a pre-registered determinism requirement. No other parameter deviates from library defaults except the frozen M0 continuity config. **No config search of any kind.**

---

## 9. Fair Comparison Protocol

Every Wave 1 model runs under an identical matrix; the **only** varying factor is the model family (plus the single gated preprocessing diagnostic m5, clearly labeled as fairness-breaking and therefore decision-ineligible on its own):

| Dimension | Fixed value for all models |
|---|---|
| Dataset | `data/input/train.csv` only (test used only for contract checks; no Phase 8 inference) |
| Feature set | **F2 exactly**: 13 base + 7 missingness flags + `available_measurement_count` (21 features) |
| Exclusions | `Id`, `Drafted`, `School` (asserted) |
| Folds | Frozen file, sha256[:16] `96937649526bcadb`, 2781 rows, labels 0..4; never recomputed |
| Metric | ROC-AUC, positive-class proba via verified `estimator.classes_` |
| OOF construction | One row per train row; same fold mapping; finite probabilities in [0,1]; no single-class fold |
| Preprocessing | Audited Phase 7 F2 builder: fold-fitted median imputer + most_frequent + OHE(handle_unknown="ignore") in `ColumnTransformer`+`Pipeline`; LR additionally gets fold-fitted StandardScaler (model requirement, pre-registered); m5 is the sole, gated exception |
| Seed | 42 everywhere |
| Artifact naming | `phase8_model_family_comparison_v1_<model_key>_*` with pre-write guards |
| Candidate log | One v2 row under `outputs/reports/`; main log untouched |
| Leakage checks | §13 checklist instantiated per model |
| Leaderboard | Untouched |

**Pre-registered evidence rule (flagging, not auto-adoption):** a challenger is flagged **"promotable evidence"** if `OOF(model) − OOF(m0) ≥ 0.005436` AND paired fold deltas vs m0 positive in ≥ 4/5 folds AND slice guard clear. Models below threshold are flagged "no qualifying evidence"; slice-guard trips are "escalated". **Phase 8 produces a classified evidence table — it does not crown a winner.** Selecting 1–3 candidates for later phases is a project director decision recorded in `phase8_acceptance.md`. The threshold's RF-noise provenance is recorded as a known limitation (§4).

**Explicit separation (frozen):** pre-registered default-ish configs = the only permitted comparison mode; search/tuning loops = HPO, blocked until Phase 10; ensembles = blocked; submissions = blocked.

---

## 10. Notebook / Script Architecture Blueprint

### 10.1 Decision: one notebook for Wave 1, reserved names for Wave 2

**Decision: a single Wave 1 notebook**, `notebooks/08_phase8_model_family_comparison.ipynb` (`experiment_id = phase8_model_family_comparison_v1`), with the environment/dependency audit as an internal section — **not** a separate dependency-check notebook, because Wave 1 requires zero installs and a standalone 08a would verify nothing that the internal section does not. A separate notebook becomes justified exactly when Wave 2 is authorized, because environment mutation must be isolated from comparison logic; the name `notebooks/08b_phase8_external_gbdt_comparison.ipynb` (`experiment_id = phase8_model_family_comparison_v2_external`) is **reserved, not created**. Justification against the criteria: single notebook maximizes top-to-bottom reproducibility and audit simplicity; the registry + run cap prevents scope creep; the m0 gate prevents drift; Codex compatibility is highest with one linear artifact; HPO risk is controlled by the frozen registry, not by notebook count.

| Notebook propuesto | Rol | Por qué separado | Inputs | Outputs | Cuándo se ejecutaría | Riesgo si se fusiona | Riesgo si se separa |
|---|---|---|---|---|---|---|---|
| `08_phase8_model_family_comparison.ipynb` | Wave 1 comparison (the only one this plan proposes to build) | — (single artifact) | train.csv, frozen folds, F2 OOF reference | §14 Wave 1 artifacts | Only after §17 authorization | — | — |
| `08b_phase8_external_gbdt_comparison.ipynb` | **Reserved** Wave 2 | Env mutation (installs) must not contaminate the reproducible Wave 1 run | Wave 1 artifacts + newly authorized deps | v2_external artifacts | Only after a separate Wave 2 authorization | Mid-run installs would break Wave 1 reproducibility | None (it simply stays unbuilt until gated) |
| `08c_..._review.ipynb` | **Not proposed** | Post-run audit is runbook §12 procedure (independent recompute), not a notebook deliverable | — | — | — | — | Fragmentation without a control point |

### 10.2 Cell-by-cell architecture (Wave 1 notebook — to be built only if authorized)

| Sección / celda | Nombre | Propósito | Inputs | Outputs | Validaciones obligatorias | Riesgos controlados | Artefactos asociados |
|---|---|---|---|---|---|---|---|
| 1 | Title, scope & guardrails | Declare phase, experiment_id, non-scope (no HPO/submissions/LB/Phase 9+) | — | markdown | — | Scope creep | — |
| 2 | Imports & dependency check | Import sklearn/pandas/numpy only; record versions; **assert xgboost/lightgbm/catboost are NOT imported** | venv | env dict | Versions == 3.13.13/1.9.0/3.0.3/2.4.6 | Env drift; silent installs | report env block |
| 3 | Path config & repo-root validation | Relative paths from repo root | — | path constants | Root markers exist | Wrong CWD | — |
| 4 | Environment & git record | `git rev-parse HEAD` + dirty flag recorded | git | report fields | HEAD == authorized hash | Wrong baseline | report |
| 5 | Protected-path & no-overwrite checks | Assert no `phase8_..._v1_*` artifact already exists; main-log read + checksum | outputs/, logs/ | guard state | Pre-write guards armed | Overwrites; log corruption | — |
| 6 | Data loading (official only) | Load train.csv (test only for contract checks) | data/input | DataFrames | 2781×16; 696×15 | Wrong data | — |
| 7 | Data contract checks | The 12 Phase 6/7 contract checks | DataFrames | assert log | dtypes, Id uniqueness, target values, missingness counts (Age 435, Sprint 145, Vertical 554, Bench 721, Broad 581, Agility 970, Shuttle 912) | Contract drift | report |
| 8 | Frozen folds load + integrity | Load fold file; never recompute | outputs/folds | fold map | 2781 rows; labels 0..4; Id order == train; sha256[:16] == `96937649526bcadb` | Fold corruption | report |
| 9 | F2 feature builder | Row-wise flags + count via audited Phase 7 builder code | train | X (21 cols), y | Flag sums == known missingness counts; `School`/`Id`/`Drafted` not in X (assert) | Feature drift; School leakage | — |
| 10 | F2 reference OOF load | Load persisted Phase 7 F2 OOF (never retrain it as "baseline") | outputs/oof | reference vector | OOF AUC == 0.8116502602456482 (recomputed from file) | Baseline drift | — |
| 11 | Model registry cell | The §8 registry verbatim: model_keys, constructors, statuses, gates | — | registry dict | Exactly the ratified configs; m5 runs only if note authorizes | Informal HPO; creep | report registry table |
| 12 | Model eligibility checks | Per model: importable, supports `predict_proba` or decision-equivalent, deterministic seed set | registry | eligibility table | All Wave 1 eligible; anything else ⇒ skip + record (never substitute) | Silent substitutions | report |
| 13 | Per-model preprocessing builders | §10.5 matrix: shared F2 pipeline; LR scaler branch; m5 native-NaN branch (gated) | registry | pipeline factories | Fit happens only inside fold loop | Preprocessing leakage | — |
| 14 | CV/OOF loop (design) | For each model × 5 frozen folds: fit on train mask, predict val mask | X, y, folds | per-model OOF arrays | `classes_` locates label 1 exactly once; probas finite in [0,1]; no single-class fold; OOF fold map == frozen map | Class-index bugs; leakage | per-model OOF CSVs |
| 15 | M0 integrity gate | m0 must reproduce F2 OOF ± 1e-6 | m0 OOF | gate verdict | **STOP notebook if gate fails** | Env/feature drift invalidating everything | report |
| 16 | Fold-level metrics | Per model per fold AUC | OOFs | fold_metrics table | 5 rows per model | Variance hidden by means | fold_metrics CSV |
| 17 | OOF ROC-AUC + paired deltas | OOF AUC per model; paired per-fold deltas vs m0 | OOFs | summary rows | Same-sign counts computed | Noise read as signal | model_summary CSV |
| 18 | Slice diagnostics | 7 mandatory slices per model (incl. `frequent_vs_rare_school_group` diagnostic-only, `Age_missing`) | OOFs + slices | slice table | n < 50 flagged non-evaluable; >0.02 drop vs m0 ⇒ escalated | Subgroup harm (the Phase 7 lesson) | slice_report CSV |
| 19 | Evidence classification | Apply §9 flagging rule per model: promotable evidence / no qualifying evidence / escalated | summary | decision table | Rule applied verbatim; no max-picking language | Auto-adoption | report |
| 20 | Leakage checklist | §13 instantiated per model | run state | checklist table | All items pass or run stops | All taxonomy layers | report |
| 21 | Artifact writes | All §14 files with pre-write guards | results | files | Guard trip ⇒ stop; manifest row per artifact | Overwrites | manifest CSV |
| 22 | Candidate log row | One v2-schema row | results | log candidate CSV | Main log byte-identical (assert) | Log corruption | log candidate |
| 23 | Executive conclusion | Classified table + explicit "no winner crowned; selection is a project director decision"; **Phase 9/10/11 remain locked** | — | markdown | Required closing statements present | Overclaim | report |

### 10.3 Model registry architecture

| model_key | Modelo | Estado | Dependencia | Preprocessing requerido | Config inicial pre-registrada | Riesgo | Condición de inclusión |
|---|---|---|---|---|---|---|---|
| `m0_random_forest_frozen` | RandomForestClassifier | Reference (gate) | sklearn (installed) | Shared F2 pipeline | `n_estimators=100, max_depth=5, random_state=42, n_jobs=-1` | None | Always (integrity gate) |
| `m1_logistic_regression` | LogisticRegression | Active candidate | sklearn | Shared + fold-fitted StandardScaler (numeric) | `max_iter=1000, random_state=42` | Convergence (mitigated by config) | Authorization note |
| `m2_random_forest_default` | RandomForestClassifier | Active candidate | sklearn | Shared F2 pipeline | `n_estimators=100, max_depth=None, random_state=42, n_jobs=-1` | Perceived as tuning (pre-registered, single) | Authorization note |
| `m3_extra_trees_default` | ExtraTreesClassifier | Optional candidate | sklearn | Shared F2 pipeline | `n_estimators=100, random_state=42, n_jobs=-1` | Low marginal info | Authorization note (first to drop) |
| `m4_hist_gradient_boosting` | HistGradientBoostingClassifier | Active candidate | sklearn | Shared F2 pipeline | `random_state=42, early_stopping=False` | None notable | Authorization note |
| `m5_hgb_native_missing` | HistGradientBoostingClassifier | Gated diagnostic | sklearn | F2 features, **no numeric imputation** (flags retained) | as m4 | Breaks strict same-preprocessing fairness ⇒ decision-ineligible alone | Explicit line in authorization note |
| `xgboost` | XGBClassifier | Deferred — Wave 2 | **NOT INSTALLED** | Shared F2 pipeline (if ever run) | to be pre-registered at Wave 2 gate | Env mutation | Separate Wave 2 note + pinned install |
| `lightgbm` | LGBMClassifier | Deferred — Wave 2 | **NOT INSTALLED** | Shared F2 pipeline (if ever run) | to be pre-registered at Wave 2 gate | Env mutation | Separate Wave 2 note + pinned install |
| `catboost` | CatBoostClassifier | Deferred — Wave 2, double-gated | **NOT INSTALLED** | Shared F2 pipeline only; **native-categorical School pathway blocked** | to be pre-registered at Wave 2 gate | School leakage temptation | Wave 2 note + School-policy reconfirmation |
| `deep_tabular` | MLP / TabNet / FT-Transformer / SAINT / NODE | Blocked | not installed | — | — | Cost; irreproducibility | GBDT plateau evidence + future-phase authorization |

### 10.4 (folded into 10.2) — eligibility, loop and gates are cells 12–15 above.

### 10.5 Preprocessing architecture per model

| Modelo | Numeric preprocessing | Categorical preprocessing | Missing-value strategy | Scaling needed | School policy | Riesgo de leakage | Diseño recomendado |
|---|---|---|---|---|---|---|---|
| m0 / m2 (RF) | fold-fitted median impute | fold-fitted most_frequent + OHE(ignore) | median + 7 flags + count (F2) | No | Excluded | Low (audited builder) | Reuse Phase 7 F2 pipeline verbatim |
| m3 (ET) | same | same | same | No | Excluded | Low | Same shared pipeline |
| m1 (LR) | fold-fitted median impute → fold-fitted StandardScaler | same OHE | same F2 | **Yes (model requirement, pre-registered)** | Excluded | Low; scaler fitted inside folds only | Shared pipeline + scaler step |
| m4 (HGB) | fold-fitted median impute | same OHE | same F2 | No | Excluded | Low | Same shared pipeline |
| m5 (HGB native, gated) | **none** — NaNs passed to HGB | same OHE | native NaN handling + flags + count retained | No | Excluded | Low for leakage; **high for comparability** | Diagnostic only; labeled fairness-breaking; never decision-eligible alone |
| Wave 2 GBDTs (future) | shared F2 pipeline | same OHE (no native-categorical shortcut) | F2 | No | **Excluded — hard gate** | Library-specific shortcuts | Pre-register at Wave 2 gate |

Invariants: same F2 features for all; no per-model feature engineering; all fitting inside training folds; no global statistics; no tuning.

### 10.6 Validation architecture

| Componente | Diseño esperado | Evidencia requerida | Stop condition |
|---|---|---|---|
| Frozen fold loading | Load committed file; assert count/labels/order/sha | sha256[:16] == `96937649526bcadb` | Any mismatch |
| M0 integrity gate | m0 OOF == 0.8116502602456482 ± 1e-6 | recomputed from in-run OOF | Gate fails ⇒ everything downstream uninterpretable |
| ROC-AUC per fold | `roc_auc_score` on val-fold proba | fold_metrics CSV | NaN/undefined AUC |
| OOF ROC-AUC | Full-vector AUC per model | model_summary CSV | — |
| `estimator.classes_` | Label 1 located exactly once before proba extraction | helper raises by design | Helper raises |
| Probability validity | finite, [0,1], no NaN | per-model asserts | Any violation |
| Paired fold deltas | model − m0 per fold; same-sign count | model_summary | — |
| Paired OOF comparison | model − m0 OOF delta vs 0.005436 flag | decision table | — |
| Slice diagnostics | 7 mandatory dims per model; n ≥ 50 policy; >0.02 drop ⇒ escalated | slice_report CSV | Escalation = flag for director review, never auto-decide |
| Model summary table | One row per model with classification | model_summary CSV | — |
| Leakage checklist per model | §13 instantiated | report section | Any failure ⇒ stop run |
| Artifact manifest | One row per written artifact (path, sha256, rows) | manifest CSV | Guard trip |

### 10.7 Artifact architecture

| Artifact | Path pattern | Producer section | Purpose | Overwrite policy | Required before acceptance |
|---|---|---|---|---|---|
| Per-model OOF | `outputs/oof/phase8_model_family_comparison_v1_<model_key>_oof_predictions.csv` | cell 14/21 | Independent recomputation currency | Never (pre-write guard) | Yes |
| Model summary | `outputs/validation/phase8_model_family_comparison_v1_model_summary.csv` | cell 17/21 | Primary comparison table | Never | Yes |
| Fold metrics | `outputs/validation/phase8_model_family_comparison_v1_fold_metrics.csv` | cell 16/21 | Fold-level diagnostics | Never | Yes |
| Slice report | `outputs/validation/phase8_model_family_comparison_v1_slice_report.csv` | cell 18/21 | Subgroup robustness | Never | Yes |
| Validation report | `outputs/reports/phase8_model_family_comparison_v1_validation_report.md` | cell 23 | Full narrative + tables + leakage checklists | Never | Yes |
| Candidate log | `outputs/reports/phase8_model_family_comparison_v1_experiment_log_candidate.csv` | cell 22 | v2-schema row; main log untouched | Never | Yes |
| Artifact manifest | `outputs/reports/phase8_model_family_comparison_v1_artifact_manifest.csv` | cell 21 | Path + sha256 + row count per artifact | Never | Yes |
| Acceptance record | `docs/08_model_comparison/phase8_acceptance.md` | post-run, project director | Closure decision (1–3 candidates or null result) | Human-authored | Yes (at closure) |

### 10.8 Fable → Codex fidelity contract (traceability)

| Decisión de Fable | Sección del notebook | Instrucción correspondiente para Codex | Cómo verificar fidelidad |
|---|---|---|---|
| Staged Wave 1, sklearn-only, no installs | cell 2 | "Assert external GBDTs not imported; any `pip install` = stop" | Env record + absence of installs in session log |
| F2 frozen, 21 features, School excluded | cells 9 | "Build F2 with audited Phase 7 builder; assert feature list and exclusions" | Feature-list assert output; flag-sum asserts |
| Frozen folds, sha-checked | cell 8 | "Load fold file; assert sha/rows/labels/order; never recompute" | Notebook assert output |
| M0 gate ± 1e-6 | cell 15 | "Stop the notebook if m0 ≠ 0.8116502602456482 ± 1e-6" | Gate verdict in report; independent recompute |
| Registry of 6 configs, cap ≤ 6, m5 gated | cell 11 | "Implement exactly the ratified registry; never add/substitute/alter a config" | Registry table diff vs brief §8 |
| Flagging rule, no winner crowned | cell 19 | "Classify per rule; selection language prohibited" | Decision-table wording |
| Slice guard incl. `Age_missing` | cell 18 | "All 7 mandatory slices; n ≥ 50; >0.02 ⇒ escalated" | slice_report contents |
| Pre-write guards + manifest | cell 21 | "Fail-if-exists on every path; write manifest" | Manifest vs filesystem |
| Main log protected | cells 5/22 | "Read-before/assert-after byte-identical" | Checksum asserts |
| No HPO/submissions/LB/Phase 9+ | cells 1/23 | Stop rules + closing statements | Report closing section |

---

## 11. Fold-Safe Implementation Design, if Later Authorized

No notebook is created now. The future Wave 1 notebook is bound by the §10 blueprint plus this contract: runs top-to-bottom from repo root; relative paths; `PROJECT_SEED = 42`; executed headless with `.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace` (the environment that produced and reproduced all Phase 6/6A/7/7B results: Python 3.13.13, scikit-learn 1.9.0, pandas 3.0.3, numpy 2.4.6); reuses the audited Phase 7 notebook-07 builders for the F2 feature block and fold-safe pipelines rather than rewriting them; records environment + `git rev-parse HEAD` + dirty flag in the report; two-role verification after the run (independent stdlib rank-AUC recomputation of every OOF file, the proven 6A/7 pattern). **Forbidden inside the notebook:** test-data fitting (test used only for contract checks; no Phase 8 inference), submissions, HPO of any form, installs, alternate configs, School in features, LB values, `logs/experiment_log.csv` writes, Phase 9/10/11 work.

---

## 12. Validation, Slice Reports and Acceptance Criteria

### 12.1 Acceptance of the planning package (level A)

| Criterion | Condition | Evidence source | What happens if it fails |
|---|---|---|---|
| Repository state verified | §1 all PASS at `7166c2e` | §1 table | Re-verify; stop if HEAD/forbidden paths differ |
| Phase 7/7B closure verified | Acceptance records commit-anchored (`42ef12a`/`7166c2e`) | §1, §2 | Phase 8 stays blocked |
| Phase 8 not previously executed | No `phase8_*` artifacts | §1 check | Treat as collision; investigate before anything |
| F2 verified | OOF 0.811650; 21 features; policies | §3 | Mark Not confirmed yet; block |
| Model candidates named & classified | §8 registry complete | §8 | Amend before ratification |
| References reviewed / deferred with reason | §5 table; compact summaries sufficed | §5 | Request targeted review |
| Theory-to-practice transfer | §5 table | §5 | Amend |
| Agents/skills plan | §6 | §6 | Amend |
| Metric & folds verified | §3/§4 | §3 | Block |
| Protected paths + prohibited actions listed | §13/§16 + runbook | this brief | Amend |
| Comparison protocol justified | §9 | §9 | Amend |
| Notebook blueprint included | §10 cell-by-cell | §10 | Amend |
| Fable→Codex fidelity contract | §10.8 + Deliverable C | §10.8 | Amend |
| HPO / submissions / LB blocked; School explicit; artifacts/log policy explicit | §4, §8, §9, §14 | this brief | Block |
| Project director approval required before execution | §17 | §17 | Absolute |
| Phase 9/10/11 locked | §18-equivalent statements (§4, §16, §17) | this brief | Absolute |

### 12.2 Acceptance of a future authorized execution (level B)

| Criterion | Condition | Evidence source | What happens if it fails |
|---|---|---|---|
| Identical folds & feature set for all models | fold sha + feature asserts pass per model | notebook asserts + report | Stop run |
| M0 integrity gate | 0.8116502602456482 ± 1e-6 | report + independent recompute | Stop; everything uninterpretable |
| No model-specific feature leakage | shared builder; checklist per model | §13 checklist | Stop |
| No HPO | configs byte-identical to ratified registry | registry diff | Stop; record violation |
| No submissions; no LB | no files in `outputs/submissions/`; no LB references | git status + report | Stop |
| OOF validity | finite, [0,1], no NaN, no single-class fold, fold map == frozen | per-model asserts | Stop |
| `classes_` verified | label 1 exactly once per fit | helper design | Stop |
| Fold-level metrics saved | fold_metrics CSV complete | artifact | Block acceptance |
| OOF ROC-AUC + paired deltas computed | model_summary complete | artifact | Block acceptance |
| Slice diagnostics with min-n policy | slice_report complete; n < 50 flagged; escalations listed | artifact | Block acceptance |
| Artifact manifest created | manifest rows == written files, sha-matched | manifest CSV | Block acceptance |
| Candidate log separate; main log untouched | byte-identical assert | checksum | Stop |
| Validation report generated | report complete with leakage checklists | artifact | Block acceptance |
| No forbidden diffs; only expected untracked artifacts | post-run git checks | runbook §12 | Stop |
| Independent recomputation matches | ≤ 1e-9 per OOF file | audit procedure | Block acceptance until resolved |
| Phase 9/10/11 remain locked | closing statements present; no out-of-scope work | report | Block acceptance |

**Pre-registered edge cases:** model fails to converge / errors ⇒ record as `failed_run`, never substitute a config, continue with remaining registry, report; AUC undefined on a slice ⇒ flag non-evaluable; escalated slice ⇒ project director review with the slice table (the Phase 7 F1/F5/F3 pattern); guard trip / HEAD mismatch / fold mismatch / proba invalid / `classes_` failure / mid-run pressure to add models or change configs ⇒ **stop the run**.

---

## 13. Leakage Control Strategy

Instantiates `docs/05_methodology/leakage_checklist_phase6.md` for model comparison:

| Layer | Phase 8 control |
|---|---|
| Data / external | Official CSVs only; references = methodology only; registry contains no externally derived values |
| Test-to-train | Test rows only for contract checks; **no Phase 8 fitting touches test; no inference; no submission** |
| Preprocessing / imputation / encoding | Shared fold-fitted F2 pipeline; LR scaler fold-fitted; m5's NaN pass-through is row-wise (no fitting) |
| Feature computation | F2 frozen; **no per-model feature engineering by construction** |
| Target encoding / feature selection / dim reduction / rare grouping | Absent (blocked) |
| Role statistics | Only fold-fitted OHE of raw categoricals |
| HPO / model selection | Frozen registry; run cap; flagging rule ≠ adoption; director decides; **searching = stop condition** |
| Model-specific shortcuts | CatBoost native-categorical (School) pathway explicitly blocked; HGB native-NaN allowed only as the gated m5 diagnostic |
| Leaderboard | Untouched |
| Confound/group | Folds frozen; grouped CV dormant (refined D2); new duplication evidence = stop, not protocol change |
| Diagnostic-only variables | `frequent_vs_rare_school_group` and `measurement_completeness_group` stay out of all feature matrices (assert) |
| Verification doctrine | Two-role rule: in-notebook self-checks **plus** post-run independent stdlib rank-AUC recomputation of every OOF file by a different role/session |

---

## 14. Artifact, Documentation and Git Plan

**Created/updated in this planning run (authorized set only):**

```text
docs/08_model_comparison/phase8_master_planning_brief.md      (this file)
docs/08_model_comparison/phase8_operator_runbook.md
docs/08_model_comparison/prompt_codex_phase8_execution_plan.md
```

**Future artifacts if Wave 1 execution is authorized (names reserved; NOT created now):** the §10.7 table — notebook 08, six-at-most per-model OOF files, model_summary, fold_metrics, slice_report, validation_report, experiment_log_candidate, artifact_manifest, and `docs/08_model_comparison/phase8_acceptance.md` at closure. **Reserved for a future gated Wave 2:** `notebooks/08b_phase8_external_gbdt_comparison.ipynb` + `phase8_model_family_comparison_v2_external_*` artifacts. The orientative `phase8_execution_plan.md` / `phase8_model_registry.md` / `phase8_validation_and_acceptance_criteria.md` are **subsumed by §§7–12 of this brief** (separate near-duplicate files would create documentation drift); they can be extracted verbatim later if the project director prefers.

**Git policy:** this run stages and commits **nothing** (`git add .` and `git commit -a` are permanently forbidden). Recommended sequencing if the project director proceeds: (1) selectively commit the three planning docs (one explicit instruction, individual `git add` per file) so the execution session verifies a planning-inclusive hash; (2) after execution + audit + signed acceptance, a second selective commit of notebook + artifacts + acceptance, with the resulting hash recorded back into the acceptance record (the established `42ef12a` → `7166c2e` pattern); planning docs, notebooks, artifacts and acceptance records must not be mixed into one undifferentiated commit without that declared strategy. Main log untouched; v2 migration stays separately gated.

---

## 15. Risks, Failure Modes and Mitigations

| Risk | Failure mode | Mitigation |
|---|---|---|
| Phase 8 drifts into HPO | "Just try a few depths/learning rates" | Frozen registry with exact constructors; cap ≤ 6 runs; config change = stop condition; HPO gates live in Phase 10 (7 conditions, `research_notes_hpo.md`) |
| Dependency mutation mid-run | `pip install xgboost` inside the comparison session | Wave 2 hard gate; cell-2 assert that external GBDTs are absent in Wave 1; installs = stop |
| Unfair preprocessing advantage | Per-model pipeline tweaks | Shared audited F2 builder; deviations only where pre-registered as model requirements (LR scaler) or gated diagnostics (m5) |
| m5 misread as a decision result | Native-NaN HGB "wins" and gets adopted | m5 labeled fairness-breaking, decision-ineligible alone; any adoption path requires its own future pre-registered design |
| Winner-crowning by max-picking | Top OOF treated as selection | Flagging rule + explicit "no winner" language; selection only in `phase8_acceptance.md` by the director |
| Slice harm hidden by global gains | The Phase 7 F1/F5/F3 lesson | Mandatory slice guard incl. `Age_missing` (n = 435, 8 positives — known fragile); >0.02 ⇒ escalated |
| Threshold misapplied across families | 0.005436 is RF-noise-derived | Documented limitation; flag-not-adopt semantics; per-family noise is a Phase 9 question |
| Artifact overwrite / unanchored results | Lost audit trail | Pre-write guards; manifest with sha256; selective-commit + hash-record pattern |
| Environment drift | Irreproducible numbers | Pinned venv asserted in cell 2; M0 gate catches drift numerically |
| Generator-verifier collusion | Unreviewed defects | Two-role rule: independent static review + independent OOF recomputation |
| Phase 9/10/11 pull | "Tune the winner / submit the winner" | gateguard + locks in §4/§17; refusal wired into Deliverable C |

---

## 16. Explicit Non-Actions

This planning run did **not**: execute Phase 8 or any experiment; create or execute any notebook; train any model; run any model-family comparison; install any package; generate any OOF/validation/report/submission artifact; run HPO; consult the public leaderboard; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`, or any tracked file; stage anything; commit anything; push anything; open Phase 9, Phase 10 or Phase 11. The only filesystem writes were the three authorized documents under `docs/08_model_comparison/`.

---

## 17. Required Project Director Authorization Before Execution

Phase 8 execution may begin only after the project director explicitly and in writing:

1. Approves this brief and the runbook (or records amendments, which then freeze).
2. **Ratifies the §8 registry**: model list, exact constructor configs, statuses, the m5 gate decision (authorize or strike), the cap (≤ 6 trained runs), and the Wave 1/Wave 2 boundary.
3. Confirms the operative thresholds: flag rule 0.005436 + ≥ 4/5 same-sign + slice guard (n ≥ 50, 0.02 escalation); M0 tolerance ± 1e-6.
4. Confirms the §10.7/§14 artifact names and the no-commit-without-instruction policy.
5. Records the authorized starting commit hash (currently `7166c2e`; it advances if these planning docs are committed first — recommended; the Project Authorization Note must state the hash the session must verify).
6. Issues an explicit "execute Phase 8 Wave 1" instruction referencing `prompt_codex_phase8_execution_plan.md` with the signed Project Authorization Note (runbook §10 format).

Wave 2 (external GBDTs) additionally requires its own note covering: authorization to install named packages with pinned versions into the project venv (or a separate env decision), Python 3.13 compatibility verification, pre-registered Wave 2 configs, and the CatBoost School-policy reconfirmation. Absent any item: **planned, not executable.**

---

## 18. Recommended Next Step

**Option A — Review the generated Phase 8 planning package; execution remains blocked until explicit project director authorization.**

Concretely: (1) read this brief top-to-bottom; (2) ratify or amend §8 (registry/configs/cap/m5) and §17's parameters; (3) decide whether to selectively commit the three planning docs first (recommended — execution should verify a planning-inclusive hash, and per the runbook, not start from an untracked planning package); (4) when ready, issue the authorization per §17 using Deliverable C. **Phase 9, Phase 10 and Phase 11 remain locked throughout. Future phases remain locked.**
