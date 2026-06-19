# Phase 11 Master Planning Brief — Final Refit, Test Inference and Submission Readiness

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Document type:** Master planning brief (Deliverable A of the Phase 11 planning package). **Planning only — Phase 11 is not executed by this document.**
**Date:** 2026-06-19
**Authoring brain:** Opus (strategic architect / methodological auditor).
**Companion deliverables:** `phase11_operator_runbook.md` (B), `prompt_codex_phase11_submission_readiness_execution.md` (C), `prompt_opus_phase11_final_submission_review.md` (D).

> This brief designs a future Phase 11. It trains nothing, refits nothing, runs no inference, creates no submission, uses no leaderboard, and declares no winner. Phase 11 execution remains **locked** behind a separate, signed authorization.

---

## 0. Executive Verdict

Phase 11 is designed as a **bounded, reproducible, leakage-safe, submission-format-safe final-refit and submission-readiness phase**. It carries the Phase 10 evidence forward without reinterpreting it:

- **Primary final-refit candidate (planning):** `catboost_tuned` — best global OOF ROC-AUC (`0.8303208581`), beating the M0 anchor by **+0.0186706 (5/5 folds)** — **warning-heavy and not a final winner**. It does **not** clear the historical promotion bar over M1 (+0.0032388 < 0.005436, 3/5 folds), has **no repeated-CV stability confirmation**, and retains robust-slice warnings.
- **Fallback / reference candidate:** `m1_logistic_regression` **baseline** — simpler, more stable, statistically indistinguishable from its tuned variant.
- **Rejected tuned variant:** `m1_logistic_regression_tuned` (noise-level: +0.0003998, 3/5 folds).
- **Anchor only:** `m0_random_forest_frozen`. **Dropped:** XGBoost, LightGBM (`no_qualifying_evidence`).

Phase 11 introduces two new control gates before any submission can be relied upon: a **Candidate Selection Gate** (§12) and a **CatBoost Stability Gate** (§13, either pass-or-written-waiver). The official metric is ROC-AUC on positive-class probabilities; the official submission is `Id,Drafted`, **696 rows**, Id-order matched to `sample_submission.csv`. **No model is declared a winner or submission-ready by this brief.** Recommended next step: **§30 — A** (review and authorize the package; execution stays locked).

## 1. Repository State Verification

Read-only checks performed at authoring time:

| Check | Result | Status |
|---|---|---|
| `git rev-parse --short HEAD` | `de11fae` | PASS (= expected Phase 10 acceptance commit) |
| `git rev-parse HEAD` | `de11fae08a511a5a230a12cecb29d980aa60af74` | PASS |
| Commit message | `validation: accept phase 10 standard optimization with warnings` | PASS |
| Staged files | none | PASS |
| `git diff --check` | clean (RC 0) | PASS |
| Forbidden-path tracked diffs (`data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json`) | empty | PASS |
| `logs/experiment_log.csv` diff | empty (unchanged) | PASS |
| `outputs/submissions/` contents | only `submission_001_baseline.csv` (pre-existing Phase 2 baseline) | PASS (no Phase 11 submission) |
| `docs/11_submission_readiness/` exists before this run | no — created by this run | informational |
| Prior chain (`fc7a625`, `e894dd2`, `12c59b8`, `eb55a18`, `4bbcd7a`, `041ba10`) | present in `git log` | PASS |

`de11fae` tracked the Phase 10 acceptance + the 13 execution artifacts (notebook, 2 OOF, 6 validation CSVs, 4 reports). No blocker. Planning may proceed.

## 2. Evidence Reviewed

Phase 10: `phase10_acceptance.md` (committed), `phase10_project_authorization_note.md`, `phase10_master_planning_brief.md`, `phase10_operator_runbook.md`, `prompt_codex_phase10_execution_plan.md`, `prompt_opus_phase10_strategic_review.md`; the `phase10_standard_20260619_0152_*` validation/report/oof artifacts; `notebooks/10_phase10_model_optimization.ipynb` (static). Phase 9: `phase9b_lite_transition_memo.md`, `phase9a_acceptance.md`, `phase9a_improvement_backlog.md`. Phase 8: `phase8_acceptance.md`, `phase8_wave2_acceptance.md`. Phase 7: `phase7_acceptance.md`, `phase7b_role_interaction_acceptance.md`; frozen fold file `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`. Methodology/contract: `validation_protocol_phase6.md`, `leakage_checklist_phase6.md`, `challenge_brief.md`, `submission_checklist.md`, `project_execution_plan_v3.md` (§14 Phase 11 blueprint, §16.7 submission-readiness gates). Official data verified read-only (counts only): `train.csv` 2781×16, `test.csv` 696×15, `sample_submission.csv` 696×2.

## 3. Numerical Results and Phase 10 Carry-Forward Status

| model_key | OOF ROC-AUC | Δ vs M0 | Δ vs M1 base | +folds vs M0 | +folds vs M1 | carry status |
|---|---:|---:|---:|---:|---:|---|
| m0_random_forest_frozen | 0.8116502602456482 | — | −0.0154318 | — | 1/5 | anchor / reference only |
| m1_logistic_regression_baseline | 0.8270821069632867 | +0.0154318 | — | 4/5 | — | **fallback / reference** |
| catboost_baseline | 0.8202943968641223 | +0.0086441 | −0.0067877 | 4/5 | 2/5 | historical baseline / reference |
| m1_logistic_regression_tuned | 0.8274819177762125 | +0.0158317 | +0.0003998 | 4/5 | 3/5 | **rejected (noise-level)** |
| catboost_tuned | 0.8303208581017550 | +0.0186706 | +0.0032388 | 5/5 | 3/5 | **primary final-refit candidate (warning-heavy)** |

