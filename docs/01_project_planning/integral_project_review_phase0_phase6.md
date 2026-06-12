# Integral Project Review — Phase 0 to Phase 6

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-11
**Review basis:** Repository state at commit `35852e9` (`docs: freeze phase 5 methodology decisions`), branch `master`, plus untracked working-tree content.
**Review mode:** Read-only analysis. No notebooks executed, no data modified, no artifacts generated, nothing staged or committed.

Claim labels used throughout: `Confirmed fact`, `Repository evidence`, `Inference`, `Risk`, `Opportunity`, `Recommendation`, `Blocked by gate`, `Open decision`, `Automation candidate`, `Human decision required`, `Not confirmed yet`.

---

## 1. Executive diagnosis

The project is methodologically disciplined and unusually well documented for its stage, but it currently has **two non-comparable baselines** and **its most important implementation work (Phase 6) is entirely untracked**.

- `Repository evidence` — Phases 0–5 are committed with coherent, mutually referencing documentation. The Phase 5 freeze (`docs/05_methodology/`) is specific, evidence-cited, and internally consistent.
- `Repository evidence` — The Phase 6 validation harness exists, executed, and self-reports passing all 9 leakage checks (`outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`), but the notebook and every Phase 6 artifact are untracked. There is no commit anchoring the Phase 6 results to a code version.
- `Confirmed fact` — Phase 2 CV mean ROC-AUC is **0.812964** (`logs/experiment_log.csv`); Phase 6 mean fold ROC-AUC is **0.729253** and OOF ROC-AUC is **0.726616** (`outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`). The gap — 0.0837 on fold means, 0.0863 against the OOF anchor — is unexplained because **five pipeline factors differ simultaneously** (see Section 5).
- `Risk` — If Phase 7 starts now, no feature-block ablation result can be interpreted: there is no single credible anchor score, and the quantitative ablation threshold (explicitly `Not confirmed yet` in `docs/05_methodology/phase5_execution_decisions.md`) cannot be set against two incompatible baselines.
- `Recommendation` — Phase 6 should go to **manual human review now**, and a **Phase 6A Baseline Reconciliation Audit must be mandatory before Phase 7**. See `docs/01_project_planning/phase6a_baseline_reconciliation_plan.md`.

---

## 2. Evidence inspected

All inspection was read-only. Notebook cells were read as JSON source; no cell was executed.

| Evidence | Status |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `README.md`, `requirements.txt` | Inspected |
| `docs/README.md`, `docs/MIGRATION_LOG.md` | Inspected |
| `docs/00_project_contract/challenge_brief.md`, `submission_checklist.md` | Inspected |
| `docs/01_project_planning/project_execution_plan_v1.md` (untracked), `project_execution_plan_v2_context_efficient.md` (tracked) | Inspected |
| `docs/03_eda/experiment_notes.md` | Inspected |
| `docs/04_research/` — all 8 files (pdf audit, key findings, 6 research notes) | Inspected |
| `docs/05_methodology/` — all 4 files | Inspected |
| `notebooks/01_baseline_reproduction.ipynb` (tracked) | Source cells inspected, not executed |
| `notebooks/02_eda_and_data_contract.ipynb` (tracked) | Structure inspected |
| `notebooks/03_validation_harness_phase6.ipynb` (untracked) | Source cells and stored outputs inspected, not executed |
| `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md` | Inspected in full |
| `outputs/reports/phase6_rf_sanity_baseline_v1_experiment_log_candidate.csv` | Header + row inspected |
| `outputs/validation/phase6_rf_sanity_baseline_v1_slice_report.csv` | Header + sample rows inspected |
| `outputs/oof/phase6_rf_sanity_baseline_v1_oof_predictions.csv` | Header inspected (`Id, fold, y_true, y_pred_proba`) |
| `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` | Header inspected (`Id, fold`) |
| `logs/experiment_log.csv` | Full content inspected (header + 1 row) |
| `.claude/skills/` (21 skills), `.claude/agents/` (10 agents) | Listed |
| Git state: `git status --short`, `git log --oneline -10`, `git diff --check` | Run |

Missing files: none of the listed evidence files were missing. `docs/project_execution_plan.md` is referenced in `docs/README.md` as previously deleted — `Not confirmed yet` what it contained; it is not recoverable from the working tree.

