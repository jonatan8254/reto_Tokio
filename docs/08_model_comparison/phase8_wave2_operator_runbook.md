# Phase 8 Wave 2 Operator Runbook — How to Use the Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-17
**Companion documents:** `phase8_wave2_master_planning_brief.md` (the plan), `prompt_codex_phase8_wave2_execution_plan.md` (the future execution prompt)
**Standing rule:** Wave 2 execution is blocked until §12's gates are satisfied. No package install, no environment creation. **Phase 9, Phase 10 and Phase 11 remain locked.**

---

## 0. Purpose

This runbook tells the user/project director exactly how to take the Phase 8 Wave 2 planning package from "planned" to "executed, audited, accepted, and commit-anchored" without breaking any project gate — and, above all, without contaminating the pinned environment that produced every accepted result. It is procedural; all methodology lives in the master brief.

---

## 1. Required Starting State

Before doing anything with this package, verify (read-only):

```powershell
git rev-parse --short HEAD     # expected: 041ba10, or the successor hash if the planning docs were committed
git status --short             # only known untracked items; nothing staged; no tracked modifications
git diff --check               # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
git diff -- logs/experiment_log.csv   # empty (unchanged)
```

Also confirm these exist (committed in `041ba10`): `docs/08_model_comparison/phase8_acceptance.md`, `notebooks/08_phase8_model_family_comparison.ipynb`, `outputs/oof/phase8_model_family_comparison_v1_m0_random_forest_frozen_oof_predictions.csv`, `outputs/oof/phase8_model_family_comparison_v1_m1_logistic_regression_oof_predictions.csv`, `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`.

Confirm no Wave 2 artifact already exists: no `phase8_wave2_*` file under `outputs/`, and no `notebooks/08b*`/`08c*` notebook.

If any check fails: stop, classify (blocker / warning / informational), and resolve before proceeding.

**Recommended policy:** do not authorize Wave 2 execution from an untracked planning package. Commit the three planning documents first (step 3 of §7), then use the resulting HEAD as the authorized starting hash recorded in the Project Authorization Note.

---

## 2. File Usage Order

1. `phase8_wave2_master_planning_brief.md` — read fully; this is the decision document.
2. This runbook — follow the workflow in §7.
3. `prompt_codex_phase8_wave2_execution_plan.md` — use **only after** the §12 gates pass; it is inert until then.

---

## 3. When to Use Each Deliverable

| Situation | Use |
|---|---|
| Deciding whether Wave 2 is well-designed | Master brief §§0–15, 18 |
| Choosing the environment/dependency strategy | Master brief §7 + this runbook §9 |
| Ratifying the GBDT registry, configs and cap | Master brief §8, §11, §14, §20 checklist |
| Deciding CatBoost | Master brief §9 + this runbook §10 |
| Reviewing the future notebook design | Master brief §12 + this runbook §8 |
| Preparing to authorize execution | This runbook §§4, 7, 11–12 |
| Launching the execution session | Deliverable C (the Codex prompt), with the Project Authorization Note attached |
| Auditing results after execution | This runbook §14 |
| Closing Wave 2 | This runbook §15 |

---

## 4. What the Project Director Must Review Before Authorizing Execution

Checklist (mirrors brief §20):

- [ ] Brief read; no objection to the block architecture (§10) or the staged Sub-wave 2A/2B design (§8).
- [ ] **Environment strategy decided** (§7): read-only dependency check authorized; separate Wave 2 env (mirroring scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6 + pinned GBDTs) authorized; `.venv`/requirements explicitly *not* mutated.
- [ ] GBDT registry ratified exactly (model_keys, configs, statuses), or amended in writing.
- [ ] Cap confirmed: ≤ 3 trained GBDTs.
- [ ] **CatBoost decision recorded** (§9): authorize Sub-wave 2B with School-exclusion reconfirmation, or defer/omit.
- [ ] Thresholds confirmed: flag rule 0.005436 + ≥ 4/5 same-sign vs M0; slice guard (n ≥ 50; 0.02 escalation); M0 anchor tolerance ± 1e-9.
- [ ] Understood and accepted: Wave 2 produces a **classified evidence table, not a winner**; selection happens in `phase8_wave2_acceptance.md`.
- [ ] Artifact names (brief §12.8/§16) accepted, including the `phase8_wave2_external_gbdt_v1` namespace.
- [ ] Decision made on committing the three planning docs before execution (recommended).
- [ ] Authorized starting hash written into the Project Authorization Note.
- [ ] Confirmed comparators m0/m1 are **carried from persisted OOF, not retrained**.

---

## 5. What Claude Opus Is Allowed to Do

