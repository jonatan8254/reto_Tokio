# Final Package Structure Blueprint — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY. Nothing in this run is built, trained, refit, tuned, submitted, committed, staged, or pushed. No model is run, no historical artifact is created or modified, no submission is generated or uploaded, and `logs/experiment_log.csv` is untouched. This document specifies the structure of a future portable package; it does not produce it. The construction step is deferred and governed by a separate build specification (`prompt_build_final_portable_package.md`).**

---

## 1. Purpose and scope

This blueprint fixes the exact, minimal, portable folder that a later build run will assemble for the final deliverable of the project:

```text
Reto Tokio / GCI World NFL Draft Prediction
```

The deliverable is a self-contained package built around a single comprehensive notebook that loads the official data, reproduces the leakage-safe validation, refits the selected candidate(s) on full train, generates a format-compliant submission, and documents the methodology. The package must be runnable from a clean kernel, must respect data governance, and must read as a professional technical data-science project with no reference to internal build tooling.

This document decides:

- the exact base tree and a per-item table;
- which historical artifacts (if any) are copied in;
- an explicit exclude list;
- `data/` vs `data/input/`;
- handling of both data-governance scenarios A and B;
- whether at most one optional extra file is justified.

Everything concrete below is grounded in the ground-truth and evidence digest. Items not established there are marked **Not confirmed yet**.

---

## 2. Base tree (canonical)

The portable folder is named `final_integrated_notebook_package/`. The canonical base tree is:

```text
final_integrated_notebook_package/
|- README.md
|- requirements.txt
|- references.md
|- 99_final_integrated_project_report.ipynb
|- data/            (train.csv, test.csv, sample_submission.csv)
|- outputs/
```

Design principle: **if a need can be met inside the README or the notebook, no separate file is added.** The package is intentionally five top-level entries plus two directories. The notebook carries the analytical weight; the README carries operating instructions and the results summary; `references.md` carries the bibliography and the single permitted generative-AI disclosure.

---

## 3. Per-item specification

The table below specifies every path in the package. "Include in ZIP?" reflects Scenario A (private/course package); Scenario B differences are addressed in Section 6.

| Path | Purpose | Required? | Include in ZIP? | Notes |
|---|---|---|---|---|
| `README.md` | Project charter, challenge summary, ROC-AUC metric, data governance, F2 feature overview, run instructions, results summary table, reproducibility statement, author attribution | Yes | Yes | Single source of operating instructions. Must not name any internal build tooling. Author: Jonatan Estiven Sanchez Vargas, Universidad Nacional de Colombia, Systems and Computer Engineering. |
| `requirements.txt` | Pinned/declared runtime dependencies for the notebook | Yes | Yes | Core: numpy, pandas, scikit-learn (versions from base `.venv`: numpy 2.4.6, pandas 3.0.3, scikit-learn 1.9.0, Python 3.13.13). CatBoost is optional and best declared as an extras note, since it ran in a separate environment (catboost 1.2.10), not the base `.venv`. |
| `references.md` | Bibliography (cite the real reference library, do not ship the PDFs) plus the generative-AI assistance disclosure subsection | Yes | Yes | Sources cited only from the confirmed `references/` library (Section 7). ChatGPT disclosure is sober, auxiliary, and confined to its own subsection. |
| `99_final_integrated_project_report.ipynb` | The comprehensive deliverable notebook: data contract, frozen validation, F2 pipeline, model evidence, OOF reporting, full-train refit, test inference, submission generation and validation, slice diagnostics, references | Yes | Yes | Carries the full analytical narrative. Runs top-to-bottom from a clean kernel; relative paths; fixed seed 42; verifies `estimator.classes_` before extracting the positive-class probability. |
| `data/train.csv` | Official training data, 2781 rows x 16 cols (incl. Drafted, School, Id) | Conditional | Yes (Scenario A) / No (Scenario B) | Official competition file. Not modified. Excluded under Scenario B; replaced by placeholder + instructions. |
| `data/test.csv` | Official test data, 696 rows x 15 cols (no Drafted) | Conditional | Yes (Scenario A) / No (Scenario B) | Official competition file. Drives the 696-row submission and Id order. |
| `data/sample_submission.csv` | Submission template, 696 rows x 2 cols [Id, Drafted] | Conditional | Yes (Scenario A) / No (Scenario B) | Defines required submission schema and Id order. |
| `outputs/` | Empty target directory for artifacts generated at runtime (the validated submission and any runtime reports) | Yes (as empty dir) | Yes (empty) | Created empty; populated only when the notebook runs. Preserve the directory in the ZIP via a `.gitkeep` placeholder. No historical artifacts copied in (see Section 4). |