PDFs, books, slides, and papers were **not** parsed, per project reading policy. Research evidence was used only through `docs/04_research/` summaries.

---

## 3. Current project state

### 3.1 Completed and committed

| Item | Evidence | Label |
|---|---|---|
| Project contract (target `Drafted`, ID `Id`, positive class 1, ROC-AUC on probabilities, 696-row submission) | `docs/00_project_contract/challenge_brief.md` | Confirmed fact |
| Phase 2 baseline reproduced: RF(100, depth 5, seed 2025), CV 0.812964 ± 0.025740, public LB 0.80792 | `notebooks/01_baseline_reproduction.ipynb`, `logs/experiment_log.csv`, commits `e28c8a5` (*Reproduce official baseline locally*) and `e9deb7c` (*Record baseline public leaderboard score*) | Repository evidence |
| Phase 3 EDA + data contract: train (2781,16), test (696,15), contract checks pass, 4 signal families hypothesized | `docs/03_eda/experiment_notes.md` (committed by `39948d1` at its pre-reorganization path `docs/experiment_notes.md`, moved to `03_eda/` by `8305950`), `notebooks/02_eda_and_data_contract.ipynb` | Repository evidence |
| Phase 4A/4B research synthesis: 8 tracked research docs; PDF audit 34 detected / 26 reviewed / 0 failed | `docs/04_research/*`, `docs/MIGRATION_LOG.md`, commit `8305950` | Repository evidence |
| Phase 5 methodology freeze: ~17 frozen decisions including StratifiedKFold(5, shuffle, seed 42), score-input policy, class-index verification, LB-as-sanity-only, Phase 6 submission block, first-baseline column exclusions | `docs/05_methodology/phase5_execution_decisions.md`, commit `35852e9` (HEAD) | Repository evidence |

> Full commit history (`git log --oneline`): `35852e9`, `8305950`, `39948d1`, `e9deb7c`, `e28c8a5`, `e6eabbf`, `5d01461`.

### 3.2 Implemented but uncommitted

| Item | Evidence | Label |
|---|---|---|
| Phase 6 validation harness notebook, executed with stored outputs | `notebooks/03_validation_harness_phase6.ipynb` (untracked, `??` in `git status`) | Repository evidence |
| All five Phase 6 artifacts (folds, OOF, slice report, validation report, log candidate) under `experiment_id = phase6_rf_sanity_baseline_v1` | `outputs/folds/`, `outputs/oof/`, `outputs/validation/`, `outputs/reports/` (all untracked) | Repository evidence |
| `CLAUDE.md` and `.claude/` (project instructions, 21 skills, 10 agents) | untracked per `git status --short` | Repository evidence |
| `docs/01_project_planning/project_execution_plan_v1.md` | untracked | Repository evidence |
| Two EDA draft notebooks (`*_before_refactor`, `*_before_interpretive_integration`) | untracked | Repository evidence |

`Risk` — The Phase 6 result is not anchored to any commit. The log candidate's `git_commit_or_status` field literally says `review_git_status_for_exact_state`, i.e., traceability was deferred. If the notebook is edited before commit, the artifacts and the code that produced them can silently diverge.

### 3.3 Documented but not implemented

| Item | Evidence | Label |
|---|---|---|
| Experiment log v2 schema (23 columns) — proposed, migration explicitly deferred pending separate approval | `docs/05_methodology/phase5_execution_decisions.md` | Repository evidence / Blocked by gate |
| Phase 7 feature blocks (Blocks 0–6), fixed-fold ablation method | `docs/04_research/research_notes_feature_engineering.md` | Blocked by gate |
| Phase 8 model-family comparison protocol | `docs/04_research/research_notes_tabular_models.md` | Blocked by gate |
| Phase 10 HPO gates (7 activation conditions) | `docs/04_research/research_notes_hpo.md` | Blocked by gate |
| Phase 11 submission process beyond the Phase 2 baseline | `docs/00_project_contract/submission_checklist.md` | Blocked by gate |
| Phase 6A audit (mentioned as possible future audit in `CLAUDE.md`) | `CLAUDE.md` ("A future Phase 6A audit may compare Phase 2 vs Phase 6 under controlled conditions, but do not run it unless explicitly asked.") | Blocked by gate — design only in this document set |

