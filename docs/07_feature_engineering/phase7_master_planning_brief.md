# Phase 7 Master Planning Brief — Reto Tokio / GCI World NFL Draft Prediction

**Phase:** Phase 7 — Feature Engineering (Missingness / Measurement Availability), PLANNING ONLY
**Date:** 2026-06-12
**Planning baseline commit:** `c4d5647` (*docs: record phase 6a acceptance hash*)
**Status:** Planning package. **Phase 7 execution is NOT authorized by this document.** Phase 8 remains locked.

---

## 0. Executive Verdict

**Phase 7 can be planned safely.** Every entry gate holds: Phase 5 frozen (`35852e9`), Phase 6 accepted with warnings and commit-anchored (`d3b0aed`, hash recorded in `dbc2efc`), Phase 6A executed, audited, accepted with warnings and commit-anchored (`f1fb717`, hash recorded in `c4d5647`). The working tree is clean on tracked files, nothing is staged, and no forbidden path is modified.

Phase 6A leaves Phase 7 with an unusually well-posed question. The Phase 2 vs Phase 6 gap (~0.084 fold-mean / 0.0863 OOF) decomposed almost entirely into the **imputation statistic** (mean vs median: +0.075655 OOF, robust across all 5 D1 seeds, 25/25 same-sign fold pairs), while encoding (−0.000804), BMI (+0.000332), RF seed, and global-preprocessing leakage were each within the measured seed-noise floor (std 0.002718). The accepted interpretation is that mean imputation acts as an **implicit informative-missingness signal** under the depth-5 tree model. Phase 7's core job is therefore to test whether **explicit, row-wise, leakage-safe missingness/measurement-availability features** recover (or beat) that signal cleanly — under the frozen folds, the frozen anchor, the ratified ablation threshold (OOF gain ≥ 0.005436 with same-sign fold deltas in ≥ 4/5 folds), and the ratified minimum slice size (n ≥ 50).

This brief specifies the block architecture, the pre-registered variant ladder, the validation/acceptance machinery, the leakage controls, the artifact/Git plan, the ECC agent/skill plan, and the explicit authorization gate. One discrepancy was found during verification (a referenced Recapitulaciones file that does not exist); it is informational and does not block planning (see §1).

**Recommended next step:** user/project director review of this package, then explicit execution authorization per §16.

---

## 1. Repository State Verification

Commands run on 2026-06-12 (read-only):

| Check | Expected | Observed | Status |
|---|---|---|---|
| `git rev-parse --short HEAD` | `c4d5647` | `c4d5647` | PASS |
| Phase 6A closure commit | `f1fb717` exists | `f1fb717` *validation: accept phase 6a baseline reconciliation* — commits acceptance record + notebooks 04/05/06 + all Phase 6A artifacts | PASS |
| Phase 6A hash-record commit | `c4d5647` exists | `c4d5647` *docs: record phase 6a acceptance hash* — updates `docs/06_validation/phase6a_acceptance.md` only | PASS |
| `git status --short` | no staged files, no tracked modifications | Only expected untracked items (`.claude/`, `CLAUDE.md`, `Libros/`, `Prompts/`, `Recapitulaciones/`, plan v1, 2 backup notebooks, `notebooks/_official/`) | PASS |
| `git diff --cached --name-only` | empty | empty | PASS |
| `git diff --check` | clean | clean (exit 0) | PASS |
| Forbidden-paths diff (`data/input`, `notebooks/_official`, `references`, `outputs/submissions`, `logs/experiment_log.csv`, `.vscode/settings.json`) | empty | empty | PASS |
| `git log --oneline -n 8` | Phase 6/6A closure sequence | `c4d5647`, `f1fb717`, `dbc2efc`, `18f0a12`, `d3b0aed`, `35852e9`, `8305950`, `39948d1` | PASS |

**Discrepancy found (informational, not a blocker):**

- `Recapitulaciones/recapitulacion_integral_chat_reto_tokio_phase6a_closure_phase7_phase8_ready.md` — **does not exist**. `Recapitulaciones/` contains only three older fase-3-era files. Severity: **informational**. The repository's own committed evidence (acceptance records + commits) independently confirms the claimed project state, so planning can proceed. The two Lote-2 recap files (`...phase4b_phase5.md`, `...phase5_phase6_acceptance.md`) are likewise absent: **Not confirmed yet**.

**Path corrections for Lote-1 items (files exist, at migrated paths):**

- `docs/experiment_notes.md` → actual: `docs/03_eda/experiment_notes.md` (reviewed).
- `docs/challenge_brief.md` → actual: `docs/00_project_contract/challenge_brief.md` (reviewed).
- `docs/submission_checklist.md` → actual: `docs/00_project_contract/submission_checklist.md` (reviewed).

---

## 2. Evidence Reviewed

All inspection read-only; no notebook executed in this run.

