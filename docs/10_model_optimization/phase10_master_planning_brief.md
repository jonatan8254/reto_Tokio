# Phase 10 Master Planning Brief — Complete Model Optimization and Controlled Model Selection

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Planning brief (Deliverable A of the Phase 10 planning package). **Planning only — nothing here is executed.**
**Date:** 2026-06-19
**Author role:** Opus strategic architect / methodology auditor (first brain of the Opus → Codex → Opus separation).
**Baseline commit at planning time:** `12c59b8` (*planning: add phase 9b lite transition memo*).

> This brief designs Phase 10. It does not open Phase 10. It trains nothing, tunes nothing, creates no notebook, generates no submission, and selects no winner. Execution remains blocked until a signed Phase 10 Project Authorization Note exists. Phase 11 remains locked.

---

## 0. Executive Verdict

Phase 10 is designed here as a **bounded, leakage-safe, selection-bias-aware HPO and controlled candidate-selection phase** operating only on the frozen F2 feature set and the frozen 5-fold split, with **ROC-AUC on out-of-fold (OOF) positive-class probabilities as the single primary metric**. The inherited evidence supports a narrow scope:

- **M1 (`m1_logistic_regression`)** is the **primary optimization candidate** (candidate-with-warning), because it is the strongest local ranker across every Phase 9A lens (ROC, PR-AUC, neg-class AP, Brier, top-k) and 4/5 folds vs M0 — but it is **not a winner**, and HPO cannot be allowed to paper over its `Age_missing=1` collapse or its robust-size `Position=QB` loss.
- **CatBoost (`catboost`)** is the **secondary / observe candidate**, eligible only for **limited** tuning and only after its robust-slice instability is understood (backlog B5); it trails M1 and is more slice-unstable.
- **M0 (`m0_random_forest_frozen`)** stays the **anchor/reference** — **no HPO by default**.
- **XGBoost and LightGBM** stay **dropped for now** (`no_qualifying_evidence`, near-duplicate, sub-M0) — **no deep HPO by default**; reopening requires a written methodological justification and at most a small diagnostic budget.

Six of the seven documented HPO activation gates are satisfied; **one is not** (the experiment-log-schema-active gate depends on the deferred log-v2 migration decision). Phase 10 therefore remains correctly **locked** pending project-director authorization, and this brief routes the open gate explicitly rather than waving it through.

**Verdict: a complete Phase 10 plan is ready for review; execution stays blocked.**

---

## 1. Repository State Verification

Verification run read-only at planning time (no mutation, no staging):

| Check | Expected | Observed | Status |
|---|---|---|---|
| `git rev-parse --short HEAD` | `12c59b8` or documented successor preserving Phase 9B-Lite | `12c59b8` | PASS |
| Staged files | none | none | PASS |
| `git diff --check` | clean | clean | PASS |
| Forbidden-path tracked diffs (`data/input`, `notebooks/_official`, `references`, `outputs/submissions`, `logs/experiment_log.csv`, `.vscode/settings.json`) | empty | empty | PASS |
| `logs/experiment_log.csv` | unchanged | unchanged (no diff) | PASS |
| `docs/10_model_optimization/` | absent (to be created by this planning run) | absent → created | INFORMATIONAL |
| Recent log | …`4bbcd7a` → `0207436` → `eb55a18` (accept 9A) → `12c59b8` (9B-Lite) | matches | PASS |

The Phase 9A artifacts created during the strategic review are now committed (no longer untracked) under `eb55a18`/`12c59b8`. Baseline is **safe and as documented**; planning may proceed.

---

## 2. Evidence Reviewed

Read-only, no execution. Governing and evidentiary documents consulted:

- **Contract:** `docs/00_project_contract/challenge_brief.md`, `docs/00_project_contract/submission_checklist.md`.
- **Plan/methodology:** `docs/01_project_planning/project_execution_plan_v3.md` (§6 validation contract, §7 leakage contract, §11–§13/§16 modeling+HPO blueprint, §19 skills/agents), `docs/05_methodology/validation_protocol_phase6.md`, `docs/05_methodology/leakage_checklist_phase6.md`, `docs/05_methodology/phase5_execution_decisions.md` (referenced).
- **Feature evidence:** `docs/07_feature_engineering/phase7_acceptance.md` (F2 adopted), `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md` (F4 rejected; keep F2).
- **Model evidence:** `docs/08_model_comparison/phase8_acceptance.md` (Wave 1), `docs/08_model_comparison/phase8_wave2_acceptance.md` (Wave 2).
- **Diagnostics:** `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md`, `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md`, `docs/09_auc_ranking_diagnostics/phase9b_lite_transition_memo.md`; `outputs/reports/phase9a_auc_ranking_diagnostics_v1_validation_report.md`; `outputs/validation/phase9a_auc_ranking_diagnostics_v1_*` (global_metrics, topk_quantile, slice_report, fold_paired, score_distribution, disagreement); `notebooks/09a_auc_ranking_diagnostics.ipynb` (static reference only).
- **Research:** `docs/04_research/research_notes_hpo.md`, `research_notes_validation.md`, `research_notes_reproducibility.md`, `research_notes_leakage.md`, `research_notes_tabular_models.md`, `research_notes_feature_engineering.md`, `pdf_key_findings.md` (Cawley & Talbot model-selection/overfitting; The Kaggle Book; Optuna paper; ISLP; Kuhn & Johnson — referenced through summaries per the reading policy).

No metric was recomputed in this planning run. All numbers below are quoted from the accepted Phase 8/9A records.

---

## 3. Numerical Results and Frozen Model Status

Inherited OOF ROC-AUC on the frozen folds (Phase 9A independently reproduced, max abs diff ≤ 1.11e-16):

| model_key | OOF ROC-AUC | PR-AUC (AP) | neg-class AP | Brier | folds + vs M0 | folds + vs M1 | inherited status |
|---|---:|---:|---:|---:|---:|---:|---|
| `m0_random_forest_frozen` | 0.8116502602456482 | 0.863811 | 0.778719 | 0.158603 | — | 1/5 | anchor / reference |
| `m1_logistic_regression` | 0.8270821069632867 | 0.874184 | 0.790499 | 0.141434 | 4/5 | — | **primary candidate-with-warning** |
| `catboost` | 0.8202943968641223 | 0.870463 | 0.788618 | 0.147291 | 4/5 | 2/5 | secondary / observe (escalated) |
| `xgboost` | 0.8113477083751576 | 0.864025 | 0.781012 | 0.157459 | 1/5 | 1/5 | dropped (`no_qualifying_evidence`) |
| `lightgbm` | 0.8062204891415921 | 0.858134 | 0.777041 | 0.166400 | 1/5 | 0/5 | dropped (`no_qualifying_evidence`) |