Global positive rate = **0.6483279396** (= train class balance 1803/2781; OOF covers all train rows). Pre-registered promotion bar (inherited): Δ ≥ **0.005436** AND same-sign positive folds ≥ **4/5** AND mandatory-slice guard clear. **CatBoost tuned clears the bar vs M0 but not vs M1.** Independent recompute in the Phase 10 review reproduced all five AUCs to ≤1.11e-16.

Recoverable tuned config (from `hpo_results.csv`): **CatBoost tuned** = `depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]`. **M1 baseline** exact config (C, penalty, solver, scaling) is **Not confirmed yet** in this planning run — future execution must recover it from the Phase 8 accepted artifacts / `notebooks/10_phase10_model_optimization.ipynb` baseline loader rather than guessing.

## 4. Frozen Decisions Preserved

1. Official metric = ROC-AUC on positive-class probabilities for `Drafted=1`; verify `estimator.classes_` before extraction.
2. Submission = `Id,Drafted`, **696 rows**, Id-order matched to `sample_submission.csv` (= `test.csv` order).
3. Feature set = **F2** only (13 base + 7 missingness flags + `available_measurement_count`); **School excluded**; no new features.
4. **CatBoost tuned = best global OOF candidate, warning-heavy, not a final winner.**
5. **M1 baseline = fallback/reference; M1 tuned = rejected (noise).**
6. **M0 = anchor only; XGBoost/LightGBM = dropped (`no_qualifying_evidence`), not reopened.**
7. No HPO, ensembles, blending, stacking, calibration fitting, or threshold tuning (ROC-AUC is threshold-free).
8. No external data; no leaderboard-for-selection; no manual prediction editing; `logs/experiment_log.csv` not modified without acceptance.
9. Phase 10 acceptance (`de11fae`) is the governing prior decision and must not be reinterpreted.

## 5. Phase 11 Purpose and Non-Purpose

**Purpose (future, authorized execution only):** resolve the final candidate under explicit gates; run the CatBoost Stability Gate or record a written waiver; refit the selected model on **full train (2781 rows)** under the F2/preprocessing contract; run leakage-safe test inference (696 rows); generate a submission CSV; run the full submission validation suite; hash artifacts and write a manifest, a validation report, and a candidate experiment log; obtain a final Opus review; **prepare the file for manual, user-side upload** without automating upload.

**Non-purpose (this planning run and always within Phase 11 planning):** no training/refit, no inference, no notebook creation/execution, no submission, no write under `outputs/submissions/`, no leaderboard, no upload, no winner/submission-ready declaration, no HPO, no ensembling/calibration/threshold tuning, no edits to `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`; no staging/commit/push.

## 6. Alignment with Existing Planning and Methodology Documents

| Source document | Key constraint or decision inherited | How Phase 11 planning must respect it | Risk if ignored | Status |
|---|---|---|---|---|
| `phase10_acceptance.md` (`de11fae`) | CatBoost tuned best OOF but warning-heavy, not winner; M1 baseline fallback; M1 tuned rejected | Carry these roles verbatim into §11/§12; do not re-rank | Contradicting the accepted record | PASS |
| `phase10_project_authorization_note.md` | Gate discipline; F2-only; School excluded; no LB; candidate-log-only | Reuse the same gate/lock pattern for Phase 11 | Scope creep | PASS |
| `phase10_validation_report.md` / `selection_bias_warning_report.md` | CatBoost no repeated-CV; deterministic search; Age_missing/QB worsened | Drive the CatBoost Stability Gate (§13) and slice caveats | Promoting on global gain alone | PASS |
| `phase9a_acceptance.md` + backlog | M1 `Age_missing=1` collapse (8 pos, fragile), QB robust loss; threshold 0.005436 provenance | Document as test-relevant caveats (test has 115 Age-missing rows) | Blind reliance on a fragile slice | PASS |
| `phase9b_lite_transition_memo.md` | M1 primary carry; CatBoost observe; XGB/LGBM dropped | Keep XGB/LGBM out of Phase 11 | Reopening dropped models | PASS |
| `phase8_acceptance.md` / `phase8_wave2_acceptance.md` | M1 candidate-with-warning; CatBoost escalated; XGB/LGBM no_qualifying_evidence; M1 baseline config source | Recover M1 baseline config from here; keep drops | Wrong baseline config | PASS (M1 exact config Not confirmed yet) |
| `phase7_acceptance.md` / `phase7b_*` | F2 adopted; F4 rejected; School excluded | Lock F2 as the only feature contract (§15) | Feature drift / leakage | PASS |
| `validation_protocol_phase6.md` | ROC-AUC; `classes_` policy; LB sanity-check only | Apply to inference + LB policy (§17/§19) | Wrong score direction | PASS |
| `leakage_checklist_phase6.md` | Learned transforms fit on train only; test for structure/inference only | Drive refit/inference contract (§15–§17) | Test leakage | PASS |
| `challenge_brief.md` | 696 test rows; last submitted file = final ranking; private LB = full test | Drive validation suite + upload-ordering policy (§18/§19) | Disqualification / format error | PASS |
| `submission_checklist.md` | Exact `Id,Drafted`; 696 rows; Id-order; probs in [0,1]; no manual edits; traceable | Becomes the §18 validation suite verbatim | Invalid submission | PASS |
| `project_execution_plan_v3.md` §14/§16.7 | Phase 11 = final refit/inference/validated submission/LB sanity; SHA-256 + head/tail Id checks; submissions gitignored; human authorization per file | Drive artifact policy (§21) + authorization gates (§29) | Untraceable submission | PASS |

## 7. Planning Document Consistency Checks