### 3.4 Ambiguous or not confirmed

| Item | Status | Evidence |
|---|---|---|
| Phase 1 as a distinct documented phase | Not confirmed yet — commits `5d01461`/`e6eabbf` suggest setup work, no Phase-1 deliverable doc exists | `git log`, absence of phase-1 doc |
| Phase 6 acceptance | Not accepted. `CLAUDE.md`: "Phase 6 is ready for manual review, not automatically closed." No acceptance record exists anywhere | `CLAUDE.md`, absence of acceptance artifact |
| Unit of observation (row independence; could the same athlete appear in multiple Years?) | Not confirmed yet — explicitly flagged in Phase 5 and repeated in the Phase 6 report | `docs/05_methodology/phase5_execution_decisions.md`, validation report |
| Need for grouped CV | Open decision, conditional on unit-of-observation evidence | same |
| Minimum slice size; quantitative ablation threshold | Not confirmed yet — blocked on a credible Phase 6/6A anchor | same |
| Final School encoding | Open decision, deferred to Phase 7 staged ablation | `docs/05_methodology/leakage_checklist_phase6.md` |
| Status of `notebooks/outputs/submissions/` (empty stray nested directory) | Not confirmed yet — probably a path artifact from an early run; harmless but untracked; do not delete without approval | directory listing |

---

## 4. Critical findings

### 4.1 Strengths

1. `Repository evidence` — **Class-index verification is frozen policy and actually implemented.** Phase 6 extracts positive-class probabilities via `estimator.classes_` lookup with loud failure (`get_positive_class_proba` in `notebooks/03_validation_harness_phase6.ipynb`). This is a discipline most competition workflows skip.
2. `Repository evidence` — **Leakage rules are executable, not aspirational.** `docs/05_methodology/leakage_checklist_phase6.md` maps each transformation to Allowed/Conditional/Blocked with a phase, and the Phase 6 report verifies them item by item.
3. `Repository evidence` — **Artifact governance was followed exactly as designed**: the `{experiment_id}_*` naming convention defined in Phase 5 matches the actual Phase 6 artifacts byte-for-name.
4. `Repository evidence` — **Main log protection worked.** Phase 6 wrote a candidate row to `outputs/reports/` and left `logs/experiment_log.csv` untouched (verified: file is tracked, no diff, 1 row).
5. `Repository evidence` — **Diagnostic/feature separation enforced.** `Age_missing`, `physical_missing_count`, `available_measurement_count`, `measurement_completeness_group`, `frequent_vs_rare_school_group` never entered the feature matrix; the report records this explicitly.
6. `Inference` — The documentation chain (contract → EDA → research → methodology → harness) has genuine internal referential integrity: Phase 5 cites Phase 3/4 evidence per decision; Phase 6 implements Phase 5 verbatim.

### 4.2 Weaknesses

1. `Risk` — **Phase 6 work is entirely untracked** (notebook + all artifacts). One careless `git clean`, branch switch with conflicts, or disk issue destroys the only copy of the project's most advanced implementation. The artifacts also cannot be tied to the code version that produced them.
2. `Risk` — **The Phase 2 baseline contains preprocessing leakage by design.** Mean imputation and LabelEncoder are fitted on the full training set *before* CV (`notebooks/01_baseline_reproduction.ipynb`, cells 5–6). This is acceptable as faithful official-baseline reproduction, but its CV score 0.812964 is leakage-inflated to an unknown degree and **must not serve as the Phase 7 comparison anchor**.
3. `Risk` — **No quantitative anchor exists for Phase 7 decisions.** The frozen plan requires ablation thresholds "after first frozen-fold baseline," but the project now has two baselines that disagree by ~0.084 on fold means (~0.086 on OOF) with no decomposition of why.
4. `Inference` — Phase 2 uses `predict_proba(X)[:, 1]` without `classes_` verification (cell 8). It happens to be correct here, but it predates and violates the later-frozen class-index policy. Historical note only; do not retrofit the committed notebook.
5. `Risk` — **Submission and figure artifacts are gitignored** (`outputs/submissions/*.csv`, `outputs/figures/*` in `.gitignore`), and no checksums are recorded anywhere. For Phase 11, a submitted file would be unverifiable after the fact. (Recommendation: future reports must record SHA-256 of submission files; see Plan v3 §5.)
6. `Inference` — The Phase 6 OOF AUC (0.726616) is slightly below the fold-mean (0.729253) — normal and unconcerning, but worth noting that OOF, not fold-mean, should be the canonical single-number anchor going forward because it is computed on one consistent prediction vector.