- Global positive rate: **0.648328** (majority-positive; mild imbalance). AP baseline 0.6483; neg-class AP baseline 0.3517.
- Rank correlations: M1↔CatBoost Spearman **0.818**; XGB↔LGBM **0.952** (near-duplicate).
- Pre-registered evidence rule (inherited from Phase 7/8): **promote only if `OOF − OOF(M0) ≥ 0.005436` AND same-sign positive folds ≥ 4/5 AND slice guard clear.** Slice guard = any mandatory slice with n ≥ 50 degrading > 0.02 AUC vs M0.
- **No final winner. No submission-ready model. No HPO executed. No submissions. No leaderboard used.**

Frozen infrastructure to preserve unchanged: folds `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`, fold SHA256[:16] `96937649526bcadb`, 2781 rows, folds 0..4; OOF schema `Id,fold,y_true,y_pred_proba`. F2 feature set per §4.

---

## 4. Frozen Decisions Preserved

Phase 10 inherits and **must not alter** any of the following:

1. **Metric:** ROC-AUC via `sklearn.metrics.roc_auc_score` on positive-class probabilities for `Drafted=1`, extracted only after verifying `estimator.classes_` contains label `1` (never blind `predict_proba(X)[:,1]`).
2. **Folds:** the frozen 5-fold file, loaded and integrity-asserted (2781 rows, folds 0..4, SHA match), never recomputed for selection.
3. **Feature set:** **F2** — base Phase 6 features (`Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type, Position_Type, Position`) + seven missingness flags (`Age_missing, Sprint_40yd_missing, Vertical_Jump_missing, Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing, Shuttle_missing`) + `available_measurement_count`. **No new features in Phase 10.** F4 rejected; BMI not adopted; `measurement_completeness_group` diagnostic-only.
4. **Imputation/encoding policy:** median imputation + fold-safe one-hot encoding, fitted inside training folds only.
5. **School:** excluded from every feature matrix; diagnostic slice dimension only.
6. **No external data; no public leaderboard** for any selection/tuning/preprocessing decision.
7. **Candidate roles (Phase 8 + 9A + 9B-Lite):** M0 anchor; M1 primary candidate-with-warning; CatBoost secondary observe; XGBoost/LightGBM dropped `no_qualifying_evidence`.
8. **Artifact/log governance:** versioned `experiment_id`/`run_id`, check-and-fail on existing paths, candidate logs under `outputs/reports/`, `logs/experiment_log.csv` untouched until a separate human-approved merge.

---

## 5. Phase 10 Purpose and Non-Purpose

**Purpose (designed, not executed):** bounded HPO of the eligible candidates on F2/frozen folds; strict OOF generation; honest tuned-vs-default comparison against M0/M1/CatBoost baselines; overfitting and selection-bias control; fold-level and slice-level stability review (including inherited warnings); production of a phase-gated candidate-selection recommendation; preparation for a future Phase 11 **without opening it**.

**Non-purpose (explicitly out of scope for the whole phase):** executing Phase 10 now; training/HPO in this planning run; creating notebooks now; submissions; leaderboard use; opening Phase 11; declaring a final winner or submission-ready model; ensembles/blending/stacking; probability calibration fitting; threshold tuning; modifying `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`; external data; School-as-feature; staging/commit/push.

---

## 6. Alignment with Existing Planning and Methodology Documents

| Source document | Key constraint or decision inherited | How Phase 10 planning must respect it | Risk if ignored | Status |
|---|---|---|---|---|
| `docs/00_project_contract/challenge_brief.md` | ROC-AUC on positive-class proba; official files only; no external data; LB is sanity-check only; reproducible/auditable | Primary metric = ROC-AUC; F2 from official files only; no LB in any tuning decision | Disqualification / invalid result | Confirmed |
| `docs/00_project_contract/submission_checklist.md` | Submission format `Id,Drafted`, 696 rows; submissions are a later-phase act | Phase 10 produces **no** submission; checklist cited only as Phase 11 handoff context | Premature/invalid submission | Confirmed |
| `project_execution_plan_v3.md` §6 | Frozen folds loaded + integrity-asserted; OOF anchor; class-index check; slice diagnostics mandatory | All Phase 10 runs load the frozen fold file, assert integrity, verify `classes_`, emit slice report | Leakage / non-comparable results | Confirmed |
| `project_execution_plan_v3.md` §7 | Fit-scope rule; blocked globals; no LB leakage; pre-registered experiment list | HPO search space, candidates, budget pre-registered before running; all learned steps fold-fitted | Selection bias / leakage | Confirmed |
| `project_execution_plan_v3.md` §13/§16.6 | Bounded HPO blueprint; Optuna fixed seed; ≤50–100 trials; objective OOF ROC-AUC; 7 activation gates | Phase 10 design instantiates §13 exactly; gate 5 (log-schema) flagged open | Gate erosion | Confirmed (gate 5 open) |
| `docs/05_methodology/validation_protocol_phase6.md` | StratifiedKFold(5, shuffle, 42); OOF; slice schema; LB prohibitions | Reuse the frozen splitter spec; never re-tune on LB | Non-comparability | Confirmed |
| `docs/05_methodology/leakage_checklist_phase6.md` | Fold-fitted learned transforms; HPO/model selection blocked until Phase 10 after gates | Phase 10 is the first phase allowed HPO, and only post-gates | Leakage | Confirmed |
| `docs/07_feature_engineering/phase7_acceptance.md` + `phase7b_role_interaction_acceptance.md` | **F2 adopted; F4 rejected; School excluded; mean imputation not adopted** | Phase 10 freezes F2; no feature re-exploration | Scope creep / leakage | Confirmed |
| `docs/08_model_comparison/phase8_acceptance.md` (Wave 1) | M1 candidate-with-warning; RF/ExtraTrees/HGB rejected; M0 anchor | M1 primary; M0 anchor; rejected sklearn families not reopened | Re-litigating closed evidence | Confirmed |
| `docs/08_model_comparison/phase8_wave2_acceptance.md` (Wave 2) | CatBoost escalated; XGB/LGBM `no_qualifying_evidence`; separate GBDT env; `.venv` untouched | CatBoost secondary/limited; XGB/LGBM dropped; GBDT runs use separate env, never mutate `.venv` | Env contamination / unjustified promotion | Confirmed |
| `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md` + `phase9a_improvement_backlog.md` | M1 strongest local ranker but warned (Age_missing=1, QB); CatBoost slice-unstable; B5/B8 HPO-locked | Phase 10 carries B5/B8 as entry conditions; warnings tracked, not tuned away | Overfitting to fragile slices | Confirmed |
| `docs/09_auc_ranking_diagnostics/phase9b_lite_transition_memo.md` | M1 primary; CatBoost secondary observe; XGB/LGBM dropped; Phase 10/11 locked | Phase 10 candidate scope = exactly this; cannot reinterpret 9A as final selection | Contradicting the immediate predecessor | Confirmed |
| `docs/04_research/research_notes_hpo.md` | 7 HPO gates; Optuna future; HPO improves stable candidates, not rescues methodology | Gates enumerated in §15/§21; budget conservative; tuned-vs-default honesty required | Premature/over-tuning | Confirmed |