- [x] Phase 11 cannot contradict Phase 10 acceptance — roles carried verbatim (§3/§4/§11).
- [x] Phase 11 cannot reinterpret CatBoost tuned as a final winner before final submission-readiness gates — stated in §0/§11/§12/§13.
- [x] Phase 11 cannot treat M1 tuned as preferred over M1 baseline — M1 tuned is rejected (§11).
- [x] Phase 11 must preserve M1 baseline as fallback/reference — §14.
- [x] Phase 11 must keep CatBoost tuned as candidate for final-refit planning only, warning-heavy — §11/§12.
- [x] Phase 11 cannot reopen HPO — §5/§28; CatBoost uses the recovered tuned config as-is.
- [x] Phase 11 cannot reopen XGBoost/LightGBM — §11.
- [x] Phase 11 cannot introduce new features — F2-only (§15).
- [x] Phase 11 cannot use School as a feature — assert raise-on-violation (§15).
- [x] Phase 11 cannot use external data — §15/§28.
- [x] Phase 11 cannot use leaderboard to select a model — §19.
- [x] Phase 11 cannot create or upload a submission during planning — §5/§28.
- [x] Phase 11 must preserve official submission format and validation gates — §18.
- [x] Phase 11 must preserve artifact lineage and no-manual-edit policy — §21/§22.

**No contradictions found** between older and newer documents. One informational reconciliation: v3 §14 frames Phase 11 around a single accepted candidate; the actual evidence path produced a **warning-heavy primary (CatBoost tuned) plus a fallback (M1 baseline)** — handled by the Candidate Selection Gate (§12) and the dual-artifact option (§12 Option C), consistent with v3 §16.7's "accepted Phase 9/10 candidate + human authorization per file."

## 8. Scientific and Methodological Evidence Transfer

| Source / Reference | Methodological principle | Phase 11 practical decision | Section affected | Risk mitigated | Limitation / caution |
|---|---|---|---|---|---|
| `validation_protocol_phase6.md`; Cawley & Talbot (research notes) | Final refit only after selection is frozen | Selection gate (§12) precedes any full-train fit | §12/§16 | Selection bias bleeding into refit | Selection uses OOF evidence, not test |
| `leakage_checklist_phase6.md`; Kuhn & Johnson | Test must not influence fitting or model choice | Imputers/encoders fit on full train only; test for inference + structure only | §15/§16/§17 | Test leakage | Unknown test categories need safe handling |
| `submission_checklist.md` | Sample submission validates schema/order, not model fitting | `sample_submission.csv` used only for Id set/order/schema validation | §17/§18 | Hidden leakage via sample file | None beyond schema use |
| `challenge_brief.md`; QA.pdf | Leaderboard reuse causes misleading optimization | LB is post-submission sanity check only; never selects (§19) | §19 | Leaderboard chasing | Public LB = subset; private = full test |
| `validation_protocol_phase6.md` | AUC needs probabilities/scores, not hard labels | Extract `predict_proba` for `Drafted=1` after `classes_` check | §16/§17 | Wrong/zeroed AUC | Some models need calibration awareness (not fitted here) |
| `project_execution_plan_v3.md` §14; reproducibility notes | Artifact lineage is part of reproducibility | SHA-256 + manifest + commit/run_id recorded; submissions gitignored | §21/§22 | Untraceable submission | Checksum is the only durable submission identity |
| `submission_checklist.md`; GCI_sesion7.pdf | Manual prediction editing invalidates traceability and can disqualify | No manual edits; predictions generated by code only; manual-edit check | §17/§18/§22 | Disqualification | — |
| `phase10_acceptance.md` | Fallback candidates are useful when the primary is warning-heavy | M1 baseline retained as fallback; dual-artifact option | §12/§14 | Single-point failure on a warned model | Fallback is weaker on global OOF |
| `phase9a_acceptance.md`; `phase10_*slice_report` | Slice warnings must be documented before final reliance | CatBoost Stability Gate + slice caveats (Age_missing=1, QB, Year 2011) | §13 | Over-trusting a globally-best but locally-fragile model | Test has 115 Age-missing rows (16.5%) |

## 9. ECC Agents and Skills Plan

Live availability check `/plugin list ecc@ecc` was **not executed** in this planning run (read-only planning; no tool installation). Inventory below is from `project_execution_plan_v3.md` §19 and is marked **Not confirmed yet** until a live check.

| Stage or need | Agent/skill suggested | Use proposed | Risk mitigated | Activation condition |
|---|---|---|---|---|
| Phase 11 planning review (this stage) | `mle-reviewer` (read-only) | Optionally sanity-check this brief's gates/contracts | Planning blind spots | Director request; read-only |
| Future execution authoring | Codex executor (Deliverable C) | Build the Phase 11 notebook + artifacts exactly as authorized | Scope creep, leakage | Signed Phase 11 authorization |
| Post-execution audit | Opus reviewer (Deliverable D) | Independent submission/artifact audit | Self-certification, format errors | After Codex + artifacts exist |
| Format/lineage check | (built-in tools) | SHA-256, row/Id checks via stdlib | Untraceable/invalid file | During execution + review |
| Prohibited | any web/scraping/LB-loop/upload-bot agent | **Do not use** | External data / auto-upload / LB chasing | Never (project rules) |

No agent/skill installation is recommended now; no concrete gap requires a new agent for Phase 11. Prohibited categories (web scraping, external sports data, autonomous leaderboard loops, deployment, frontend/backend/API, DB optimization, prediction markets, social/content, auto-upload bots) are **excluded**.

## 10. Proposed Phase 11 Block Architecture