### 4.3 Inconsistencies

1. `Repository evidence` — **`docs/README.md` is stale.** It lists only `phase5_methodology_plan.md` under Phase 5, omits `phase5_execution_decisions.md`, `validation_protocol_phase6.md`, `leakage_checklist_phase6.md`, and still says "The next recommended step is Phase 5 in Plan Mode." `CLAUDE.md` documents this caveat and forbids fixing it without an explicit request. **Not fixed here, per instruction.**
2. `Repository evidence` — **Two execution plans coexist** (`v1` untracked, `v2` tracked) with overlapping scope and no statement of which is authoritative. Plan v3 (created alongside this review) explicitly supersedes both; v1/v2 become historical references.
3. `Inference` — `CLAUDE.md` phase-status block says "Phase 0: Documented / effectively closed by later progress" while `challenge_brief.md` requires explicit approval for Phase 1 that was never recorded. Practically moot (the project advanced), but it means **phase closure was never an explicit recorded event for any phase** — closures are inferred from later work existing. Plan v3 introduces explicit acceptance records to stop this pattern.
4. `Repository evidence` — The log candidate row's `notebook_or_script` field uses a Windows backslash path (`notebooks\03_validation_harness_phase6.ipynb`) while every doc uses forward slashes. Trivial, but a normalization rule belongs in the artifact contract (Plan v3 §5).

### 4.4 Leakage risks

1. `Confirmed fact` — Phase 2: global (pre-CV) mean imputation and global LabelEncoder fit. Leakage class: *preprocessing leakage* / *imputation leakage* / *encoding leakage* per the project taxonomy (`docs/04_research/research_notes_leakage.md`). Contained: it is documented, flagged in the log (`risk_flags` includes `train_mean_imputation; label_encoding`), and quarantined as reproduction-only.
2. `Repository evidence` — Phase 6: no leakage found. Preprocessing is inside a `Pipeline`/`ColumnTransformer` fitted per fold; test data used only for contract checks; School excluded; diagnostics segregated.
3. `Risk` (forward-looking) — **Unit-of-observation leakage.** If the same athlete appears in multiple `Year` rows, StratifiedKFold can place the same athlete in train and validation folds. The data has no name column, so this is hard to verify directly; near-duplicate physical profiles across adjacent years would be the only observable signature. Status: `Open decision`, flagged since Phase 5, never probed. A bounded, diagnostic-only near-duplicate scan is a legitimate Phase 6A/7-entry check (design only; `Blocked by gate` for execution until approved).
4. `Risk` (forward-looking) — **Phase 7 rare-grouping and role-statistics leakage** are the most likely future failure points: thresholds (e.g., "rare if count < 5") and role means must be learned inside folds, and it is easy to compute them once globally "just for speed." The Phase 6 diagnostic threshold (`frequent_vs_rare_school_group`, rare < 5 train rows) was computed globally — acceptable because it is diagnostic-only, but the same code pattern copied into feature engineering would be leakage. This exact trap should be named in the Phase 7 prompt template (Plan v3 §20).
5. `Risk` (forward-looking) — **Ablation-selection leakage**: repeatedly evaluating feature blocks on the same 5 frozen folds and keeping the winners is implicit selection on the validation data. Mitigations belong in Phase 7/9 design (fixed candidate list declared before running; secondary confirmation via repeated CV with different seeds at consolidation time — Phase 9).

### 4.5 Validation risks