### Conflicts found

- **None blocking.** One reconciliation note: `project_execution_plan_v3.md` §12 anticipated a full **Phase 9** consolidation feeding "1–3 candidates" into Phase 10; the project instead executed **Phase 9A (diagnostic) + Phase 9B-Lite (transition memo)**. The 9B-Lite memo (most-recent accepted evidence, top of the §4-prioritization order) explicitly defines the carry/secondary/drop set, which **satisfies the spirit of the v3 "1–3 candidates" gate** with M1 (primary) and CatBoost (secondary). This is recorded as an informational reconciliation, not a contradiction. The v3 §16.6 note that the **log-schema gate has a hidden dependency on the deferred v2 migration** is carried forward as the one open gate (§21).

## 7. Planning Document Consistency Checks

- [x] Phase 10 cannot contradict Phase 9B-Lite → candidate scope = M1 primary, CatBoost secondary, XGB/LGBM dropped, M0 anchor.
- [x] Phase 10 cannot reinterpret Phase 9A as final model selection → 9A is diagnostic; no winner inherited.
- [x] Phase 10 cannot unlock Phase 11 → Phase 11 stays locked; handoff is design-only (§24/Section 24).
- [x] Phase 10 cannot convert CatBoost into a winner without posterior evidence → CatBoost limited/secondary, tuned only post-B5, never auto-promoted.
- [x] Phase 10 cannot reopen XGBoost/LightGBM for deep HPO unless a strong documented methodological justification exists → default = no deep HPO; reopening = written justification + small diagnostic budget only.
- [x] Phase 10 must preserve M1 primary / CatBoost secondary-observe / M0 anchor.
- [x] Phase 10 must keep ROC-AUC primary; PR-AUC/top-k/lift/Brier/slices/score-distributions are complementary diagnostics only.
- [x] Phase 10 must preserve the frozen validation/fold protocol.
- [x] Phase 10 must protect against overfitting, selection bias, and leaderboard chasing.

All consistency checks pass at planning level.

## 8. Scientific and Methodological Evidence Transfer

| Source / Reference | Methodological principle | Phase 10 practical decision | Artifact or planning section affected | Risk mitigated | Limitation / caution |
|---|---|---|---|---|---|
| Cawley & Talbot (model selection / overfitting in performance evaluation) | HPO overfits the validation criterion; repeated selection biases estimates | Conservative pre-registered search spaces; fixed budget; repeated-CV (different splitter seeds, secondary) confirmation on the tuned winner before any acceptance | §13 search space, §14 budget, §16 controls, §17 slice/stability | Selection-bias-inflated OOF | Repeated-CV is descriptive confirmation, not a new selection rule |
| The Kaggle Book (2nd ed.) | Disciplined tuning **after** baseline/validation/features are stable; diversity ≠ count | HPO only post-gates; XGB/LGBM near-duplicate (Spearman 0.952) not re-tuned for "more models" | §11 eligibility, §12 strategy | Wasted budget on redundant weak rankers | Default-config result ≠ tuned ceiling |
| Optuna (next-generation HPO framework) | Sampler/pruner with fixed seed; reproducible studies; maximize objective | Optuna TPE, fixed sampler seed, `direction="maximize"`, study persistence, sequential-before-parallel; pruning only if intermediate metrics are meaningful | §12/§13 design, §19 artifacts | Non-reproducible tuning | Pruning on CV folds can mislead — use cautiously |
| ISLP (Intro to Statistical Learning) | OOF/CV estimates have variance; AUC must use scores not labels | OOF ROC-AUC objective; report fold mean/std; treat single-realization leads as provisional (backlog B3) | §15 metric protocol, §17 stability | Fold-luck mistaken for signal | n=2781 — fold-std ≈ 0.03 is non-trivial |
| Kuhn & Johnson (feature engineering & selection; subgroup analysis) | Subgroup/slice divergence; small-n slices are high variance | Min-n slice rules (n≥50 descriptive; fragile flag when positives sparse); Age_missing=1 (8 positives) never decisive alone | §17 slice strategy | Over-reading fragile slices | Multiplicity across many slices/metrics |
| `research_notes_hpo.md` | 7 activation gates; HPO objective = fixed-fold mean/OOF ROC-AUC; log trials reproducibly | Gate checklist enforced pre-run; objective fixed; full trial logging into candidate artifacts | §15/§21 gates, §13 governance | Premature HPO | Gate 5 (log schema) open — routed to director |
| `research_notes_reproducibility.md` | Notebook-first, fixed seeds, traceable outputs; no manual edits | Phase 10 notebook standard (§14/Section 18); versioned artifacts; no manual prediction edits | §14 notebook, §19 artifacts | Unreproducible/unauditable runs | Log v2 migration still deferred |
| `research_notes_leakage.md` / leakage checklist | Learned transforms fold-fitted; test only for inference; no LB leakage | Per-run leakage checklist instantiated; HPO inside CV with fold-fitted preprocessing | §16 controls | Pipeline/target/LB leakage | CatBoost native categoricals tempt School leakage — keep `cat_features=[]` |
| `research_notes_tabular_models.md` | Native missing-value handling differs across GBDTs; small-n favors simpler robust models | Document M1 (linear) vs CatBoost (GBDT) tuning differences; prefer simpler within noise | §12 strategy | Mis-specified tuning | XGB/LGBM age-missing slice curiosity is fragile (B6) |

References inform methodology only — **no external athlete/school/NFL data** is imported.

## 9. ECC Agents and Skills Plan