| Evidence | Status | Role in this plan |
|---|---|---|
| `docs/06_validation/phase6a_acceptance.md` | Reviewed (signed; ACCEPT WITH WARNINGS; acceptance commit `f1fb717`) | Source of ratified decisions (§4) and Phase 7 gate conditions |
| `docs/06_validation/phase6_acceptance.md` | Reviewed (signed earlier; ACCEPT WITH WARNINGS) | Anchor/frozen-folds/candidate-log ratifications |
| `outputs/reports/phase6a_baseline_reconciliation_report.md` | Reviewed | V0–V7 results, gap decomposition |
| `outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv` | Reviewed | Variant-level numbers |
| `outputs/reports/phase6a_d1_d2_diagnostics_report.md` + `outputs/validation/phase6a_d1_seed_sweep_summary.csv` | Reviewed | Noise floor, threshold derivation, first-pass D2 |
| `outputs/reports/phase6a_d2_refined_probe_report.md` + `outputs/validation/phase6a_d2_refined_tier_summary.csv` | Reviewed | Refined D2 verdict (escalation cleared) |
| `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md` | Reviewed (prior turns, committed) | Phase 6 harness reference |
| `docs/01_project_planning/project_execution_plan_v3.md` | Reviewed (committed `18f0a12`) | Phase plan, artifact/validation/leakage contracts |
| `docs/01_project_planning/phase6a_baseline_reconciliation_plan.md` | Reviewed | Variant-design discipline reused here |
| `docs/01_project_planning/integral_project_review_phase0_phase6.md` | Reviewed | Project diagnosis |
| `docs/05_methodology/phase5_execution_decisions.md` | Reviewed | Frozen validation/seed/score-input decisions |
| `docs/05_methodology/phase5_methodology_plan.md` | Reviewed in prior phases; not re-read line-by-line this run | Consolidated Phase 5 plan |
| `docs/05_methodology/validation_protocol_phase6.md` | Reviewed (prior turns) | Acceptance-criteria machinery |
| `docs/05_methodology/leakage_checklist_phase6.md` | Reviewed | Allowed/Conditional/Blocked transformation taxonomy; Phase 7 conditional items |
| `docs/03_eda/experiment_notes.md` | Reviewed | Phase 3 signal families; missingness subfamilies; slice mandate |
| `docs/00_project_contract/challenge_brief.md` | Reviewed | Contract: target, metric, 696 rows, audit expectations, external-data prohibition |
| `docs/00_project_contract/submission_checklist.md` | Reviewed | Pre-submission gates (Phase 7 generates none) |
| `docs/04_research/pdf_key_findings.md`, `research_notes_feature_engineering.md`, `research_notes_validation.md`, `research_notes_leakage.md`, `research_notes_reproducibility.md` | Reviewed | Theory-to-practice transfer (§5); reference routing |
| `Recapitulaciones/recapitulacion_integral_chat_reto_tokio_phase6a_closure_phase7_phase8_ready.md` | **Not confirmed yet** (file absent) | — |
| `references/books/` (10), `references/papers/` (11), `references/course_materials/` (notes, qa, readings, slides, tutorials) | Inventory confirmed on disk; consumed via the project's Phase 4B summaries per reading policy | §5 references table |
| `.claude/agents/` (10), `.claude/skills/` (21) | Confirmed on disk | §6 ECC plan |

Per the project reading policy, full PDFs were **not** re-parsed in this run; references are used through the committed Phase 4B audit (`pdf_review_audit.md`, `pdf_key_findings.md`) and research notes. `/plugin list ecc@ecc` is a CLI user command not invocable from agent context; availability was verified by direct disk inspection plus the live agent registry (all 10 agents spawnable).

---

## 3. Numerical Results Validation

All values below were checked against committed artifacts; the Phase 6A numbers were additionally verified earlier by independent recomputation from raw OOF files (stdlib rank-based AUC, max abs diff ≤ 1.1e-16).

