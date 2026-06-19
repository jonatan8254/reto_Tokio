# Phase 10 Project Authorization Note

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Project Director Authorization Note (governs future Phase 10 execution only).
**Date:** 2026-06-19
**Governing documents:** `phase10_master_planning_brief.md`, `phase10_operator_runbook.md`, `prompt_codex_phase10_execution_plan.md`, `prompt_opus_phase10_strategic_review.md`.

> This note authorizes the scope below for a future Codex execution of Phase 10. It does not itself execute Phase 10, train any model, run HPO, create a notebook, generate a submission, use the leaderboard, open Phase 11, or declare a final winner / submission-ready model.

---

## 1. Authorization Verdict

Phase 10 execution is authorized **only** under the bounded **Standard-budget** protocol defined in the Phase 10 planning package (`phase10_master_planning_brief.md` §11–§21), for the candidate scope and gate-5 waiver recorded in this note.

This authorization does **not** authorize Phase 11, submissions, leaderboard use, final winner declaration, or submission-ready model declaration. It does not authorize any deviation from the pre-registered search spaces, the frozen folds, or the F2 feature set.

## 2. Authorized Starting Commit

```text
Full hash:  e894dd2dc15589dfe3a281129eacbfde95e00ccf
Short hash: e894dd2
Message:    planning: add phase 10 model optimization package
```

Verified at note-creation time: `git rev-parse --short HEAD` → `e894dd2`; `git status --short` clean of staged files; `git diff --check` clean; forbidden-path tracked diffs empty; `logs/experiment_log.csv` unchanged. Codex **must independently re-verify this hash** (or a documented successor explicitly authorized in writing by the director) before executing anything.

## 3. Scope Authorized

```text
- creation/execution of notebooks/10_phase10_model_optimization.ipynb;
- bounded HPO for M1 LogisticRegression (Standard budget, pre-registered search space);
- pre-HPO B5 diagnosis for CatBoost (slice-instability characterization, read-only over
  existing OOF, before any CatBoost tuning);
- limited HPO for CatBoost (Standard budget) only if the B5 diagnosis supports proceeding;
- generation of versioned OOF predictions per candidate;
- generation of validation/diagnostic artifacts (hpo_results, model_summary, fold_metrics,
  slice_report, topk_quantile, score_distribution);
- generation of a candidate experiment log row under outputs/reports/ (never the main log);
- generation of an artifact manifest;
- generation of a validation report and a selection-bias warning report;
- no modification of logs/experiment_log.csv.
```

## 4. Scope Explicitly Not Authorized

```text
- Phase 11;
- submissions;
- leaderboard use;
- final winner declaration;
- submission-ready model declaration;
- XGBoost HPO;
- LightGBM HPO;
- M0 HPO (M0 stays anchor, loaded from persisted OOF only);
- ensembles;
- blending;
- stacking;
- calibration fitting;
- threshold tuning;
- external data;
- School as a feature;
- modifying forbidden paths (logs/experiment_log.csv, data/input/, notebooks/_official/,
  references/, outputs/submissions/, .venv, requirements.txt, lockfiles,
  .vscode/settings.json, Libros/, Prompts/, Recapitulaciones/);
- git add .;
- git commit -a;
- push.
```

## 5. Candidate Eligibility Decisions

| Candidate | Authorized Phase 10 role | HPO allowed? | Conditions | Notes |
|---|---|---|---|---|
| M1 LogisticRegression | Primary optimization candidate | Yes | Standard bounded HPO only; pre-registered space (`C` log-uniform [1e-3,1e2], `penalty` {l2,l1}, `class_weight` {None,balanced}, compatible solver, fixed `max_iter`) | Candidate with warnings (`Age_missing=1`, `Position=QB`), not winner |
| CatBoost | Secondary / observe candidate | Conditional limited HPO | Only after B5 slice-instability diagnosis; separate Wave 2 environment; `cat_features=[]`; no test-based early stopping | Not promoted, not winner; robust-slice instability (Year 2009/2011, OG/OLB, avail_count) must be characterized first |
| M0 RandomForest frozen | Anchor/reference | No | Load from persisted OOF only (`m0_random_forest_frozen`, n_estimators=100, max_depth=5, seed=42) | No HPO; all deltas are paired against this anchor |
| XGBoost | Dropped for now | No | None | `no_qualifying_evidence` (Phase 8 Wave 2 + Phase 9A); near-duplicate of LightGBM (Spearman 0.952) |
| LightGBM | Dropped for now | No | None | `no_qualifying_evidence`; weakest global ranker, most slice warnings (13) |