Live `/plugin list ecc@ecc` was **not executed** in this planning run (planning-only, read-only). The inventory below is taken from the **documented** `project_execution_plan_v3.md` §19 list and the harness-confirmed agent set; mark any divergence at execution time. **Status: documented, not freshly verified → treat as `Not confirmed yet` until a live check at execution.**

| Stage or need | Agent/skill suggested | Use proposed | Risk mitigated | Activation condition |
|---|---|---|---|---|
| Independent read of this planning package | `mle-reviewer` / `code-reviewer` (agent) | Read-only review of the brief/runbook/prompts vs governing docs | Self-certification of planning | Now (read-only) |
| Lineage / state questions | `code-explorer` (agent) | Trace OOF/fold artifact lineage read-only | Drift from frozen state | Now (read-only) |
| Hidden-assumption / untracked-artifact sweep | `silent-failure-hunter` (agent) | Pre-execution sweep for path collisions / silent fallbacks | Artifact overwrite / silent failure | Pre-execution review |
| Phase 10 notebook implementation (future) | Codex + `python-reviewer` / `python-patterns` / `python-testing` | Implement + review the HPO notebook under governance | Buggy/unsafe implementation | After signed authorization |
| HPO governance checklist (conceptual) | `gateguard` / `safety-guard` / `verification-loop` (skills) | Conceptual pre-action checklists (no execution authority) | Gate erosion | Now (advisory only) |
| Git discipline | `git-workflow` (skill) | Advisory only — `CLAUDE.md` Hard Git rules always win | Forbidden git ops | Always advisory |
| Post-execution audit (future) | `mle-reviewer` + `code-reviewer` (agents) | Independent recomputation/audit of Phase 10 outputs (two-role rule) | Generator==verifier collusion | After Codex execution |

**Classification:** (1) *Use now in planning* — `mle-reviewer`/`code-reviewer`/`code-explorer` (read-only), `gateguard`/`verification-loop` (advisory). (2) *Keep available, don't invoke unless needed* — `silent-failure-hunter`, `architect`/`planner`, `doc-updater`. (3) *Execution only* — `python-*`, `mle-workflow`, `eval-harness`, `build-error-resolver`. (4) *Future/prohibited phases* — anything submission/Phase-11-oriented. (5) *Risky/prohibited here* — none required; **do not install anything**. No concrete gap justifies a new agent/skill; the installed set covers Phase 10 needs. New assets must **never** be recommended for submissions, leaderboard optimization, external sports data, scraping, autonomous LB loops, deployment, or app/DB work.

## 10. Proposed Phase 10 Block Architecture

| Block | Name | Objective | Required evidence | Methodological basis | Outputs planned | Risks mitigated | Advancement condition |
|---|---|---|---|---|---|---|---|
| P10-B0 | Gate & integrity verification | Confirm HEAD, folds, F2, candidate baselines, gates | Authorized hash; fold SHA `96937649526bcadb`; F2 spec; M0/M1/CatBoost OOF | v3 §6/§7; HPO gate 1–7 | gate-check log lines in report | Running on wrong baseline | All gates pass incl. authorization note |
| P10-B1 | Pre-HPO slice diagnosis (B5/B3) | Understand CatBoost slice instability + M1 lead stability **before** tuning | Phase 9A slice/fold/disagreement artifacts | Cawley & Talbot; Kuhn & Johnson | diagnosis section in report (read-only over existing OOF) | Tuning before understanding | Diagnosis documented |
| P10-B2 | M1 bounded HPO (primary) | Tune M1 within pre-registered space; OOF ROC-AUC objective | F2; frozen folds; M1 baseline 0.827082 | research_notes_hpo; Optuna; v3 §13 | `phase10_..._hpo_results.csv`, M1 OOF, model_summary | Over-tuning / leakage | Search space + budget respected; leakage checklist clear |
| P10-B3 | CatBoost limited HPO (secondary, conditional) | Limited tuning **only if** B5 diagnosis justifies | B5 outcome; CatBoost baseline 0.820294; separate GBDT env | v3 §16.8; Wave 2 acceptance | CatBoost OOF, hpo_results (separate env) | Promoting unstable model | B5 justifies AND env-isolation confirmed |
| P10-B4 | Comparison & stability | Tuned-vs-default deltas; fold-level paired deltas; repeated-CV confirmation | B2/B3 OOF; M0/M1 anchors | ISLP; §7.9 v3 | comparison tables, selection-bias warning report | Selection bias / fold-luck | Paired deltas + repeated-CV reported honestly |
| P10-B5 | Slice & selection-bias review | Slice safety vs global gains; multiplicity acknowledgment | B2/B3 slice reports | Kuhn & Johnson | slice_report, selection_bias_warning_report | Cherry-picking / fragile-slice promotion | Robust-slice degradation flagged |
| P10-B6 | Candidate recommendation & acceptance draft | Accept/observe/reject/defer per candidate; **no winner** | All above | v3 §12/§13 governance | validation_report, experiment_log_candidate, acceptance draft | Implicit winner declaration | Director-signed acceptance (separate step) |

XGBoost/LightGBM appear in **no** block by default; a future reopening would add a clearly-labeled diagnostic-only sub-block under a separate written justification.

## 11. Candidate Scope and Eligibility

| Candidate | Current status inherited | Phase 10 eligibility | Optimization depth allowed | Required justification | Main risk | Default decision |
|---|---|---|---|---|---|---|
| `m1_logistic_regression` | candidate-with-warning (strongest local ranker) | **Primary** | Standard bounded HPO | Already justified by Phase 8/9A evidence | Tuning hides Age_missing=1 / QB warnings | Tune within pre-registered space; remains not-winner |
| `catboost` | escalated / observe (beats M0, trails M1) | **Secondary** | **Limited** HPO, conditional | Requires B5 slice-instability diagnosis first | Overfitting fragile/robust slices | Limited tuning only if B5 justifies; else observe |
| `m0_random_forest_frozen` | reference anchor | **Anchor/reference only** | **None by default** | Anchor must stay fixed for paired deltas | Drift of the comparison baseline | Keep frozen config (100, depth 5, seed 42) |
| `xgboost` | `no_qualifying_evidence` (≈/below M0, near-dup) | **Dropped for now** | **None by default** | Reopening needs written methodological justification | Resurrecting a redundant weak ranker | Do not tune; diagnostic reference only |
| `lightgbm` | `no_qualifying_evidence` (weakest, near-dup) | **Dropped for now** | **None by default** | Reopening needs written methodological justification | Same as XGBoost | Do not tune; diagnostic reference only |

