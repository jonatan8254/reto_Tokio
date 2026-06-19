# Phase 10 Operator Runbook — How to Use the Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Operator runbook (Deliverable B of the Phase 10 planning package).
**Date:** 2026-06-19
**Companion documents:** `phase10_master_planning_brief.md` (Deliverable A), `prompt_codex_phase10_execution_plan.md` (Deliverable C), `prompt_opus_phase10_strategic_review.md` (Deliverable D).

> This runbook explains how to move from planning to authorized execution **without breaking any gate**. It authorizes no execution by itself. Phase 10 stays locked until a signed Phase 10 Project Authorization Note exists. Phase 11 remains locked throughout.

---

## 0. Purpose

Give the project director and any operator (human, Opus, Codex) a single, sequential procedure for: reviewing the Phase 10 plan, deciding budget/candidate scope, authorizing execution safely, running the Codex executor, auditing its outputs with Opus, and closing Phase 10 with a signed acceptance — all while preserving the frozen folds, F2, the candidate roles, and the no-winner / no-submission / Phase-11-locked invariants.

## 1. Required Starting State

Before anything, verify (read-only):

```bash
git rev-parse --short HEAD        # expect 12c59b8 or a documented successor preserving Phase 9B-Lite
git status --short                # no staged files; only known untracked items
git diff --check                  # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
git diff -- logs/experiment_log.csv   # empty
```

Also confirm present and accepted: `docs/09_auc_ranking_diagnostics/phase9b_lite_transition_memo.md`, `phase9a_acceptance.md`, `phase9a_improvement_backlog.md`, `docs/05_methodology/validation_protocol_phase6.md`, `docs/05_methodology/leakage_checklist_phase6.md`, the frozen fold file `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` (SHA256[:16] `96937649526bcadb`), and the five Phase 8/9A OOF baselines. If any is missing → **Stop** (see §12).

## 2. File Usage Order

1. `phase10_master_planning_brief.md` — read first; it is the governing design.
2. `phase10_operator_runbook.md` — this file; the procedure.
3. `prompt_codex_phase10_execution_plan.md` — used **only after** a signed authorization note.
4. `prompt_opus_phase10_strategic_review.md` — used **only after** Codex execution + independent recomputation.
5. `phase10_acceptance.md` — created by Opus as a draft at the end; signed by the director.

## 3. When to Use Each Deliverable

| Deliverable | Used by | When | Produces |
|---|---|---|---|
| A — Master brief | Director / Opus | Review & authorization decision | Understanding + authorization inputs |
| B — Runbook | Operator | Throughout | Sequencing + gate discipline |
| C — Codex prompt | Codex | After signed authorization note | Notebook + artifacts |
| D — Opus review prompt | Opus | After Codex + independent recomputation | Backlog/recommendation + acceptance draft |

## 4. What the User/Project Director Must Review Before Authorizing Execution

- The candidate eligibility table (brief §11) — confirm M1 primary, CatBoost secondary/limited, M0 anchor, XGB/LGBM dropped.
- The search-space (brief §13) and budget modes (brief §14) — **select one budget mode**.
- Whether **CatBoost limited HPO** is authorized, and that the **B5 slice-instability diagnosis precedes it**.
- Whether any **XGB/LGBM diagnostic reopening** is authorized (requires written methodological justification; default = no).
- **Gate 5 (experiment-log schema active):** resolve the deferred log-v2 migration decision **or explicitly waive it in writing** (brief §15/§21). This is the one open HPO gate.
- Reaffirm the locks: no final winner, no submission-ready model, no Phase 11, no leaderboard, no School-as-feature, no external data.

## 5. What Opus Is Allowed to Do in Planning

Read-only repository inspection; create/update only the four planning deliverables in `docs/10_model_optimization/` (this run already did so); align with methodology; design HPO strategy, eligibility, search spaces, budgets, artifacts, notebook standard, stop rules, acceptance criteria. **Opus executes no HPO, trains nothing, creates no notebook now, generates no submission, declares no winner, stages/commits nothing.**

## 6. What Codex Is Allowed to Do in Future Execution

