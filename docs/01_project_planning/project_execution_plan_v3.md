# Project Execution Plan v3 — Reto Tokio

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-11
**Status:** Active execution plan. Supersedes `project_execution_plan_v1.md` (untracked, historical) and `project_execution_plan_v2_context_efficient.md` (tracked, historical reference). Where v1/v2 conflict with v3, v3 governs; where v3 conflicts with `CLAUDE.md`, `AGENTS.md`, or `docs/05_methodology/`, the **stricter** rule governs and the conflict must be reported.
**Companion documents:** `integral_project_review_phase0_phase6.md` (diagnosis), `phase6a_baseline_reconciliation_plan.md` (Phase 6A detail).

---

## 1. Purpose of v3

v1 and v2 were written before any implementation existed. The project now has: a committed Phase 2 baseline (CV 0.812964, public LB 0.80792), committed Phase 3 EDA, committed Phase 4 research, a committed Phase 5 methodology freeze, and an implemented-but-uncommitted Phase 6 validation harness (fold mean 0.729253, OOF 0.726616). v3 exists because:

1. **Two non-comparable baselines exist** (Phase 2 leaky-by-design vs Phase 6 leakage-safe) and prior plans never anticipated reconciling them. v3 inserts a mandatory **Phase 6A**.
2. **Phase closure has never been an explicit event** — prior phases closed by inference from later work. v3 introduces written acceptance records per phase.
3. **Automation is now real** (Claude Code with 21 local skills and 10 local agents) and prior plans had no automation boundaries. v3 defines what may be automated, by whom, and behind which human gates.
4. **Artifact, validation, and leakage rules are frozen** but scattered across four methodology docs. v3 consolidates them into operational contracts (§5–§7) that future prompts can cite directly.
5. Prior plans lacked **per-phase acceptance criteria, stop conditions, and executor assignments**. v3 provides them so future sessions can execute phases with minimal ambiguity.

v3 changes no frozen methodology decision. It operationalizes them.

---

## 2. Operating principles

1. **Leakage prevention first.** Any transformation that learns a statistic from rows is fitted only inside training folds. When in doubt, treat it as learned.
2. **Reproducibility.** Every important result must be regenerable from a notebook that runs top-to-bottom from the repo root with fixed seeds and relative paths.
3. **Traceability.** Every experiment has an `experiment_id`, declared inputs, named artifacts, and (from Phase 6 acceptance onward) a commit hash recorded at run time. Results not anchored to a commit are provisional.
4. **Phase gates.** No phase starts without its entry criteria met and recorded human acceptance of the prior phase. Gates are never opened implicitly by doing the work.
5. **Public leaderboard discipline.** The LB is a post-submission sanity check (Phase 11 only). It never drives feature, model, preprocessing, HPO, or submission-choice decisions. LB-informed reasoning anywhere else is a protocol violation, even when it "obviously" points the right way.
6. **Human approval gates.** Phase acceptance, gate openings, log migration, anchor/threshold ratification, encoding policy, BMI adoption, all submissions, and all commits are human decisions. Claude drafts; humans accept.
7. **Automation boundaries.** Automation may read, analyze, draft documents, and (when a phase authorizes it) implement notebooks. Automation never self-authorizes execution of training runs, artifact generation outside the authorized experiment, log writes, or git operations.
8. **Artifact governance.** No artifact overwrites another without a new `experiment_id`/`run_id`. Diagnostic artifacts and decision artifacts are kept distinct (§5).
9. **Simplicity before complexity.** Prefer one parametrized harness over many bespoke notebooks; prefer fewer well-controlled experiments over many uncontrolled ones; prefer dismissing a hypothesis cheaply over carrying it.
10. **Competitiveness without leaderboard chasing.** The route to a strong private-LB score is a trustworthy local validation signal, exploited methodically. Local OOF on frozen folds is the optimization currency; the leaderboard is not.

---

## 3. Source hierarchy

When sources conflict, authority descends in this order. A lower source never overrides a higher one; conflicts are reported, not silently resolved.

1. **Official challenge rules** (as recorded in `docs/00_project_contract/challenge_brief.md`; original sources in `notebooks/_official/` — read-only).
2. **`CLAUDE.md` and `AGENTS.md`** — operating rules, forbidden paths, hard git rules. (`README.md` for environment context.)
3. **`docs/00_project_contract/`** — competition contract and submission checklist.
4. **`docs/05_methodology/`** — frozen validation protocol, leakage checklist, execution decisions. Changing a frozen decision requires an explicit, documented human decision.
5. **This plan (`project_execution_plan_v3.md`)** and its companion review/Phase-6A documents.
6. **`docs/03_eda/` and `docs/04_research/`** — evidence base; informs but does not override frozen decisions.
7. **Notebooks** — implementations; evidence of what was done, not policy.
8. **`outputs/`** — generated evidence; authoritative for *what a run produced*, never for policy.
9. **`logs/experiment_log.csv`** — historical record; append-governed, never policy.
10. **Chat recaps, prompts, untracked planning documents** (`Prompts/`, `Recapitulaciones/`, `project_execution_plan_v1.md`) — historical context only; lowest authority; never cite as a gate-opener.

---

## 4. Global constraints

These bind every phase and every executor (human, Claude Code, Codex, notebook):

