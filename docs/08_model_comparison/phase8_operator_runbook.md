# Phase 8 Operator Runbook — How to Use the Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-12
**Companion documents:** `phase8_master_planning_brief.md` (the plan), `prompt_codex_phase8_execution_plan.md` (the future execution prompt)
**Standing rule:** Phase 8 execution is blocked until §10's gates are satisfied. **Phase 9, Phase 10 and Phase 11 remain locked.**

---

## 0. Purpose

This runbook tells the user/project director exactly how to take the Phase 8 planning package from "planned" to "executed, audited, accepted, and commit-anchored" without breaking any project gate. It is procedural; all methodology lives in the master brief. It covers Wave 1 (sklearn-native comparison) only; Wave 2 (external GBDTs) has its own future gate (brief §17).

---

## 1. Required Starting State

Before doing anything with this package, verify (read-only):

```powershell
git rev-parse --short HEAD     # expected: 7166c2e, or the successor hash if the planning docs were committed
git status --short             # only known untracked items; nothing staged; no tracked modifications
git diff --check               # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
```

Also confirm these exist (committed): `docs/07_feature_engineering/phase7_acceptance.md`, `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md`, `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, `outputs/oof/phase7_missingness_availability_v1_phase7_f2_median_flags_count_oof_predictions.csv`.

Confirm no Phase 8 artifact already exists: no `phase8_*` file under `outputs/` and no `notebooks/08*` notebook.

If any check fails: stop, classify (blocker / warning / informational), and resolve before proceeding.

**Recommended policy:** do not authorize Phase 8 execution from an untracked planning package. Commit the three planning documents first (step 3 of §7), then use the resulting HEAD as the authorized starting hash recorded in the Project Authorization Note.

---

## 2. File Usage Order

1. `phase8_master_planning_brief.md` — read fully; this is the decision document.
2. This runbook — follow the workflow in §7.
3. `prompt_codex_phase8_execution_plan.md` — use **only after** the §10 gates pass; it is inert until then.

---

## 3. When to Use Each Deliverable

| Situation | Use |
|---|---|
| Deciding whether Phase 8 is well-designed | Master brief §§0–13, 15 |
| Ratifying the model registry, configs, cap and thresholds | Master brief §8, §9, §12, §17 checklist |
| Reviewing the future notebook design | Master brief §10 (blueprint) + this runbook §8 |
| Preparing to authorize execution | This runbook §§4, 7–10 |
| Launching the execution session | Deliverable C (the Codex prompt), with the Project Authorization Note attached |
| Auditing results after execution | This runbook §12 |
| Closing Phase 8 | This runbook §13 |
| Considering external GBDTs (Wave 2) | Brief §8/§17 — separate gate; not covered by the Wave 1 note |

---

## 4. What the Project Director Must Review Before Authorizing Execution

Checklist (mirrors brief §17):

- [ ] Brief read; no objection to the block architecture (§7) or the staged Wave 1/Wave 2 design (§8).
- [ ] Model registry ratified exactly (model_keys, constructor params, statuses), or amended in writing.
- [ ] Decision recorded on `m3_extra_trees_default` (include / drop) and on the gated `m5_hgb_native_missing` diagnostic (authorize / strike).
- [ ] Run cap confirmed: ≤ 6 trained model-runs in Wave 1.
- [ ] Thresholds confirmed: flag rule 0.005436 OOF gain + ≥ 4/5 same-sign folds + slice guard (n ≥ 50; 0.02 escalation); M0 tolerance ± 1e-6.
- [ ] Understood and accepted: Phase 8 produces a **classified evidence table, not a winner**; candidate selection happens in `phase8_acceptance.md`.
- [ ] Artifact names (brief §10.7/§14) accepted.
- [ ] Decision made on committing the three planning docs before execution (recommended).
- [ ] Authorized starting hash written into the Project Authorization Note.
- [ ] Confirmed Wave 2 (xgboost/lightgbm/catboost) stays locked: no installs are authorized by the Wave 1 note.

---

## 5. What Fable Is Allowed to Do

- Plan, audit, review, and verify (read-only by default).
- Create/update **only** explicitly authorized files.
- After explicit authorization: implement and headlessly execute notebook 08 via the project venv, run post-run verification, and report.
- Stage/commit **only** named files, **only** on an explicit instruction for that exact action.
- Never: HPO, submissions, ensembles, leaderboard use, external data, package installs, forbidden-path modification, Phase 9/10/11.

## 6. What Codex / Executor Is Allowed to Do

- Same boundary set as §5, scoped by Deliverable C.
- Codex receives the execution prompt **only after** the §10 gates pass and the Project Authorization Note exists.
- Codex must stop on any failed integrity check and return control to the user/project director; it may not self-expand scope, add or substitute models, alter configs, install packages, or commit.
- If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project director approval (Fidelity Contract, Deliverable C).

---

## 7. Step-by-Step Workflow

1. **Verify starting state** (§1 commands). Any failure ⇒ stop.
2. **Review the brief**; complete the §4 checklist.
3. *(Recommended)* **Selectively commit the three planning docs** (explicit instruction; individual `git add` per file; record the new hash).
4. **Write the Project Authorization Note** (§10 format) including the authorized hash, the ratified registry, the m3/m5 decisions, and any amendments.
5. **Launch execution** by giving the executor Deliverable C + the Project Authorization Note.
6. Executor runs **Block 0 checks live** (incl. the no-pre-existing-`phase8_*`-artifacts check); proceeds only on all-PASS.
7. Executor implements notebook 08 per the brief §10 blueprint; **independent static review** (two-role rule: mle-reviewer + code-reviewer/python-reviewer + silent-failure-hunter + eval-harness) before execution.
8. Executor runs the notebook headlessly (`.venv\Scripts\python.exe -m nbconvert --to notebook --execute --inplace`); the M0 gate and all integrity asserts are self-enforcing (stop-on-fail).
9. **Post-run audit** (§12 below) — independent of the executor's self-report.
10. **Decision meeting**: review the classified evidence table (promotable evidence / no qualifying evidence / escalated / failed_run per model); the project director selects 1–3 candidates (or records a null result); draft `phase8_acceptance.md`; the project director signs; selective commit; record hash. **Phase 9/10/11 stay locked.**

---

## 8. How to Review the Notebook Architecture Before Execution

Before authorizing Codex, the project director must check, against brief §10:

- **F2 fidelity:** the feature cell builds exactly the 21 F2 features with the audited Phase 7 builder; `Id`, `Drafted`, `School` asserted out; flag sums asserted against the known train missingness counts.
- **Model classification:** the registry cell matches brief §8 verbatim — statuses, constructor params, m5 gate, Wave 2 absent. Models well-classified; nothing promoted from Deferred/Blocked.
- **No HPO:** no loops over parameter values anywhere; no second config per family beyond the pre-registered m0/m2 pair; no early-stopping/validation-split tuning paths.
- **No submissions:** no write path under `outputs/submissions/`; no test-set inference.
- **School exclusion:** School appears only in the diagnostic slice computation, never in any feature matrix (assert present).
- **Artifact paths:** exactly the §10.7 names with pre-write guards and the manifest cell.
- **Leakage checks sufficient:** fold-fitted pipelines only; main-log read-before/assert-after; `classes_` verification helper; OOF validity asserts; frozen-fold sha assert.
- **Codex prompt fidelity:** Deliverable C's instructions match the blueprint one-to-one (brief §10.8 traceability table); the Fidelity Contract section is present and unmodified.

Any mismatch ⇒ do not authorize; amend the planning package first.

---

## 9. Commands/Checks to Request Before Execution

Immediately before the run (inside the execution session):

```powershell
git rev-parse --short HEAD          # must equal the authorized hash
git status --short                  # no staged files; no tracked modifications
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git ls-files docs/08_model_comparison/phase8_master_planning_brief.md docs/08_model_comparison/phase8_operator_runbook.md docs/08_model_comparison/prompt_codex_phase8_execution_plan.md
# expected: all three files listed (tracked) — per the §1 recommended policy
& .venv\Scripts\python.exe -c "import sys,pandas,sklearn,numpy; print(sys.version.split()[0], pandas.__version__, sklearn.__version__, numpy.__version__)"
# expected: 3.13.13 / 3.0.3 / 1.9.0 / 2.4.6
& .venv\Scripts\python.exe -c "import importlib.util as u; print([n for n in ('xgboost','lightgbm','catboost') if u.find_spec(n)])"
# expected: []  (Wave 1 must run with no external GBDTs present)
```

Plus, inside the notebook (self-enforcing): frozen-folds sha256[:16] == `96937649526bcadb`; 2781 rows; labels 0..4; Id order == train order; F2 reference OOF recomputed from the persisted file == 0.8116502602456482; M0 in-run OOF == 0.8116502602456482 ± 1e-6; main-log read-before/assert-after; pre-write guards on every artifact path; no pre-existing `phase8_model_family_comparison_v1_*` artifact.

---

## 10. Project Authorization Gates

Execution requires a written Project Authorization Note containing, at minimum:

```text
PHASE 8 WAVE 1 EXECUTION AUTHORIZATION
Date: ____
Authorized starting commit hash: ____
Model registry ratified as specified in brief §8: yes / amended (attach amendments)
m3_extra_trees_default: include / drop
m5_hgb_native_missing (gated diagnostic): authorized / not authorized
Run cap (<= 6 trained runs): confirmed
Thresholds ratified as specified in brief §17.3: yes / amended
Artifact names ratified (brief §10.7 / §14): yes / amended
Wave 2 (external GBDTs) remains locked; no installs authorized: confirmed
Authorized executor: Fable / Codex / ____
Signature (user/project director): ____
```

No note ⇒ no execution. An amended note freezes the amendments; further mid-run changes are a stop condition. Wave 2 requires its own separate note (installs, pinned versions, pre-registered configs, CatBoost School-policy reconfirmation).

---

## 11. Failure Conditions and Stop Rules

Stop immediately, report, and await user/project director input if any of the following occurs:

1. HEAD ≠ authorized hash; or staged files / tracked modifications / forbidden-path diffs appear at any point.
2. A `phase8_*` artifact already exists at session start (possible double execution).
3. Frozen-fold integrity failure (count, labels, order, or sha mismatch).
4. M0 gate failure (F2 not reproduced within ± 1e-6).
5. Any probability invalid (NaN, outside [0,1]) or single-class validation fold.
6. `estimator.classes_` does not locate label 1 exactly once.
7. Artifact path collision (pre-write guard trip).
8. Any leakage warning or fit-scope doubt raised by reviewer or executor.
9. Mandatory slice (n ≥ 50) degradation > 0.02 vs M0 on any model (escalation — recorded, never auto-decided).
10. Any request to add/substitute models, alter configs, tune parameters, or install packages mid-run.
11. `logs/experiment_log.csv` differs at any checkpoint.
12. Environment versions differ from the pinned set, or an external GBDT import succeeds in Wave 1.
13. Any action that would require a forbidden capability (HPO, submission, ensemble, LB, external data, Phase 9/10/11).

A model erroring or failing to converge is **not** a stop condition: record it as `failed_run`, continue the remaining registry, report.

---

## 12. Output Audit Procedure

After execution, **a role other than the executor** (or the project director directly) must:

1. Recompute every reported OOF ROC-AUC from the persisted `outputs/oof/phase8_*_oof_predictions.csv` files independently (stdlib rank-based AUC — the 6A/7 pattern) and match the model summary to ≤ 1e-9.
2. Verify m0's OOF vector is consistent with the committed Phase 7 F2 OOF (max |Δ| at floating-point level).
3. Recheck fold integrity from the artifacts (row counts, labels, Id↔fold mapping vs the frozen file) for every model.
4. Re-apply the §9 flagging rule from the recomputed numbers; confirm the report's classifications (promotable evidence / no qualifying evidence / escalated / failed_run).
5. Inspect the slice report: all 7 mandatory dimensions per model; n < 50 flagged; escalations match the report; pay specific attention to `Age_missing = 1` (n = 435, 8 positives — known fragile).
6. Verify the artifact manifest: every listed file exists, sha256 matches, no unlisted `phase8_*` file exists.
7. Run the §1 git checks: only expected new untracked artifacts; nothing tracked modified; forbidden paths clean; main log byte-identical.
8. Record the audit outcome in the draft `phase8_acceptance.md`.

---

## 13. Phase 8 Closure Criteria

Phase 8 (Wave 1) closes only when **all** hold:

1. All ratified registry models executed (or recorded as `failed_run` / explicitly skipped by recorded decision) within the cap.
2. Every model classified per the pre-registered flagging rule; escalations resolved by recorded project director decision.
3. Independent audit (§12) passed.
4. `docs/08_model_comparison/phase8_acceptance.md` written, including: the classified evidence table; the project director's selection of 1–3 candidates for future phases (or an explicit null result — also a valid closure); the m5 diagnostic reading (if run) with its fairness caveat; slice findings incl. `Age_missing`; the threshold-provenance limitation; warnings; and the Wave 2 / Phase 9/10/11 dependency notes.
5. Project director sign-off recorded in the acceptance record.
6. Selective commit executed on explicit instruction; commit hash recorded back into the acceptance record (the `42ef12a` → `7166c2e` pattern).
7. No unresolved leakage warning; main log untouched; no submission generated; no install performed.

---

## 14. Handoff to Phase 9 Without Opening Phase 9

At closure, prepare (inside `phase8_acceptance.md`, no new files): the selected 1–3 candidates (or null result) with their evidence; open questions routed forward *as names only, no experiments* — e.g., per-family seed-noise calibration before final selection (Phase 9), error analysis of disagreement between families (Phase 9), whether Wave 2 external GBDTs are worth their dependency cost (separate Wave 2 gate), HPO of selected candidates (Phase 10, only after its 7 documented conditions), submissions (Phase 11) — and the statements:

```text
Phase 9 remains locked.
Phase 10 remains locked.
Phase 11 remains locked.
Future phases remain locked.
```

A later phase may be considered only after Phase 8 is planned, authorized, executed (if so decided), audited, accepted, committed (if authorized), hash-recorded, free of critical leakage warnings — **and** the user/project director explicitly authorizes opening that specific phase.
