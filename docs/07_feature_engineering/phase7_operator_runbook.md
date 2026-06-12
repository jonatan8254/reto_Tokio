# Phase 7 Operator Runbook — How to Use the Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-12
**Companion documents:** `phase7_master_planning_brief.md` (the plan), `prompt_codex_phase7_execution_plan.md` (the future execution prompt)
**Standing rule:** Phase 7 execution is blocked until §9's gates are satisfied. **Phase 8 remains locked.**

---

## 0. Purpose

This runbook tells the user/project director exactly how to take the Phase 7 planning package from "planned" to "executed, audited, accepted, and commit-anchored" without breaking any project gate. It is procedural; all methodology lives in the master brief.

---

## 1. Required Starting State

Before doing anything with this package, verify (read-only):

```powershell
git rev-parse --short HEAD     # expected: c4d5647, or the successor hash if the planning docs were committed
git status --short             # only known untracked items; nothing staged; no tracked modifications
git diff --check               # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
```

Also confirm these exist (committed): `docs/06_validation/phase6_acceptance.md`, `docs/06_validation/phase6a_acceptance.md`, `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`.

If any check fails: stop, classify (blocker / warning / informational), and resolve before proceeding.

**Recommended policy:** do not authorize Phase 7 execution from an untracked planning package. Commit the three planning documents first (step 3 of §7), then use the resulting HEAD as the authorized starting hash recorded in the Project Authorization Note.

---

## 2. File Usage Order

1. `phase7_master_planning_brief.md` — read fully; this is the decision document.
2. This runbook — follow the workflow in §7.
3. `prompt_codex_phase7_execution_plan.md` — use **only after** the §9 gates pass; it is inert until then.

---

## 3. When to Use Each Deliverable

| Situation | Use |
|---|---|
| Deciding whether Phase 7 is well-designed | Master brief §§0–12, 14 |
| Ratifying features/variants/thresholds | Master brief §9, §11, §16 checklist |
| Preparing to authorize execution | This runbook §§4, 7–9 |
| Launching the execution session | Deliverable C (the Codex prompt), with the Project Authorization Note attached |
| Auditing results after execution | This runbook §11 |
| Closing Phase 7 | This runbook §12 |

---

## 4. What the User/Project Director Must Review Before Authorizing Execution

Checklist (mirrors brief §16):

- [ ] Brief read; no objection to the block architecture (§7) or the ladder (§9).
- [ ] Feature definitions ratified exactly (flags, count, fixed bins `{0}/{1–3}/{4–5}/{6}`), or amended in writing.
- [ ] Gated-variant activation rules (F6: `F5−F1 ≥ 0.005436`; F4: an earlier rung passed + explicit approval) ratified.
- [ ] Thresholds confirmed: 0.005436 OOF gain; ≥ 4/5 same-sign; slice n ≥ 50; 0.02 slice-degradation escalation; F0 tolerance ±1e-6; cap ≤ 8 trained variants.
- [ ] Artifact names (brief §13) accepted.
- [ ] BMI disposition accepted (not adopted in Phase 7 core, from existing V5 evidence).
- [ ] Decision made on committing the three planning docs before execution (recommended).
- [ ] Authorized starting hash written into the Project Authorization Note.

---

## 5. What Fable Is Allowed to Do

- Plan, audit, review, and verify (read-only by default).
- Create/update **only** explicitly authorized files.
- After explicit authorization: implement and headlessly execute notebook 07 via the project venv, run post-run verification, and report.
- Stage/commit **only** named files, **only** on an explicit instruction for that exact action.
- Never: HPO, submissions, model-family comparison, leaderboard use, external data, forbidden-path modification, Phase 8.

## 6. What Codex Is Allowed to Do

- Same boundary set as §5, scoped by Deliverable C.
- Codex receives the execution prompt **only after** the §9 gates pass and the Project Authorization Note exists.
- Codex must stop on any failed integrity check and return control to the user/project director; it may not self-expand scope, redefine variants, or commit.

---

## 7. Step-by-Step Workflow

1. **Verify starting state** (§1 commands). Any failure ⇒ stop.
2. **Review the brief**; complete the §4 checklist.
3. *(Recommended)* **Selectively commit the three planning docs** (explicit instruction; individual `git add` per file; record the new hash).
4. **Write the Project Authorization Note** (§9 format) including the authorized hash and any amendments.
5. **Launch execution** by giving the executor Deliverable C + the Project Authorization Note.
6. Executor runs **Block 0 checks live**; proceeds only on all-PASS.
7. Executor implements notebook 07 per the brief §10 contract; **independent static review** (two-role rule: mle-reviewer + code-reviewer/python-reviewer + silent-failure-hunter) before execution.
8. Executor runs the notebook headlessly (`.venv\Scripts\python.exe -m nbconvert --execute --inplace`); the F0 gate and all integrity asserts are self-enforcing (stop-on-fail).
9. **Post-run audit** (§11 below) — independent of the executor's self-report.
10. **Decision meeting**: classify each rung (adopted / rejected / escalated) per the pre-registered rule; draft `phase7_acceptance.md`; the user/project director signs; selective commit; record hash. Phase 8 stays locked.

---