- **Data:** only `data/input/train.csv`, `test.csv`, `sample_submission.csv`. Never modified. No external data of any kind (athletes, schools, conferences, rankings, geography, draft history, NFL outcomes, manual labels).
- **Notebooks:** `notebooks/_official/` is never executed or modified. Backup/draft notebooks are not executed unless explicitly requested. Deliverable notebooks run top-to-bottom from repo root, relative paths, fixed seeds, no hidden state.
- **Logs:** `logs/experiment_log.csv` is never overwritten, truncated, or schema-migrated without separate explicit approval. New experiments write **candidate** rows under `outputs/reports/` until a human merges them.
- **Outputs:** writes only to approved folders with contract-conformant names (§5). No overwrites without new `experiment_id`. No manual edits to any generated file.
- **Submissions:** forbidden outside Phase 11. Generated only from a logged, reproducible, verified final candidate. Never manually edited.
- **Public leaderboard:** see §2.5.
- **Git:** never `git add .`, `git commit`, or `git push` without an explicit user request for that exact action. Stage selectively. Never stage: `data/input/`, `notebooks/_official/`, `references/`, `outputs/submissions/`, `logs/experiment_log.csv`, `.vscode/settings.json`, `Libros/`, `Prompts/`, `Recapitulaciones/`, backup notebooks, `.venv/`, `*.zip`.
- **HPO:** blocked until Phase 10 gates (§16.6). No Optuna, GridSearchCV, RandomizedSearchCV, or informal "trying a few values" before then.
- **Model comparison:** blocked until Phase 8. No XGBoost/LightGBM/CatBoost/deep-tabular/ensembles before their gates.
- **School:** never a model feature before Phase 7 Block 4, and then only via fold-safe staged encodings (§17.3).
- **Test data:** structure/shape/order checks and final inference only. Never for fitting, tuning, selection, drift correction, or preprocessing decisions.
- **Reference materials:** PDFs/books/slides accessed only through existing `docs/04_research/` summaries unless a task explicitly asks to inspect a specific source.

---

## 5. Global artifact contract

### 5.1 Locations and purposes

| Location | Purpose | Writable by |
|---|---|---|
| `notebooks/` | Deliverable phase notebooks, numbered `NN_<phase_slug>.ipynb` | Implementation phases only |
| `docs/<phase folder>/` | Plans, protocols, reviews, acceptance records | Documentation tasks |
| `outputs/folds/` | `{experiment_id}_fold_assignments.csv` (`Id,fold`) | Experiment runs |
| `outputs/oof/` | `{experiment_id}_oof_predictions.csv` (`Id,fold,y_true,y_pred_proba`) | Experiment runs |
| `outputs/validation/` | `{experiment_id}_slice_report.csv` and variant-summary CSVs | Experiment runs |
| `outputs/reports/` | `{experiment_id}_validation_report.md`, `{experiment_id}_experiment_log_candidate.csv` | Experiment runs |
| `outputs/submissions/` | `{experiment_id}_submission.csv` — **Phase 11 only** | Phase 11 only |
| `logs/` | `experiment_log.csv` (main log) | Human-approved merges only |

### 5.2 Rules

1. **`experiment_id`** is mandatory, unique, lowercase snake_case, pattern `phase<N><suffix>_<short_description>_v<K>` (existing example: `phase6_rf_sanity_baseline_v1`). For multi-variant audits, variants use `phase6a_<variant_id>` (see Phase 6A plan).
2. **`run_id`** (timestamp or v-increment) is required whenever the same experiment definition is re-executed. A re-run never silently overwrites: either bump `v<K>` or refuse to write if the path exists. From Phase 6A onward, every artifact writer must check-and-fail on existing paths.
3. **No manual prediction edits.** Ever.
4. **Candidate logs vs main log:** every experiment writes `{experiment_id}_experiment_log_candidate.csv` to `outputs/reports/`. Merging into `logs/experiment_log.csv` is a separate, human-approved step that must respect the active schema (legacy until v2 migration is separately approved). Automated steps must verify schema match before any log write and abort on mismatch.
5. **Commit anchoring:** from Phase 6 acceptance onward, each report records the `git rev-parse HEAD` at run time (and whether the tree was dirty). `review_git_status_for_exact_state` is no longer an acceptable value.
6. **Checksums:** every Phase 11 submission report records the SHA-256 of the submission CSV, row count, and head/tail Id checks (submission CSVs are gitignored, so the checksum is the only durable identity).
7. **Path style:** forward slashes in all recorded paths.
8. **Diagnostic vs decision artifacts:** slice reports and diagnostic-only variant results are *diagnostic artifacts* — they inform understanding and must never be cited as the basis for selecting features, models, preprocessing, or submissions. Decision artifacts are validation reports plus the human acceptance records that cite them. Every report must state which kind it is.
9. **Artifact review before commit:** generated artifacts are committed only after the phase's human review, selectively, never via `git add .`. Figures and submission CSVs remain gitignored; their checksums live in reports.
10. **Environment record:** every validation report from Phase 6A onward records Python version and versions of numpy/pandas/scikit-learn used.

---

## 6. Global validation contract

Frozen by Phase 5 (`docs/05_methodology/validation_protocol_phase6.md`); operational form:

1. **Metric:** ROC-AUC via `sklearn.metrics.roc_auc_score`, on positive-class probabilities for `Drafted = 1`. Never hard labels.
2. **Probability extraction:** after fit, read `estimator.classes_`, locate label `1`, fail loudly if absent. Never assume `predict_proba(X)[:, 1]`.
3. **Fold strategy:** `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` with fold labels `0..4`.
4. **Fixed folds:** the canonical fold assignment is the file `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` (to be committed at Phase 6 acceptance, becoming the **project frozen folds**). All Phase 6A/7/8/9 experiments **load** this file and assert integrity (2781 rows, expected per-fold class counts) — they do not recompute folds. Recomputing folds is allowed only to verify the file reproduces from the frozen splitter spec.
5. **Canonical anchor number:** **OOF ROC-AUC on the frozen folds** (single consistent prediction vector). Fold mean ± std is always reported alongside. *(Ratification of OOF-as-anchor is a Phase 6 acceptance item — Human decision required.)*
6. **OOF predictions:** required for every experiment from Phase 6 onward; saved per the artifact contract; used for paired comparisons between experiments (per-fold deltas on identical rows), which are more sensitive than comparing fold means under fold-std ≈ 0.03.
7. **Slice diagnostics:** mandatory dimensions: `Player_Type`, `Position_Type`, `Year`, measurement completeness, `Age_missing`, frequent-vs-rare `School`. Always report `n` with each slice AUC; slices below the minimum-n threshold (to be set in Phase 6A from observed variance) are reported but flagged `low_n_unstable`. Slices are diagnostic artifacts (§5.2.8).
8. **Temporal/Year:** diagnostic only. No temporal split unless official evidence ever justifies it.
9. **Grouped CV:** dormant/conditional. Activates only if unit-of-observation evidence (Phase 6A diagnostic D2) shows likely athlete duplication across rows. If activated, this is a major protocol change requiring human approval and re-baselining.
10. **Public leaderboard:** §2.5.
11. **Acceptance criteria for any validation artifact:** frozen-fold integrity asserted; class-index verified; no NaN/inf predictions; OOF row count = 2781; report includes fold table, OOF AUC, slice table with n, leakage checklist, environment record, commit hash.

