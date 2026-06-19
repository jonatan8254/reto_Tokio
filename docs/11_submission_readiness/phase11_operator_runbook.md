# Phase 11 Operator Runbook — How to Use the Submission Readiness Planning Package

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Operator runbook (Deliverable B of the Phase 11 planning package).
**Date:** 2026-06-19
**Companion documents:** `phase11_master_planning_brief.md` (A), `prompt_codex_phase11_submission_readiness_execution.md` (C), `prompt_opus_phase11_final_submission_review.md` (D).

> This runbook explains how to move from planning to authorized execution **without breaking any submission-readiness gate**. It authorizes no execution by itself. Phase 11 stays locked until a signed Phase 11 Project Authorization Note exists. **No automatic upload ever occurs.**

---

## 0. Purpose

Give the project director and any operator (human, Opus, Codex) a single, sequential procedure for: reviewing the Phase 11 plan, deciding the final candidate and the CatBoost stability decision, authorizing execution safely, running the Codex executor, auditing its outputs with Opus, validating the submission file, and handing the file to the director for **manual** upload — all while preserving F2, the candidate roles, the official submission format, artifact lineage, and the no-winner / no-leaderboard-for-selection / no-auto-upload invariants.

## 1. Required Starting State

Before anything, verify (read-only):

```bash
git rev-parse --short HEAD        # expect de11fae or a documented successor preserving Phase 10 acceptance
git status --short                # no staged files; only known untracked items
git diff --check                  # clean
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # empty
git diff -- logs/experiment_log.csv   # empty
find outputs/submissions -maxdepth 2 -type f   # only submission_001_baseline.csv (pre-existing)
```

Also confirm present and accepted: `docs/10_model_optimization/phase10_acceptance.md`, the `phase10_standard_20260619_0152_*` artifacts (validation report, selection-bias report, model_summary, slice_report, hpo_results, 2 tuned OOF), `docs/05_methodology/validation_protocol_phase6.md`, `docs/05_methodology/leakage_checklist_phase6.md`, `docs/00_project_contract/submission_checklist.md`, `docs/00_project_contract/challenge_brief.md`, the official `data/input/{train,test,sample_submission}.csv` (2781 / 696 / 696 rows), and the frozen fold file (SHA256[:16] `96937649526bcadb`). If any is missing → **Stop** (§16).

## 2. File Usage Order

1. `phase11_master_planning_brief.md` — read first; it is the governing design.
2. `phase11_operator_runbook.md` — this file; the procedure.
3. `prompt_codex_phase11_submission_readiness_execution.md` — used **only after** a signed authorization note.
4. `prompt_opus_phase11_final_submission_review.md` — used **only after** Codex execution produces artifacts.
5. `docs/11_submission_readiness/phase11_acceptance.md` — created by Opus as a draft at the end; signed by the director.

## 3. When to Use Each Deliverable

| Deliverable | Used by | When | Produces |
|---|---|---|---|
| A — Master brief | Director / Opus | Review & authorization decision | Understanding + authorization inputs |
| B — Runbook | Operator | Throughout | Sequencing + gate discipline |
| C — Codex prompt | Codex | After signed authorization note | Notebook + artifacts + submission |
| D — Opus review prompt | Opus | After Codex execution | Submission audit + acceptance draft |

## 4. What the User/Project Director Must Review Before Authorizing Execution

- The candidate eligibility table (brief §11) — confirm CatBoost tuned primary, M1 baseline fallback, M1 tuned rejected, M0 anchor, XGB/LGBM dropped.
- The final candidate decision options (brief §12) — **select one of Option A / B / C / D.**
- The **CatBoost Stability Gate** (brief §13) — decide: **run the repeated-CV stability audit** or **sign a written waiver** with the explicit acknowledgement (best global OOF but slice warnings + no repeated-CV).
- The F2 feature/data contract (brief §15) — confirm F2-only, School excluded, no external data.
- The submission validation suite (brief §18) — confirm the 696-row / `Id,Drafted` / Id-order / [0,1] / no-NaN-inf-dup / no-manual-edit / SHA-256 gates.
- The leaderboard + upload policy (brief §19) — reaffirm: LB never selects; upload is manual, user-side; **last submitted file = final ranking**.
- Reaffirm the locks: no final winner, no submission-ready model before validation+review, no Phase 11 modeling reopening, no auto-upload.