1. `Inference` — StratifiedKFold(5, shuffle, 42) is appropriate for n=2781, positive rate ~0.648, absent grouping evidence. The fold-AUC std (0.0306) is large relative to plausible feature-block effects, which means **single-run fold-mean differences smaller than ~0.01–0.015 are not credibly distinguishable from noise**. The quantitative ablation threshold must be set with this in mind (Open decision, Phase 6A output).
2. `Inference` — Year-as-diagnostic-only remains appropriate: 11 Year slices were computed and no official temporal split requirement exists. Re-evaluate only if Year slices show monotone degradation (not assessed here — would require reading slice values; deferred to Phase 6 manual review).
3. `Repository evidence` — Slice diagnostics are well defined (7 dimensions, all `computed`). Gap: **no minimum-n policy for slices** — tiny slices will produce noisy AUCs that invite overinterpretation. Plan v3 sets a reporting rule (report n alongside AUC; flag slices with n below a threshold to be fixed in Phase 6A from observed variance).
4. `Risk` — Public LB 0.80792 vs Phase 2 CV 0.812964 (difference −0.005) will tempt the conclusion "global preprocessing didn't hurt, keep Phase 2's pipeline." That reasoning is leaderboard-informed pipeline selection — exactly what the frozen policy forbids. The reconciliation must be decided on internal evidence only.

### 4.6 Traceability risks