Notebook content guidance (so no extra files are needed):

- **Final results are recorded as a Markdown table inside the notebook**, not shipped as a CSV. This keeps the package minimal while preserving the comparison the reader needs.
- The notebook embeds the accepted OOF ROC-AUC figures (Section 5) as recorded context, because the minimal package will not recompute every historical variant. Figures that can be recomputed from the official CSVs (the M1 baseline OOF, fold-level metrics) are computed live; figures that depend on the separate CatBoost environment are presented as recorded results with their configuration.

---

## 4. Historical artifacts: copy NONE into the portable folder

**Decision: copy no historical artifact into `final_integrated_notebook_package/`. The package ships empty `outputs/` and regenerates what it needs from the official CSVs.**

Justification:

1. **Reproducibility over transcription.** The portable notebook reconstructs the frozen validation deterministically: `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`. The frozen fold file (`outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, SHA256[:16] `96937649526bcadb`, 2781 rows, folds 0..4) is reproducible in-memory from the same seed and splitter, so shipping it adds a stale dependency without adding capability. The notebook may assert integrity (2781 rows, folds 0..4) against the regenerated assignments rather than against a copied file.
2. **The historical OOF and validation CSVs are diagnostic traces, not deliverables.** The accepted OOF ROC-AUC values are recorded in the notebook narrative (Section 5); the per-variant OOF files from Phases 6-10 are not required to produce or validate the final submission.
3. **The existing Phase 11 submissions are gitignored and identified by SHA-256, not by being shipped.** The two validated submissions already exist on disk and must not be modified. The portable package regenerates a submission from code; it does not bundle prior submission CSVs.
4. **Minimalism.** Every copied artifact would need provenance, a freshness contract, and an exclusion rationale. Shipping none removes that burden entirely.

The only tolerated near-exception, **left unselected by default**: if a future build decision requires byte-identical folds rather than seed-reproducible folds, a single small file (`phase6_rf_sanity_baseline_v1_fold_assignments.csv`) could be placed under `outputs/folds/`. This is **not adopted here**; the package regenerates folds from seed 42. Record the choice explicitly in the build run if it changes.

---

## 5. Recorded results to embed in the notebook (not shipped as files)

These accepted figures are embedded as a Markdown results table in the notebook. They are grounded in the evidence digest and must not be altered.

| Model | OOF ROC-AUC | Delta vs M0 | Same-sign folds vs M0 | Role |
|---|---:|---:|---:|---|
| M0 RandomForest (frozen) | 0.8116502602456482 | 0.0 | anchor | Reference anchor |
| M1 LogisticRegression (baseline) | 0.8270821069632867 | +0.0154318 | 4/5 | Fallback / reference candidate |
| CatBoost (baseline) | 0.8202943968641223 | +0.0086441 | 4/5 | Secondary observe |
| XGBoost | 0.8113477083751576 | -0.0003026 | 1/5 | Dropped |
| LightGBM | 0.8062204891415921 | -0.0054298 | 1/5 | Dropped |
| M1 (tuned) | 0.8274819177762125 | +0.0158317 | 4/5 | Rejected (noise-level vs M1 base) |
| CatBoost (tuned) | 0.8303208581017550 | +0.0186706 | 5/5 | Best global OOF; warning-heavy; primary candidate |

Supporting facts to record in the notebook:

- Target = `Drafted` (1 = drafted); metric = ROC-AUC on positive-class probability; train positive rate 0.6483279396 (978 negatives, 1803 positives).
- F2 feature set (21 features, frozen): base 13 (Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type, Position_Type, Position) + 7 missingness flags (Age_missing, Sprint_40yd_missing, Vertical_Jump_missing, Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing, Shuttle_missing) + available_measurement_count. School excluded as a feature.
- Preprocessing: median imputation + one-hot encoding fitted inside training folds during CV, on full train for the final refit; test is transform-only.
- Pre-registered promotion bar: delta >= 0.005436 AND same-sign positive folds >= 4/5 AND slice guard clear.
- CatBoost tuned config: depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]. CatBoost ran in a separate environment (catboost 1.2.10); the base `.venv` was untouched.
- Two validated submissions already exist (Phase 11, run_id `phase11_option_c_20260619_0001`), both 696 rows, header [Id, Drafted], no winner declared, not uploaded:
  - CatBoost tuned submission SHA-256 `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8`
  - M1 baseline submission SHA-256 `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640`
- No final winner is declared. The submission row count must be exactly 696; Id order matches `sample_submission.csv`. Public leaderboard is sanity-check only and never drives selection.

**Not confirmed yet:** the exact M1 baseline configuration (C, penalty, solver, scaling). The build run must recover this from the Phase 8 artifacts and must not invent it. Until recovered, the notebook records the M1 config as **Not confirmed yet**.

---

## 6. Data governance: Scenarios A and B

The package supports two distribution scenarios. The structure is identical; only the contents of `data/` differ.

### Scenario A — private / course package (default for internal review and course submission)

- Include the three official files under `data/`: `train.csv`, `test.csv`, `sample_submission.csv`.
- The notebook reads directly from `data/` and runs end-to-end without manual upload.
- ZIP size remains small and Colab-friendly (the three CSVs are roughly 1.5 MB total).

### Scenario B — restricted distribution (CSVs may not be redistributed)

- **Exclude** the three official CSVs from the ZIP.
- Ship a placeholder marker plus instructions in their place:
  - a `data/README.md` (or a clearly named placeholder file inside `data/`) that lists the three required filenames, their exact shapes (train 2781 x 16, test 696 x 15, sample_submission 696 x 2 [Id, Drafted]), and the instruction to obtain them from the official competition source and place them under `data/`;
  - the main `README.md` states the dependency and points to `data/`.
- The notebook detects missing files and prints a clear instruction to place the official CSVs under `data/` (and, in a hosted environment, to upload them) before running.

The placeholder under Scenario B is the only file that may exist under `data/` in that scenario; it is the minimal way to preserve the directory and convey instructions without redistributing restricted data.

---

## 7. References policy

`references.md` cites the real reference library only. Do not ship the PDFs; cite them. The confirmed library that exists on disk:

Books: Kuhn & Johnson (Feature Engineering and Selection, 2021); Feature Engineering for Modern ML (2024); Fundamentals of Data Engineering (2022); Hands-On Machine Learning with Scikit-Learn and PyTorch (2026); An Introduction to Statistical Learning (Python); Machine Learning with LightGBM and Python (2023); Python for Data Analysis 3rd ed. (2022); Python Machine Learning by Example 4th ed. (2024); The Kaggle Book 2nd ed. (2025); The Kaggle Workbook (2023).

Papers: CatBoost (unbiased boosting with categorical features); Causal Feature Selection for Responsible ML; Cawley & Talbot (model-selection overfitting); A Closer Look at Deep Learning on Tabular Datasets; Feature Selection Survey (2024); Leakage and the Reproducibility Crisis in ML-based Science; LightGBM; Meta-analysis of Overfitting on Kaggle; On Leakage in ML Pipelines; Optuna; XGBoost.

Course materials physically exist (`references/course_materials/`) but are internal and are **not** cited as external scholarly sources in the shipped `references.md`.

**Generative AI assistance disclosure (the only permitted mention).** A short, sober subsection at the end of `references.md` discloses that ChatGPT was used in an auxiliary capacity for conceptual consultation on validation, leakage, and feature-engineering frameworks; coding recommendations and debugging guidance; and notebook-organization and documentation review. It states explicitly that it did not train or tune models, select winners, or execute submissions. No other tool of this kind is named anywhere in the package.

**Citation hygiene note.** Two entries in the working bibliography carry "citation details to verify" flags (the "On leakage in ML pipelines" authorship/year and one feature-engineering title). Treat their full citation details as **Not confirmed yet**; the build run must verify them against the source PDFs before finalizing `references.md`.

---

## 8. Explicit EXCLUDE list

The following must never enter the portable ZIP, and must never be referenced in the shipped narrative (README, notebook, `references.md`):

| Excluded path / item | Reason |
|---|---|
| `.git/` | Version-control internals; large; irrelevant to running the notebook. |
| `.venv/` | Local virtual environment; not portable; regenerated from `requirements.txt`. |
| `Libros/` | Internal/private materials. |
| `Prompts/` | Internal planning/build materials. |
| `Recapitulaciones/` | Internal session recaps. |
| `.obsidian/` | Editor/workspace config. |
| `.claude/` | Internal tooling configuration. |
| `AGENTS.md` | Internal build/operations documentation. |
| `CLAUDE.md` | Internal build/operations documentation. |
| `notebooks/_official/` | Official source notebooks; repo-only; not necessary to run the deliverable. Excluded unless a strict, documented need arises (none identified). |
| `references/` PDFs (books, papers, course_materials) | Cite, do not ship. Large binary payload; bibliography in `references.md` suffices. |
| Backup notebooks (`notebooks/02_*_before_*.ipynb`, other `*_before_*`) | Untracked drafts; superseded; not deliverables. |
| The 14 working phase notebooks (`notebooks/01..11`, including `07b`, `08b`, `08c`, `09a`, and the executed `11_phase11_submission_readiness.ipynb`) | The portable package ships only `99_final_integrated_project_report.ipynb`; the phase notebooks stay in the repo. |
| `docs/` (all phase/planning docs, this blueprint included) | Internal planning and acceptance records; summarized in README and notebook, not shipped. |
| `outputs/oof/`, `outputs/validation/`, `outputs/reports/` historical artifacts | Diagnostic traces; regenerated or recorded in-notebook; not required for the final submission. |
| `outputs/submissions/*.csv` (existing Phase 11 files) | Gitignored; identified by SHA-256; the package regenerates a submission from code and must not modify these. |
| `logs/experiment_log.csv` | Historical main log; out of scope; must not be touched. |
| `.vscode/settings.json` | Local editor config. |
| `Sin titulo.canvas`, `*.pyc`, `__pycache__/`, `*.zip`, temp/cache/scratch files | Caches, temporaries, and stray artifacts. |
| Any build-specification, session-recap, conversation-transcript, or internal-tooling file or mention | Forbidden in the shipped narrative; the package presents as a professional technical project. |

Narrative exclusion (prose-level): the shipped files (README, notebook, `references.md`) must contain no mention of any internal build tooling, automation utility, session recap, or build-time helper as part of the methodology or build story. The package reads as a professional technical data-science project. The single permitted generative-support mention is the sober ChatGPT disclosure, which appears only in the dedicated subsection of Section 7.

---

## 9. `data/` vs `data/input/`: use `data/`

**Decision: use a flat `data/` directory holding the three official CSVs directly. Do not introduce `data/input/` in the portable package.**

Justification:

1. **Simplicity is the package's governing principle.** The portable folder does not produce intermediate or processed data on disk; it has a single data role (official inputs). A second nesting level (`data/input/`) signals an input-vs-processed distinction that does not exist here.
2. **The base tree in this deliverable's specification lists `data/ (train.csv, test.csv, sample_submission.csv)`** directly under `data/`. Matching that keeps the blueprint and the build run consistent.
3. **Shorter, unambiguous read paths** in both local and hosted runs: `data/train.csv` is immediately clear in a minimal package.

This is a deliberate departure from the full repository layout, which uses `data/input/`. The repository keeps `data/input/` because it distinguishes official inputs from other data roles across many notebooks; the portable package has no such need. The build run must point the portable notebook at `data/`, not `data/input/`.

---

## 10. Optional extra file: not adopted

The brief permits at most one extra file (`manifest.csv` or `RUN_IN_COLAB.md`) only if truly useful. **Neither is adopted.**

- `manifest.csv`: superseded by the in-notebook results table and the README results summary; a separate manifest adds a freshness contract for no new capability.
- `RUN_IN_COLAB.md`: the hosted-run instructions (upload the official CSVs, install core dependencies, run top-to-bottom) fit naturally in a short README subsection; a dedicated file is not warranted.

If a later build decision finds a genuine need (for example, a hosted environment that cannot surface README instructions at the right moment), `RUN_IN_COLAB.md` is the single preferred candidate — but it is **not** part of this blueprint and must be justified and recorded when added.

---

## 11. Acceptance conditions for the future build run

When the package is later assembled (separate, authorized step), it should satisfy:

1. Base tree exactly as Section 2; `data/` flat per Section 9; `outputs/` shipped empty.
2. Scenario A or Scenario B selected explicitly and applied to `data/` per Section 6.
3. No historical artifact copied in (Section 4) unless the byte-identical-folds exception is explicitly invoked and recorded.
4. Notebook runs top-to-bottom from a clean kernel, relative paths, seed 42, `estimator.classes_` verified before positive-class extraction, submission exactly 696 rows with Id order matching `sample_submission.csv`.
5. No excluded path or excluded prose anywhere in the shipped files (Section 8); ChatGPT disclosure confined to Section 7's subsection.
6. M1 baseline config recovered from Phase 8 artifacts (currently **Not confirmed yet**); two flagged citations verified before `references.md` is finalized.
7. No winner declared; no submission uploaded; existing Phase 11 submissions and `logs/experiment_log.csv` untouched.

---

## 12. Open items marked "Not confirmed yet"

- Exact M1 LogisticRegression baseline configuration (C, penalty, solver, scaling) — recover from Phase 8 artifacts; do not invent.
- Full citation details for two flagged bibliography entries ("On leakage in ML pipelines" authorship/year; one feature-engineering title) — verify against source PDFs.
- Whether byte-identical frozen folds (vs seed-reproducible folds) will be required by the build run — default is seed-reproducible; revisit only if a documented need arises.