## 5. What Opus Is Allowed to Do in Planning

Read-only repository inspection; create/update only the four planning deliverables in `docs/11_submission_readiness/` (this run already did so); align with methodology; design the candidate selection gate, CatBoost stability gate, refit/inference protocols, submission validation suite, artifact architecture, notebook standard, stop rules, acceptance criteria. **Opus executes no refit, runs no inference, creates no notebook now, generates no submission, uses no leaderboard, declares no winner, stages/commits nothing.**

## 6. What Codex Is Allowed to Do in Future Execution

Only after a signed authorization note: create `notebooks/11_phase11_submission_readiness.ipynb`; verify the authorized commit + Phase 10 acceptance; load official data + Phase 10 accepted artifacts; resolve the candidate selection gate and the CatBoost stability gate/waiver per the note; build the **F2** matrix (assert School excluded); **fit preprocessing + the selected model on full train only**; run leakage-safe **test inference**; **generate the submission CSV** under `outputs/submissions/`; run the **full submission validation suite**; write versioned artifacts + a **candidate** log row (never the main log); run CatBoost only in the **separate Wave 2 environment**. Codex **must not**: upload; use the leaderboard for selection; declare a winner; reopen HPO/XGBoost/LightGBM; build ensembles/calibration/threshold tuning; introduce new features or School or external data; manually edit predictions; touch forbidden paths; stage/commit/push.

## 7. What Opus Is Allowed to Do After Codex Execution

Read-only audit of Codex outputs; **independent verification** of the submission (schema, 696 rows, Id set/order, probability range, no NaN/inf/dup, SHA-256, lineage) verifier ≠ generator; review of the candidate selection gate and CatBoost stability gate/waiver; a phase-gated recommendation matrix; the acceptance **draft** (`phase11_acceptance.md`, signature blank). Opus **must not** upload, change predictions, declare a final winner without director acceptance, use the leaderboard, or open new modeling.

## 8. What No Agent Is Allowed to Do