Rules: M1 may be optimized but stays **not a final winner**; CatBoost only secondary/limited and only if 9A/9B-Lite evidence justifies; M0 stays anchor (no exploratory HPO); XGB/LGBM no deep HPO by default; any XGB/LGBM reopening = written justification + **at most a small diagnostic budget**; **no model may be declared winner or submission-ready during Phase 10 or its planning.**

## 12. HPO Strategy by Candidate Family

- **M1 LogisticRegression (primary):** linear model on F2 with fold-fitted median imputation + one-hot + standardization. Tunable: regularization strength `C`, penalty type (`l2` default; `l1` via `saga`), `class_weight` (`None` vs `balanced` — relevant under majority-positive base rate, affects fitted coefficients hence ranking), `solver` (compatible with chosen penalty). Fixed: F2 features, fold protocol, imputation/scaling policy, `max_iter` set high enough to converge (convergence is a correctness requirement, not a tuning lever). **HPO cannot fix the `Age_missing=1` slice** — that is a representation issue, tracked as a warning, not a tuning target.
- **CatBoost (secondary, limited, conditional on B5):** GBDT with `cat_features=[]` (School still excluded; no native categorical encoding). Tunable (small): `depth`, `learning_rate`, `l2_leaf_reg`, `iterations`, `border_count`, fixed `random_seed`. Forbidden: early stopping using any test/eval signal that touches selection; `eval_set` on test; native categorical handling. Runs in the **separate Wave 2 environment**, never mutating `.venv`/`requirements.txt`.
- **M0 RandomForest (anchor):** no tuning; frozen `(n_estimators=100, max_depth=5, random_state=42)` reproduced from persisted OOF for paired comparison.
- **XGBoost/LightGBM (dropped):** no tuning by default. A reopening, if ever authorized, is **confirmatory** (does a tiny, pre-registered space change the drop verdict?) — not a resurrection search.

Comparison policy: every tuned variant compared against (a) its own untuned default OOF, (b) M1 accepted baseline, (c) M0 anchor — by paired per-fold OOF deltas (more sensitive than fold-mean comparison under fold-std ≈ 0.03), with same-sign fold counts and the inherited 0.005436 evidence threshold reported (the threshold structures the read; it does not replace director judgment, and per-family seed/implementation variance is unmeasured).

## 13. Search-Space Design

| Candidate family | Eligibility | Hyperparameter | Proposed range / values | Rationale | Risk | Budget impact | Allowed in Phase 10? |
|---|---|---|---|---|---|---|---|
| M1 LogisticRegression | Primary | `C` | log-uniform [1e-3, 1e2] | Core bias/variance lever for linear ranking | Over-search overfits CV | Low | Yes |
| M1 LogisticRegression | Primary | `penalty` | {`l2`, `l1`} | l1 sparsity vs l2 shrinkage on F2 | solver coupling | Low | Yes |
| M1 LogisticRegression | Primary | `class_weight` | {`None`, `balanced`} | Majority-positive base rate may shift coefficients/ranking | Minor; rank metric | Low | Yes |
| M1 LogisticRegression | Primary | `solver` | {`lbfgs`, `saga`} (penalty-compatible) | Needed to support l1/elasticnet | Convergence | Low | Yes (structural) |
| M1 LogisticRegression | Primary | `max_iter` | fixed (e.g. 2000) | Convergence correctness, not tuning | Non-convergence | None | Fixed, not searched |
| CatBoost | Secondary (cond.) | `depth` | {4, 6, 8} | Capacity vs overfit on n=2781 | Overfit fragile slices | Med | Conditional (post-B5) |
| CatBoost | Secondary (cond.) | `learning_rate` | log-uniform [0.01, 0.2] | Standard GBDT lever | Interaction w/ iterations | Med | Conditional |
| CatBoost | Secondary (cond.) | `l2_leaf_reg` | {1, 3, 5, 9} | Regularization for stability | — | Low | Conditional |
| CatBoost | Secondary (cond.) | `iterations` | {200, 400, 800} | Depth of boosting | Runtime / overfit | Med | Conditional |
| CatBoost | Secondary (cond.) | `border_count` | {64, 128} | Numeric binning granularity | Minor | Low | Conditional |
| CatBoost | Secondary (cond.) | `random_seed` | fixed (42) | Reproducibility | — | None | Fixed |
| M0 RandomForest | Anchor | — | none (frozen) | Anchor stability | Drift | None | **No** |
| XGBoost | Dropped | — | none by default | Redundant weak ranker | Resurrection bias | None | **No** (unless written justification, tiny diagnostic only) |
| LightGBM | Dropped | — | none by default | Weakest, near-duplicate | Resurrection bias | None | **No** (unless written justification, tiny diagnostic only) |

Search spaces are intentionally **small and justifiable**; they are pre-registered and **may not be widened after seeing results** without a new authorization.

## 14. Budget Strategy Under Limited Time

| Budget mode | Candidate families | Max trials / configs | Expected runtime risk | When to use | Stop condition |
|---|---|---|---|---|---|
| **Minimal** | M1 only | ≤ 25 M1 trials | Low | First pass / tight time | Budget exhausted OR no gain > noise floor over patience window |
| **Standard** | M1 (≤ 50) + CatBoost limited (≤ 30, post-B5) | ≤ 80 total | Medium | Default if B5 justifies CatBoost | Per-candidate budget exhausted OR plateau |
| **Extended** | M1 (≤ 100) + CatBoost (≤ 50) + optional XGB/LGBM diagnostic (≤ 20 each, **written justification only**) | ≤ 190 total | Medium-High | Only with explicit director authorization | Per-candidate budget exhausted; no space widening |

Guardrails against: excessive trial counts; repeated CV overfitting (repeated-CV confirmation is a separate, labelled secondary check); changing the search space after seeing results without re-authorization; comparing too many variants without a selection-bias warning; deeply optimizing dropped candidates; optimizing auxiliary metrics instead of ROC-AUC; any leaderboard feedback. Optuna specifics: TPE sampler with fixed seed; `direction="maximize"`; objective = OOF/fixed-fold mean ROC-AUC; sequential deterministic runs before any parallelism; study persisted as an artifact; pruning only if intermediate fold metrics are meaningful and correctly reported; **no leaderboard, no trial cherry-picking, no manual prediction edits.**

## 15. Validation, OOF and Metric Protocol