## 6. Budget Mode

```text
Budget mode: Standard
```

```text
M1:               up to 50 trials/configurations.
CatBoost:         up to 30 trials/configurations, only if the B5 diagnosis justifies proceeding.
XGBoost/LightGBM: 0 trials (no deep HPO authorized; no diagnostic reopening authorized in this note).
M0:               0 trials (anchor only, no tuning).
```

Objective for any tuned candidate = OOF / fixed-fold mean ROC-AUC on the frozen 5-fold split (`StratifiedKFold`, `random_state=42`, fold SHA256[:16] = `96937649526bcadb`, 2781 rows). The pre-registered search space may not be widened after seeing results; exceeding the Standard caps above requires a new, separately signed authorization.

## 7. Gate 5 Waiver Decision

Gate 5 (experiment-log schema active) is the one open HPO activation gate identified in `research_notes_hpo.md` and carried through the Phase 10 master planning brief (6 of 7 gates met).

```text
Gate 5 is explicitly waived for this Phase 10 execution only, under the condition that:
- logs/experiment_log.csv remains unchanged;
- all experiment records are written to
  outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv;
- integration into logs/experiment_log.csv remains blocked until a later
  acceptance/migration decision.
```

This waiver is scoped to this Phase 10 execution and does not retroactively close gate 5 for any other phase.

## 8. Required Pre-HPO Diagnostics

Before any CatBoost tuning, Codex must execute the **B5** diagnosis (CatBoost robust-slice instability: Year 2009/2011, OG/OLB, `available_measurement_count=0`) read-only over the existing Phase 8/9A persisted OOF, per `phase10_master_planning_brief.md` §17 and `prompt_codex_phase10_execution_plan.md` §6 (block P10-B1). CatBoost HPO proceeds only if this diagnosis supports proceeding; the diagnosis itself trains nothing.