---

## 7. Global leakage contract

Frozen by Phase 5 (`docs/05_methodology/leakage_checklist_phase6.md`); operational form:

1. **Fit-scope rule:** any transformation learning any statistic from rows (imputers, encoders, scalers, rare-groupers, role statistics, target encoders, selectors, dimensionality reducers) fits only on the training fold inside CV; for the final model, on full train only.
2. **Blocked globally before CV, always:** global imputation, encoding, scaling, rare grouping, role statistics, feature selection, target encoding, dimensionality reduction, HPO/model selection.
3. **Row-wise transformations** (missingness flags, same-row ratios like BMI, same-row counts) are allowed when computed from current-row values only with no learned parameters. They must still be *declared* per experiment.
4. **Feature engineering (Phase 7):** every learned mapping (frequency tables, rare thresholds, role means/z-scores) is fold-fitted. The known trap: the Phase 6 *diagnostic* rare-school threshold was computed globally — legitimate as a diagnostic, **leakage if copied into features**. Phase 7 prompts must name this trap explicitly.
5. **Target encoding:** blocked until Phase 7 Block 4+, and then only strict OOF with smoothing, with prior School encodings demonstrated stable first.
6. **School:** excluded from features until Phase 7 Block 4; staged per §17.3; always monitored via rare/frequent slices.
7. **Test data:** §4.
8. **Leaderboard leakage:** no decision anywhere in Phases 6–10 may cite an LB number, including the existing 0.80792 (it may be *reported* as history; it may not *justify* a choice).
9. **Selection leakage across experiments:** declare the experiment list before running (pre-registration style); do not extend a phase's experiment list mid-phase just because results disappoint, without a recorded human decision; confirm consolidated candidates in Phase 9 with secondary checks (repeated CV with different seeds) before HPO.
10. **Reusable per-experiment leakage checklist** (template; instantiate in every validation report):

```text
[ ] Feature matrix excludes Id
[ ] Feature matrix excludes Drafted
[ ] Feature matrix excludes School (unless Phase 7 Block 4+ with fold-safe encoding, named)
[ ] All learned preprocessing fitted inside training folds only
[ ] All row-wise features declared and parameter-free
[ ] Frozen folds loaded from file and integrity-asserted
[ ] Positive-class probability via verified estimator.classes_
[ ] OOF predictions only from models that did not train on those rows
[ ] No NaN/inf predictions; values in [0,1]
[ ] Test data used only for allowed operations (named)
[ ] No public leaderboard input to any decision
[ ] No HPO / no model-family comparison (unless phase-authorized, named)
[ ] No submission generated (unless Phase 11)
[ ] Main experiment log untouched; candidate row written
[ ] Artifact paths conform to contract; no overwrites
[ ] Commit hash + environment recorded
```

---

## 8. Phase plan

Common to all phases: forbidden actions in §4 always apply; every phase ends with a one-page **acceptance record** in the phase's docs folder (what was reviewed, what was accepted, open items), signed off by the human; "Stop conditions" mean: stop, report, await human input — never improvise past them.

---

### Phase 0 — Contract and rules
- **Purpose:** competition contract, prohibitions, submission rules.
- **Current status:** Complete in substance (committed `docs/00_project_contract/`); never explicitly closed.
- **Disposition in v3:** Closed retroactively. No further work. Contract docs are authoritative per §3.
- **Human approval:** retroactive closure is noted in the Phase 6 acceptance record (one line); no separate ceremony.

### Phase 1 — Project setup and reproducibility
- **Purpose:** repo structure, environment, seeds, git workflow.
- **Current status:** Functionally complete (commits `5d01461`, `e6eabbf`); never documented as a phase.
- **Disposition in v3:** Closed retroactively. Residual items folded into later phases: environment recording in reports (§5.2.10); `requirements.txt` pinning is an open `Human decision required` item (file not editable under current task scopes).

### Phase 2 — Baseline reproduction
- **Purpose:** faithful local reproduction of the official baseline.
- **Current status:** **Closed.** Committed notebook, log row, submission, public LB 0.80792.
- **Standing interpretation (binding):** Phase 2's CV 0.812964 is a *historical reference*, leakage-inflated by design (global mean imputation + global LabelEncoder). It is **not** a valid comparison anchor for any future decision. It is the *reconciliation subject* of Phase 6A.
- **Forbidden:** modifying or re-running the committed notebook; copying its global preprocessing into any future pipeline.

### Phase 3 — EDA and data contract
- **Purpose:** data contract verification, EDA, risk register, hypothesis register.
- **Current status:** **Closed.** Committed notebook + `docs/03_eda/experiment_notes.md` + 24 figures.
- **Standing interpretation:** the four signal families (role context, measurement availability, role-aware physical profile, institutional context) are **hypotheses**, not approved features.

### Phase 4 — Research synthesis
- **Purpose:** convert PDF/course evidence into project rules (validation, leakage, FE, models, HPO, reproducibility).
- **Current status:** **Closed in substance.** 8 committed docs; consumed as Phase 5 inputs.

### Phase 5 — Methodology freeze
- **Purpose:** freeze metric, folds, seeds, leakage rules, artifact rules, gates.
- **Current status:** **Closed.** Commit `35852e9` (HEAD).
- **Standing rule:** unfreezing any decision requires an explicit documented human decision naming the decision, evidence, and consequence.

---