| Quantity | Value | Source | Status |
|---|---|---|---|
| Phase 6 anchor OOF ROC-AUC | 0.726616 | `phase6_acceptance.md`, OOF artifact | Confirmed |
| Phase 6 fold mean ± std | 0.729253 ± 0.030629 | same | Confirmed |
| Phase 2 baseline CV mean | 0.812964 | `logs/experiment_log.csv` (read-only), acceptance records | Confirmed |
| Phase 2 public LB | 0.80792 | same (history only; never a criterion) | Confirmed |
| V0 / V1 / V2 / V3 OOF | 0.726616 / 0.811638 / 0.810277 / 0.808729 | 6A variant summary | Confirmed |
| V4 / V5 / V6 / V7 OOF | 0.809010 / 0.726948 / 0.725812 / 0.802271 | same | Confirmed |
| D1 v0median mean / std (OOF, 5 seeds) | 0.725873 / 0.002718 | D1 sweep summary | Confirmed |
| D1 v7mean mean / std | 0.802124 / 0.001097 | same | Confirmed |
| D1 paired v7−v0 mean delta / min | 0.076251 / 0.074131 | same | Confirmed |
| D1 same-sign positive fold pairs | 25/25 | same | Confirmed |
| D2 refined T1→T4 fold-spanning rows | 220 (7.91%) → 41 (1.47%) → 16 (0.58%) → 0 (0.00%); T4b = 0 | refined tier summary | Confirmed |
| Refined D2 escalation | False (cleared); grouped CV dormant | refined probe report | Confirmed |
| Ratified ablation threshold | OOF gain ≥ 0.005436 AND same-sign fold deltas ≥ 4/5 | `phase6a_acceptance.md` §5 | Confirmed |
| Ratified minimum slice size | n ≥ 50 | same | Confirmed |
| Frozen folds integrity | `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, 2781 rows, labels 0..4, sha256[:16] `96937649526bcadb` | committed fold file | Confirmed |
| Train contract | 2781×16; class balance 1803 (`Drafted=1`) / 978; test 696×15; submission 696 rows | challenge brief + contract checks | Confirmed |
| Train missingness | Age 435, Sprint_40yd 145, Vertical_Jump 554, Bench_Press_Reps 721, Broad_Jump 581, Agility_3cone 970, Shuttle 912; Height/Weight 0 | challenge brief; verified directly against `train.csv` | Confirmed |
| Test missingness exists (features computable row-wise at final inference) | Age 115, Sprint 29, Vertical 143, Bench 184, Broad 147, Agility 247, Shuttle 228 | challenge brief | Confirmed |

No numerical discrepancy was found between the prompt's claimed values and the repository evidence.

---

## 4. Frozen Decisions Preserved

Ratified in `docs/06_validation/phase6a_acceptance.md` §5 (and earlier records); this plan preserves all of them. None of the evidence reviewed justifies reopening any of them.

| # | Frozen decision | Phase 7 consequence |
|---|---|---|
| 1 | **V0 is the incumbent anchor** (OOF 0.726616 on frozen folds) | All Phase 7 deltas are computed against a re-verified V0 run (F0 gate) |
| 2 | **V7 is the clean upgrade candidate, not auto-adopted** | V7's OOF is carried in as an *implicit-missingness diagnostic reference*, never as the anchor |
| 3 | **V4 is not adopted** (conflates ordinal+mean+BMI) | No Phase 7 variant reproduces V4's bundle |
| 4 | **One-hot retained** as categorical policy | All Phase 7 variants use fold-fitted OneHotEncoder for role categoricals |
| 5 | **Median retained** in the incumbent anchor | The anchor branch of the ladder stays median; mean appears only as the pre-registered F5 contrast |
| 6 | **Mean imputation = explicit missingness hypothesis**, never a silent tweak | Tested head-to-head against explicit flags (§9 design) |
| 7 | **BMI deferred to Phase 7 decision** | Resolved in Block 1 from existing V5 evidence: +0.000332 < 0.005436 ⇒ **not adopted in the Phase 7 core**; re-proposable later only with new evidence (no new run needed) |
| 8 | **No material same-athlete duplication; grouped CV dormant; StratifiedKFold frozen folds retained** | Folds loaded from the committed file and integrity-asserted; never recomputed |
| 9 | **Candidate log v2 separate; legacy `logs/experiment_log.csv` untouched; migration deferred** | Phase 7 writes candidate rows under `outputs/reports/` only |
| 10 | **Public LB never a selection criterion** | No LB consultation anywhere in Phase 7 |
| 11 | **No HPO / no model-family comparison / no submissions in Phase 7** | RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42) is the only estimator; no parameter changes (changing depth/estimators would constitute informal HPO) |
| 12 | **School excluded from the feature matrix** | Diagnostic-only (slice dimension), as in Phase 6/6A |
| 13 | **Phase 8 locked** | §18 of this brief; no model-comparison planning beyond dependency notes |

Honest caveat preserved from the 6A acceptance warnings: with `max_depth=5`, the frozen model may under-exploit added binary flags. If flags fail the threshold under this configuration, the recorded conclusion must be *"no qualifying gain under the frozen model configuration"*, not *"missingness has no value"* — that distinction is a Phase 8 input, not a license to tune.

---

## 5. References Reviewed and Theory-to-Practice Transfer

Sources are those the project's own Phase 4B audit marks **Reviewed** (`docs/04_research/pdf_review_audit.md`, `pdf_key_findings.md`); they are applied here strictly as methodology. **No reference may contribute external data of any kind to the model** (athletes, schools, conferences, rankings, geography, NFL history, draft outcomes).

| Fuente / referencia | Principio metodológico | Aplicación práctica a Phase 7 | Riesgo que mitiga | Cómo integrarlo al plan |
|---|---|---|---|---|
| Kuhn & Johnson, *Feature Engineering and Selection* (2021) | Missingness can itself be predictive; encode it explicitly (indicators) rather than hiding it inside imputation | Block 2 feature family: per-column missingness flags + availability count as first-class candidates | Signal loss / silent dependence on imputation artifacts | §9 variant ladder F1–F3 |
| *Feature Engineering for Modern ML* (2024) | All learned transformations must be estimated within resampling folds | Every imputer/encoder lives inside the per-fold `Pipeline`/`ColumnTransformer`; row-wise features are parameter-free | Preprocessing/imputation/encoding leakage | §12 leakage strategy; notebook contract §10 |
| *The Kaggle Book* (2nd ed., 2025) | Trust a frozen local CV; treat the public LB as noise; pre-register experiments | Frozen folds + pre-registered ladder + hard variant cap; LB prohibited as criterion | Leaderboard chasing; adaptive overfitting | §9 cap; §11 acceptance rule; §15 non-actions |
| *The Kaggle Workbook* (2023) | Ablate one change at a time on identical folds | Single-factor rungs (flags → count → bins); paired per-fold deltas vs F0 | Confounded conclusions (the Phase 2 lesson) | §9 ladder design |
| ISLP (*Introduction to Statistical Learning, Python*) | Model-selection variance is real; effects must clear a noise estimate | D1 seed-noise floor (0.002718) converted into the ratified threshold 0.005436 | Reading noise as signal | §11 acceptance criteria |
| *Hands-On ML* (sklearn/PyTorch, 2026) | `Pipeline`/`ColumnTransformer` as the leakage-safety idiom; verify estimator internals | Reuse the audited 6A pipeline builders; `estimator.classes_` checked before any proba extraction | Silent class-index bugs; fit-scope drift | §10 implementation design |
| *Python for Data Analysis* (3rd ed., 2022) | NaN semantics in pandas are subtle (`isna`, count vs sum, dtype traps) | Flag/count features defined via explicit `isna()` on named columns; unit-style asserts on counts (e.g., flags sum = known train missingness) | Silently wrong features | §10 data-contract checks |
| Cawley & Talbot, *On Over-fitting in Model Selection* | Repeated selection on the same CV biases estimates; selection is part of training | Hard cap on trained variants (≤ 8); pre-registration; no "best-of" picking inside the run without a recorded rule | HPO-by-stealth; selection bias | §9 cap + §16 gate |
| *Leakage and the Reproducibility Crisis in ML Science* + *On Leakage in ML Pipelines* | Pipeline-wide leakage taxonomy (13 layers in project notes) | Per-variant instantiated leakage checklist (§12) reusing the Phase 6 checklist categories | All taxonomy layers | §12 table |
| *Meta-analysis of Overfitting on Kaggle* | Adaptive test-set reuse inflates public scores | Phase 7 produces zero submissions; LB untouched | Adaptive overfitting to LB | §15 non-actions |
| *Causal Feature Selection for Responsible ML* | Predictive ≠ causal; report associations only | Reports use ranking/association language; the `Player_Type → completeness → Drafted` pattern stays descriptive | Causal overclaim | §11 report contract |
| GCI course materials (sesión 7, QA, competition tutorial) | Code must be clean, deterministic, seed-controlled, auditable; external data invalidates ranking; reproducible-code audits possible | Notebook contract (§10): top-to-bottom, relative paths, PROJECT_SEED=42, environment + commit recorded | Disqualification / audit failure | §10, §13 |
| CatBoost / LightGBM / XGBoost papers | Categorical/missing handling is model-dependent | Out of Phase 7 scope by gate; noted only as Phase 8 dependency (frozen RF is the only estimator) | Premature model comparison | §18 lock |

---

## 6. ECC Agents and Skills Plan

Availability verified on disk: **10/10 agents** in `.claude/agents/`, **21/21 skills** in `.claude/skills/` (exact match with the expected inventory). No new installation is recommended: no capability gap was identified for Phase 7's scope; everything needed (planning, ML review, leakage review, gate enforcement, verification) is covered. Adding tools now would increase surface without mitigating any identified risk.

**Classification:**

1. **Use actively in Phase 7:** planner, plan-orchestrate, mle-reviewer, mle-workflow, code-reviewer, python-reviewer, silent-failure-hunter, eval-harness, gateguard, verification-loop, repo-scan, git-workflow (commit step only, post-authorization).
2. **Available, invoke on need:** architect, code-explorer, docs-lookup, documentation-lookup, python-patterns, python-testing, codebase-onboarding, code-tour, context-budget, token-budget-advisor, safety-guard, architecture-decision-records (only if a policy decision at closure merits an ADR).
3. **Not for Phase 7 (future phases):** agent-eval, agent-architecture-audit, automation-audit-ops (Phase 12 automation review), build-error-resolver (dormant unless an environment/build failure appears).
4. **Risky/prohibited uses:** no installed item is inherently prohibited, but **any** agent/skill applied toward HPO, submissions, leaderboard optimization, model-family comparison, ensembling, scraping, or external data is prohibited in this project phase regardless of the tool.

| Etapa o necesidad | Agente/skill sugerido | Uso propuesto | Riesgo mitigado | Condición de activación |
|---|---|---|---|---|
| Block 0 pre-flight | repo-scan + gateguard | Verify HEAD, clean tree, gates intact | Building on a wrong baseline | Start of any Phase 7 session |
| Plan review | planner / plan-orchestrate | Re-validate this package against repo state | Stale plan execution | Before authorization (§16) |
| Notebook design review | mle-reviewer + eval-harness + mle-workflow | Review data contracts, fold use, OOF/eval design of notebook 07 draft | Methodological defects before any run | After draft, before execution |
| Static code review (two-role rule) | code-reviewer + python-reviewer + python-patterns | Independent review of notebook 07 code; generator ≠ verifier | Leakage/code defects | After draft, before execution |
| Silent-failure pass | silent-failure-hunter | Proba extraction, NaN paths, swallowed exceptions, artifact writes | Silent metric corruption | Same gate as code review |
| Execution session guard | gateguard + safety-guard | Keep HPO/submissions/Phase-8/forbidden paths blocked during the run | Scope creep mid-run | During authorized execution |
| Post-run verification | verification-loop (+ independent stdlib recompute, as in 6A) | Recompute OOF AUCs from persisted files; git/forbidden-path checks | Self-reported-only results | Immediately after execution |
| Selective commit | git-workflow | Stage the explicit file list only; record hash into acceptance record | `git add .` accidents; unanchored results | **Only after explicit user authorization** |
| Long-session hygiene | context-budget / token-budget-advisor | Keep execution sessions within budget | Context-degradation errors | If sessions grow long |
| Policy decision record | architecture-decision-records | Optional ADR if imputation/missingness policy changes at closure | Undocumented policy drift | At Phase 7 acceptance, if warranted |

---

## 7. Proposed Phase 7 Block Architecture

The suggested 7-block architecture was evaluated against §13's minimum areas and adopted with one refinement: Block 2 is named a *Specification* block to stress that features are pre-registered on paper before any code exists. No block was added or removed — the suggested set maps 1:1 onto the minimum areas, and finer granularity would add ceremony without new control points; coarser granularity would merge decision gates that must stay separable (specification vs implementation vs validation).

| Block | Nombre | Objetivo | Decisiones que cubre | Evidencia necesaria | Riesgos mitigados | Salida esperada | Condición de avance |
|---|---|---|---|---|---|---|---|
| 0 | Repository, Git & Phase Gate Verification | Prove the execution session starts from the accepted baseline | None (verification only) | HEAD = authorized hash; clean tree; acceptance records present; folds sha `96937649526bcadb` | Building on wrong/dirty baseline | Recorded verification block in notebook + report | All checks PASS; any FAIL ⇒ stop |
| 1 | Baseline Policy Freeze | Freeze the policies every variant inherits | Anchor=V0; median+one-hot; no School; **BMI not adopted** (V5 evidence below threshold); threshold 0.005436 + 4/5; min slice 50; candidate-log separation | `phase6a_acceptance.md`; D1 summary | Silent policy drift; re-litigating closed decisions | Frozen-policy section in notebook + brief | Policies restated verbatim and asserted in code |
| 2 | Missingness / Measurement Availability Feature Specification | Pre-register exact feature definitions and the variant ladder | Which features, exact formulas, what is deferred/prohibited | §9 of this brief, ratified at §16 | Unbounded feature creation; adaptive design | Ratified variant table (this brief §9) | Ratification at the Project Authorization Gate (§16) |
| 3 | Fold-Safe Implementation Design | Define how the notebook computes everything leakage-safely | Pipeline structure, fold loop, guards, asserts | §10 of this brief; Phase 6/6A audited code as template | All fit-scope leakage layers | Notebook contract (§10), then the notebook itself | Independent review (two-role rule) passes |
| 4 | Validation, Slice Reports & Acceptance Criteria | Decide, per rung, adopted/rejected with evidence | Threshold rule application; slice guard; edge cases | §11 tables | Reading noise as signal; subgroup harm | Variant summary + slice report + decision table | Every rung classified by the pre-registered rule |
| 5 | Artifact, Documentation & Git Plan | Keep results traceable and commit-anchorable | Artifact names; candidate log; selective-commit list | §13 | Overwrites; unanchored results; log corruption | All §13 artifacts written; main log untouched | Pre-write guards held; post-run git checks clean |
| 6 | Execution Authorization Gate | Separate decision from implementation | Whether to execute at all; any deviation from this plan | This brief + runbook reviewed | Unauthorized execution | Project Authorization Note (runbook §9) | **Explicit user/project director authorization recorded** |

Block 6 is logically *before* Blocks 3–5's execution; it sits last in the table because the planning artifacts it ratifies are Blocks 0–5. Operational ordering is in the runbook.

---

## 8. Block-by-Block Phase 7 Plan

For each §13 minimum area:

**8.1 Repo/Git/gate verification (Block 0).** Objective: session starts at the authorized commit with a clean tree. Evidence: §1 command set re-run live. Decisions: none. Risks: wrong baseline. Output: verification table. Advance: all PASS. Stop: any mismatch ⇒ report severity (blocker if HEAD differs or forbidden paths show diffs) and halt.

**8.2 Baseline policy freeze (Block 1).** Objective: every variant inherits the ratified policy set. Decisions covered: anchor, imputation, encoding, BMI disposition (resolved: not adopted, from existing V5 evidence — no new run), School exclusion, log policy. Evidence: acceptance records. Output: frozen-policy cell + assertions (e.g., `School not in features` raise-on-violation). Advance: assertions in place. Stop: any pressure to alter a frozen policy mid-run.

**8.3 Missingness feature planning (Block 2).** Objective: pre-registered, parameter-free, row-wise definitions (§9). Evidence: train/test missingness counts; Phase 3 hypotheses; leakage checklist (missingness indicators: *Allowed, row-wise, Phase 6+*; `available_measurement_count`: *Allowed row-wise, Phase 7*). Risks: cardinality blowups (co-missingness), adaptive redefinition. Output: ratified table. Advance: §16 ratification. Stop: any feature requiring fitting that is not in the fold-safe plan.

**8.4 Fold-safe implementation design (Block 3).** §10. Advance: independent review. Stop: review finds fit-scope defects.

**8.5 Validation & acceptance (Block 4).** §11. Advance: all rungs classified. Stop: §11 edge-case stop conditions.

**8.6 Artifacts/docs/Git (Block 5).** §13. Advance: artifacts exist, guards held. Stop: collision or forbidden-path touch.

**8.7 Authorization gate (Block 6).** §16. Advance: signed note. Stop: absent authorization = no execution.

**8.8 Closure & Phase 8 lock (§18).** Phase 7 closes only via a future signed `docs/07_feature_engineering/phase7_acceptance.md`; Phase 8 stays locked regardless of outcome until separately authorized.

---

## 9. Candidate Feature Specification

**Feature definitions (all row-wise, parameter-free, computable identically on train and test rows at final-inference time):**

- `Age_missing` = 1 if `Age` is NaN else 0. (Kept separate from physical-test missingness per Phase 3 evidence.)
- `<col>_missing` for each of the 6 physical tests: `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`.
- `available_measurement_count` = count of non-missing among the 6 physical tests (0–6). Identity: `physical_missing_count = 6 − available_measurement_count` — perfectly collinear, so **only `available_measurement_count` enters**; the mirror is documented, not duplicated.
- `measurement_completeness_group` = predeclared constant bins on `available_measurement_count`: `0 → "none"`, `1–3 → "low"`, `4–5 → "partial"`, `6 → "complete"`, encoded as the ordered integers 0–3 by a fixed row-wise mapping (no fitting, no quantiles). Bin edges are fixed *now, in this brief*, not tuned later.

**Pre-registered variant ladder** (frozen folds; RF(100, depth 5, seed 42); fold-fitted preprocessing; hard cap: **≤ 8 trained variants** without a new recorded authorization):

| Rung | variant_id (proposed) | Feature set / pipeline | Imputation | Trained? | Purpose |
|---|---|---|---|---|---|
| F0 | `phase7_f0_anchor_recheck` | Phase 6 anchor: 13 raw features | median | Yes (gate) | Integrity gate: must reproduce OOF 0.726616 (±1e-6) or stop |
| Vref0 | copy of V0 OOF | — | — | No (copied) | Paired-delta base |
| Vref7 | copy of V7 OOF | — | — | No (copied) | **Implicit-missingness diagnostic reference**: the implicit-missingness effect (+0.0757) that explicit flags should recover |
| F1 | `phase7_f1_median_flags` | F0 + 7 missingness flags (Age + 6 tests) = 20 features | median | Yes | Core hypothesis: explicit flags under median |
| F5 | `phase7_f5_mean_flags` | same 20 features | **mean** | Yes | Completes the 2×2 with V0/V7: do flags subsume the imputation-statistic effect? |
| F2 | `phase7_f2_median_flags_count` | F1 + `available_measurement_count` = 21 | median | Yes | Incremental value of the count beyond flags |
| F3 | `phase7_f3_median_flags_count_bins` | F2 + `measurement_completeness_group` = 22 | median | Yes | Incremental value of coarse bins |
| F6 (gated) | `phase7_f6_mean_flags_count` | F5 + count | mean | Only if F5 clearly leads F1 (pre-registered rule: F5−F1 OOF ≥ threshold) | Mirror increment on the mean branch |
| F4 (gated) | `phase7_f4_role_interactions` | best accepted rung + predeclared `available_measurement_count × Player_Type` interaction (via fold-fitted OHE products) | inherit | Only under the hardened F4 activation conditions below | Role-aware completeness, limited form |

**Interpretation map (pre-registered):** F1 ≈ Vref7's gain ⇒ flags capture the mechanism; adopt flags, keep median (cleanest policy). F5 ≫ F1 ⇒ fill-value placement adds signal beyond indicators; imputation-statistic policy goes to the acceptance decision with both numbers. F1 ≈ F0 (no gain) ⇒ record "no qualifying gain under frozen model config" (see §4 caveat); the mean-vs-flags question becomes a Phase 8 input.

**Imputation-policy clarification:** Even if F5 passes the acceptance threshold, mean imputation is not automatically adopted as the new default policy. Any change from median to mean imputation must be explicitly decided in `phase7_acceptance.md`.

**F4 hardened activation conditions:** `phase7_f4_role_interactions` may be activated only if (1) an earlier rung passes the acceptance threshold; (2) slice diagnostics show meaningful heterogeneity by `Player_Type` or `Position_Type`; and (3) the user/project director explicitly authorizes F4 in the initial Project Authorization Note. If F4 is not authorized initially, activating it later requires stopping the current run and issuing a new Project Authorization Note with a new `run_id`.

**Feature families table:**

| Feature family | Feature candidata | Tipo | Row-wise/Fold-safe | Riesgo de leakage | Riesgo de overfitting | Acción recomendada | Justificación |
|---|---|---|---|---|---|---|---|
| Age missingness | `Age_missing` | binary flag | Row-wise | None (current-row only) | Low | **Allowed — F1** | Phase 3 flags Age missingness as a distinct, strong subfamily |
| Physical-test missingness | 6 × `<col>_missing` | binary flags | Row-wise | None | Low | **Allowed — F1** | Direct explicit encoding of the V7 mechanism |
| Availability count | `available_measurement_count` | integer 0–6 | Row-wise | None | Low | **Allowed — F2** | Phase 3 hypothesis; leakage checklist marks it Allowed for Phase 7 |
| Mirror count | `physical_missing_count` | integer | Row-wise | None | Low | **Excluded (redundant)** | Perfectly collinear with the count above |
| Completeness bins | `measurement_completeness_group` (fixed bins) | ordered categorical → int | Row-wise (predeclared constants) | None if bins are constants | Low–moderate | **Allowed — F3** | Bins fixed in this brief; quantile/learned bins would require fold fitting and are not proposed |
| Co-missingness patterns | pattern key over 7 flags | categorical (≤ 2⁷ = 128 levels) | Row-wise to compute, but useful only with grouping/encoding that learns | Low to compute; **encoding risk** | **High** (rare patterns) | **Deferred** | Cardinality + rare-level instability; revisit only if F1–F3 leave a large residual vs Vref7, with fold-safe rare grouping and a new gate |
| Role-aware completeness | `available_measurement_count × Player_Type`; missingness × `Position_Type` | interactions | Row-wise products of row-wise features and fold-fitted OHE columns | Low if built inside the pipeline | Moderate (dimensionality) | **Gated — F4 only** | Phase 3 hypothesis (`Player_Type → completeness → Drafted`, descriptive); limited predeclared form only |
| BMI | `Weight / Height²` | ratio | Row-wise | None | Low | **Not adopted in Phase 7 core** | Already measured clean (V5 − V0 = +0.000332 < 0.005436); decision recorded in Block 1; re-proposable later with new evidence |
| School (any form) | frequency/count/target encodings | learned | Requires fold fitting | **High** | **High** | **Prohibited in Phase 7 core** (frozen) | Stays diagnostic-only slice; staged School work is a separate, later gated wave |
| Role-normalized physical stats | role z-scores/percentiles | learned group stats | Fold-fit required | High if global | Moderate | **Deferred** (later wave) | FE roadmap Block 3; out of this phase's missingness scope |

---

## 10. Fold-Safe Implementation Design, if Later Authorized

No notebook is created now. The future notebook is bound by this contract:

- **File:** `notebooks/07_phase7_missingness_availability_feature_block.ipynb`; `experiment_id = phase7_missingness_availability_v1`.
- Runs top-to-bottom from repo root; relative paths via a project-root finder; `PROJECT_SEED = 42`; environment block records Python/numpy/pandas/sklearn versions + `git rev-parse HEAD` + dirty flag. Executed headless with the project venv (`.venv\Scripts\python.exe`, Python 3.13.13, pandas 3.0.3, scikit-learn 1.9.0 — the environment that produced and reproduced all 6A results).
- **Structure** (adopting §16 of the planning prompt's suggested skeleton, unchanged — it matches the audited 04/05/06 notebooks): title/scope/guardrails → imports/config → path & environment checks → data loading + contract checks (the 12 checks used in 6A) → frozen-fold loading + integrity asserts (2781 rows, labels 0..4, Id order = train order, sha256[:16] = `96937649526bcadb`) → baseline policy freeze cell (Block 1 assertions) → feature-block definitions (row-wise builders with unit-style asserts: e.g., flag sums must equal the known train missingness counts of §3) → fold-safe pipelines (numeric `SimpleImputer(median|mean)` + categorical `most_frequent`+`OneHotEncoder(handle_unknown="ignore")` inside `ColumnTransformer`+`Pipeline`, fitted per fold on the training mask only — reusing the audited 6A builders) → per-variant OOF (`get_positive_class_proba` with `estimator.classes_` verification; probabilities asserted finite, in [0,1], no NaN; no single-class fold) → F0 integrity gate (stop if ≠ 0.726616 ± 1e-6) → paired fold deltas vs F0 → slice diagnostics (the 7 Phase 6 dimensions, min-n=50 flag) → acceptance-rule evaluation per rung → artifact writes (pre-write guards: fail-if-exists; main log read-before/assert-unchanged-after) → executive conclusion cell.
- **Forbidden inside the notebook:** test-data fitting of any kind (test used only for contract checks; final inference is not a Phase 7 task), submissions, HPO, alternate estimators, School in features, LB values, `logs/experiment_log.csv` writes.

---

## 11. Validation, Slice Reports and Acceptance Criteria

**Primary currency:** OOF ROC-AUC on the frozen folds, positive-class probabilities for `Drafted = 1` via verified `estimator.classes_`. Secondary: fold mean ± std, per-fold paired deltas vs F0.

**Adoption rule (ratified, applied per rung):** adopt only if `OOF(variant) − OOF(F0) ≥ 0.005436` **and** the paired fold delta is positive in ≥ 4/5 folds **and** the slice guard passes.

**Slice guard (pre-registered):** mandatory slices = `Player_Type`, `Position_Type`, `Year`, `Age_missing`, `available_measurement_count`, `measurement_completeness_group`, frequent-vs-rare `School` group (diagnostic only). Slices with n < 50 are reported but flagged non-evaluable. If any mandatory slice with n ≥ 50 degrades by more than 0.02 AUC versus F0, the rung is **escalated to user/project director review** (not auto-adopted, not auto-rejected) with the slice table attached.

**Pre-registered edge-case handling:**

| Scenario | Action |
|---|---|
| Gain < threshold | Reject rung; record numbers; no redefinition-and-retry within the run |
| Mean OOF up but same-sign < 4/5 | Reject (variance-driven); record |
| OOF up but mandatory slice (n ≥ 50) drops > 0.02 | Stop rung; user/project director review with slice evidence |
| Any leakage warning / fit-scope doubt | **Stop the run**; report; no result from a doubted pipeline is interpretable |
| Fold-integrity failure (count/labels/order/sha) | **Stop immediately** (6A stop-condition pattern) |
| Probabilities NaN / outside [0,1] / single-class fold | Stop; defect, not a result |
| `classes_` does not locate label 1 exactly once | Stop (the helper raises by design) |
| Existing artifact collision | Stop; never overwrite; new run_id requires authorization |
| HEAD ≠ authorized hash at session start | Stop before any compute |
| F0 ≠ 0.726616 ± 1e-6 | **Stop — integrity gate failed**; everything downstream uninterpretable |
| Pressure to add/modify variants mid-run | Stop; record request; require user/project director decision (6A discipline) |

**Report contract:** variant summary table; fold-by-fold AUC; paired deltas; gap-vs-Vref7 readout (how much of +0.0757 the explicit features recover); slice report; per-variant leakage checklist; environment + commit; explicit *adopted / rejected / escalated* per rung; association-only language.

---

## 12. Leakage Control Strategy

Instantiates `docs/05_methodology/leakage_checklist_phase6.md` for Phase 7:

| Layer (project taxonomy) | Phase 7 control |
|---|---|
| Data / external | Official CSVs only; references contribute methodology, never data |
| Test-to-train | Test rows used only for contract checks; **no Phase 7 fitting touches test**; no final inference in Phase 7 |
| Preprocessing / imputation / encoding | All imputers/encoders inside per-fold `Pipeline`/`ColumnTransformer`, fitted on the training mask only |
| Feature computation | All §9 features are row-wise, parameter-free; **a feature requiring fitting is out of this phase's scope by construction** |
| Target encoding | Absent (blocked) |
| Feature selection | Absent; the ladder is pre-registered, not searched |
| Role statistics | Only fold-fitted OHE of raw role categoricals; F4 interactions built inside the pipeline if activated |
| Rare grouping | Absent (co-missingness deferred partly for this reason) |
| HPO / model selection | Single frozen estimator; variant cap; adoption by pre-registered rule, not by max-picking |
| Leaderboard | Untouched |
| Confound/group | Folds frozen; grouped CV dormant per refined D2; D2 remains a heuristic (acceptance warning) — any new duplication evidence is a stop condition, not a silent protocol change |
| Drift misuse | No test-distribution-driven choices; drift remains descriptive |
| Diagnostic-only variables | `frequent_vs_rare_school_group` stays out of the feature matrix; its global threshold is legitimate only because it is diagnostic (flagged in Phase 6 acceptance — the same pattern as a *feature* would be leakage) |

Verification doctrine (proven in 6A): self-checks inside the notebook **plus** post-run independent recomputation of headline OOF AUCs from persisted artifacts by a different role/session (two-role rule).

---

## 13. Artifact, Documentation and Git Plan

**Created/updated in this planning run (authorized set only):**

```text
docs/07_feature_engineering/phase7_master_planning_brief.md      (this file)
docs/07_feature_engineering/phase7_operator_runbook.md
docs/07_feature_engineering/prompt_codex_phase7_execution_plan.md
```

**Future artifacts if execution is authorized (names reserved; NOT created now):**

```text
notebooks/07_phase7_missingness_availability_feature_block.ipynb
outputs/oof/phase7_missingness_availability_v1_<variant_id>_oof_predictions.csv   (one per trained variant F0, F1, F5, F2, F3 [, F6, F4])
outputs/validation/phase7_missingness_availability_v1_variant_summary.csv
outputs/validation/phase7_missingness_availability_v1_slice_report.csv
outputs/reports/phase7_missingness_availability_v1_validation_report.md
outputs/reports/phase7_missingness_availability_v1_experiment_log_candidate.csv
docs/07_feature_engineering/phase7_acceptance.md                                   (at closure, signed by the user/project director)
```

Naming deviation from the orientative list, justified: per-variant OOF files follow the `phase6a_<variant>_oof_predictions.csv` precedent (one file per trained variant) instead of a single OOF file, because paired-delta auditing requires every variant's OOF to be independently recomputable. The orientative `phase7_execution_plan.md` / `phase7_candidate_feature_spec.md` / `phase7_validation_and_acceptance_criteria.md` are **subsumed by §§7–11 of this brief**; creating them as separate files is not recommended (documentation drift risk across near-duplicate sources). If the director prefers separate files, they can be extracted verbatim later.

**Git policy:** this run stages and commits **nothing**. After execution and review, the selective-commit candidate list is: notebook 07 + the artifacts above + `phase7_acceptance.md` + these three planning docs — staged individually (never `git add .` / `git commit -a`), only on explicit instruction, with the resulting hash recorded into the acceptance record (the `f1fb717` → `c4d5647` pattern). Main log untouched; v2 migration stays separately gated.

---

## 14. Risks, Failure Modes and Mitigations

| Risk | Failure mode | Mitigation |
|---|---|---|
| Depth-5 RF under-uses flags | False "missingness useless" conclusion | Pre-registered interpretation (§4 caveat, §9 map); finding routed to Phase 8 as input, not tuned away |
| F5 (mean+flags) tempts silent imputation-policy change | Anchor drift without decision record | Policy change only via signed `phase7_acceptance.md`; F5 is a measurement, not a default |
| Variant creep ("one more feature") | Selection bias; HPO-by-stealth | Hard cap ≤ 8 trained variants; gated F4/F6 with pre-registered activation rules; mid-run change = stop condition |
| Slice harm hidden by global gain | Subgroup regression (e.g., `special_teams`) | Slice guard with n ≥ 50 and 0.02 escalation rule |
| Redundant/collinear features muddy interpretation | Ambiguous rung attribution | Single-factor ladder; collinear mirror count excluded by construction |
| Artifact overwrite or unanchored results | Lost audit trail | Pre-write guards; experiment_id naming; commit-anchoring step with recorded hash |
| Environment drift | Irreproducible numbers | Pin to `.venv` (3.13.13 / pandas 3.0.3 / sklearn 1.9.0); environment recorded in report; F0 gate catches drift numerically |
| Generator-verifier collusion | Unreviewed defects | Two-role rule: independent static review + independent OOF recomputation post-run |
| Phase 8 pull ("just try LightGBM on the winner") | Gate violation | gateguard + §18 lock; explicit refusal wired into the Codex prompt |

---

## 15. Explicit Non-Actions

This planning run did **not**: execute Phase 7 or any experiment; create or execute any notebook; train any model; generate any OOF/validation/report artifact under `outputs/`; generate any submission; run HPO; compare model families; consult the public leaderboard; modify `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`, or any tracked file; stage anything; commit anything; push anything; install any tool; open Phase 8.

The only filesystem writes were the three authorized documents under `docs/07_feature_engineering/`.

---

## 16. Required User Authorization Before Execution

Phase 7 execution may begin only after the user/project director explicitly and in writing:

1. Approves this brief and the runbook (or records amendments).
2. **Ratifies the §9 variant ladder and exact feature definitions** (including the fixed completeness bins and the gated F4/F6 activation rules), or edits them — after which they freeze.
3. Confirms the operative thresholds: OOF gain ≥ 0.005436; same-sign ≥ 4/5; slice min n ≥ 50; slice-degradation escalation at 0.02; F0 tolerance ±1e-6; variant cap ≤ 8.
4. Confirms the artifact names of §13 and the no-commit-without-instruction policy.
5. Records the authorized starting commit hash for the execution session (currently `c4d5647`; it will advance if these planning docs are committed first — the Project Authorization Note must state the hash the session must verify).
6. Issues an explicit "execute Phase 7" instruction referencing `prompt_codex_phase7_execution_plan.md`.

Absent any item above, the state remains: **planned, not executable**.

---

## 17. Recommended Next Step

**Option A — Review the generated Phase 7 planning package; execution remains blocked until explicit user authorization.**

Concretely: (1) read this brief top-to-bottom; (2) ratify or amend §9 and §16's parameters; (3) decide whether to selectively commit the three planning docs first (recommended, so the execution session can verify a planning-inclusive hash); (4) when ready, issue the authorization per §16 using Deliverable C. Phase 8 remains locked throughout (§18 of the planning prompt; §4 item 13 here).