- **Primary metric:** ROC-AUC on positive-class probabilities for `Drafted=1` (official metric). HPO objective = fixed-fold mean / OOF ROC-AUC on the frozen folds.
- **Complementary diagnostics (never selection rules):** PR-AUC / Average Precision (baseline 0.6483 shown), negative-class AP (baseline 0.3517), precision@k / recall@k / lift@k, top-decile / top-quintile capture, cumulative gains, enrichment by score quantile, Brier (diagnostic), score-distribution diagnostics, fold-level paired deltas, slice ROC-AUC with min-n rules, rank correlation / disagreement.
- **Hierarchy rules:** ROC-AUC is primary because it is the official metric; auxiliary metrics characterize ranking utility but do not replace it; Brier is diagnostic; **threshold tuning is irrelevant to ROC-AUC ranking and is prohibited**; calibration fitting is not allowed in Phase 10 and must not alter selection without a future protocol; any ROC-vs-auxiliary or global-vs-slice conflict is **reported as a warning, not hidden.**
- **OOF rules:** OOF predictions generated only from validation folds, schema `Id,fold,y_true,y_pred_proba`, 2781 rows; `estimator.classes_` checked; no NaN/inf; values in [0,1]; fold alignment asserted against the frozen file.
- **HPO activation gates (7, from `research_notes_hpo.md`):** (1) validation protocol frozen — **met**; (2) leakage-safe pipeline implemented — **met** (Phase 6/7/8); (3) feature blocks tested by ablation — **met** (Phase 7/7B → F2); (4) 1–3 model candidates from fair comparison — **met** (M1 primary, CatBoost secondary via Phase 8/9A/9B-Lite); (5) experiment-log schema active — **OPEN** (legacy schema; v2 migration deferred — director decision required); (6) no unresolved leakage issue — **met**; (7) no public-leaderboard dependence — **met**. **6/7 satisfied; gate 5 open → Phase 10 stays locked until resolved or explicitly waived in writing.**

## 16. Leakage, Overfitting and Selection-Bias Controls

| Risk | How it could occur in Phase 10 | Required control | Evidence/artifact required | Stop or warning? |
|---|---|---|---|---|
| Preprocessing leakage | Imputer/encoder/scaler fitted outside folds during HPO | Fit all learned steps inside training folds within each trial | per-trial pipeline in notebook; leakage checklist in report | Stop |
| HPO selection bias | Many trials on same CV inflate OOF | Conservative budget; repeated-CV (different splitter seeds, secondary) confirmation on tuned winner | `hpo_results.csv`; selection_bias_warning_report | Warning (Stop if uncontrolled) |
| Search-space drift | Widening space after seeing results | Pre-registered space; re-authorization required to change | planning brief space table; report attestation | Stop |
| Test-data fitting | Using test for tuning/early-stop | Test only for final inference (Phase 11); none in Phase 10 | leakage checklist; no submission artifact | Stop |
| School leakage | CatBoost native categoricals / School as feature | `cat_features=[]`; School excluded; raise-on-violation assert | feature-matrix assert; report | Stop |
| External data | Any non-official source | Official files only | data-source attestation | Stop |
| Leaderboard chasing | LB used to pick configs | No LB anywhere in Phase 10 | report attestation | Stop |
| Auxiliary-metric optimization | Tuning to PR-AUC/top-k instead of ROC-AUC | Objective fixed to ROC-AUC; others diagnostic | hpo objective record | Warning |
| Fragile-slice cherry-picking | Promoting from small-n slice movement | Min-n rules; fragile flags; full slice reporting | slice_report | Warning |
| Artifact overwrite | Re-run silently overwrites OOF | check-and-fail on existing paths; `run_id` bump | artifact_manifest | Stop |
| Main-log mutation | Writing to `logs/experiment_log.csv` | Candidate log only under `outputs/reports/` | log read-before/assert-after | Stop |
| Anchor drift | M0 retuned/altered | M0 loaded from persisted OOF; frozen config | M0 integrity gate (≤1e-9) | Stop |

Future execution must require: all learned preprocessing fold-fitted; OOF only from validation folds; `classes_` checked; no test fitting; no external data; no School-as-feature; candidate logs separated; versioned artifacts with `experiment_id`/`run_id`; no overwrites without run ids; fold-alignment / probability-range / NaN-inf / duplicate / row-count checks; comparison against accepted baselines.

## 17. Fold-Level and Slice-Level Validation Strategy

| Slice / subgroup | Why it matters | Minimum n / class-count rule | Metric(s) | Warning threshold | How Phase 10 uses it | Risk if ignored |
|---|---|---|---|---|---|---|
| `Age_missing=1` | M1 collapse (0.5442) on this slice | n=435 but **only 8 positives → fragile** | ROC-AUC, capture | >0.02 drop vs M0 (flag fragile) | Guardrail only; never decisive alone | Over-/under-reacting to 8 positives |
| `Position=QB` | M1 robust-size loss (−0.046) | n=162 (n_pos≥20, robust) | ROC-AUC | >0.02 drop vs M0 | Robust-size warning can block promotion | Ignoring a decision-relevant loss |
| `Year` (2009/2011/2017…) | CatBoost robust-slice instability (−0.045/−0.025) | n≥50 | ROC-AUC | >0.02 drop vs M0 | Block/observe CatBoost promotion | Tuning into temporal instability |
| `available_measurement_count` / completeness | CatBoost −0.0649 at count 0 (n=56) | n≥50 | ROC-AUC | >0.02 drop vs M0 | Stability check | Missing a real degradation |
| `Player_Type` / `Position_Type` / `Position` (sufficient n) | Role heterogeneity | n≥50 | ROC-AUC | >0.02 drop vs M0 | Robustness monitoring | Hidden subgroup failure |
| frequent-vs-rare `School` | Institutional context | n≥50, **diagnostic only, never a feature** | ROC-AUC | >0.02 drop vs M0 | Diagnostic slice only | School leakage temptation |

Rules: min-n default **n ≥ 50** for descriptive slice diagnostics; stricter / fragile flags when positives or negatives are sparse; **small-n slices cannot promote or reject a model alone**; robust-size slice degradation can trigger warnings or block promotion; slice diagnostics are guardrails, **not HPO objectives**; multiplicity is acknowledged; slice reports must not seed search spaces without new authorization. Fold-level: report per-fold AUC, fold mean/std, and paired per-fold deltas vs M0/M1; a global gain that is not same-sign across most folds is treated as fragile (backlog B3).

## 18. Future Notebook Architecture and Documentation Standard