1. `Risk` — Untracked Phase 6 notebook/artifacts (see 4.2.1).
2. `Risk` — `git_commit_or_status = review_git_status_for_exact_state` in the log candidate: the run is not pinned to a commit.
3. `Risk` — Gitignored submissions with no recorded checksums (see 4.2.5).
4. `Risk` — Environment versions are not recorded in any report (`requirements.txt` is unpinned: no version specifiers). Scikit-learn version changes can change RandomForest results. Recommendation: future validation reports record `python -V` and key package versions; pinning `requirements.txt` is a separate `Human decision required` (file is outside this task's allowed edits).
5. `Repository evidence` — `Libros/`, `Prompts/`, `Recapitulaciones/`, `competition.zip`, `Contexto.zip`, `Libros.zip` sit in the repo root; the zips are gitignored, the folders untracked-but-not-ignored. They are reference material that `git status` noise will permanently include. Governance decision (ignore vs. relocate) is `Human decision required` and out of scope here.

### 4.7 Automation risks

1. `Risk` — **Over-trusting self-reported checklists.** The Phase 6 leakage checklist is computed by the same notebook it audits. It is good evidence, not independent verification. Future automation should keep *generation* and *verification* in separate steps (separate prompt/agent, reading artifacts only).
2. `Risk` — **Gate erosion via helpful automation.** Several installed skills (`mle-workflow`, `verification-loop`, `eval-harness`) are designed to *run* things. Used naively they would execute notebooks or training, violating current gates. Skills must never override `CLAUDE.md` gates; Plan v3 §19 assigns each skill/agent a phase and a permission boundary.
3. `Risk` — **Artifact overwrite by re-run.** The Phase 6 notebook writes fixed `phase6_rf_sanity_baseline_v1_*` paths; re-running it overwrites artifacts in place with no run history. Acceptable for a sanity baseline; not acceptable from Phase 6A onward (Plan v3 mandates new `experiment_id` per variant/run).
4. `Risk` — **Log schema drift**: the candidate row uses the v2 schema while the main log is legacy. If a future automated step appends v2 rows to the legacy CSV, the log corrupts. Migration remains `Blocked by gate` (separate approval), and Plan v3 makes "schema check before any log write" a hard rule.

### 4.8 Hidden opportunities

1. `Opportunity` / `Automation candidate` — The Phase 6 harness is ~90% of a **reusable evaluation engine**: parametrize (feature matrix builder, preprocessing spec, model, experiment_id) and every Phase 6A/7/8 run becomes a config, not new code. This is the single highest-leverage refactor available, and it can be designed now and implemented as the Phase 6A notebook.
2. `Opportunity` — The fold assignment file (`outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`) can become the **canonical frozen folds** for all future experiments (load, never recompute), making every comparison paired at the row level and enabling paired statistics on OOF vectors instead of fold-mean eyeballing.
3. `Opportunity` — OOF prediction files per experiment enable **paired comparisons** (e.g., per-fold deltas, McNemar-style or rank-based checks) which are far more sensitive than comparing two fold-means under std ~0.03. Cheap, leakage-free, and unused so far.
4. `Opportunity` — Phase 3 found `Age_missing` strongly target-associated and measurement availability structured by role (`docs/03_eda/experiment_notes.md`). These row-wise, parameter-free features are leakage-trivial and are the natural Block 1 — high information, low risk.
5. `Opportunity` — A short, versioned **acceptance record** convention (`docs/06_validation/phase6_acceptance.md` etc., one page: what was reviewed, what was accepted, what remains open) closes the "phases are never explicitly closed" pattern at near-zero cost.
6. `Opportunity` / `Automation candidate` — A read-only **pre-commit audit prompt** (verify only intended files staged; forbidden paths untouched; artifacts named per contract) would mechanize the Hard Git rules in `CLAUDE.md`.

---

## 5. Baseline reconciliation analysis

### 5.1 Phase 2 vs Phase 6 differences

`Repository evidence` — extracted from notebook source (not executed):

| Factor | Phase 2 (`01_baseline_reproduction.ipynb`) | Phase 6 (`03_validation_harness_phase6.ipynb`) |
|---|---|---|
| Feature columns | Year, Age, Height, Weight, 6 physical tests, Player_Type, Position_Type, Position, **BMI** (14) | Year, Age, Height, Weight, 6 physical tests, Player_Type, Position_Type, Position (13; **no BMI**) |
| BMI | Included (`Weight / Height**2`, official baseline feature) | Excluded |
| Numeric imputation | **Mean**, fitted on **full train before CV** (and applied to test) | **Median**, fitted **inside each training fold** |
| Imputed columns | Age + 6 physical tests (Height/Weight/Year not imputed) | All numeric features via SimpleImputer(median) |
| Categorical encoding | **LabelEncoder** (ordinal integers), fitted on **full train before CV** | **OneHotEncoder**(handle_unknown="ignore"), fitted **inside each fold** (after most_frequent imputation) |
| Model | RandomForestClassifier(100, depth 5, **random_state=2025**) | RandomForestClassifier(100, depth 5, **random_state=42**, n_jobs=-1) |
| Fold splitter | StratifiedKFold(5, shuffle, 42) | StratifiedKFold(5, shuffle, 42) — **same** |
| Probability extraction | `predict_proba[:, 1]` unverified | `classes_`-verified |
| Score | CV mean 0.812964 ± 0.025740 | fold mean 0.729253 ± 0.030629; OOF 0.726616 |

The splitter is identical, so fold membership should match; everything else about the pipeline differs in five confounded factors: (a) fit scope (global vs in-fold), (b) imputation statistic (mean vs median), (c) categorical representation (ordinal vs one-hot), (d) BMI presence, (e) model seed.

### 5.2 Likely causes of metric gap

All of the following are `Inference` (hypotheses to be tested in Phase 6A, not conclusions):

1. **Categorical representation × shallow trees** — plausibly the largest contributor. With `max_depth=5`, ordinal-encoded `Position` lets a single split partition many positions at once; one-hot encoding spreads the same information over many binary columns, consuming the depth budget and diluting per-tree feature sampling. Direction: would lower Phase 6 relative to Phase 2.
2. **BMI presence** — an informative engineered ratio absent from Phase 6. Direction: lowers Phase 6.
3. **Global-fit imputation/encoding leakage** — validation-fold rows influence Phase 2's imputation means and encoder fit, inflating Phase 2's CV optimistically. Magnitude unknown; the small CV-vs-LB gap (0.813 → 0.808) *suggests* modest inflation but is not decisive evidence (different data subset) and must not drive decisions.
4. **Mean vs median imputation** — second-order; physical-test distributions are skewed, so the statistic changes imputed values materially for high-missingness columns, but effect direction on AUC is unclear.
5. **Model seed (2025 vs 42)** — pure noise term; with 100 trees, expected effect well under one fold-std. Needs one cheap variant to confirm and dismiss.

No single factor can be attributed without controlled isolation. That is precisely what Phase 6A is for.

### 5.3 Whether Phase 6A is needed

`Recommendation` — **Yes, mandatory before Phase 7.** Reasons:

1. The Phase 7 ablation threshold (frozen plan requirement, currently `Not confirmed yet`) cannot be set without one credible anchor.
2. Without decomposition, every Phase 7 result invites the wrong question ("why are we still below 0.81?") and pressure to silently re-adopt the leaky Phase 2 pipeline.
3. The encoding question (ordinal vs one-hot for role categoricals under tree models) is a **pipeline** decision, not a feature decision, and must be settled before feature ablations or every block result is conditional on an unsettled pipeline.
4. It is cheap: same harness, same frozen folds, a handful of single-factor variants.

`CLAUDE.md` already anticipates this: "A future Phase 6A audit may compare Phase 2 vs Phase 6 under controlled conditions, but do not run it unless explicitly asked." Execution remains `Blocked by gate` / `Human decision required`; the plan is designed in `docs/01_project_planning/phase6a_baseline_reconciliation_plan.md`.

### 5.4 What must remain forbidden before Phase 7

`Blocked by gate` — during Phase 6 review and Phase 6A:

- No submissions; no public-leaderboard feedback of any kind.
- No HPO, no Optuna, no Grid/RandomizedSearchCV.
- No model families beyond the fixed RandomForestClassifier(100, depth 5) reference.
- No new features beyond the BMI diagnostic variant explicitly defined in the Phase 6A plan; no Block 1+ features.
- No School in any feature matrix.
- No modification of `logs/experiment_log.csv`, `data/input/`, `notebooks/_official/`, `outputs/submissions/`.
- No re-tuning of fold structure, seeds, or n_splits to make numbers look better.
- No adoption of any Phase 6A variant as "the model" — Phase 6A produces an *anchor and a pipeline policy decision*, nothing else.

---

## 6. Gate review

| Gate | Current status | Evidence | Can proceed? | Blocking issue |
|---|---|---|---|---|
| Phase 0 → 1 (contract documented) | Satisfied in substance; never explicitly approved | `docs/00_project_contract/*` exist; later phases proceeded | Moot | Closure-by-inference pattern (see 4.3.3) |
| Phase 2 closure (baseline reproduced + LB recorded) | Satisfied | committed notebook, log row, LB 0.80792 | Yes (closed) | — |
| Phase 3 closure (EDA + contract) | Satisfied | committed notebook, `experiment_notes.md`, commit `39948d1` | Yes (closed) | — |
| Phase 4 closure (research synthesis) | Satisfied in substance | 8 committed docs treated as Phase 5 inputs | Yes (effectively closed) | No explicit closure record |
| Phase 5 closure (methodology frozen) | Satisfied | commit `35852e9` (HEAD) | Yes (closed) | — |
| Phase 6 acceptance | **Open** — implemented, self-checked, awaiting manual review | untracked notebook + artifacts; `CLAUDE.md` status block | **No — human review required** | Untracked work; no acceptance record; review checklist undefined until Plan v3 §8 |
| Phase 6A entry | Design ready (this document set); execution not authorized | `phase6a_baseline_reconciliation_plan.md` | **No — requires explicit human authorization** after Phase 6 review | Human decision required |
| Phase 7 entry | Blocked | Phase 5 transition policy: "Phase 6 harness tested... baseline reproducible under frozen folds" | **No** | Phase 6 not accepted; no anchor; ablation threshold unset; Phase 6A not run |
| Phase 8 entry | Blocked | tabular-models guardrails | No | Phase 7 not started |
| Phase 10 entry (HPO) | Blocked — 7 activation conditions, ~2 of 7 plausibly met (validation protocol frozen; no LB dependence) | `research_notes_hpo.md` | No | feature blocks untested; no candidate models; log v2 not active |
| Phase 11 entry (submissions) | Blocked | Phase 5 transition policy | No | everything upstream |
| Log v2 migration | Blocked — separate approval required | `phase5_execution_decisions.md` | No | Human decision required |

---

## 7. Open decisions

| Decision | Current status | Evidence | Why it matters |
|---|---|---|---|
| Phase 6 acceptance (and committing the Phase 6 notebook + artifacts) | Pending human review | `CLAUDE.md`; untracked files | Unanchored results; everything downstream depends on it |
| Authorize Phase 6A execution | Pending — design exists, execution blocked | `phase6a_baseline_reconciliation_plan.md` | Without it, Phase 7 results uninterpretable |
| Canonical anchor metric (recommend: OOF ROC-AUC on frozen folds) | Proposed in Plan v3, needs ratification | this review §4.2.6 | Single comparable number across all future experiments |
| Unit of observation / athlete duplication across Years | Not confirmed yet; never probed | Phase 5 + Phase 6 report | Possible identity leakage across folds; affects grouped-CV decision |
| Grouped CV activation | Conditional, dormant | `phase5_execution_decisions.md` | Only matters if duplication is found |
| Quantitative ablation threshold for Phase 7 | Not confirmed yet — to be derived from Phase 6A variance evidence | same | Prevents noise-chasing in Phase 7 |
| Minimum slice size for diagnostics | Not confirmed yet | same | Prevents overreading tiny-slice AUCs |
| Categorical encoding policy for tree models (ordinal vs one-hot) | Unsettled — the hidden pipeline decision inside the baseline gap | §5.2.1 | Must be fixed before Phase 7 or all blocks are confounded |
| BMI adoption as a Block 0 feature | Open — currently a diagnostic variant only | Phase 6A plan §4 | Row-wise and parameter-free (leakage-trivial) but adoption is a feature decision belonging to Phase 7 Block 0, with human approval |
| Experiment log v2 migration | Deferred, separate approval | `phase5_execution_decisions.md` | Schema drift risk if mishandled |
| Repo hygiene: `Libros/`, `Prompts/`, `Recapitulaciones/`, zips, stray `notebooks/outputs/` | Untouched per rules | `CLAUDE.md` forbidden paths | Permanent `git status` noise; human call |
| `requirements.txt` version pinning | Not pinned | file content | Reproducibility across environments; outside allowed edits here |

---

## 8. Automation-readiness assessment

### 8.1 Safe to automate now

`Automation candidate` (all read-only or doc-producing):

- Repository state audits (git status/log checks, forbidden-path verification, artifact-naming conformance checks).
- Documentation consistency checks (docs vs notebooks vs artifacts cross-referencing).
- Generation of phase prompts from the templates in Plan v3 §20.
- Leakage-checklist rendering as a reusable per-experiment template (text artifact).
- Acceptance-record drafting (human signs; Claude drafts).

### 8.2 Unsafe to automate now

- Anything that executes notebooks or trains models (gates).
- Any write under `outputs/`, `logs/`, `data/`, `notebooks/` (gates).
- Log v2 migration (separate approval).
- Git staging/committing (Hard Git rules: explicit user request only).
- Phase transitions (each requires recorded human acceptance).
- "Fixing" stale docs (`docs/README.md`) — explicitly forbidden without request.

### 8.3 Human approval required

1. Phase 6 acceptance after manual review (and the decision to commit the Phase 6 notebook + which artifacts).
2. Phase 6A authorization, variant list ratification, and BMI-diagnostic inclusion.
3. Anchor metric and ablation threshold ratification (from Phase 6A evidence).
4. Encoding policy decision (from Phase 6A evidence).
5. Log v2 migration plan.
6. Any model-family, HPO, or submission gate opening — every one, individually.

### 8.4 Suggested future automation controls

- **Two-role rule**: the agent/notebook that generates an experiment never performs its acceptance audit; a separate read-only review pass does.
- **Config-over-code**: one parametrized harness (from the Phase 6 notebook), experiments defined as declarative variant specs; eliminates copy-paste leakage bugs.
- **Frozen-folds-as-file**: all future runs load `phase6_rf_sanity_baseline_v1_fold_assignments.csv` (or its committed successor) and assert fold integrity (row count, per-fold class counts) before training.
- **Pre-write guards**: before any artifact write, assert the target path matches `{experiment_id}_*` and does not already exist; before any log write, assert schema match.
- **Stop conditions everywhere**: every future prompt ends with explicit stop conditions and a "report, don't fix" rule for surprises (Plan v3 §8, §18.9).

---

## 9. Final diagnosis

The project is healthy, disciplined, and gated — and is currently standing on an unaccepted, uncommitted Phase 6 plus an unexplained ~0.08–0.09 baseline gap that would poison Phase 7 interpretation if ignored.

**Decision: Proceed to Phase 6 manual review.**

Immediately after Phase 6 acceptance, **Phase 6A (Baseline Reconciliation Audit) must run before Phase 7** — it should be treated as mandatory, not optional (`Recommendation`; execution remains `Blocked by gate` until a human explicitly authorizes it). Do not start Phase 7, Phase 8, Phase 10, or Phase 11 under any circumstances until Phase 6 is accepted, Phase 6A is closed, the anchor metric is ratified, and the ablation threshold is set from observed variance.