- Plan, audit, review, and verify (read-only by default).
- Create/update **only** explicitly authorized files (the three Wave 2 planning docs in this run).
- After explicit authorization: implement and headlessly execute the `08b`/`08c` notebooks **in the authorized separate environment**, run post-run verification, and report.
- Stage/commit **only** named files, **only** on an explicit instruction for that exact action.
- Never: install into `.venv`, modify `requirements`/lockfiles, HPO, submissions, ensembles, leaderboard use, external data, forbidden-path modification, Wave 1 artifact modification, Phase 9/10/11.

## 6. What Codex / Executor Is Allowed to Do Later

- Same boundary set as §5, scoped by Deliverable C.
- Codex receives the execution prompt **only after** the §12 gates pass and the Project Authorization Note exists.
- Codex must stop on any failed integrity check and return control to the user/project director; it may not self-expand scope, add or substitute models, alter configs, install packages, create environments, mutate `.venv`, or commit.
- If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project director approval (Fidelity Contract, Deliverable C).

---

## 7. Step-by-Step Workflow

1. **Verify starting state** (§1 commands). Any failure ⇒ stop.
2. **Review the brief**; complete the §4 checklist.
3. *(Recommended)* **Selectively commit the three planning docs** (explicit instruction; individual `git add` per file; record the new hash).
4. **Write the Project Authorization Note** (§12 format) including the authorized hash, the environment decision, the ratified registry, the CatBoost (2B) decision, and any amendments.
5. **Run the read-only dependency check** (`08b`): authorize implementation + headless execution of `08b` *only*; it installs nothing and trains nothing; review `dependency_report` + `environment_report`.
6. **Decide on install** based on `08b`: if the director authorizes, create the **separate** Wave 2 env (pinned mirror + pinned GBDTs) — never `.venv`.
7. **Launch comparison** by giving the executor Deliverable C + the Project Authorization Note; executor runs Block 0 checks live; proceeds only on all-PASS.
8. Executor implements `08c` per the brief §12 blueprint; **independent static review** (two-role rule: mle-reviewer + code-reviewer/python-reviewer + silent-failure-hunter + eval-harness) before execution.
9. Executor runs `08c` headlessly in the separate env; M0 anchor recheck and all integrity asserts are self-enforcing (stop-on-fail).
10. **Post-run audit** (§14 below) — independent of the executor's self-report.
11. **Decision meeting**: review the classified evidence table (promotable / no_qualifying / escalated / failed_run per GBDT); the director selects candidate(s) (or records a null result); draft `phase8_wave2_acceptance.md`; the director signs; selective commit; record hash. **Phase 9/10/11 stay locked.**

---

## 8. How to Review the Notebook Architecture Before Execution

Before authorizing Codex, the project director must check, against brief §12:

- **Two-notebook structure:** `08b` is read-only (no install, no training); `08c` runs only in the separate authorized env. No install logic inside `08c`.
- **Comparator carryover:** `08c` loads m0/m1 from persisted Wave 1 OOF and re-verifies M0 (== 0.8116502602456482 ± 1e-9); it does **not** retrain RF/LR.
- **F2 fidelity:** builds exactly the 21 F2 features with the audited builder; `Id`/`Drafted`/`School` asserted out; flag sums asserted against known missingness counts.
- **Registry fidelity:** the registry cell matches brief §8 verbatim — statuses, configs, cap ≤ 3, CatBoost gated. Nothing promoted from Gated/Blocked without authorization.
- **No HPO:** single config per family; no loops over parameter values; no `eval_set`/early stopping.
- **CatBoost gate:** CatBoost runs only if Sub-wave 2B is authorized, with `cat_features=[]` and a School-exclusion assert.
- **School exclusion:** School appears only in the diagnostic slice, never in any feature matrix (assert present).
- **Artifact paths:** exactly the §12.8 `phase8_wave2_external_gbdt_v1` names with pre-write guards and a manifest cell.
- **Leakage checks:** fold-fitted pipelines only; main-log read-before/assert-after; `classes_` helper; OOF validity asserts; frozen-fold sha assert.
- **Codex prompt fidelity:** Deliverable C matches the blueprint one-to-one (brief §12.9 traceability); the Fidelity Contract section is present and unmodified.

Any mismatch ⇒ do not authorize; amend the planning package first.

---

## 9. How to Review the Environment and Dependency Strategy

Against brief §7:

- **`.venv` is sacred.** Confirm the plan never installs into `.venv` and never edits `requirements`/lockfiles. The pinned stack (Python 3.13.13 / scikit-learn 1.9.0 / pandas 3.0.3 / numpy 2.4.6) reproduces M0 = F2 to 6.66e-16; mutating it endangers all accepted work.
- **Separate env mirrors the pinned scientific stack** plus pinned GBDT versions, so the F2 pipeline behaves identically and only the GBDTs are new.
- **Read-only check first.** `08b` must record versions and GBDT wheel availability/compatibility on Python 3.13 and install nothing.
- **Pinned versions.** The director should require named, pinned XGBoost/LightGBM/CatBoost versions in the authorization note (not floating `latest`), and confirm Windows runtime prerequisites (e.g., LightGBM/OpenMP) are noted.
- **Rollback.** A separate env is trivially discardable; `.venv` is never at risk.

If the dependency check reveals incompatibility, **defer** Wave 2 (Strategy C) rather than forcing installs.

---

## 10. How to Review the CatBoost Double Gate

Against brief §9:

- **Gate 1:** the general Wave 2 authorization exists.
- **Gate 2:** a separate explicit line authorizes Sub-wave 2B (CatBoost).
- **School reconfirmation:** the note re-affirms School stays excluded; the notebook asserts `School ∉ features`.
- **No native categorical:** CatBoost runs with `cat_features=[]` on the same pre-encoded numeric F2 matrix as XGB/LGBM — its target-statistic encoding is disabled. Verify the config assert.
- **Deferrable:** if 2A already answers the question, or 2B risk outweighs value, omit CatBoost. XGBoost + LightGBM alone is a complete, defensible Wave 2.

If any gate is unmet, CatBoost is not run.

---

## 11. Commands/Checks to Request Before Execution

Immediately before the comparison run (`08c`, inside the execution session):

```powershell
git rev-parse --short HEAD          # must equal the authorized hash
git status --short                  # no staged files; no tracked modifications
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git ls-files docs/08_model_comparison/phase8_wave2_master_planning_brief.md docs/08_model_comparison/phase8_wave2_operator_runbook.md docs/08_model_comparison/prompt_codex_phase8_wave2_execution_plan.md
# expected: all three files listed (tracked) — per the §1 recommended policy
# In the SEPARATE Wave 2 env (NOT .venv):
python -c "import sys,sklearn,pandas,numpy; print(sys.version.split()[0], sklearn.__version__, pandas.__version__, numpy.__version__)"
# expected: 3.13.13 / 1.9.0 / 3.0.3 / 2.4.6  (mirror of the pinned stack)
python -c "import xgboost,lightgbm; print('xgb', xgboost.__version__, 'lgbm', lightgbm.__version__)"   # pinned versions present
# catboost import only if Sub-wave 2B authorized
```

Plus, inside `08c` (self-enforcing): frozen-folds sha256[:16] == `96937649526bcadb`; 2781 rows; labels 0..4; Id order == train order; m0 persisted OOF recomputed == 0.8116502602456482; main-log read-before/assert-after; pre-write guards on every artifact path; no pre-existing `phase8_wave2_external_gbdt_v1_*` artifact; `.venv` and `requirements` unmodified.

---

## 12. Project Director Authorization Gates

Execution requires a written Project Authorization Note containing, at minimum:

```text
PHASE 8 WAVE 2 EXECUTION AUTHORIZATION
Date: ____
Authorized starting commit hash: ____
Environment strategy: read-only dependency check authorized: yes
                      separate Wave 2 env (pinned mirror + pinned GBDTs) authorized: yes / not yet
                      .venv / requirements modification: NOT authorized (confirm)
GBDT registry ratified as specified in brief §8: yes / amended (attach amendments)
Pinned GBDT versions: xgboost==____  lightgbm==____  catboost==____ (if 2B)
Sub-wave 2A (XGBoost + LightGBM): authorized
Sub-wave 2B (CatBoost): authorized + School-exclusion reconfirmed / deferred / omitted
Run cap (<= 3 trained GBDTs): confirmed
Thresholds ratified as specified in brief §20.5: yes / amended
Artifact names + namespace ratified (brief §12.8 / §16): yes / amended
Comparators m0/m1 carried from persisted OOF, not retrained: confirmed
Authorized executor: Opus / Codex / ____
Signature (user/project director): ____
```

No note ⇒ no execution. An amended note freezes the amendments; further mid-run changes are a stop condition. The dependency-install step (separate env) is itself a gated decision the note must grant explicitly; if the note authorizes only the read-only check, stop after `08b`.

---

## 13. Failure Conditions and Stop Rules

Stop immediately, report, and await user/project director input if any of the following occurs:

1. HEAD ≠ authorized hash; or staged files / tracked modifications / forbidden-path diffs appear at any point.
2. A `phase8_wave2_*` artifact already exists at session start (possible double execution).
3. Any attempt or evidence of install into `.venv`, or modification of `requirements`/lockfiles.
4. Frozen-fold integrity failure (count, labels, order, or sha mismatch).
5. M0 anchor recheck failure (m0 persisted OOF ≠ 0.8116502602456482 ± 1e-9).
6. Any probability invalid (NaN, outside [0,1]) or single-class validation fold.
7. `estimator.classes_` does not locate label 1 exactly once.
8. Artifact path collision (pre-write guard trip).
9. Any leakage warning or fit-scope doubt; CatBoost run without the 2B gate or with non-empty `cat_features`.
10. Mandatory slice (n ≥ 50) degradation > 0.02 vs M0 on any GBDT (escalation — recorded, never auto-decided).
11. Any request to add/substitute models, alter configs, tune parameters, add `eval_set`/early stopping, or install additional packages mid-run.
12. `logs/experiment_log.csv` differs at any checkpoint.
13. Environment versions differ from the pinned mirror; or a GBDT import unexpectedly resolves against `.venv`.
14. Any action that would require a forbidden capability (HPO, submission, ensemble, LB, external data, Phase 9/10/11).

A GBDT failing to import or converge is **not** a stop condition: record it as `failed_run`, continue the remaining registry, report.

---

## 14. Output Audit Procedure

After execution, **a role other than the executor** (or the director directly) must:

1. Recompute every reported OOF ROC-AUC from the persisted `outputs/oof/phase8_wave2_*_oof_predictions.csv` files independently (stdlib rank-based AUC — the 6A/7/Wave-1 pattern) and match the model summary to ≤ 1e-9.
2. Verify the m0 comparator vector matches the committed Wave 1 m0 OOF (max |Δ| at floating-point level) and reproduces 0.8116502602456482.
3. Recheck fold integrity from the artifacts (row counts, labels, Id↔fold mapping vs the frozen file) for every GBDT.
4. Re-apply the §14 flag rule from the recomputed numbers; confirm classifications (promotable / no_qualifying / escalated / failed_run) and the paired-vs-M1 readout.
5. Inspect the slice report: all 7 mandatory dimensions per GBDT; n < 50 flagged; escalations match; check `Age_missing=1` (n=435, 8 positives) explicitly against M0 0.6917 and m1 0.5442.
6. Verify the dependency_report and environment_report record exact pinned versions; confirm `.venv`/`requirements` are byte-unchanged.
7. Verify the artifact manifest: every listed file exists, sha256 matches, no unlisted `phase8_wave2_*` file.
8. Run the §1 git checks: only expected new untracked artifacts; nothing tracked modified; forbidden paths clean; main log byte-identical.
9. Record the audit outcome in the draft `phase8_wave2_acceptance.md`.

---

## 15. Wave 2 Closure Criteria

Wave 2 closes only when **all** hold:

1. All ratified registry GBDTs executed (or recorded as `failed_run` / explicitly skipped by recorded decision) within the cap; CatBoost run only if 2B was authorized.
2. Every GBDT classified per the pre-registered flag rule; escalations resolved by recorded director decision.
3. Independent audit (§14) passed; `.venv`/requirements confirmed unchanged.
4. `docs/08_model_comparison/phase8_wave2_acceptance.md` written, including: the classified evidence table; the director's selection of candidate(s) for future phases (or an explicit null result — also a valid closure); the CatBoost reading (if run) with its gate record; slice findings incl. `Age_missing=1`; the threshold-provenance limitation; the environment/dependency record; warnings; and the Phase 9/10/11 dependency notes.
5. Project director sign-off recorded.
6. Selective commit executed on explicit instruction; commit hash recorded back into the acceptance record (the `041ba10` pattern).
7. No unresolved leakage warning; main log untouched; no submission generated; no `.venv` mutation.

---

## 16. Handoff to Phase 9 Without Opening Phase 9

At closure, prepare (inside `phase8_wave2_acceptance.md`, no new files): the selected GBDT candidate(s) (or null result) with their evidence vs M0 and M1; the consolidated Phase 8 picture (Wave 1 + Wave 2) as Phase 9 input; open questions routed forward *as names only, no experiments* — e.g., per-family seed-noise calibration before final selection (Phase 9), error analysis of where GBDTs and sklearn families disagree (Phase 9), whether any candidate merits HPO (Phase 10, only after its 7 documented conditions), submissions (Phase 11) — and the statements:

```text
Phase 9 remains locked.
Phase 10 remains locked.
Phase 11 remains locked.
Future phases remain locked.
```

A later phase may be considered only after Wave 2 is planned, authorized, executed (if so decided), audited, accepted, committed (if authorized), hash-recorded, free of critical leakage warnings — **and** the user/project director explicitly authorizes opening that specific phase.