## 8. Commands/Checks to Request Before Execution

Immediately before the run (inside the execution session):

```powershell
git rev-parse --short HEAD          # must equal the authorized hash
git status --short                  # no staged files; no tracked modifications
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git ls-files docs/07_feature_engineering/phase7_master_planning_brief.md docs/07_feature_engineering/phase7_operator_runbook.md docs/07_feature_engineering/prompt_codex_phase7_execution_plan.md
# expected: all three files listed (tracked)
& .venv\Scripts\python.exe -c "import sys,pandas,sklearn,numpy; print(sys.version.split()[0], pandas.__version__, sklearn.__version__, numpy.__version__)"
# expected: 3.13.13 / 3.0.3 / 1.9.0 / 2.4.6
```

Plus, inside the notebook (self-enforcing): frozen-folds sha256[:16] == `96937649526bcadb`; 2781 rows; labels 0..4; Id order == train order; F0 OOF == 0.726616 ± 1e-6; main-log read-before/assert-after; pre-write guards on every artifact path.

---

## 9. Project Authorization Gates

Execution requires a written Project Authorization Note containing, at minimum:

```text
PHASE 7 EXECUTION AUTHORIZATION
Date: ____
Authorized starting commit hash: ____
Variant ladder ratified as specified in brief §9: yes / amended (attach amendments)
Thresholds ratified as specified in brief §16.3: yes / amended
Artifact names ratified (brief §13): yes / amended
Authorized executor: Fable / Codex / ____
Signature (user/project director): ____
```

No note ⇒ no execution. An amended note freezes the amendments; further mid-run changes are a stop condition.

---

## 10. Failure Conditions and Stop Rules

Stop immediately, report, and await user/project director input if any of the following occurs (superset of brief §11 edge cases):

1. HEAD ≠ authorized hash; or staged files / tracked modifications / forbidden-path diffs appear at any point.
2. Frozen-fold integrity failure (count, labels, order, or sha mismatch).
3. F0 gate failure (anchor not reproduced within ±1e-6).
4. Any probability invalid (NaN, outside [0,1]) or single-class validation fold.
5. `estimator.classes_` does not locate label 1 exactly once.
6. Artifact path collision (pre-write guard trip).
7. Any leakage warning or fit-scope doubt raised by reviewer or executor.
8. Mandatory slice (n ≥ 50) degradation > 0.02 on an otherwise-passing rung (escalation, not auto-decision).
9. Any request to add/alter variants, features, thresholds, or model parameters mid-run.
10. `logs/experiment_log.csv` differs at any checkpoint.
11. Environment versions differ from the pinned set.
12. Any action that would require a forbidden capability (HPO, submission, model family, LB, external data, Phase 8).

---

## 11. Output Audit Procedure

After execution, **a role other than the executor** (or the operator directly) must:

1. Recompute every reported OOF ROC-AUC from the persisted `outputs/oof/phase7_*_oof_predictions.csv` files independently (e.g., stdlib rank-based AUC — the 6A pattern) and match the variant summary to ≤ 1e-9.
2. Verify F0's OOF vector is consistent with the committed Phase 6 OOF (max |Δ| at floating-point level).
3. Recheck fold integrity from the artifacts (row counts, labels, Id↔fold mapping vs the frozen file).
4. Re-evaluate the acceptance rule per rung from the recomputed numbers; confirm the report's adopted/rejected/escalated labels.
5. Inspect the slice report: all mandatory dimensions present; n < 50 rows flagged; no unexplained gaps.
6. Run the §1 git checks: only the expected new untracked artifacts; nothing tracked modified; forbidden paths clean; main log byte-identical.
7. Record the audit outcome in the draft `phase7_acceptance.md`.

---

## 12. Phase 7 Closure Criteria

Phase 7 closes only when **all** hold:

1. All pre-registered rungs executed (or explicitly skipped by recorded decision) within the cap.
2. Every rung classified adopted / rejected / escalated-and-resolved per the pre-registered rule.
3. Independent audit (§11) passed.
4. `docs/07_feature_engineering/phase7_acceptance.md` written, including: the adopted feature set (possibly empty — a clean null result also closes the phase), the imputation-policy decision with evidence (F1 vs F5 vs Vref7), the BMI disposition record, slice findings, warnings, and the Phase 8 dependency notes.
5. User/project director sign-off recorded in the acceptance record.
6. Selective commit executed on explicit instruction; commit hash recorded back into the acceptance record (the `f1fb717`→`c4d5647` pattern).
7. No unresolved leakage warning; main log untouched; no submission generated.

---

## 13. Handoff to Phase 8 Without Opening Phase 8

At closure, prepare (inside `phase7_acceptance.md`, no new files): the frozen post-Phase-7 anchor and feature set; the F1/F5/Vref7 evidence summary as model-comparison context (tree-depth caveat explicitly stated); open questions routed to Phase 8 (e.g., whether native-missing-value learners change the missingness picture — *names only, no experiments*); and the statement:

```text
Phase 8 remains locked.
```

Phase 8 may be considered only after Phase 7 is executed, audited, accepted, committed, hash-recorded, free of critical leakage warnings — **and** explicitly authorized by the user/project director.