Upload any file (manual, user-side only); use the public leaderboard for any selection; declare a final winner / submission-ready model before validation + review + acceptance; reopen HPO/XGBoost/LightGBM; build ensembles/blending/stacking/calibration/threshold tuning; use external data; use School as a feature; manually edit predictions; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`; run `git add .` / `git commit -a`; stage/commit/push without an explicit per-action instruction; fit any transform/model on test data.

## 9. Step-by-Step Workflow

1. **Review** (Director + optional read-only `mle-reviewer`): read brief; confirm starting state (§1).
2. **Decide** (Director): candidate option (brief §12); CatBoost stability — audit or waiver (brief §13); reaffirm locks.
3. **Authorize** (Director): write & sign the Phase 11 Project Authorization Note (records the authorized hash, the candidate option, the stability decision, and per-file submission authorization).
4. **Execute** (Codex via Deliverable C): build notebook; P11-B0 gate → P11-B1 selection gate → P11-B2 stability gate/waiver → P11-B3 F2 build → P11-B4 full-train refit → P11-B5 test inference → P11-B6 submission + validation → P11-B7 artifacts + candidate log.
5. **Independent review** (Opus via Deliverable D): re-verify submission schema/Id-order/probability-range/hashes/lineage; produce recommendation matrix + acceptance draft. If mismatch → **Stop/Blocker**.
6. **Close** (Director): review acceptance draft; if approved, authorize a **selective** commit of the trackable artifacts (the submission CSV is gitignored — record its SHA-256) and record the resulting hash into `phase11_acceptance.md`.
7. **Manual upload** (Director only, §21): choose the file and the **upload order** (last file = final ranking); upload via the competition page; record timestamp/order manually. **No agent uploads.**

## 10. Commands/Checks to Request Before Execution

```bash
# baseline gate
git rev-parse HEAD
git status --short
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git diff -- logs/experiment_log.csv
# official files (read-only): train 2781, test 696, sample_submission 696; columns Id,Drafted
# fold integrity (read-only; reference lineage): SHA256[:16] = 96937649526bcadb
# Phase 10 acceptance + artifacts present
```

Inside the notebook, the executor must additionally: assert HEAD == authorized hash; assert `test.csv` has no `Drafted`; assert F2 column-set and School-absent; verify `estimator.classes_` contains label 1; fit transforms on full train only (no test access in fit); validate the submission per §14; read `logs/experiment_log.csv` before and assert byte-identical after; check-and-fail on existing artifact paths.

## 11. Project Authorization Gates

- **Gate A (planning accepted):** director has read the brief and runbook.
- **Gate B (decisions made):** candidate option + CatBoost stability decision recorded.
- **Gate C (authorization signed):** Phase 11 Project Authorization Note signed with the authorized hash and per-file submission authorization.
- **Gate D (execution complete):** Codex artifacts + validated submission produced; no forbidden-path / main-log changes.
- **Gate E (independent review passed):** submission schema/Id-order/probability/hashes/lineage verified by Opus.
- **Gate F (acceptance signed):** director signs `phase11_acceptance.md`; selective-commit hash + submission SHA-256 recorded.
- **Gate G (manual upload):** director uploads; ordering/timestamp tracked manually. Separate and director-only.

## 12. Candidate Selection Gate

The selection is resolved **before** any full-train fit, using **OOF evidence only** (never the leaderboard). Default: **CatBoost tuned primary + M1 baseline fallback** (brief §12 Option A, optionally superset Option C to produce both). The gate records: chosen candidate(s); the Phase 10 OOF deltas (CatBoost tuned +0.0186706 vs M0 / +0.0032388 vs M1; M1 tuned rejected as noise); and confirmation that M1 tuned is **not** used and XGB/LGBM are **not** reopened. If eligibility is unclear → **Stop** and request a director decision.

## 13. CatBoost Stability Gate

CatBoost tuned may be the final-refit candidate **only if** this gate passes **or** is waived in writing (brief §13). **Pass** = a CatBoost repeated-CV stability audit (different splitter seeds, frozen-fold-consistent, diagnostic only) confirms a stable sign of lead and no catastrophic robust-slice degradation beyond the documented set. **Waiver** = a director-signed statement acknowledging CatBoost has the best global OOF AUC **but** retains slice warnings (Age_missing=1, QB, Year 2011, avail_count 0, OG, OLB) and lacks repeated-CV confirmation. **Leaderboard feedback must not be used for this gate.** If neither → fall back to M1 baseline or **block** (brief §12 B/D).

## 14. Submission Validation Checklist

- [ ] Columns exactly `Id, Drafted`.
- [ ] Row count == **696**; matches `test.csv` and `sample_submission.csv`.
- [ ] Id set exactly matches the official test/sample Id set.
- [ ] Id order matches `sample_submission.csv` (= `test.csv`).
- [ ] `Drafted` numeric; all in `[0, 1]`; no NaN; no inf.
- [ ] No duplicate Id (696 unique).
- [ ] Predictions generated by code only; **no manual edits** (regenerate-and-compare / hash).
- [ ] SHA-256 of the submission recorded in the manifest + report.
- [ ] Report identifies model, commit hash, run_id, and feature set (F2).
- [ ] File **not** uploaded automatically.

## 15. Leaderboard Upload Gate

- [ ] No leaderboard score was used to select the model or the submission.
- [ ] The submission passed the full §14 validation suite.
- [ ] The Opus review (Deliverable D) accepted the artifact (with or without warnings) or the director overrode with documentation.
- [ ] The director (not any agent) performs the upload via the competition page.
- [ ] Under multiple valid files, the director consciously chooses the **upload order** (last file = final ranking).
- [ ] Upload timestamp/order recorded manually by the director.
- [ ] No repeated upload loop; no model change driven by public LB without a new documented phase.

## 16. Failure Conditions and Stop Rules

Apply brief §24 in full. Hard stops: wrong/undocumented HEAD; forbidden-path diff; main-log change; missing Phase 10 acceptance/report/summary; missing submission checklist or sample submission; unresolved candidate eligibility; CatBoost gate required but neither passed nor waived; feature-contract violation (new feature / School); external data; HPO; test used for fitting; unconfirmable probability direction; unverifiable row count / Id set / Id order; NaN/inf/out-of-range predictions; manual editing; leaderboard used for selection; any automatic upload attempt; a winner declared during planning. On any stop: **stop, report, await the director** — never improvise past it.

## 17. Output Audit Procedure

1. Confirm all expected artifacts exist (brief §21) and are contract-named with `run_id`.
2. Independently re-validate the submission: columns, 696 rows, Id set/order vs `sample_submission.csv`, `[0,1]` range, no NaN/inf, no duplicate Id.
3. Recompute the submission **SHA-256** and confirm it matches the manifest/report.
4. Confirm the selected candidate config matches the recovered Phase 10 config (CatBoost: depth 6 / lr 0.01 / l2 9 / iters 800 / border 128 / seed 42; M1 baseline: the recovered Phase 8 config).
5. Confirm no test data entered any `fit` (read the notebook statically).
6. Confirm `logs/experiment_log.csv` byte-identical; only the authorized submission appears under `outputs/submissions/`; `.venv`/`requirements.txt` unchanged.
7. Record PASS/BLOCKER; on blocker, stop and report.

## 18. Notebook Quality Review Checklist

- [ ] Title, scope, explicit non-actions present.
- [ ] Clean imports; `PROJECT_SEED`; `experiment_id`/`run_id`; centralized relative paths.
- [ ] Authorized-commit validation; loads only official data + Phase 10 accepted artifacts.
- [ ] Candidate selection gate + CatBoost stability gate/waiver check present.
- [ ] F2 built; School-exclusion assert; missingness flags + `available_measurement_count` recomputed deterministically.
- [ ] All learned preprocessing fitted on **full train only**; test transformed only.
- [ ] Positive-class probability via verified `estimator.classes_`.
- [ ] Submission generated by code; §14 validation suite implemented inline.
- [ ] Markdown objective/inputs/method/output/risk before each major block; interpretation after results.
- [ ] Versioned artifact writes with check-and-fail; commit hash + environment recorded.
- [ ] No test fitting, no School/external data, no leaderboard, no auto-upload, no HPO, no winner-before-acceptance.

## 19. Submission Artifact Review Checklist

- [ ] Submission file exists under `outputs/submissions/phase11_submission_readiness_<run_id>_<candidate>_submission.csv` (gitignored — identity is its SHA-256).
- [ ] Passes the full §14 validation suite independently.
- [ ] Manifest lists the submission with its SHA-256, row count, and head/tail Id check.
- [ ] Validation report links lineage: anchor (M0) → feature blocks (Phase 7 F2) → comparison (Phase 8) → diagnostics (Phase 9A) → HPO (Phase 10) → final refit (Phase 11).
- [ ] Candidate experiment log row written (separate file; main log untouched).
- [ ] No second, undocumented submission file present.

## 20. Phase 11 Closure Criteria

Phase 11 closes only when: future-execution acceptance criteria (brief §23) are met; the submission passed the §14 suite; the validation report + submission validation + final refit report + artifact manifest + candidate log exist; the Opus review produced a phase-gated recommendation (accept-with-warnings / accept-pending-user-decision / reject-regenerate / use-fallback / additional-audit / defer / prohibited); the director signs `phase11_acceptance.md`; and (on explicit instruction) a selective commit is made with its hash + the submission SHA-256 recorded. **The director's manual upload is a separate, post-closure action; no agent uploads.**

## 21. Handoff to Manual Upload Without Automating Upload

The Phase 11 acceptance prepares a **validated submission file** and a clear **upload note** for the director — it does **not** upload. The director: (a) confirms the accepted file and its SHA-256; (b) decides which file to upload and, under multiple valid files, the **order** (the **last submitted file determines final ranking**; the **private leaderboard uses the full test set**); (c) uploads via the official competition page; (d) records the upload timestamp/order manually; (e) optionally reads the public-LB score **only as a sanity check**, never as a trigger to change the model without a new documented phase. Codex/Opus never upload, never reorder, and never claim an upload occurred unless the director confirms it.