**No notebook is created now.** The future Phase 10 notebook must be notebook-first, reproducible, audit-ready, fold-safe, HPO-controlled, strictly local-validation-based, free of leaderboard influence.

| Notebook / module | Purpose | Main sections | Inputs | Outputs | Risks controlled | Required before execution? |
|---|---|---|---|---|---|---|
| `notebooks/10_phase10_model_optimization.ipynb` | Bounded HPO + comparison for M1 (and CatBoost if B5 justifies) | title/scope/non-actions; imports; seed; paths; load F2 + frozen folds + assert integrity; load M0/M1/CatBoost baselines; pre-HPO diagnosis (B5/B3); fold-safe HPO per candidate; OOF generation; global/fold/slice metrics; top-k/score-dist diagnostics; comparison vs baselines; selection-bias report; versioned artifact writes; executive summary + warnings | F2 from official files; frozen fold file; persisted OOF baselines | OOF, hpo_results, model_summary, fold_metrics, slice_report, topk_quantile, score_distribution, selection_bias_warning_report, validation_report, experiment_log_candidate, artifact_manifest | leakage, overfitting, selection bias, overwrites, LB chasing | Yes — defined here, built by Codex post-authorization |

Required documentation pattern — every major code block preceded by a Markdown cell:

```markdown
## <Number>. <Title>
**Objective.**
**Inputs.**
**Method.**
**Expected output.**
**Risk controlled.**
```

Each code cell starts with a comment (e.g. `# 4.2 Validate frozen fold assignments`). After relevant results, a Markdown interpretation block:

```markdown
### Interpretation
- **Main result:**
- **Methodological reading:**
- **Risk or warning:**
- **Diagnostic decision:**
```

The notebook must not: use test data for fitting; use School as a feature; use external data; create submissions; use leaderboard; declare a final winner or submission-ready model; overwrite artifacts without `run_id`; modify `logs/experiment_log.csv`; open Phase 11.

## 19. Future Artifact Architecture

**No execution artifacts are created now.** Future Phase 10 execution must produce versioned artifacts:

| Artifact family | Proposed file(s) | Purpose | Required inputs | Required checks | Produced by | Must exist before closure? | Notes |
|---|---|---|---|---|---|---|---|
| Notebook | `notebooks/10_phase10_model_optimization.ipynb` | Reproducible HPO+comparison | F2, folds, baselines | top-to-bottom run; seeds | Codex | Yes | static review before run |
| HPO results | `outputs/validation/phase10_model_optimization_<run_id>_hpo_results.csv` | All trials/configs + scores | search space, folds | reproducible; seed logged | Codex | Yes | full trials or reproducible summary |
| Best/variant summary | `outputs/validation/phase10_model_optimization_<run_id>_model_summary.csv` | Per-candidate tuned vs default | OOF | recomputed from OOF | Codex | Yes | deltas vs M0/M1/CatBoost |
| Fold metrics | `outputs/validation/phase10_model_optimization_<run_id>_fold_metrics.csv` | Per-fold AUC + paired deltas | OOF | fold alignment | Codex | Yes | — |
| OOF predictions | `outputs/oof/phase10_model_optimization_<run_id>_<candidate>_oof_predictions.csv` | Per-candidate OOF | folds | schema/range/NaN/dup | Codex | Yes | 2781 rows |
| Slice report | `outputs/validation/phase10_model_optimization_<run_id>_slice_report.csv` | Slice safety | OOF + slice dims | min-n rules | Codex | Yes | School diagnostic-only |
| Ranking diagnostics | `outputs/validation/phase10_model_optimization_<run_id>_topk_quantile.csv` | top-k / lift / quantiles | OOF | baselines shown | Codex | Yes | diagnostic only |
| Score distribution | `outputs/validation/phase10_model_optimization_<run_id>_score_distribution.csv` | Degeneracy/compression checks | OOF | — | Codex | Yes | diagnostic only |
| Selection-bias report | `outputs/reports/phase10_model_optimization_<run_id>_selection_bias_warning_report.md` | Overfitting/selection-bias warnings | hpo_results, repeated-CV | honest tuned-vs-default | Codex | Yes | — |
| Validation report | `outputs/reports/phase10_model_optimization_<run_id>_validation_report.md` | Decision artifact | all above | commit hash + env recorded | Codex | Yes | states diagnostic vs decision |
| Experiment log candidate | `outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv` | Candidate log row(s) | run metadata | schema; not main log | Codex | Yes | §20 fields |
| Artifact manifest | `outputs/reports/phase10_model_optimization_<run_id>_artifact_manifest.csv` | Hash lineage | all artifacts | SHA per file | Codex | Yes | manifest self-exclusion expected |
| Acceptance draft | `docs/10_model_optimization/phase10_acceptance.md` | Director-sign acceptance | validation report | hash/signature blank | Opus (post-Codex) | Yes | drafted, not signed |

Names may be improved if repository convention suggests better structure, with justification; `experiment_id = phase10_model_optimization_v<K>`, `run_id` required on every re-run; no overwrites without a new `run_id`; forward slashes; Python + numpy/pandas/sklearn (+ GBDT) versions recorded.

## 20. Candidate Experiment Log Policy

`logs/experiment_log.csv` must **not** be modified during execution until a human acceptance explicitly authorizes integration (and only after the deferred schema-v2 decision). Future execution writes only a candidate log: `outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv`, with at least: `experiment_id, run_id, candidate_family, variant_id, base_candidate, features_used, School_used_as_feature=False, external_data_used=False, leaderboard_used=False, hpo_strategy, hpo_budget_mode, hpo_trials_or_configs, cv_protocol, fold_sha, primary_metric, oof_auc, delta_vs_m0, delta_vs_m1, delta_vs_current_candidate_baseline_if_applicable, fold_mean_auc, fold_std_auc, same_sign_positive_folds_vs_m1, slice_guard_status, leakage_checks_passed, selection_bias_warning_status, artifacts_manifest_path, validation_report_path, notes`. **Not written now — planned only.**

## 21. Acceptance Criteria

**Phase 10 planning acceptance (this run):** package created only in `docs/10_model_optimization/`; methodology docs reviewed & aligned (§6); consistency checks done (§7); candidate eligibility stated (§11); HPO search spaces justified (§13); budget modes defined (§14); CV/fold protocol preserved (§15); leakage & selection-bias controls stated (§16); slice warnings inherited (§17); artifact families defined (§19); notebook standard defined (§18); candidate-log policy defined (§20); Codex execution prompt created but not executed (Deliverable C); Opus strategic-review prompt created but not executed (Deliverable D); Phase 11 locked.