The **B3** stability question (whether M1's OOF lead is stable under resampling) must be addressed via a secondary, clearly labeled repeated-CV confirmation (different splitter seeds) on the tuned M1 winner, per planning brief §17 and Codex prompt §6 — diagnostic only, never a selection rule.

## 9. Required Validation Protocol

```text
Metric: ROC-AUC (official metric), on positive-class probabilities for Drafted = 1,
        verified via estimator.classes_ before extraction.
CV splitter: StratifiedKFold(n_splits=5, shuffle=True, random_state=42) — frozen,
             loaded from outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv
             (SHA256[:16] = 96937649526bcadb, 2781 rows, fold labels 0..4). Asserted,
             never recomputed for selection.
Feature set: F2 only (base Phase 6 features + 7 missingness flags +
             available_measurement_count). No new features. School excluded
             (assert raise-on-violation).
Diagnostics: PR-AUC/AP, neg-class AP, Brier, top-k/quantile capture, score-distribution,
             slice ROC-AUC (min-n >= 50), rank correlation/disagreement — all diagnostic,
             never selection rules. Threshold tuning prohibited.
Anchors: M0 OOF must reproduce the persisted Phase 7 F2 value within 1e-9; M1 baseline
         (pre-HPO default) = 0.8270821069632867.
```

## 10. Required Leakage and Selection-Bias Controls

```text
- all learned preprocessing fitted inside the training fold only, including within every
  HPO trial (median imputation, one-hot encoding);
- test data used only for structural checks, never fitting/selection/HPO;
- no School as feature (assert); no external data; no leaderboard feedback anywhere;
- search space pre-registered in the planning brief; no widening after seeing results;
- M0 not tuned; XGBoost/LightGBM not deep-tuned (no written justification attached to
  this note);
- candidate log kept separate from the main log; main log read-before and asserted
  byte-identical after;
- check-and-fail on existing artifact paths; no overwrites without a new run_id;
- number of compared variants/trials reported (multiplicity disclosure);
- slice diagnostics used only as guardrails (degradation on a robust-size slice can block
  promotion), never as HPO objectives or search-space seeds.
```

## 11. Required Artifact Policy

All Phase 10 artifacts must use `experiment_id = phase10_model_optimization_v<K>` with a mandatory `run_id`, written only to the contract paths in `prompt_codex_phase10_execution_plan.md` §4 (`notebooks/10_phase10_model_optimization.ipynb`; `outputs/oof/...`; `outputs/validation/...`; `outputs/reports/...`). Check-and-fail if a target path already exists — no silent overwrite. `docs/10_model_optimization/phase10_acceptance.md` is reserved for the post-execution Opus strategic review (Deliverable D) and must not be created by Codex.

## 12. Required Candidate Experiment Log Policy

A single candidate log must be written to `outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv` with the field schema defined in `prompt_codex_phase10_execution_plan.md` §10 (`experiment_id, run_id, candidate_family, variant_id, base_candidate, features_used, School_used_as_feature=False, external_data_used=False, leaderboard_used=False, hpo_strategy, hpo_budget_mode, hpo_trials_or_configs, cv_protocol, fold_sha, primary_metric, oof_auc, delta_vs_m0, delta_vs_m1, delta_vs_current_candidate_baseline_if_applicable, fold_mean_auc, fold_std_auc, same_sign_positive_folds_vs_m1, slice_guard_status, leakage_checks_passed, selection_bias_warning_status, artifacts_manifest_path, validation_report_path, notes`). `logs/experiment_log.csv` must not be modified.

## 13. Forbidden Actions

```text
- Phase 11 (any opening action);
- creating or submitting outputs/submissions/* artifacts;
- using the public leaderboard for any decision;
- declaring a final winner or a submission-ready model;
- building ensembles, blending, stacking, calibration, or threshold tuning as executed
  actions;
- using external data of any kind;
- using School as a model feature;
- modifying logs/experiment_log.csv, data/input/, notebooks/_official/, references/,
  outputs/submissions/, .venv, requirements.txt, lockfiles, .vscode/settings.json,
  Libros/, Prompts/, Recapitulaciones/, backup notebooks;
- git add . / git commit -a / commit / push without an explicit, separate per-action
  instruction from the project director;
- widening the pre-registered search space after seeing results;
- exceeding the Standard budget caps in §6 of this note;
- HPO on XGBoost, LightGBM, or M0.
```

## 14. Phase 11 Lock

Phase 11 remains locked regardless of any Phase 10 outcome. A Phase 10 optimized candidate is, at most, a **candidate for future Phase 11 planning** — never a winner and never submission-ready. Opening Phase 11 requires its own separate authorization, its own submission-readiness gates (`project_execution_plan_v3.md` §16.7), and the submission checklist (`docs/00_project_contract/submission_checklist.md`).

## 15. Required Codex Execution Prompt

Future execution must use exactly:

```text
docs/10_model_optimization/prompt_codex_phase10_execution_plan.md
```

Codex is the second brain in the Opus → Codex → Opus separation: a reproducible executor, not a strategist. Codex must not alter scope, must verify this note's preconditions (§2, §6, §7) before doing anything, and must stop and report if any precondition is unmet.

## 16. Required Post-Codex Opus Review

After Codex execution and before any acceptance, review must use exactly:

```text
docs/10_model_optimization/prompt_opus_phase10_strategic_review.md
```

This review performs an independent recomputation (verifier ≠ generator) and produces the phase-gated recommendation matrix and the `phase10_acceptance.md` draft. Phase 10 cannot close before this independent recomputation passes and the Opus strategic review is complete. The director signs the acceptance; no agent self-certifies its own run.

## 17. Stop Rules

Codex must stop and report, without proceeding, if any of the following holds:

```text
- HEAD is not e894dd2dc15589dfe3a281129eacbfde95e00ccf or a documented successor
  explicitly authorized in writing by the director;
- forbidden paths have tracked diffs;
- logs/experiment_log.csv has changed;
- frozen folds cannot be verified, or the fold SHA does not match
  96937649526bcadb;
- the F2 feature set cannot be confirmed, or School appears in the feature matrix;
- external data is introduced;
- positive-class probability direction cannot be verified through estimator.classes_;
- the HPO search space differs from the planning package (brief §13);
- the trial/config budget would exceed Standard mode (§6 of this note);
- any instruction would create a submission;
- any instruction would use the leaderboard;
- any instruction would open Phase 11;
- any instruction would declare a final winner or a submission-ready model;
- the B5 diagnosis does not support proceeding but CatBoost tuning is attempted anyway;
- gate 5 conditions in §7 of this note are violated (i.e., the main log is touched, or
  candidate records are written anywhere other than the contract path).
```

On any stop condition: stop, report, and await the project director. Do not improvise past a stop rule.

## 18. Project Director Authorization Statement

```text
I authorize Phase 10 execution strictly under the scope, budget mode, candidate
eligibility decisions, and gate-5 waiver recorded in this note, starting from commit
e894dd2dc15589dfe3a281129eacbfde95e00ccf. This authorization does not extend to
Phase 11, submissions, leaderboard use, final winner declaration, or submission-ready
model declaration.
```

Signature (project director): ____
Date: ____
Authorized hash confirmed at signature time: ____