| Block | Name | Objective | Required evidence | Methodological basis | Outputs planned | Risks mitigated | Advancement condition |
|---|---|---|---|---|---|---|---|
| P11-B0 | Gate & integrity check | Verify HEAD, forbidden paths, Phase 10 acceptance, official files | `de11fae`; Phase 10 artifacts; official CSVs | v3 §16.7; submission_checklist | gate log (in-notebook) | Wrong baseline / missing evidence | All checks pass |
| P11-B1 | Candidate selection gate | Resolve primary vs fallback under authorization | `phase10_acceptance`; model_summary | §12; Cawley & Talbot | candidate_selection_report.csv | Selecting on noise / LB | Authorized candidate chosen |
| P11-B2 | CatBoost stability gate | Pass-or-waiver for CatBoost reliance | repeated-CV (new, diagnostic) or written waiver | §13; validation notes | stability note / waiver record | Over-trust of warned model | Gate pass or signed waiver |
| P11-B3 | Feature/data contract build | Construct F2 matrix for full train + test deterministically | F2 spec; leakage checklist | §15; leakage_checklist | (in-notebook) feature build + asserts | School/leakage/feature drift | School-excluded asserts pass |
| P11-B4 | Final refit on full train | Fit preprocessing + selected model on full train only | selected candidate config | §16; leakage checklist | fitted model (in-memory), final_refit_report.csv | Test leakage in fit | Refit completes, no test access |
| P11-B5 | Test inference | Generate `Drafted=1` probabilities for 696 test rows | fitted pipeline; test.csv | §17; classes_ policy | raw predictions (in-notebook) | Wrong score direction / leakage | Probs in [0,1], 696 rows |
| P11-B6 | Submission build + validation | Create + validate the submission CSV | sample_submission.csv; predictions | §18; submission_checklist | submission.csv + submission_validation.csv | Format/Id/order errors | All validation checks pass |
| P11-B7 | Artifacts, manifest, candidate log | Hash + record lineage; write report | all above | §21/§22; v3 §14 | manifest, validation_report.md, experiment_log_candidate.csv | Untraceable submission | SHA-256 + manifest written |
| P11-B8 | Final Opus review (Deliverable D) | Independent audit + accept/defer/reject | all artifacts | §25; verifier≠generator | acceptance draft | Self-certification | Review complete |
| P11-B9 | Manual upload handoff | Prepare file + ordering note for user upload | accepted artifact | §19; challenge_brief | upload note (for user) | Auto-upload / wrong last file | Director decision; no automation |

## 11. Candidate Scope and Eligibility for Final Refit

| Candidate | Current status inherited | Phase 11 eligibility | Final refit allowed in future execution? | Required gate | Main risk | Default decision |
|---|---|---|---|---|---|---|
| `catboost_tuned` | best global OOF, warning-heavy, not winner | **Primary final-refit candidate (planning)** | Yes, **conditional** | Candidate Selection Gate **and** CatBoost Stability Gate (pass or written waiver) | Slice fragility (Age_missing=1, QB), no repeated-CV | Refit as primary if both gates clear |
| `m1_logistic_regression` (baseline) | fallback/reference | **Fallback / reference candidate** | Yes, as fallback or dual artifact | Candidate Selection Gate | Lower global OOF; same Age_missing fragility | Refit as fallback / dual-artifact |
| `m1_logistic_regression_tuned` | rejected (noise-level) | **Rejected tuned variant** | No (unless new documented justification) | New justification doc | Complexity for no gain | Do not use |
| `m0_random_forest_frozen` | anchor | **Anchor / reference only** | No final submission by default | Explicit re-authorization | Weakest of the carried set | Reference only |
| `xgboost` | dropped, `no_qualifying_evidence` | **Dropped for now** | No | Written justification + new evidence | Re-promoting weak model | Do not reopen |
| `lightgbm` | dropped, `no_qualifying_evidence` | **Dropped for now** | No | Written justification + new evidence | Re-promoting weak model | Do not reopen |

## 12. Final Candidate Decision Planning

| Decision option | Evidence supporting it | Evidence against it | Required pre-execution gate | Future action if gate passes | Future action if gate fails |
|---|---|---|---|---|---|
| **A. CatBoost tuned as primary** | Best global OOF (0.8303), +0.0187 vs M0 (5/5), best AP/neg-AP/Brier | Below bar vs M1 (3/5), no repeated-CV, Age_missing/QB worsened | Selection + Stability Gate | Refit CatBoost on full train; build submission | Fall back to Option B or block (D) |
| **B. M1 baseline as conservative fallback** | Simpler, stable, 4/5 vs M0; well-characterized | Lower global OOF than CatBoost tuned | Selection Gate | Refit M1 baseline on full train; build submission | Block (D) |
| **C. Generate both, upload only after user decision** | Preserves optionality; both are valid artifacts; last-file-wins ranking is user-controlled | Two files to manage; multiplicity discipline needed | Selection Gate (both authorized) | Build both submissions + validation; user picks upload order | Block (D) |
| **D. Block pending additional audit** | If stability gate fails or integrity issue found | Delays submission | — | — | Document blocker; await director |

**Default recommendation:** **CatBoost tuned as primary for future Phase 11 execution, with M1 baseline fallback (Option A with C as a safe superset)** — but **no final winner until the submission validation suite (§18) and the final Opus review (§25) pass.** "Best global OOF" ≠ "final winner." The director chooses the option and authorizes per-file.

## 13. CatBoost Stability Gate