**Future Phase 10 execution acceptance (for the later run):** authorized starting commit verified; forbidden paths unchanged; `logs/experiment_log.csv` unchanged; folds verified (SHA); positive-class probability direction verified; OOF generated fold-safely; HPO space matches planning; HPO budget matches authorization; **gate 5 (log schema) resolved or explicitly waived**; no School-as-feature; no external data; no leaderboard; no submissions; metrics recomputed from OOF; variant comparison vs M0/M1/CatBoost done; fold-level stability reported; slice report done; selection-bias warning report done; artifact manifest done; candidate log written separately; acceptance draft produced; **no final winner without human acceptance**; Phase 11 locked.

## 22. Stop Rules

| Stop rule | Applies to planning / execution | Trigger | Required action | Can continue after mitigation? |
|---|---|---|---|---|
| Wrong/undocumented HEAD | both | HEAD ≠ expected and not documented | Stop, report | Yes, after director documents baseline |
| Forbidden-path diff | both | tracked diff in a forbidden path | Stop, report | Yes, after revert/clarify |
| Main-log changed | both | `logs/experiment_log.csv` diff | Stop, report | Yes, after restore |
| Missing predecessor doc | both | 9B-Lite memo / 9A acceptance / 9A backlog / val-protocol / leakage-checklist absent | Stop, report | Yes, once located/restored |
| Folds unconfirmed | execution | fold SHA mismatch / integrity fail | Stop, report | No until folds restored |
| Probability direction unconfirmed | execution | `classes_` lacks label 1 | Stop, report | No until fixed |
| Candidate eligibility unclear | both | scope ambiguity | Stop, ask director | Yes, after clarification |
| HPO violates leakage controls | execution | preprocessing fit outside folds | Stop, report | No until corrected |
| HPO budget undefined | both | no budget mode selected | Stop, ask director | Yes, after selection |
| Search space changed post-hoc | execution | space widened after results | Stop, report | Only with new authorization |
| Submission / Phase 11 implied | both | any instruction to submit or open Phase 11 | Stop, refuse | No |
| School as feature | both | School enters feature matrix | Stop, report | No |
| External data | both | non-official source | Stop, report | No |
| Leaderboard for selection | both | LB feedback used | Stop, report | No |
| Winner declared in planning/exec | both | final-winner claim without acceptance | Stop, report | No |
| Gate 5 unresolved | execution | log-schema gate open at run time | Stop, route to director | Yes, after resolution/waiver |

Stop means: stop, report, await human input — never improvise past a stop rule.

## 23. Opus-Codex-Opus Workflow

- **Opus now (this brief + runbook + 2 prompts):** designs Phase 10; reviews methodology; defines candidate eligibility, search spaces, budgets, artifacts, notebook standard, stop rules, acceptance criteria. **Executes no HPO.**
- **Codex later (only after signed authorization):** executes exactly what is authorized; creates the notebook and artifacts; trains/tunes only inside the fold-safe protocol; uses only official data + accepted artifacts + the separate GBDT env (never mutating `.venv`); opens no Phase 11; creates no submission; uses no leaderboard; declares no winner.
- **Opus after Codex:** audits outputs; independently recomputes/verifies critical metrics; evaluates accept/observe/reject/defer per candidate; may recommend readiness for Phase 11 *planning*; creates no submission; declares no final winner without acceptance.

## 24. Handoff to Phase 11 Without Opening Phase 11

Phase 10's deliverable to Phase 11 is **a documented, phase-gated candidate recommendation**, not a submission and not a winner. The handoff records: which candidate(s) survived with what tuned-vs-default evidence; their slice/stability warnings; the open questions (calibration as diagnostic, ensemble M1↔CatBoost as a future-locked idea per backlog B7); and the explicit statement that **Phase 11 (final refit on full train, test inference, submission, LB sanity-check, last-submission ordering) remains locked** and requires its own authorization, its own gates (submission-readiness per v3 §16.7), and the submission checklist. **Phase 10 produces no `outputs/submissions/` artifact.**

## 25. Risks, Failure Modes and Mitigations

- **HPO overfits CV / selection bias** → conservative pre-registered budget; repeated-CV confirmation; honest tuned-vs-default delta; keep defaults if gain < noise floor.
- **Tuning M1 to hide a slice problem** → Age_missing=1 / QB are warnings tracked separately; HPO objective is global ROC-AUC, slices are guardrails.
- **CatBoost promoted on local gains** → secondary/limited only; B5 diagnosis first; robust-slice degradation can block promotion.
- **XGB/LGBM resurrection** → dropped by default; reopening needs written justification + tiny diagnostic budget; near-duplicate (0.952) noted.
- **Environment contamination** → GBDT runs in the separate Wave 2 env; `.venv`/`requirements.txt`/lockfiles untouched.
- **Gate erosion by executors** → two-role rule; stop rules; gate 5 explicitly open.
- **Artifact overwrite / log drift** → check-and-fail paths; candidate log only; schema asserts.
- **Leaderboard temptation** → no LB anywhere in Phase 10; any LB reasoning is a protocol violation.

## 26. Explicit Non-Actions

No Phase 10 execution; no model training; no HPO; no notebook creation now; no notebook execution; no submissions; no leaderboard; no Phase 11; no final-winner / submission-ready declaration; no ensembles/blending/stacking/calibration/threshold tuning; no external data; no School-as-feature; no modification of `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`; no staging; no commit; no push; no `git add .`; no `git commit -a`.

## 27. Required User Authorization Before Execution

A signed **Phase 10 Project Authorization Note** is required before any execution, and must: confirm the authorized starting commit; select a budget mode (Minimal / Standard / Extended); confirm whether CatBoost limited HPO is authorized (and that B5 diagnosis precedes it); confirm whether any XGB/LGBM diagnostic reopening is authorized (with written justification); **resolve or explicitly waive gate 5 (experiment-log schema)**; and reaffirm the locks (no winner, no submission, no Phase 11). Until then, the Codex prompt (Deliverable C) is **inert**.

## 28. Recommended Next Step

**A. Review this Phase 10 planning package; execution remains blocked until explicit user authorization.** Recommended sequencing once authorized: resolve gate 5 → run P10-B1 pre-HPO diagnosis (B5/B3) → M1 bounded HPO (Minimal/Standard) → conditional CatBoost limited HPO → comparison/stability/slice/selection-bias review → Opus strategic review → director-signed `phase10_acceptance.md`. Phase 11 remains locked.