### Phase 6 — Validation harness review and acceptance
- **Purpose:** human review and formal acceptance of the implemented harness; anchor the work in git.
- **Current status:** Implemented and self-checked in working tree; **untracked; not accepted**.
- **Entry criteria:** met (Phase 5 closed; harness + artifacts exist).
- **Tasks:**
  1. Human reads `notebooks/03_validation_harness_phase6.ipynb` against `docs/05_methodology/validation_protocol_phase6.md` acceptance criteria (all 10) and `leakage_checklist_phase6.md`.
  2. Human reviews `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`, slice report (including Year-trend and rare-school slices), OOF and fold artifacts.
  3. Decide the canonical anchor (recommended: OOF ROC-AUC = 0.726616 on frozen folds) — ratify or amend.
  4. Decide what to commit: the notebook; fold assignments (becomes the project frozen-folds file); OOF; slice report; validation report; log candidate. (Commit only on explicit instruction, selective staging, per Hard Git rules.)
  5. Write `docs/06_validation/phase6_acceptance.md` (acceptance record; new folder is acceptable at that time — not created now).
  6. Decide whether to merge the Phase 6 candidate row into `logs/experiment_log.csv` (legacy schema requires mapping or deferral — explicit choice either way).
- **Task granularity:** one review session; one acceptance record.
- **Allowed:** reading everything; drafting the acceptance record (Claude may draft, human signs).
- **Forbidden:** editing the notebook to "fix" review findings before acceptance decision (findings → record → human decides fix-vs-accept); any new experiment; submissions; HPO.
- **Artifacts expected:** acceptance record; (on instruction) commits anchoring Phase 6.
- **Acceptance criteria:** all 10 protocol criteria confirmed by the human against artifacts; anchor metric ratified; commit decision recorded; open items listed.
- **Risks:** rubber-stamping the self-check (mitigate: human spot-verifies at least the per-fold fit-scope and class-index code paths); editing before anchoring.
- **Validation/leakage checks:** §6.11 / §7.10 verified by reviewer, not regenerated.
- **Git/logging policy:** first commit of Phase 6 work happens here, selectively, on explicit instruction.
- **Automation level:** low (drafting support only).
- **Recommended executor:** human-led; Claude Code as reading assistant.
- **Skills/agents:** `code-reviewer` or `mle-reviewer` agent for an independent read of the notebook (read-only); `verification-loop`/`gateguard` style checks conceptually, without execution.
- **Human approval before next phase:** **Yes — mandatory.**
- **Stop conditions:** any protocol criterion fails → record as finding, stop, human decides remediation path.
- **Decision points:** anchor ratification; commit scope; candidate-log merge or deferral; authorize Phase 6A.

---

### Phase 6A — Baseline reconciliation audit
- **Purpose:** explain the baseline gap — 0.0837 on fold means (0.812964 − 0.729253), 0.0863 on the OOF anchor (0.812964 − 0.726616) — between Phase 2 (leaky) and Phase 6 (clean) via single-factor variants on frozen folds; ratify the Phase 7 anchor, the encoding policy, and the ablation threshold.
- **Current status:** Designed (see `phase6a_baseline_reconciliation_plan.md`); **execution blocked until explicitly authorized** after Phase 6 acceptance.
- **Entry criteria:** Phase 6 accepted and anchored in git; frozen-folds file committed; variant list ratified by human.
- **Tasks / blueprint:** see §9 below and the dedicated plan.
- **Automation level:** medium (notebook implementation by Claude Code once authorized; analysis drafting; human ratifies conclusions).
- **Recommended executor:** Claude Code implements notebook → human reviews → notebook-led execution → Claude drafts report → human accepts.
- **Human approval before next phase:** **Yes — mandatory** (closes Phase 6A and either re-opens Phase 6 findings or opens Phase 7).
- **Stop conditions:** see Phase 6A plan §9.

---

### Phase 7 — Leakage-safe feature block ablations
- **Purpose:** test feature Blocks 0–6 under fixed-fold ablation against the ratified anchor.
- **Current status:** Not started. **Blocked.**
- **Entry criteria:** Phase 6 accepted; Phase 6A closed; anchor + ablation threshold + encoding policy ratified; Block 0 definition (including the BMI decision) ratified.
- **Blueprint:** §10. Do not start.
- **Human approval before next phase:** Yes — block-by-block approvals plus end-of-phase acceptance.

### Phase 8 — Model-family comparison
- **Purpose:** compare shortlisted model families fairly on fixed features/folds/metric.
- **Current status:** Not started. **Blocked** until Phase 7 acceptance.
- **Blueprint:** §11.

### Phase 9 — Candidate consolidation and robustness checks
- **Purpose:** consolidate 1–3 candidate pipelines; stability/variance/slice/calibration checks before HPO.
- **Current status:** Not started. **Blocked.**
- **Blueprint:** §12.

### Phase 10 — Bounded HPO
- **Purpose:** bounded, logged, leakage-safe hyperparameter optimization of the consolidated candidates.
- **Current status:** Not started. **Blocked** by the 7 activation gates (§16.6).
- **Blueprint:** §13.

### Phase 11 — Final training and submission generation
- **Purpose:** final refit, test inference, verified submission, sanity LB check.
- **Current status:** Not started. **Blocked.**
- **Blueprint:** §14.

### Phase 12 — Final audit, documentation, and handoff
- **Purpose:** reproducibility/leakage/artifact/git audits; final narrative; handoff package.
- **Current status:** Not started.
- **Blueprint:** §15.

---

## 9. Phase 6A detailed execution blueprint

Authoritative detail lives in `docs/01_project_planning/phase6a_baseline_reconciliation_plan.md`. Summary of the binding points:

- **Why:** five confounded pipeline factors (fit scope, imputation statistic, encoding, BMI, model seed) separate the two baselines; Phase 7 cannot be interpreted until they are decomposed and one anchor + one pipeline policy is ratified.
- **Variants:** a pre-registered, human-ratified list of ≤ 8 single-factor variants on the frozen folds (see plan §4–§5), each labeled *diagnostic-only* (contains deliberate leakage or unapproved features, exists only to measure an effect) or *methodologically acceptable* (could legitimately become the Phase 7 anchor pipeline).
- **Diagnostic-only examples:** exact Phase 2 replica under Phase 6 reporting; replica minus BMI; replica with seed 42. **Acceptable examples:** Phase 6 current; Phase 6 with fold-safe ordinal encoding; Phase 6 with fold-safe mean imputation; Phase 6 + BMI (row-wise, parameter-free) as a *boundary* variant whose adoption is a Phase 7 Block 0 decision.
- **Must not happen:** no new variants mid-run without human approval; no HPO; no other model families; no feature work beyond declared variants; no submissions; no LB; no adoption of any variant as "the model"; no threshold-shopping.
- **Future artifact names:** `notebooks/04_phase6a_baseline_reconciliation.ipynb`; `outputs/reports/phase6a_baseline_reconciliation_report.md`; `outputs/reports/phase6a_baseline_reconciliation_experiment_log_candidate.csv`; `outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv`; `outputs/oof/phase6a_<variant_id>_oof_predictions.csv`; `outputs/folds/phase6a_fixed_fold_assignments.csv` (copy/verification of the frozen folds). Names reserved now; nothing created until authorized.
- **Acceptance criteria:** gap decomposed with attributed contributions per factor; unexplained residual small relative to fold std; anchor ratified; encoding policy ratified; ablation threshold derived from observed variance (e.g., from per-fold paired deltas and seed-variant noise) and ratified; report written; human acceptance record signed.
- **Anti-feature-selection guard:** Phase 6A compares *pipelines on a fixed feature set*, never feature subsets (the single BMI on/off contrast is a pre-registered pipeline-history question, not a feature search). Any urge to "also try" a feature goes to the Phase 7 backlog.
- **Phase 6 closure:** Phase 6 closes when its acceptance record is signed; Phase 6A findings may append an addendum (e.g., revised anchor) but do not reopen the harness unless a defect is found — in which case: stop condition, human decision.

## 10. Phase 7 feature block execution blueprint

**Do not start Phase 7.** Future design only.

- **Block order** (from `research_notes_feature_engineering.md`, confirmed): Block 0 anchor pipeline (post-6A, including the ratified BMI decision) → Block 1 missingness/measurement-availability (row-wise: `Age_missing`, per-test missing flags, `available_measurement_count`) → Block 2 role context (already partially in baseline; formalize) → Block 3 role-aware physical profile (fold-fitted role statistics, z-scores, ranks; interactions like speed×size) → Block 4 School safe encodings (fold-fitted frequency/count, fold-fitted rare grouping with documented unknown-category policy; OOF target encoding only if earlier School encodings are stable and a human approves) → Block 5 interactions → Block 6 feature selection (fold-safe only).
- **Method:** fixed-fold ablation. Every block run = anchor pipeline ± block, identical frozen folds, OOF AUC + paired per-fold deltas vs anchor, slice diagnostics. One block at a time; cumulative composition only of accepted blocks.
- **Baseline anchor:** the Phase 6A-ratified pipeline OOF. Never Phase 2's 0.812964.
- **Acceptance threshold:** the Phase 6A-ratified threshold (placeholder intuition: improvements below ~½ fold-std on OOF with inconsistent fold signs are noise; exact rule comes from 6A variance evidence). A block that meets threshold but degrades a mandatory slice materially triggers a human review, not auto-acceptance.
- **Leakage checks:** §7 checklist per run; explicit attention to fold-fitted thresholds/role statistics (§7.4 trap).
- **Artifacts:** `experiment_id = phase7_block<N>_<desc>_v<K>` across the §5 folders; per-block validation report; per-block candidate log row.
- **Prompt strategy:** one prompt per block from the §20 template; the prompt pre-registers exactly which features the block contains.
- **Rollback:** a block is rejected by simply not composing it; accepted-block list lives in the phase acceptance record; if a later interaction reveals a problem, re-run the composition without the suspect block (new experiment_id), never edit history.
- **Human checkpoints:** ratify block definitions before any run; accept/reject each block on evidence; end-of-phase acceptance freezes the Phase 8 feature set.

## 11. Phase 8 model-family comparison blueprint

**Do not start Phase 8.** Future design only.

- **Candidates (order):** RandomForest (reference, frozen config), Logistic Regression (with fold-safe scaling/imputation; interpretable floor), HistGradientBoostingClassifier (native NaN handling — note: its missing-value support changes whether imputation is even needed; document the design choice), then XGBoost, LightGBM; CatBoost last and only with the Phase 8+ School gate if Block 4 justified native categorical handling. Deep tabular: only on GBDT plateau and time budget.
- **Fair-comparison protocol:** identical frozen folds; identical Phase 7-accepted feature set; identical metric and OOF/slice reporting; default-ish, pre-registered configs (one config per family, declared before running — initial configs are not HPO if fixed in advance); same leakage checklist; one candidate log row each.
- **Allowed:** the listed families, one pre-registered config each. **Blocked:** ensembles, stacking, per-family tuning loops, adding families mid-phase without approval.
- **Acceptance:** select 1–3 candidates on OOF AUC + fold stability + slice behavior + simplicity; paired OOF deltas over fold-mean comparisons; document why losers lost.
- **Robustness:** seed-variation check on finalists (different model seeds, same folds) to size noise.
- **Human checkpoints:** ratify family/config list before running; ratify finalists after.

## 12. Phase 9 candidate consolidation blueprint

- **Stability:** repeated CV (e.g., 3 extra seeds for the *splitter* in a clearly-labeled secondary analysis — primary frozen folds remain canonical) to confirm finalists aren't fold-lucky. This is the designated guard against accumulated selection-on-frozen-folds (§7.9).
- **Variance:** fold-std and seed-std per finalist; flag fragile candidates.
- **Slices:** no finalist with a materially degraded mandatory slice proceeds without explicit human waiver.
- **Simplicity tradeoff:** prefer the simpler pipeline within noise of the best.
- **Calibration:** check only if it informs robustness understanding; ROC-AUC is rank-based, so calibration is diagnostic-only here.
- **Artifact review:** verify every finalist's artifacts are complete, contract-conformant, commit-anchored, and reproducible before HPO is even discussed.
- **Decision:** human ratifies 1–3 candidates + the exact pipelines that enter Phase 10.

## 13. Phase 10 bounded HPO blueprint

**Do not run HPO.** Future design only.