**Why CatBoost needs caution.** CatBoost tuned is the best *global* OOF ranker, but Phase 10 produced three cautions: (1) it does **not** clear the promotion bar over M1 (+0.0032388 < 0.005436; only 3/5 positive folds vs M1); (2) **no repeated-CV** stability confirmation was run for CatBoost (it was run for M1 only, where it revealed a ~0.009 spread — larger than M1's tuning gain); (3) robust-slice warnings **persist after tuning** — `Year=2011` (−0.045 vs M0), `available_measurement_count=0` (−0.0649), `Position=OG` (−0.051), `Position=OLB` (−0.027), and `Age_missing=1` / `Position=QB` actually **worsened** under tuning. The test set is materially exposed here: **115 of 696 test rows (16.5%) have missing Age**, so the `Age_missing=1` fragility is not hypothetical.

**Gate definition.** Before CatBoost tuned is relied upon for the final submission, **one of**:
- **(Pass)** Run a **repeated-CV stability audit** for CatBoost tuned (different splitter seeds, frozen-fold-consistent substrate, diagnostic only) and confirm the OOF lead over its own baseline is stable in sign and that no robust slice degrades catastrophically vs M0 beyond the documented set; **or**
- **(Waiver)** The **project director signs a written waiver** that explicitly acknowledges: CatBoost tuned has the best global OOF AUC **but** retains slice warnings (Age_missing=1, QB, Year 2011, avail_count 0, OG, OLB) and **lacks repeated-CV confirmation**, and accepts these for the final submission under time constraints.

**Trust vs selection.** This gate is a **stability/trust gate**, not a selection mechanism. **Leaderboard feedback must never be used for this gate** (or for any selection). If neither pass nor waiver is obtained, **fall back to M1 baseline (Option B)** or **block (Option D)** — do not proceed with CatBoost.

## 14. M1 Baseline Fallback Policy

`m1_logistic_regression` **baseline** is retained as the fallback/reference because it is **simpler, more stable, and well-characterized** (4/5 folds vs M0; strongest local ranker across global lenses in Phase 9A; statistically indistinguishable from its tuned variant). Policy: (a) the fallback uses the **baseline** configuration recovered from Phase 8/9A accepted artifacts — **never** the rejected tuned M1; (b) if the CatBoost Stability Gate fails or is not waived, M1 baseline becomes the submission candidate; (c) M1 baseline carries the **same `Age_missing=1` fragility** (AUC ≈ random on that 8-positive train slice) — this is documented, not hidden, and is a shared caveat, not a CatBoost-only one; (d) M1 baseline may also be produced as a **dual artifact** (Option C) so the director retains upload-order choice under the last-file-wins rule.

## 15. Feature, Data and Preprocessing Contract

**Allowed feature set (F2, 21 features):** base — `Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type, Position_Type, Position`; Phase 7 additions — `Age_missing, Sprint_40yd_missing, Vertical_Jump_missing, Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing, Shuttle_missing, available_measurement_count`. **Prohibited feature:** `School` (assert raise-on-violation).

| Contract item | Allowed future behavior | Forbidden behavior | Verification required | Stop or warning? |
|---|---|---|---|---|
| Data sources | Only `data/input/{train,test,sample_submission}.csv` | Any external/online data | Path all-list assert | **Stop** |
| Target | Train labels only for fitting | Any test label use | `test.csv` has no `Drafted` (assert) | **Stop** |
| Feature set | Exactly F2 (21 features) | New features; School | Column-set equality assert; School-absent assert | **Stop** |
| Missingness flags | Computed row-wise/deterministically from each row | Learned from other rows | Recompute + compare on a sample | **Stop** |
| `available_measurement_count` | Row-wise count of present measurements | Any cross-row statistic | Deterministic recompute | **Stop** |
| Imputation | Fit on **full train only**, applied to test | Fit on test / on train+test | Fit-scope assert; test untouched in fit | **Stop** |
| One-hot encoding | Categories learned from **full train only**; unknown test categories handled safely (all-zero / ignore) | Fit on test; drop/realign by test | Unknown-category handling test | **Stop** |
| Scaling (if M1 needs it) | Fit on full train only | Fit on test | Fit-scope assert | **Stop** |
| Probability direction | `predict_proba` column for label `1` after `classes_` check | Assume `[:,1]` blindly | `classes_` contains 1 assert | **Stop** |

The final refit is on **full train (2781 rows)**, not folds; the frozen fold file is used only for **lineage/reference** (it governed the Phase 10 OOF that justified selection). Train/test feature derivation must be identical in code.

## 16. Final Refit Protocol Design

*(Plan only — not executed now.)*

| Step | Input | Operation | Output | Leakage risk | Required check |
|---|---|---|---|---|---|
| 1 | `de11fae`; Phase 10 acceptance | Verify authorized commit + acceptance present | gate pass | — | HEAD == authorized hash |
| 2 | official CSVs | Load train/test/sample_submission | dataframes | low | row counts 2781/696/696 |
| 3 | selected candidate | Confirm candidate + gate status | candidate id | — | Selection + Stability gate resolved |
| 4 | train | Build F2 matrix; assert School excluded | X_train, y_train | medium | F2 column-set; School-absent |
| 5 | train | Fit imputer/encoder/(scaler) on **full train only** | fitted preprocessing | **high** | fit-scope assert; no test access |
| 6 | train | Fit selected model on full train only (no HPO) | fitted model | medium | seed fixed; config = recovered tuned/baseline |
| 7 | model | Verify `estimator.classes_` contains label 1 | positive-class index | **high** | assert label 1 present |
| 8 | — | Record config, seed, env, commit, run_id | refit metadata | — | written to report |

**CatBoost tuned refit:** use the accepted Phase 10 tuned hyperparameters from `hpo_results.csv` (`depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42`); `cat_features=[]` (F2 one-hot, matching Phase 10); **no School**; **no further HPO**; run in the **separate Wave 2 environment** (`catboost 1.2.10`), never mutating the base `.venv`. **M1 baseline refit:** use the baseline configuration recovered from Phase 8/9A accepted artifacts (exact `C/penalty/solver/scaling` **Not confirmed yet** here — recover, do not guess); **no tuned M1**; full-train fit only after the selection gate passes.

## 17. Test Inference Protocol Design

*(Plan only — not executed now.)*

| Step | Input | Operation | Output | Failure mode | Required check |
|---|---|---|---|---|---|
| 1 | test.csv (after selection) | Load test only after candidate is fixed | X_test_raw | premature test peeking | candidate already selected |
| 2 | X_test_raw | Apply **train-fitted** preprocessing (transform only) | X_test | refit on test | transformer not re-fit on test |
| 3 | X_test | `predict_proba` → column for `Drafted=1` | p_test (696,) | wrong column / hard labels | `classes_` index check |
| 4 | p_test | Range/shape validation | validated probs | NaN/inf/out-of-range | all in [0,1], len 696, no NaN/inf |
| 5 | test Ids + p_test | Align predictions to test/sample Id order | (Id, Drafted) rows | misalignment | Id set/order == sample_submission |
| 6 | — | No manual edits; deterministic, logged | final predictions | manual editing | code-only; manual-edit check |

No target access; `sample_submission.csv` used only for Id set/order/schema validation; no sorting except to match `sample_submission.csv` order (which equals `test.csv` order).

## 18. Submission Validation Suite

| Validation check | Expected condition | How to verify | Stop or warning? | Artifact evidence |
|---|---|---|---|---|
| Columns | exactly `Id, Drafted` | column list equality | **Stop** | submission_validation.csv |
| Row count | **696** | `len(df) == 696` | **Stop** | submission_validation.csv |
| Row count cross-match | == `test.csv` and `sample_submission.csv` | compare counts | **Stop** | submission_validation.csv |
| Id set | exactly matches official test/sample Id set | set equality | **Stop** | submission_validation.csv |
| Id order | matches `sample_submission.csv` order (= `test.csv`) | positional equality | **Stop** | submission_validation.csv |
| Drafted type | numeric | dtype/parse check | **Stop** | submission_validation.csv |
| Drafted range | all in `[0,1]` | min/max check | **Stop** | submission_validation.csv |
| No NaN | zero NaN | isna sum == 0 | **Stop** | submission_validation.csv |
| No inf | zero infinite | isinf sum == 0 | **Stop** | submission_validation.csv |
| No duplicate Id | unique Ids | nunique == 696 | **Stop** | submission_validation.csv |
| No manual edits | file == code output | regenerate + hash compare | **Stop** | SHA-256 in manifest |
| SHA-256 recorded | hash present | hash the CSV | **Stop if missing** | artifact_manifest.csv |
| Lineage | model + commit + run_id + feature set recorded | report fields present | **Stop if missing** | validation_report.md |
| Not auto-uploaded | no upload performed | policy assert | **Stop on violation** | validation_report.md |

Official expected test row count = **696** (confirmed from `test.csv` and `sample_submission.csv`). Future execution must still re-derive it from the official `sample_submission.csv` at run time, not from this document.

## 19. Leaderboard and Upload Policy

| Leaderboard-related action | Allowed? | Conditions | Risk | Required control |
|---|---|---|---|---|
| Use LB to select among models | **No** | — | Leaderboard chasing / overfitting public subset | Selection uses OOF only (§12) |
| LB as post-submission sanity check | Yes, later | Only after a locally selected + validated submission exists | Misreading subset as truth | Public LB = subset; private = full test; sanity only |
| Repeated upload loop | **No** | — | Overfitting the public LB | One considered submission; no loop |
| Change model on public LB feedback | **No** | Requires a new documented phase | Protocol violation | Documented re-authorization |
| Automatic upload by Codex/Opus | **No** | — | Uncontrolled / wrong-file submission | Upload is manual, user-side only |
| Manual upload + last-file ordering | Yes (user) | User decides which file is uploaded **last** (last submitted = final ranking) | Wrong final file ranked | User tracks order + timestamp manually |
| Claiming an upload occurred | Only if user confirms | — | False record | Opus must not assert upload without user confirmation |

**Critical project rule (challenge_brief):** the **last submitted file determines final ranking** and the **private leaderboard uses the full test set**. Under Option C (dual artifacts), the director must consciously choose the **upload order**; Codex/Opus never upload and never reorder for the user.

## 20. Future Notebook Architecture and Documentation Standard

Single planned notebook `notebooks/11_phase11_submission_readiness.ipynb` (**not created now**): notebook-first, reproducible, audit-ready, submission-format-safe, strictly train/test separated, free of leaderboard influence. Required structure — title + scope + explicit non-actions; clean imports; `PROJECT_SEED`; `experiment_id`/`run_id`; centralized relative paths; authorized-commit validation; allowed-data/artifact loading only; Phase 10 evidence loading; candidate selection gate; CatBoost stability gate or waiver check; F2 build; School-exclusion assert; full-train preprocessing fit; final refit; test inference; submission generation; submission validation suite; artifact writing; executive summary; warnings + acceptance criteria.

| Notebook / module | Purpose | Main sections | Inputs | Outputs | Risks controlled | Required before execution? |
|---|---|---|---|---|---|---|
| `notebooks/11_phase11_submission_readiness.ipynb` | Final refit → inference → validated submission | P11-B0…B7 (§10) | official CSVs; Phase 10 artifacts; selected candidate config | submission + validation/report/manifest/candidate-log | leakage, format errors, manual edits, LB influence | Yes — built only after signed authorization |

Each major code block is preceded by a Markdown cell:
```markdown
## <Number>. <Title>

**Objective.**
**Inputs.**
**Method.**
**Expected output.**
**Risk controlled.**
```
Each code cell starts with a comment, e.g. `# 5.2 Validate official sample submission alignment`. After relevant results, a Markdown `### Interpretation` block with **Main result / Methodological reading / Risk or warning / Decision**. The notebook must not: fit on test; use School/external data/leaderboard; auto-upload; declare winner before acceptance; declare submission-ready before validation; overwrite artifacts without `run_id`; modify `logs/experiment_log.csv`; reopen HPO.

## 21. Future Artifact Architecture

*(Planned future artifacts only — none created now.)*

| Artifact family | Proposed file(s) | Purpose | Required inputs | Required checks | Produced by | Must exist before closure? | Notes |
|---|---|---|---|---|---|---|---|
| Notebook | `notebooks/11_phase11_submission_readiness.ipynb` | Reproducible execution record | official CSVs; Phase 10 artifacts | runs top-to-bottom | Codex | Yes | static review before run |
| Candidate selection | `outputs/validation/phase11_submission_readiness_<run_id>_candidate_selection_report.csv` | Record selection gate decision | Phase 10 model_summary; authorization | gate fields present | Codex | Yes | no LB |
| Final refit | `outputs/validation/phase11_submission_readiness_<run_id>_final_refit_report.csv` | Record refit config/env | selected config | seed/env/commit recorded | Codex | Yes | full-train only |
| Submission validation | `outputs/validation/phase11_submission_readiness_<run_id>_submission_validation.csv` | §18 suite results | submission + sample | all checks pass | Codex | Yes | stop on fail |
| Model summary | `outputs/validation/phase11_submission_readiness_<run_id>_model_summary.csv` | Candidate metadata + OOF ref | Phase 10 OOF | lineage fields | Codex | Yes | OOF for trace only |
| Validation report | `outputs/reports/phase11_submission_readiness_<run_id>_validation_report.md` | Human-readable record + lineage | all above | model/commit/run_id/feature set stated | Codex | Yes | links anchor→…→final |
| Artifact manifest | `outputs/reports/phase11_submission_readiness_<run_id>_artifact_manifest.csv` | SHA-256 + paths | all artifacts incl. submission | hashes verifiable | Codex | Yes | submission SHA is durable identity |
| Candidate experiment log | `outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv` | Separate log (not main log) | §22 fields | schema complete | Codex | Yes | **never** the main log |
| Submission CSV | `outputs/submissions/phase11_submission_readiness_<run_id>_<candidate>_submission.csv` | The deliverable file | predictions | §18 validated | Codex | Yes (post-validation) | **gitignored** (`outputs/submissions/*.csv`) — checksum is identity |
| Acceptance | `docs/11_submission_readiness/phase11_acceptance.md` | Opus review + director sign-off | all artifacts | Opus review done | Opus → Director | Yes | no auto-upload |

Submission CSVs are gitignored (per `.gitignore` `outputs/submissions/*.csv`), so the **SHA-256 in the manifest/report is the only durable identity** of the submission — recording it is mandatory. Check-and-fail on existing paths; `experiment_id = phase11_submission_readiness_v<K>`; `run_id` mandatory.

## 22. Candidate Experiment Log Policy

`logs/experiment_log.csv` **must not be modified** during execution until a human acceptance explicitly authorizes integration. Future execution writes only `outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv` with: `experiment_id, run_id, authorized_commit, phase10_acceptance_commit, candidate_family, candidate_variant, final_refit_candidate, fallback_candidate, features_used, School_used_as_feature=False, external_data_used=False, leaderboard_used_for_selection=False, submission_created (True/False), submission_uploaded=False, model_hyperparameters_source, feature_contract, preprocessing_contract, train_rows, test_rows, submission_rows, submission_path, submission_sha256, artifact_manifest_path, validation_report_path, submission_validation_status, manual_edit_detected=False, notes`. Not written now — planned only.

## 23. Acceptance Criteria

**Phase 11 planning acceptance (this run):** package created only under `docs/11_submission_readiness/`; Phase 10 evidence reviewed and aligned; alignment table (§6) + consistency checks (§7) complete; candidate eligibility (§11) stated; CatBoost Stability Gate (§13) defined; M1 fallback policy (§14) defined; F2 contract (§15) preserved; refit (§16), inference (§17), validation suite (§18), leaderboard policy (§19), artifact families (§21), notebook standards (§20), candidate-log policy (§22) defined; Codex prompt (C) and Opus review prompt (D) created but not executed; no refit/inference/submission/leaderboard performed.

**Future Phase 11 execution acceptance (gated):** authorized starting commit verified; forbidden paths unchanged except the explicitly authorized submission output; `logs/experiment_log.csv` unchanged; Phase 10 acceptance present; candidate gate resolved; CatBoost Stability Gate passed or waived; F2 verified; School excluded; no external data; no LB for selection; full-train refit uses only train; inference uses only train-fitted transforms; submission schema/row-count/Id-set/Id-order/probability-range verified; no NaN/inf; no duplicate Id; no manual edits; SHA-256 recorded; manifest + validation report + separate candidate log written; Opus final review complete; **no automatic upload.**

## 24. Stop Rules

| Stop rule | Applies to | Trigger | Required action | Continue after mitigation? |
|---|---|---|---|---|
| Unexpected/undocumented HEAD | both | HEAD ≠ authorized hash | stop, report | Yes, after director confirms hash |
| Forbidden-path tracked diff | both | non-empty forbidden diff | stop, report | Yes, after revert/justification |
| Main log changed | both | `logs/experiment_log.csv` diff | stop, report | Yes, after revert |
| Phase 10 acceptance/report/summary missing | both | file absent | stop, report | Yes, after restored |
| Submission checklist missing (no equivalent) | planning | file absent | stop, report | Yes, after located |
| Sample submission not locatable | execution | file absent at run time | stop, report | Yes, after located |
| Candidate eligibility unclear | both | no authorized candidate | stop, request decision | Yes, after authorization |
| CatBoost gate required, not passed/waived | execution | gate unresolved | fall back to M1 or block | Yes (fallback) |
| Feature-contract violation | both | new feature / School proposed | stop, report | No (rules) |
| External data proposed | both | any external source | stop, report | No (rules) |
| HPO proposed | both | tuning attempted | stop, report | No (rules) |
| Test used for fitting | execution | transformer/model fit on test | stop, report | No (leakage) |
| Probability direction unconfirmable | execution | `classes_` lacks label 1 | stop, report | Yes, after fix |
| Row count/Id set/order unverifiable | execution | mismatch vs sample | stop, report | Yes, after fix |
| NaN/inf/out-of-range predictions | execution | invalid values | stop, report | Yes, after regenerate |
| Manual prediction editing detected/proposed | both | non-code edit | stop, report | No (rules) |
| Leaderboard used for selection | both | LB drives a choice | stop, report | No (rules) |
| Automatic upload attempted | both | upload without explicit user/platform auth | stop, report | No (rules) |
| Winner declared during planning | planning | "winner"/"submission-ready" claim | stop, correct | No |

## 25. Opus-Codex-Opus Workflow

**Opus now (this run):** creates the Phase 11 planning package; reviews Phase 10 acceptance/evidence; designs the selection gate, CatBoost stability gate, refit/inference protocols, submission validation suite, artifact architecture, stop rules, acceptance criteria; **executes no refit, creates no submission.** **Codex later (Deliverable C):** executes only the authorized scope; creates the Phase 11 notebook + artifacts; refits only after the selection gate passes; runs inference only after the feature/data contract passes; creates a submission only after the validation checks are implemented; **does not upload, does not use LB for selection, declares no winner.** **Opus after Codex (Deliverable D):** audits outputs; independently verifies submission schema/Id-order/probability-range/hashes/lineage; evaluates whether the artifact is acceptable for **user-side** upload; drafts acceptance or blocks; **does not upload, does not change predictions, opens no new modeling.** Generator ≠ verifier throughout.

## 26. Handoff from Phase 10 Without Reopening Phase 10

Phase 10 is **closed and accepted** at `de11fae` (accept-with-warnings; no winner). Phase 11 **consumes** Phase 10's accepted candidate roles and OOF evidence as fixed inputs and **does not** re-run HPO, re-rank candidates, re-open XGB/LGBM, or alter the Phase 10 acceptance. The only "new computation" Phase 11 may introduce is the **CatBoost repeated-CV stability audit (diagnostic)** under §13 — and even that is optional (a written waiver is the alternative) and never changes the Phase 10 record. All Phase 10 artifacts are read-only inputs.

## 27. Risks, Failure Modes and Mitigations

- **Over-trusting a globally-best but locally-fragile model** → CatBoost Stability Gate + documented slice caveats + M1 fallback (§13/§14). Test exposure: 115/696 Age-missing rows.
- **Test leakage in final refit** → fit-scope asserts; test loaded only after selection; transform-only on test (§15–§17).
- **Submission format error / disqualification** → full §18 validation suite (exact columns, 696 rows, Id-order, [0,1], no NaN/inf/dup, traceable).
- **Manual editing / untraceable file** → code-only generation; SHA-256 + manifest; regenerate-and-compare check (§18/§21).
- **Leaderboard chasing** → LB is sanity-only, never selects; no upload loop (§19).
- **Wrong final-ranked file** → manual upload order is the director's explicit choice; no automation (§19).
- **Scope creep (HPO/ensembling/new features)** → stop rules (§24) + frozen decisions (§4).
- **M1 baseline config drift** → recover exact config from Phase 8 artifacts; do not guess (§16).

## 28. Explicit Non-Actions

This planning run did **not**: execute Phase 11; train/refit any model; run inference; create or run a notebook; create a submission or write under `outputs/submissions/`; use the leaderboard; upload anything; declare a final winner or submission-ready model; reopen HPO/XGBoost/LightGBM; build ensembles/blending/stacking/calibration/threshold tuning; use external data or School as a feature; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `.venv`, `requirements.txt`, lockfiles, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`; stage, commit, or push.

## 29. Required User Authorization Before Execution

Phase 11 execution requires a **signed Phase 11 Project Authorization Note** (analogous to the Phase 10 note) recording: authorized starting commit (`de11fae` or a documented successor); the chosen candidate decision option (§12 A/B/C/D); the CatBoost Stability Gate decision (run audit **or** signed waiver with the §13 acknowledgement); reaffirmation of the locks (no LB for selection, no external data, no School, no HPO, no auto-upload, no winner before acceptance); and explicit authorization for the **specific submission file(s)** to be generated (per v3 §16.7). Without it, Deliverable C is inert.

## 30. Recommended Next Step

**A. Review the generated Phase 11 planning package; execution remains blocked until explicit user authorization** (signed Phase 11 Project Authorization Note per §29). The recommended future path: resolve the Candidate Selection Gate (default Option A + fallback) → resolve the CatBoost Stability Gate (audit or written waiver) → authorize → Codex execution (Deliverable C) → independent Opus review (Deliverable D) → director-signed `phase11_acceptance.md` → **manual, user-side upload with deliberate last-file ordering.** No winner, no submission, no leaderboard, and no Phase 11 execution occur until then.