Only after a signed authorization note: create `notebooks/10_phase10_model_optimization.ipynb`; load F2 + frozen folds (assert integrity) + persisted M0/M1/CatBoost baselines; run **fold-safe bounded HPO** for the authorized candidates within the pre-registered search space and selected budget; generate OOF + validation/diagnostic artifacts under the contract paths; write a **candidate** log row (never the main log); run CatBoost only in the **separate Wave 2 environment** (never mutating `.venv`/`requirements.txt`). Codex **must not**: open Phase 11; create submissions; use leaderboard; declare a winner; widen the search space mid-run; touch forbidden paths; stage/commit/push.

## 7. What Opus Is Allowed to Do After Codex Execution

Read-only audit of Codex outputs; **independent recomputation** of critical metrics (rank-AUC, AP, top-k, integrity) verifier ≠ generator; per-candidate accept/observe/reject/defer recommendation; a phase-gated recommendation matrix; the acceptance **draft** (`phase10_acceptance.md`, hash/signature blank). Opus **must not** create a submission, declare a final winner without acceptance, or open Phase 11.

## 8. What No Agent Is Allowed to Do

Open Phase 11; create or submit a submission; use the public leaderboard for any decision; declare a final winner / submission-ready model; build ensembles/blending/stacking/calibration/threshold tuning; use external data; use School as a feature; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`; run `git add .` / `git commit -a`; stage/commit/push without an explicit per-action instruction; widen a pre-registered search space after seeing results.

## 9. Step-by-Step Workflow

1. **Review** (Director + optional read-only `mle-reviewer`): read brief; confirm starting state (§1).
2. **Decide** (Director): budget mode; CatBoost yes/no; XGB/LGBM diagnostic yes/no; resolve/waive gate 5; reaffirm locks.
3. **Authorize** (Director): write & sign the Phase 10 Project Authorization Note (records the authorized hash + the §4 decisions).
4. **Execute** (Codex via Deliverable C): build notebook; P10-B0 gate check → P10-B1 pre-HPO diagnosis (B5/B3) → P10-B2 M1 HPO → P10-B3 CatBoost limited HPO (if authorized) → P10-B4 comparison/stability → P10-B5 slice/selection-bias review → write artifacts + candidate log.
5. **Independent recomputation** (Opus or a second role): re-derive ROC-AUC/AP/top-k/integrity from persisted OOF; confirm anchors (M0 ≤1e-9). If mismatch → **Stop/Blocker**.
6. **Strategic review** (Opus via Deliverable D): recommendation matrix + acceptance draft.
7. **Close** (Director): review acceptance draft; if approved, authorize a **selective** commit (per-file `git add`) and record the resulting hash into `phase10_acceptance.md`. Phase 11 stays locked.

## 10. Commands/Checks to Request Before Execution

```bash
# baseline gate
git rev-parse HEAD
git status --short
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git diff -- logs/experiment_log.csv
# fold integrity (read-only; expect SHA256[:16] = 96937649526bcadb, 2781 rows, folds 0..4)
# baseline presence (read-only): five Phase 8/9A OOF files exist and load
```

The executor must additionally, inside the notebook: assert fold SHA + 2781 rows + folds 0..4; verify `estimator.classes_` contains label 1; read `logs/experiment_log.csv` before and assert byte-identical after; check-and-fail on existing artifact paths.

## 11. Project Authorization Gates

- **Gate A (planning accepted):** director has read the brief and runbook.
- **Gate B (decisions made):** budget mode, CatBoost, XGB/LGBM, gate-5 resolution recorded.
- **Gate C (authorization signed):** Phase 10 Project Authorization Note signed with the authorized hash.
- **Gate D (execution complete):** Codex artifacts produced; no forbidden-path / main-log changes.
- **Gate E (independent recomputation passed):** metrics reproduced within tolerance.
- **Gate F (acceptance signed):** director signs `phase10_acceptance.md`; selective commit hash recorded.
- Phase 11 gate is **separate and remains locked.**

## 12. Failure Conditions and Stop Rules

Apply brief §22 in full. Hard stops: wrong/undocumented HEAD; forbidden-path diff; main-log change; missing predecessor doc; fold SHA mismatch; `classes_` missing label 1; search-space changed post-hoc; any instruction to submit / open Phase 11 / use School / use external data / use leaderboard / declare a winner; gate 5 unresolved at run time. On any stop: **stop, report, await the director** — never improvise past it.

## 13. Output Audit Procedure

1. Confirm all expected artifacts exist (brief §19) and are contract-named.
2. Independently recompute ROC-AUC (rank-based stdlib), AP, and a top-k metric from each persisted OOF; compare to `model_summary.csv`/`hpo_results.csv` within documented tolerance.
3. Confirm M0 anchor integrity (≤1e-9 vs persisted Phase 7 F2 OOF) and M1 baseline unchanged.
4. Verify OOF schema/row-count/range/NaN-inf/duplicate/fold-alignment for every OOF file.
5. Verify the artifact manifest hashes; confirm no unlisted artifact (manifest self-exclusion expected).
6. Confirm `logs/experiment_log.csv` byte-identical; no `outputs/submissions/` artifact created; `.venv`/`requirements.txt` unchanged.
7. Record PASS/BLOCKER; on blocker, stop and report.

## 14. Notebook Quality Review Checklist

- [ ] Title, scope, explicit non-actions present.
- [ ] Clean imports; `PROJECT_SEED=42`; `experiment_id`/`run_id`; centralized relative paths.
- [ ] Loads only F2 from official files + frozen folds + persisted baselines.
- [ ] Frozen-fold integrity asserted (SHA, 2781 rows, folds 0..4).
- [ ] All learned preprocessing fitted inside training folds (incl. within every HPO trial).
- [ ] Positive-class probability via verified `estimator.classes_`.
- [ ] OOF generated only from validation folds; schema/range/NaN checks.
- [ ] Markdown objective/inputs/method/output/risk before each major block; interpretation after results.
- [ ] Versioned artifact writes with check-and-fail; commit hash + environment recorded.
- [ ] No test fitting, no School feature, no external data, no submission, no leaderboard, no Phase 11.

## 15. HPO Review Checklist

- [ ] Search space matches the pre-registered tables (brief §13); not widened after results.
- [ ] Budget matches the authorized mode (brief §14); trial count within cap.
- [ ] Objective = OOF/fixed-fold mean ROC-AUC (not an auxiliary metric).
- [ ] Optuna sampler seed fixed; `direction="maximize"`; study persisted; sequential-before-parallel.
- [ ] Tuned-vs-default delta reported honestly; defaults kept if gain < noise floor.
- [ ] Repeated-CV (different splitter seeds, secondary) confirmation on the tuned winner.
- [ ] CatBoost (if run) uses `cat_features=[]`, separate env, no test-based early stopping.
- [ ] M0 not tuned; XGB/LGBM not deep-tuned unless a written justification is attached.

## 16. Selection-Bias Review Checklist

- [ ] Experiment list / candidates pre-registered before running.
- [ ] Number of compared variants reported; multiplicity acknowledged.
- [ ] No search-space change after seeing results without re-authorization.
- [ ] Slice diagnostics used as guardrails, not to seed search spaces.
- [ ] Selection-bias warning report produced; OOF lead stability characterized (backlog B3).
- [ ] No leaderboard feedback anywhere.

## 17. Phase 10 Closure Criteria

Phase 10 closes only when: execution acceptance criteria (brief §21) are met; the independent recomputation passed; the validation report + selection-bias report + slice report + artifact manifest + candidate log exist; the Opus strategic review produced a phase-gated recommendation (accept/observe/reject/defer per candidate, **no winner**); the director signs `phase10_acceptance.md`; and (on explicit instruction) a selective commit is made with its hash recorded. **No final winner and no submission-ready model are declared at closure.**

## 18. Handoff to Phase 11 Without Opening Phase 11

The Phase 10 acceptance records a **candidate recommendation** for future Phase 11 *planning* only — not a winner and not a submission. Phase 11 (final refit on full train, single test inference, submission validation suite per v3 §14, SHA-256 + row/order checks, LB sanity-check, last-submission ordering control) **remains locked** and requires its own authorization, its own submission-readiness gates (v3 §16.7), and the submission checklist. Phase 10 creates **no** `outputs/submissions/` artifact and authorizes **no** leaderboard use.