- **Activation gates (all seven, from `research_notes_hpo.md`):** validation protocol frozen ✔(already); leakage-safe pipeline implemented and accepted; feature blocks tested by ablation; 1–3 candidates from fair comparison; experiment-log schema active (requires the deferred v2 migration decision first); no unresolved leakage issue; no LB dependence.
- **Governance:** Optuna with fixed sampler seed; small, justified, pre-registered search spaces per candidate; trial budget fixed in advance (suggest ≤ 50–100 trials per candidate — exact number is a Phase 10 entry decision); objective = OOF ROC-AUC on frozen folds; sequential deterministic runs before any parallelism.
- **Overfitting controls:** the §7.9 repeated-CV confirmation on the tuned winner before acceptance; report best-vs-default delta honestly (if tuning gains less than the noise floor, keep defaults).
- **Early stop:** budget exhausted, or no improvement above noise floor over a pre-set patience window.
- **Logging/artifacts:** every trial set logged; `experiment_id = phase10_<family>_hpo_v<K>`; study artifacts under `outputs/reports/`.
- **Rollback:** tuned config rejected → candidate keeps its Phase 8 config; never re-open the search "just once more" without human approval.

## 14. Phase 11 final training and submission blueprint

**Do not create submissions.** Future design only.

- **Final candidate selection:** human selects from Phase 9/10 evidence; recorded with full rationale.
- **Refit policy:** refit the exact accepted pipeline on full train (all learned steps fitted on full train only — first and only time that's the fit scope).
- **Test inference:** single pass; class-index-verified probabilities; no post-hoc adjustment.
- **Submission validation (all must pass):** columns exactly `Id,Drafted`; 696 rows; Id order equals `sample_submission.csv` and `test.csv`; probabilities finite, non-missing, in [0,1]; SHA-256 recorded; row-count and head/tail Id spot-checks recorded.
- **No manual edits.** Regenerate or don't submit.
- **Final report:** `phase11_<candidate>_submission_report.md` linking experiment lineage from anchor → blocks → comparison → HPO → final.
- **Leaderboard sanity policy:** LB score recorded after submission as a sanity check only; a surprising LB number triggers an *audit*, never a pipeline change driven by the number itself.
- **Last-submission risk:** the platform ranks by the last submitted file — submission order is a human-controlled checklist item; the intended final file is submitted last and verified.

## 15. Phase 12 final audit and handoff blueprint

- **Reproducibility audit:** clean-environment rerun of the final notebook chain; predictions regenerate within tolerance; checksums match.
- **Documentation audit:** every phase has an acceptance record; stale docs (including `docs/README.md`) finally updated — with explicit approval at that time.
- **Artifact audit:** every logged experiment's artifacts exist, conform, and are commit-anchored.
- **Git audit:** no forbidden paths ever committed; selective-staging history clean.
- **Leakage audit:** end-to-end re-walk of §7 against the final pipeline.
- **Final narrative + lessons learned:** what worked, what was noise, what the gates caught.
- **Final package checklist:** code-audit readiness per the contract's "reproducible Colab code" expectation for high-ranking participants.

---

## 16. Modeling roadmap

### 16.1 Immediate blocked items
XGBoost, LightGBM, CatBoost, deep tabular, ensembles, stacking, any HPO (formal or informal), model-family comparison, submissions, LB feedback. All `Blocked by gate`.

### 16.2 Baseline anchors
- **Historical reference (never an anchor):** Phase 2 — 0.812964 CV / 0.80792 LB; leakage-inflated by design.
- **Provisional anchor:** Phase 6 OOF 0.726616 on frozen folds.
- **Definitive anchor:** ratified at Phase 6A closure (likely the Phase 6-style clean pipeline with the encoding policy 6A selects, possibly including BMI if Block 0 adopts it).

### 16.3 Candidate model families for later phases
Order per §11: RF (reference) → Logistic Regression → HistGradientBoosting → XGBoost → LightGBM → CatBoost (School-gated) → deep tabular (conditional).

### 16.4 Initial configurations for later phases
One pre-registered config per family, declared in the Phase 8 entry record before any run. RF stays at (100, depth 5, seed 42) as continuity reference; others use library defaults with seed 42 and only structural necessities (e.g., scaling for LR) — picking configs by peeking at results is HPO and is blocked.

### 16.5 Fair comparison protocol
§11: same frozen folds, same features, same metric, same OOF/slice reporting, paired OOF deltas, one log row each.

### 16.6 HPO activation gates
The seven gates in §13. Currently ~2/7 plausibly satisfied (protocol frozen; no LB dependence). Log-schema gate has a hidden dependency: the deferred v2 migration decision.

### 16.7 Submission-readiness gates
Phase 11 entry: accepted Phase 9/10 candidate; reproducibility verified; submission validation suite (§14) implemented; human authorization for the specific submission file.

### 16.8 Model risk ranking
| Family | Reward potential | Risk | Notes |
|---|---|---|---|
| HistGradientBoosting | High | Low-Med | Native NaN handling; strong default for this size |
| LightGBM / XGBoost | High | Med | Strong but tuning-hungry; defer gains to Phase 10 |
| CatBoost | Med-High | **High** | Native categoricals tempt School leakage shortcuts; double-gated |
| Logistic Regression | Low-Med | Low | Floor + interpretability; sensitive to imputation/scaling choices |
| RandomForest | Med (known) | Low | Continuity reference |
| Deep tabular | Low-Med | High | Small n=2781; only on GBDT plateau |
| Ensembles | Med | High | Only after OOF diversity demonstrated; Phase 9+ question at earliest |

---

## 17. Feature roadmap

### 17.1 Feature blocks to test later
Blocks 0–6 per §10, in order, one at a time, fixed-fold ablation, pre-registered contents.

### 17.2 Diagnostic-only variables
Until a block formally adopts them: `Age_missing`, `physical_missing_count`, `available_measurement_count`, `measurement_completeness_group`, `frequent_vs_rare_school_group`. Diagnostic computation may be global; feature computation must be fold-safe where learned.

### 17.3 School strategy
Staged and gated: excluded (now) → Block 4 fold-fitted frequency/count + fold-fitted rare grouping with documented unknown-category policy (Phase 7) → strict-OOF smoothed target encoding only if prior encodings stable and human approves (Phase 7+) → CatBoost-native only after Phase 8 gates. Rare/frequent slice monitoring is mandatory whenever School is in play. High-overfitting-risk variable; when in doubt, leave it out.

### 17.4 Role-aware features
Block 3: fold-fitted role means/stds → z-scores, within-role ranks/percentiles; speed×size, strength×size interactions. Phase 3 evidence: physical metrics are role-relative (`phase03_contrarian_global_vs_within_role_associations.png` hypothesis family). Every role statistic is a learned mapping → fold-fitted, no exceptions.

### 17.5 Measurement availability features
Block 1: row-wise counts/flags (parameter-free, leakage-trivial). Caution from Phase 3: availability correlates with role and possibly with selection processes — interpret via slices; bucketing cutoffs (if any) are learned → fold-fitted or fixed a priori.

### 17.6 Missingness features
Block 1: `Age_missing` (strong train-side association per Phase 3 — promising and cheap), per-test missingness flags. Row-wise, declared, leakage-trivial.

### 17.7 Risk ranking of feature ideas
| Feature idea | Reward | Leakage/overfit risk |
|---|---|---|
| Missingness flags / availability counts (Block 1) | Med-High | **Low** — best first move |
| BMI (Block 0 decision) | Low-Med | Low (row-wise) |
| Role-aware z-scores/ranks (Block 3) | Med-High | Med — fold-fitting discipline required |
| School frequency/count (Block 4) | Med | Med-High |
| School target encoding | Med | **High** — last resort, strict OOF |
| Interactions (Block 5) | Med | Med — combinatorial selection risk |
| Global role/rare statistics of any kind | — | **Forbidden** as features |

### 17.8 Feature rollback policy
Accepted-block list is the only state; rejecting/removing a block = recompose remaining blocks under a new `experiment_id`. No in-place edits of past experiments; no partial blocks (a block is accepted or rejected whole; splitting a block is a new pre-registered block definition).

---

## 18. Automation roadmap

### 18.1 What can be automated now
Read-only audits (git state, forbidden paths, artifact-name conformance); documentation drafting (acceptance records, prompts, reports *from* existing artifacts); cross-document consistency checks; leakage-checklist template instantiation.

### 18.2 What should wait
Notebook execution; artifact generation (Phase 6A authorization first); candidate-log merging; log v2 migration; any git operation; anything touching `outputs/`, `logs/`, `data/`, `notebooks/`.

### 18.3 Future scripts/notebooks to create
1. `notebooks/04_phase6a_baseline_reconciliation.ipynb` — parametrized variant harness (the §4.8.1 reusable engine), Phase 6A-gated.
2. A fold-integrity assertion cell/snippet (load frozen folds, assert counts) reused by every future notebook.
3. A submission validation suite (Phase 11-gated) implementing §14 checks.
4. (Optional, later) a read-only artifact-conformance checker script — only with approval, since `scripts/` writes are out of current scope.

### 18.4 Future prompts to create
§20 catalog.

### 18.5 Experiment/artifact governance
§5 contract; enforced by pre-write guards (§8 of the review) and the per-experiment checklist (§7.10).

### 18.6 Claude Code and Codex usage policy
Claude Code/Codex implement notebooks and draft documents **within an authorized phase**, citing this plan's contracts; they never self-authorize runs, never write outside the authorized experiment's artifact paths, never stage/commit/push without an explicit user request, and always end work with the §15-style verification block (status, diff, forbidden-path check). Research synthesis and strategy may continue in chat tools; their outputs enter the repo only through reviewed documents (lowest authority tier, §3.10).

### 18.7 Multi-agent usage policy
Generation and verification are separated (two-role rule): the implementing session/agent never performs its own acceptance audit; an independent read-only review (e.g., `mle-reviewer`/`code-reviewer` agent) reads artifacts and reports. Agents never override gates; agent suggestions that conflict with `CLAUDE.md`/this plan are recorded as recommendations, not acted on.

### 18.8 Human-in-the-loop checkpoints
Phase acceptances; gate openings; variant/block/family/config list ratifications; anchor/threshold/encoding ratifications; log merges and migration; every commit; every submission. (Full list: review §8.3.)

### 18.9 Stop conditions and rollback
Universal stop conditions: a leakage-checklist item fails; frozen-fold integrity check fails; an artifact path collision occurs; a result is too good to be true (e.g., OOF jump ≫ plausible effect — suspect leakage first); instructions conflict with a higher-authority source; any temptation to consult the LB. On stop: report, don't fix. Rollback is always "new experiment_id from last accepted state," never history edits.

---

## 19. Skills and agents roadmap

Installed locally (verified): **skills** — agent-architecture-audit, agent-eval, architecture-decision-records, automation-audit-ops, code-tour, codebase-onboarding, context-budget, documentation-lookup, eval-harness, gateguard, git-workflow, mle-workflow, plan-orchestrate, python-patterns, python-testing, repo-scan, safety-guard, security-review, security-scan, token-budget-advisor, verification-loop. **Agents** — architect, build-error-resolver, code-explorer, code-reviewer, doc-updater, docs-lookup, mle-reviewer, planner, python-reviewer, silent-failure-hunter.

### 19.1 Installed skills/agents useful now
- `mle-reviewer`, `code-reviewer` agents: independent read-only review of Phase 6 notebook and of governance docs (two-role rule).
- `code-explorer` agent: read-only structure/lineage questions.
- `silent-failure-hunter` agent: untracked-artifact / hidden-assumption sweeps (read-only).
- `architect` / `planner` agents: plan decomposition support for future phase prompts.
- `doc-updater` agent: drafting allowed documentation files only.
- `gateguard`, `safety-guard`, `verification-loop` skills: conceptual checklists for pre-action verification (use without letting them execute anything).
- `git-workflow` skill: advisory only — `CLAUDE.md` Hard Git rules always win.

### 19.2 Additional skills/agents recommended now
None. The installed set covers current needs. Do not install anything.

### 19.3 Skills/agents to defer
- `mle-workflow`, `eval-harness`: execution-oriented; defer until a phase authorizes runs (6A+), and even then subordinate to this plan's contracts.
- `python-testing`, `python-patterns`, `python-reviewer`: when notebook/script implementation resumes (6A+).
- `build-error-resolver`: only if implementation breaks (6A+).
- `plan-orchestrate`, `agent-eval`, `agent-architecture-audit`, `automation-audit-ops`: multi-agent scaling concerns — Phase 7+ at earliest, if ever; current workflow is deliberately single-threaded.
- `repo-scan`, `code-tour`, `codebase-onboarding`: onboarding/audit aids; Phase 12 handoff is their natural moment.
- `context-budget`, `token-budget-advisor`, `security-scan`, `security-review`, `architecture-decision-records`, `documentation-lookup`: situational; no scheduled phase.

### 19.4 Trigger phase for deferred skills/agents
| Asset | Trigger |
|---|---|
| `mle-workflow`, `eval-harness`, `python-*`, `build-error-resolver` | Phase 6A authorization |
| `plan-orchestrate`, multi-agent audit skills | Phase 7+, only if workflow parallelizes |
| `repo-scan`, `code-tour`, `codebase-onboarding` | Phase 12 handoff |

### 19.5 Risks of over-automation
Gate erosion by helpful executors; self-certifying experiments; artifact overwrites by re-runs; log schema drift; context dilution (agents re-deriving state and drifting from frozen decisions). Mitigations: §18.6–18.9, two-role rule, pre-write guards, schema asserts.

### 19.6 Recommended agent per future phase
| Phase | Primary executor | Review agent |
|---|---|---|
| 6 (review) | Human | `mle-reviewer` (read-only support) |
| 6A | Claude Code (implementation) → notebook | `mle-reviewer` + `silent-failure-hunter` |
| 7 | Claude Code per block prompt | `mle-reviewer` per block |
| 8 | Claude Code | `mle-reviewer` |
| 9 | Human + Claude analysis | `mle-reviewer` |
| 10 | Claude Code under HPO governance | `mle-reviewer` + `code-reviewer` |
| 11 | Human-led; Claude assists | `code-reviewer` + `silent-failure-hunter` |
| 12 | Human + `doc-updater` | `code-reviewer` |

---

## 20. Prompt roadmap for future execution

Each future prompt must contain: purpose; phase + gate citation; allowed files (explicit list); forbidden files (cite §4); expected artifacts (exact names per §5); required verification commands; stop conditions; and the human approval gate it ends at. Catalog:

| Prompt | Purpose | Allowed writes | Forbidden (beyond §4) | Expected artifacts | Verification | Human gate |
|---|---|---|---|---|---|---|
| Phase 6 review prompt | Guide human review; draft acceptance record | `docs/06_validation/phase6_acceptance.md` (draft) | notebook edits; any `outputs/` write | acceptance record draft | criteria checklist vs artifacts | Sign acceptance |
| Phase 6A implementation prompt | Build `04_phase6a_baseline_reconciliation.ipynb` per ratified variant list | the new notebook only | running it before review; extra variants | notebook (unexecuted) | reviewer pass; fold-load assert present | Approve to execute |
| Phase 6A review prompt | Independent audit of 6A artifacts + report | report annotations/none | re-running variants | review memo | checklist §7.10 per variant | Close 6A; ratify anchor/threshold/encoding |
| Phase 7 feature block prompt (template) | One block: pre-registered features, ablation vs anchor | block notebook/section + its artifacts | any other block; threshold changes | `phase7_block<N>_*` artifact set | leakage checklist; paired deltas | Accept/reject block |
| Phase 7 ablation review prompt | Independent block audit | none | — | review memo | fold integrity; fit-scope spot-check | Block decision |
| Phase 8 model comparison prompt | Pre-registered families/configs on fixed features/folds | comparison notebook + artifacts | tuning; ensembles | `phase8_*` artifact set | §11 protocol checks | Ratify finalists |
| Phase 9 consolidation prompt | Stability/variance/slice/simplicity analysis | analysis report | new models/features | consolidation report | repeated-CV labels correct | Ratify 1–3 candidates |
| Phase 10 HPO prompt | Bounded Optuna per governance | HPO notebook + study artifacts | space/budget changes mid-run | `phase10_*` artifacts | gates re-verified; budget respected | Accept/reject tuned configs |
| Phase 11 submission prompt | Final refit, inference, validated submission | final notebook + submission + report | manual edits; multiple "tries" | `phase11_*` set + SHA-256 | §14 validation suite | Authorize the submission |
| Phase 12 final audit prompt | Full audits + handoff package | audit docs | — | audit reports, final narrative | clean-env rerun evidence | Project closure |

Full prompt texts are written when each phase opens; concise contracts above are binding on those texts.

---

## 21. Prioritized action list

**Immediate (now):**
1. Human reads `integral_project_review_phase0_phase6.md` (companion to this plan).
2. **Phase 6 manual review** (Phase 6 task list, §8): review notebook + artifacts against the frozen protocol.
3. Human decides: accept Phase 6; ratify OOF-as-anchor; decide commit scope for Phase 6 work (explicit instruction required for any git action); record acceptance.
4. Human decides whether to authorize **Phase 6A** and ratifies its variant list (`phase6a_baseline_reconciliation_plan.md` §4–§5).

**After Phase 6 acceptance:**
5. (On instruction) selectively commit Phase 6 notebook + chosen artifacts + acceptance record; the fold file becomes the committed frozen folds.
6. Execute Phase 6A per its plan (implementation → review → run → report).

**After Phase 6A:**
7. Ratify: definitive anchor, encoding policy, ablation threshold, minimum slice size, Block 0 definition (BMI decision); record Phase 6A acceptance.
8. Decide the deferred log-v2 migration question (or re-defer explicitly).
9. Write the Phase 7 Block 1 prompt from the §20 template; ratify Block 1 contents.

**After Phase 7 (per-block acceptances, then phase acceptance):**
10. Freeze the Phase 8 feature set; ratify family/config list; run Phase 8; ratify finalists.
11. Phase 9 consolidation; ratify 1–3 candidates.

**Only near final submission:**
12. Verify all seven HPO gates; Phase 10 bounded HPO (or skip if gains < noise floor — skipping HPO is a legitimate outcome).
13. Phase 11: final refit, validated submission, recorded checksums, LB sanity check, last-submission ordering control.
14. Phase 12: audits, narrative, handoff.

**Final gate recommendation:** **Proceed to Phase 6 manual review now; treat Phase 6A as mandatory before Phase 7.** Nothing else opens until both are accepted in writing.
