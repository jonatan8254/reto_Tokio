# Phase 9A Operator Runbook — How to Use the Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-18
**Companion documents:** `phase9a_master_planning_brief.md` (the plan), `prompt_codex_phase9a_execution_plan.md` (the future execution prompt), `prompt_opus_phase9a_strategic_recommendation_review.md` (the post-execution strategic review prompt)
**Standing rule:** Phase 9A execution is blocked until §10's gates are satisfied. Phase 9A is diagnostic-only — it selects no winner and authorizes no submission. **Phase 10 and Phase 11 remain locked.**

---

## 0. Purpose

This runbook tells the user/project director exactly how to take the Phase 9A planning package from "planned" to "executed, audited, accepted, and commit-anchored" without breaking any project gate and without letting diagnostics drift into model selection. It is procedural; all methodology lives in the master brief. Phase 9A is read-only over already-persisted OOF predictions; it trains nothing.

---

## 1. Required Starting State

Before doing anything with this package, verify (read-only):

```powershell
git rev-parse --short HEAD     # expected: 4bbcd7a, or the successor hash if the planning docs were committed
git status --short             # only known untracked items; nothing staged; no tracked modifications
git diff --check               # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
git diff -- logs/experiment_log.csv   # empty (unchanged)
```

Also confirm these exist (committed): the five candidate OOF files (`...m0_random_forest_frozen`, `...m1_logistic_regression`, `...wave2..._xgboost`, `...wave2..._lightgbm`, `...wave2..._catboost`), the frozen-fold file `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, and both Phase 8 acceptance records.

Confirm no Phase 9A artifact already exists: no `phase9a_*` file under `outputs/`, and no `notebooks/09a*` notebook.

If any check fails: stop, classify (blocker / warning / informational), and resolve before proceeding.

**Recommended policy:** do not authorize Phase 9A execution from an untracked planning package. Commit the four planning documents first (step 3 of §7), then use the resulting HEAD as the authorized starting hash.

---

## 2. File Usage Order

1. `phase9a_master_planning_brief.md` — read fully; this is the decision document.
2. This runbook — follow the workflow in §7.
3. `prompt_codex_phase9a_execution_plan.md` — use **only after** the §10 gates pass; it is inert until then.
4. `prompt_opus_phase9a_strategic_recommendation_review.md` — use **only after** Codex execution + independent recomputation pass.

---

## 3. When to Use Each Deliverable

| Situation | Use |
|---|---|
| Deciding whether Phase 9A is well-designed | Master brief §§0–13, 18 |
| Ratifying metrics, imbalance framing, candidates, slices | Master brief §6, §8, §10, §11, §20 checklist |
| Reviewing the future notebook design | Master brief §12 + this runbook §8 |
| Preparing to authorize execution | This runbook §§4, 7, 9–10 |
| Launching the Codex execution session | Deliverable C, with the authorization note attached |
| Auditing results after execution | This runbook §11 |
| Turning results into a classified backlog + acceptance | Deliverable D (Opus strategic review) |
| Closing Phase 9A | This runbook §12 |

---

## 4. What the Project Director Must Review Before Authorizing Execution

Checklist (mirrors brief §20):

- [ ] Brief read; no objection to the block architecture (§9) or the single-notebook decision (§12).
- [ ] Metrics catalogue (§8) ratified, including which are mandatory vs optional/diagnostic.
- [ ] **Imbalance framing accepted** (§6): positive rate 0.6483, majority-positive; PR-AUC/top-k are diagnostic with baselines reported, never selection rules.
- [ ] k / quantile grids and slice min-n (n≥50, Position stricter n≥100) confirmed.
- [ ] Candidate scope (§10) confirmed: m0/m1/catboost mandatory; xgboost/lightgbm diagnostic-only; no re-promotion.
- [ ] Slice plan (§11) confirmed, including School-diagnostic-only.
- [ ] Artifact namespace `phase9a_auc_ranking_diagnostics_v1` and the 14 artifact families (§13) accepted.
- [ ] Understood and accepted: Phase 9A produces **classified diagnostics and a backlog, not a winner**; no submission, no HPO, no ensemble, no calibration fitting, no threshold tuning.
- [ ] Decision made on committing the four planning docs before execution (recommended).
- [ ] Authorized starting hash written into the authorization note.

---

## 5. What Opus (Now) Is Allowed to Do

- Plan, audit, review, and verify (read-only by default).
- Create/update **only** the four authorized Phase 9A planning documents in this run.
- After explicit authorization, the default executor is Codex per Deliverable C. Opus should not execute the notebook unless the project director explicitly overrides the default Opus→Codex→Opus workflow in writing. Execution remains read-only OOF diagnostics via the project venv, with post-run verification and reporting.
- Stage/commit **only** named files, **only** on an explicit instruction for that exact action.
- Never: train/retrain, HPO, ensembles, calibration fitting, threshold tuning, submissions, leaderboard use, external data, forbidden-path modification, winner declaration, Phase 10/11.

## 6. What Codex / Executor Is Allowed to Do Later

- Same boundary set as §5, scoped by Deliverable C.
- Codex executes **only read-only OOF diagnostics**: validates artifacts, recomputes metrics, produces the heavily-documented notebook + reports + tables + manifests + candidate log.
- Codex must stop on any failed integrity/reproduction check and return control to the director; it may not self-expand scope, add metrics that select a model, propose HPO as an executable action, ensemble, submit, declare a winner, or commit.
- Codex must **not** interpret strategically beyond a technical report. Strategic prioritization is the later Opus step (Deliverable D).
- If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project-director approval (Fidelity Contract, Deliverable C).

---

## 7. Step-by-Step Workflow

1. **Verify starting state** (§1 commands). Any failure ⇒ stop.
2. **Review the brief**; complete the §4 checklist.
3. *(Recommended)* **Selectively commit the four planning docs** (explicit instruction; individual `git add` per file; record the new hash).
4. **Write the authorization note** (§10 format) including the authorized hash and any amendments.
5. **Launch execution** by giving the executor Deliverable C + the authorization note.
6. Executor runs **Block 0 + Block 1 (integrity) live**; proceeds to metrics **only** if integrity and reproduction gates pass.
7. Executor implements `09a` per the brief §12 blueprint with the per-cell documentation standard; **independent static review** (two-role rule: mle-reviewer + silent-failure-hunter + eval-harness) before execution.
8. Executor runs the notebook headlessly (`.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace`); integrity and reproduction gates are self-enforcing (stop-on-fail).
9. **Post-run audit** (§11) — independent of the executor's self-report.
10. **Opus strategic review** (Deliverable D): read the Codex outputs, interpret, produce the classified improvement backlog, and draft `phase9a_acceptance.md`.
11. **Decision meeting**: the director reviews the diagnostic verdicts (carry / observe / drop-candidate, no winner) and the backlog; signs the acceptance; selective commit; record hash. **Phase 10/11 stay locked.**

---

## 8. How to Review the Notebook Architecture Before Execution

Before authorizing Codex, the director must check, against brief §12:

- **Read-only:** no model construction, no `.fit()`, no install, no training. Only OOF files + fold file are read.
- **Integrity-first:** Block 1 (schema/rows/range/NaN/duplicates/**alignment**/positive-rate) runs and must pass **before** any metric cell; reproduction (Block 2, ROC-AUC ±1e-9) gates the rest.
- **Documentation standard:** every important block has the Markdown header (Objetivo/Inputs/Método/Output esperado/Riesgo controlado) and every results cell has an **Interpretation** cell (Resultado/Lectura/Riesgo/Decisión diagnóstica).
- **Imbalance discipline:** positive rate reported global/fold/slice; every top-k/PR number shows its baseline; ROC↔PR/top-k conflicts flagged as warnings.
- **No selection language:** verdicts are carry/observe/drop-candidate; no "winner"/"best"/"submission-ready"; no causal claims.
- **Candidate roles preserved:** m0 anchor; m1 candidate-with-warning; catboost escalated; xgboost/lightgbm no_qualifying_evidence (not re-promoted).
- **Slices:** 7 established Phase 7/8 slice dimensions plus `Position` as an optional fine-grained diagnostic slice with a stricter minimum-n rule (`Position` n≥100); min-n enforced, n_pos fragility flag (Age_missing=1), School diagnostic-only.
- **Artifacts:** exactly the §13 names with pre-write guards + manifest + candidate log; main log read-before/assert-after.
- **Codex prompt fidelity:** Deliverable C matches the blueprint; the Fidelity Contract section is present and unmodified.

Any mismatch ⇒ do not authorize; amend the planning package first.

---

## 9. Commands/Checks to Request Before Execution

Immediately before the run (inside the execution session):

```powershell
git rev-parse --short HEAD          # must equal the authorized hash
git status --short                  # no staged files; no tracked modifications
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git ls-files docs/09_auc_ranking_diagnostics/phase9a_master_planning_brief.md docs/09_auc_ranking_diagnostics/phase9a_operator_runbook.md docs/09_auc_ranking_diagnostics/prompt_codex_phase9a_execution_plan.md docs/09_auc_ranking_diagnostics/prompt_opus_phase9a_strategic_recommendation_review.md
# expected: all four files listed (tracked) — per the §1 recommended policy
& .venv\Scripts\python.exe -c "import sys,pandas,sklearn,numpy; print(sys.version.split()[0], pandas.__version__, sklearn.__version__, numpy.__version__)"
# expected: 3.13.13 / 3.0.3 / 1.9.0 / 2.4.6
# If package versions differ from the expected versions, classify this as a warning unless metric reproduction, OOF integrity checks, or notebook execution fail.
```

Plus, inside the notebook (self-enforcing): all 5 OOF files present; schema `Id,fold,y_true,y_pred_proba`; 2781 rows each; folds 0..4; probabilities in [0,1]; no NaN/inf; no duplicate (Id,fold); **0 Id→fold and Id→y_true mismatches vs M0**; positive rate ≈ 0.6483; ROC-AUC reproduced within ±1e-9 of accepted summaries; frozen-fold sha256[:16] == `96937649526bcadb`; pre-write guards on every artifact path; no pre-existing `phase9a_auc_ranking_diagnostics_v1_*` artifact; main-log read-before/assert-after.

---

## 10. Project Director Authorization Gates

Execution requires a written authorization note containing, at minimum:

```text
PHASE 9A EXECUTION AUTHORIZATION (AUC-ORIENTED IMBALANCE AND RANKING DIAGNOSTICS)
Date: ____
Authorized starting commit hash: ____
Metrics catalogue ratified as specified in brief §8: yes / amended (attach amendments)
Imbalance framing (§6) accepted: yes
k / quantile grids and slice min-n ratified (brief §11): yes / amended
Candidate scope (§10) and slice plan (§11) ratified: yes / amended
Artifact namespace + families (brief §13): yes / amended
Diagnostic-only confirmed: no winner, no submission, no HPO, no ensemble, no calibration fitting, no threshold tuning
Phase 10 / Phase 11 remain locked: confirmed
Authorized executor: Opus / Codex / ____
Signature (user/project director): ____
```

No note ⇒ no execution. An amended note freezes the amendments; further mid-run changes are a stop condition.

---

## 11. Output Audit Procedure

After execution, **a role other than the executor** (or the director directly) must:

1. Recompute every reported metric from the persisted OOF files independently (stdlib rank-based AUC for ROC; independent PR-AUC/top-k) and match the artifacts to ≤ 1e-9 (ROC) / documented tolerance (others).
2. Re-verify OOF integrity from the artifacts: 5 files, 2781 rows, schema, range, no NaN/dupes, **0 alignment mismatches** vs M0.
3. Confirm the ROC-AUC reproduction matches accepted Phase 8 summaries within ±1e-9.
4. Confirm candidate roles preserved (m0 anchor; m1/catboost candidate-with-warning; xgboost/lightgbm no_qualifying_evidence); **no winner declared**; no submission/HPO/ensemble/calibration/threshold artifacts exist.
5. Inspect slice diagnostics: min-n enforced; positive rate reported; Age_missing=1 fragility flagged; multiplicity caution present.
6. Verify the artifact manifest: every listed file exists, sha256 matches, no unlisted `phase9a_*` file; candidate log present and main log byte-identical.
7. Run the §1 git checks: only expected new untracked artifacts; nothing tracked modified; forbidden paths clean.
8. Hand the verified outputs to the Opus strategic-review step (Deliverable D) for backlog classification and acceptance drafting.

---

## 12. Phase 9A Closure Criteria

Phase 9A closes only when **all** hold:

1. All mandatory diagnostics executed; optional diagnostics either executed or explicitly skipped by recorded decision.
2. Integrity + reproduction gates passed; independent audit (§11) passed.
3. Every candidate classified by diagnostic verdict (carry / observe / drop-candidate) — **no winner, no submission-ready designation.**
4. The improvement-hypothesis backlog is produced and **every item is phase-gated** (categories 1–7), with ensemble/HPO/calibration/threshold/submission items marked future-locked.
5. `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md` written (via the Opus review step), including: the diagnostic verdicts; the imbalance-aware reading; slice findings incl. Age_missing=1; warnings; the backlog summary; and the Phase 10/11 dependency notes.
6. Project director sign-off recorded.
7. Selective commit executed on explicit instruction; commit hash recorded back into the acceptance record (the `4bbcd7a` pattern).
8. No unresolved integrity warning; main log untouched; no submission; no model trained.

### Acceptance template (to be filled by the Opus review step, signed by the director)

```text
# Phase 9A Acceptance — AUC-Oriented Imbalance and Ranking Diagnostics
Decision: ACCEPT (DIAGNOSTIC) WITH/ WITHOUT WARNINGS
Authorized starting hash: ____
Audit status: passed / blockers: ____
ROC-AUC reproduced (±1e-9): yes
Candidate verdicts: m0 anchor; m1 carry-with-warning; catboost carry-with-warning; xgboost/lightgbm observe-or-drop (diagnostic-only)
Final winner: none
Submission status: none
Main log: unchanged
Backlog produced and phase-gated: yes
Phase 10 / Phase 11: locked
Selective-commit hash: ____
Signature (project director): ____
```

---

## 13. Failure Conditions and Stop Rules

Stop immediately, report, and await director input if any of the following occurs:

1. HEAD ≠ authorized hash; or staged files / tracked modifications / forbidden-path diffs appear at any point.
2. A `phase9a_*` artifact already exists at session start (possible double execution).
3. Any OOF file missing, wrong schema, wrong row count, probabilities out of [0,1], NaN/inf, duplicate (Id,fold), or **any Id→fold/y_true misalignment vs M0** ⇒ integrity gate failed; block before metrics.
4. ROC-AUC does not reproduce the accepted Phase 8 summaries within ±1e-9 ⇒ reproduction gate failed.
5. Any attempt to train/retrain, run HPO, ensemble/blend/stack, calibrate (fit), threshold-tune, or generate a submission.
6. Any leaderboard use or external-data use; any School-as-feature use.
7. Artifact path collision (pre-write guard trip) or any overwrite without a new `run_id`.
8. `logs/experiment_log.csv` differs at any checkpoint.
9. Any request to declare a winner / submission-ready model, or to open Phase 10/11.
10. Mid-run pressure to add metrics/slices that function as selection rules.

A slice with n < min-n is **not** a stop condition: report it as non-evaluable/fragile and continue.

---

## 14. Handoff to Phase 10/11 Without Opening Them

At closure, prepare (inside `phase9a_acceptance.md` and the backlog, no new phases): the diagnostic verdicts; the phase-gated backlog (categories 1–7); open questions routed forward *as names only, no experiments* — e.g., per-family seed-noise calibration (Phase 9B), M1↔CatBoost complementarity study (Phase 9B), any tuning question (Phase 10, locked), any ensemble idea (future ensemble phase, locked), submission/threshold strategy (Phase 11, locked) — and the statements:

```text
Phase 10 remains locked.
Phase 11 remains locked.
No final winner selected.
No submission-ready model.
Future phases remain locked.
```

A later phase may be considered only after Phase 9A is planned, authorized, executed, audited, accepted, committed, hash-recorded, free of integrity/leakage warnings — **and** the director explicitly authorizes opening that specific phase.
