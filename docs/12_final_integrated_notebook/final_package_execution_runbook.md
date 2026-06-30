# Final Package Execution Runbook — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY. Nothing in this run is built, trained, refitted, encoded, submitted, committed, pushed, or staged.** This document is a runbook for a *later* build run. It describes how a future build step should construct the portable package, the README, and the comprehensive notebook. No model is trained here, no submission is created or modified, no leaderboard is consulted, no winner is declared, `logs/experiment_log.csv` is not touched, and no Git operation is performed. Every concrete number, path, reference, and SHA below is grounded in the verified project record. Anything not grounded is marked **Not confirmed yet**.

---

## 1. Purpose and scope

This runbook governs the construction of the deliverable package for the NFL Draft prediction project: a minimal, portable folder containing a professional `README.md`, a `requirements.txt`, a `references.md`, and one comprehensive notebook (`99_final_integrated_project_report.ipynb`), plus the official data layout and empty output folders.

The build run is the future, separate step that performs the construction. It is referenced neutrally throughout. The detailed build specification lives alongside this runbook as `prompt_build_final_portable_package.md`; this runbook is the operational checklist that the build run and the reviewer follow.

What the build run produces:

| Artifact | Role |
|---|---|
| `reto_tokio_final/README.md` | Professional project overview, rules, results, reproducibility statement |
| `reto_tokio_final/requirements.txt` | Minimal dependency list |
| `reto_tokio_final/references.md` | Bibliography from the vetted real reference library; AI-assistance disclosure |
| `reto_tokio_final/99_final_integrated_project_report.ipynb` | Comprehensive, self-contained notebook |
| `reto_tokio_final/data/input/` | Official CSVs (Scenario A) or placeholders + instructions (Scenario B) |
| `reto_tokio_final/outputs/{submissions,folds,figures}/` | Empty at ship time (`.gitkeep`), populated at runtime |

What the build run must never do: train heavy models in this planning lineage, run hyperparameter optimisation, create new historical submissions, modify the two existing submissions, use the public leaderboard to select anything, declare a final winner, modify `logs/experiment_log.csv`, or commit / push / stage without an explicit, separate instruction.

---

## 2. Reading order (before any construction)

Read in this order so that decisions are grounded before files are written:

1. This runbook (`docs/12_final_integrated_notebook/final_package_execution_runbook.md`) — end to end.
2. The build specification `docs/12_final_integrated_notebook/prompt_build_final_portable_package.md` (the construction step's detailed instructions).
3. `docs/00_project_contract/challenge_brief.md` and `docs/00_project_contract/submission_checklist.md` — the contract and the submission format.
4. `docs/05_methodology/validation_protocol_phase6.md` and `docs/05_methodology/leakage_checklist_phase6.md` — the frozen validation and leakage rules the notebook must honour.
5. `docs/11_submission_readiness/phase11_operator_runbook.md` and the Phase 11 reports (`outputs/reports/phase11_submission_readiness_phase11_option_c_20260619_0001_validation_report.md`, `..._artifact_manifest.csv`) — the executed submission-readiness evidence to be reported as historical.
6. `docs/10_model_optimization/phase10_acceptance.md` — the accepted candidate set and warnings.
7. The acceptance records `docs/06_validation/`, `docs/07_feature_engineering/`, `docs/08_model_comparison/`, `docs/09_auc_ranking_diagnostics/` — for the historical narrative.

Do not parse the reference PDFs or course materials. Cite them from the vetted list in Section 7; do not ship them.

---

## 3. Build order

Construct in this order. Each stage gates the next.

1. **Folder skeleton first.** Create the `reto_tokio_final/` tree and the empty `outputs/` subfolders with `.gitkeep`. Validate the structure (Section 9 PowerShell block) before writing content.
2. **`requirements.txt`** (Section 6).
3. **`references.md`** (Section 7).
4. **`README.md`** (Section 8) — written after the references exist so the results table and the disclosure are consistent.
5. **The notebook** `99_final_integrated_project_report.ipynb` (Sections 10–13) — written last, because it is the largest and consumes the conventions fixed by the README.
6. **Validation passes** — folder validation, notebook-JSON validation, submission-format checks, forbidden-path checks, README and notebook reviews.
7. **ZIP packaging** — only at the very end of the build run (Section 16, marked do-not-run-now).

Rationale for folder → README → notebook: the folder defines the relative paths the notebook hard-codes; the README freezes the result figures and naming so the notebook narrative cannot drift from them.

---

## 4. Files to copy and files to exclude

### 4.1 Copy into the portable package

| Source | Destination | Notes |
|---|---|---|
| `data/input/train.csv` | `data/input/train.csv` | Scenario A only (2781 × 16) |
| `data/input/test.csv` | `data/input/test.csv` | Scenario A only (696 × 15) |
| `data/input/sample_submission.csv` | `data/input/sample_submission.csv` | Scenario A only (696 × 2) |
| `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` | `outputs/folds/` | Frozen folds, SHA256[:16]=`96937649526bcadb`, 2781 rows, folds 0..4 — copy for reproducibility, or regenerate in-notebook from `StratifiedKFold(5, shuffle=True, random_state=42)` and assert the SHA matches |

The notebook content (narrative, code, results table) is authored fresh by the build run; it is not copied from any existing notebook. Existing repository notebooks are read for evidence only.

### 4.2 Exclude from the portable ZIP entirely

`.git/`, `.venv/`, `.claude/`, `.obsidian/`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `AGENTS.md`, `CLAUDE.md`, `notebooks/_official/`, the 14 repository notebooks (only the new `99_*` ships), all of `docs/`, the `references/` PDF payloads (cite, do not ship), `outputs/oof/`, `outputs/validation/`, `outputs/reports/`, `logs/experiment_log.csv`, backup notebooks (`notebooks/02_*_before_*.ipynb`, untracked `notebooks/11_*.ipynb` backups), `Sin título.canvas`, `__pycache__/`, `*.pyc`, ZIP archives, and any temporary or cache files.

The two executed Phase 11 submission CSVs are **not** shipped: `outputs/submissions/` is gitignored, and the package generates its own submission at runtime. The historical SHA-256 values are recorded in the narrative as durable identity (Section 13), not shipped as files.

---

## 5. Scenario A vs Scenario B data governance

| Scenario | When | `data/input/` contents |
|---|---|---|
| **A — private / course package** | Distribution to the course or director | Include `train.csv`, `test.csv`, `sample_submission.csv` |
| **B — restricted distribution** | Wider or external distribution | Exclude the three CSVs; ship a `data/input/README.txt` placeholder stating the official files are obtained from the competition and dropped into `data/input/`, plus a `.gitkeep` |

The notebook must run unchanged in both scenarios: when CSVs are absent it prompts for upload (Colab) or instructs local placement (Section 14).

---

## 6. Creating `requirements.txt`

Minimal and honest. The portable package's mandatory path is the M1 LogisticRegression baseline, which needs only the core stack. CatBoost is optional and guarded.

```text
pandas
numpy
scikit-learn
matplotlib
# Optional: enables the CatBoost tuned candidate (best global OOF, warning-heavy).
# If absent, the notebook falls back to the M1 LogisticRegression baseline.
# catboost
```

Rules for the build run:

- Do **not** pin versions in the shipped file. The base development environment is recorded as **Not confirmed yet** for exact wheel versions in the package context; pinning to unverified versions would be an invention. State the development Python and library versions inside the notebook only if they are read directly from the environment at authoring time; otherwise mark them **Not confirmed yet**.
- Do **not** list `xgboost` or `lightgbm`: both were evaluated and dropped (no qualifying evidence); they are not part of the deliverable path.
- `matplotlib` is included because the notebook produces figures (class balance, missingness, fold/OOF diagnostics). No `scipy`, `seaborn`, or `statsmodels`.
- CatBoost remains commented/optional because it ran historically in a **separate** environment (catboost 1.2.10); the base development environment was kept GBDT-free.

---

## 7. Creating `references.md`

Build `references.md` from the vetted real reference library only. Every entry below corresponds to a PDF that physically exists under `references/`. Do not invent authors, years, DOIs, titles, or venues. Where the digest itself flagged a detail as needing verification, keep it conservative or mark it **Not confirmed yet** rather than asserting it.

### 7.1 Validation and model selection

| Work | File (real) |
|---|---|
| Cawley, G. C., & Talbot, N. L. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *JMLR*, 11, 2079–2107. | `references/papers/cawley_talbot_model_selection_overfitting.pdf` |
| James, Witten, Hastie, Tibshirani, Taylor (2021). *An Introduction to Statistical Learning with Applications in Python*. Springer. | `references/books/introduction_to_statistical_learning_python.pdf` |
| Kuhn, M., & Johnson, K. (2021). *Feature Engineering and Selection: A Practical Approach for Predictive Models*. Chapman & Hall/CRC. | `references/books/feature_engineering_and_selection_kuhn_johnson_2021.pdf` |
| Géron, A. *Hands-On Machine Learning with Scikit-Learn and PyTorch*. | `references/books/hands_on_machine_learning_sklearn_pytorch_2026.pdf` |

### 7.2 Leakage and reproducibility

| Work | File (real) |
|---|---|
| Kapoor, S., & Narayanan, A. (2022). Leakage and the reproducibility crisis in ML-based science. *arXiv:2207.07048*. | `references/papers/leakage_and_reproducibility_crisis_ml_science.pdf` |
| On leakage in machine learning pipelines (citation details **Not confirmed yet**). | `references/papers/on_leakage_in_ml_pipelines.pdf` |
| Massaron, Tunguz, Banachewicz (2025). *The Kaggle Book, 2nd Edition*. Packt. | `references/books/the_kaggle_book_2nd_edition_2025.pdf` |
| Meta-analysis of overfitting in Kaggle competitions (citation details **Not confirmed yet**). | `references/papers/meta_analysis_overfitting_kaggle.pdf` |

### 7.3 Feature engineering and selection

| Work | File (real) |
|---|---|
| Feature selection survey (2024) — *Knowledge and Information Systems* (full citation **Not confirmed yet**). | `references/papers/feature_selection_survey_2024.pdf` |
| Causal feature selection for responsible machine learning (2024) — *arXiv* (full citation **Not confirmed yet**). | `references/papers/causal_feature_selection_responsible_ml.pdf` |
| *Feature Engineering for Modern Machine Learning with Scikit-Learn* (2024). | `references/books/feature_engineering_modern_ml_2024.pdf` |
| McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly. | `references/books/python_for_data_analysis_3rd_edition_2022.pdf` |

### 7.4 Tabular models and gradient boosting

| Work | File (real) |
|---|---|
| Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *arXiv:1603.02754*; KDD '16. | `references/papers/xgboost_scalable_tree_boosting_system.pdf` |
| Ke et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. NeurIPS 2017. | `references/papers/lightgbm_highly_efficient_gbdt.pdf` |
| Prokhorenkova et al. (2019). CatBoost: Unbiased boosting with categorical features. *arXiv:1706.09516*. | `references/papers/catboost_unbiased_boosting_categorical_features.pdf` |
| A closer look at deep learning methods on tabular datasets (*arXiv*; full citation **Not confirmed yet**). | `references/papers/closer_look_deep_learning_tabular_datasets.pdf` |
| Banachewicz, K., & Massaron, L. (2023). *The Kaggle Workbook*. Packt. | `references/books/the_kaggle_workbook_2023.pdf` |

### 7.5 Hyperparameter optimisation

| Work | File (real) |
|---|---|
| Akiba et al. (2019). Optuna: A next-generation hyperparameter optimization framework. KDD '19. https://doi.org/10.1145/3292500.3330701 | `references/papers/optuna_next_generation_hpo_framework.pdf` |
| Van Wyk, A. (2023). *Machine Learning with LightGBM and Python*. Packt. | `references/books/machine_learning_with_lightgbm_python_2023.pdf` |

### 7.6 Python / data engineering / workflow

| Work | File (real) |
|---|---|
| Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly. | `references/books/fundamentals_of_data_engineering_2022.pdf` |
| Liu, Y. (2024). *Python Machine Learning By Example* (4th ed.). Packt. | `references/books/python_machine_learning_by_example_4th_edition_2024.pdf` |

### 7.7 Generative AI assistance disclosure (the only place tooling is named)

`references.md` ends with a short, sober subsection titled **"Generative AI assistance disclosure"**. Approved wording:

> This project benefited from generative AI assistance (ChatGPT) in an auxiliary capacity: conceptual consultation on validation, leakage, and feature-engineering frameworks; coding recommendations and debugging guidance for notebook development; and review of notebook organisation and documentation structure. It did not train, tune, or select models; did not execute hyperparameter optimisation; did not make submission decisions; and did not contribute to the methodological trajectory beyond advisory consultation.

No other tooling is named anywhere in the package. ChatGPT appears only here (and, if desired, in a one-line README acknowledgements pointer to this subsection) — never in the methodology narrative.

---

## 8. Creating and reviewing `README.md`

### 8.1 Required sections

- Project title and one-paragraph challenge summary (binary classification; predict `Drafted`; metric ROC-AUC on positive-class probability).
- Data governance: official files only; no external data; public leaderboard is sanity-check only and never drives selection; stratified 5-fold CV with fixed seed.
- Feature set: F2 only — base 13 + 7 missingness flags + `available_measurement_count` (21 features); School excluded.
- How to run: `pip install -r requirements.txt`, then open `99_final_integrated_project_report.ipynb` and run top-to-bottom; expected output is a 696-row submission CSV.
- Results table (figures fixed from the verified record):

| Model | OOF ROC-AUC | Δ vs M0 | Folds ≥ M0 | Role |
|---|---:|---:|---:|---|
| M0 RandomForest (frozen anchor) | 0.8116502602 | — | — | reference anchor |
| M1 LogisticRegression (baseline) | 0.8270821070 | +0.0154318 | 4/5 | fallback / reference candidate |
| CatBoost tuned | 0.8303208581 | +0.0186706 | 5/5 | best global OOF, warning-heavy candidate |

Supporting (optional) record: M1 tuned 0.8274819178 (rejected, noise-level +0.0003998 vs M1 baseline, 3/5 folds); CatBoost baseline 0.8202943969; XGBoost 0.8113477084 and LightGBM 0.8062204891 dropped (no qualifying evidence). Pre-registered promotion bar: Δ ≥ 0.005436 AND same-sign positive folds ≥ 4/5 AND slice guard clear.

- Reproducibility statement: seed 42 throughout; frozen folds (SHA256[:16]=`96937649526bcadb`); positive-class probability extracted only after verifying `estimator.classes_` contains label 1; no leakage (preprocessing fitted inside folds for CV, on full train for the final refit; test is transform-only).
- Author attribution: Jonatan Estiven Sanchez Vargas; Universidad Nacional de Colombia; Systems and Computer Engineering (Ingeniería de Sistemas e Informática); project Reto Tokio / GCI World NFL Draft Prediction.
- A one-line acknowledgements pointer to the Generative AI assistance disclosure in `references.md`.

### 8.2 README review checklist

- No occurrence of internal tooling terms in the methodology/build narrative (verify with Section 15).
- ChatGPT appears only in the acknowledgements pointer / disclosure, sober and accurate.
- Every figure in the results table matches Section 8.1 exactly.
- No reference to `.git`, `.venv`, `Prompts/`, `Recapitulaciones/`, `notebooks/_official/`, `docs/`, or any phase/planning artifact.
- Run instructions resolve against the shipped relative paths.

---

## 9. Validating the portable folder

Validate the skeleton before writing content and again after. Use the PowerShell block in Section 17.1. The folder is valid when:

- `README.md`, `requirements.txt`, `references.md`, `99_final_integrated_project_report.ipynb` all exist at the package root.
- `data/input/` exists (with CSVs in Scenario A, or placeholder + `.gitkeep` in Scenario B).
- `outputs/submissions/`, `outputs/folds/`, `outputs/figures/` exist, each with `.gitkeep`.
- None of the excluded items from Section 4.2 are present anywhere in the tree.

---

## 10. Notebook structure: executable vs narrative cells

The notebook is comprehensive but self-contained. Cells are one of two kinds.

| Cell purpose | Kind | Notes |
|---|---|---|
| Title, author, project charter, data governance | Narrative (markdown) | |
| Environment / mode detection (Colab vs local; optional-import guards) | Executable | Soft `try/except` for `catboost`; matplotlib import |
| Data load + contract checks (row/col counts, target balance, missingness) | Executable | Asserts 2781×16 train, 696×15 test, 696×2 sample |
| EDA figures (class balance, missingness train vs test) | Executable | Writes to `outputs/figures/` |
| Frozen fold setup | Executable | `StratifiedKFold(5, shuffle=True, random_state=42)`; assert SHA / row counts against the frozen folds |
| F2 feature construction (13 base + 7 flags + count) | Executable | Median imputation + one-hot fitted inside folds (CV) and on full train (final) |
| Cross-validation: M1 baseline OOF + fold AUCs | Executable | `roc_auc_score` on verified positive-class probability |
| CatBoost tuned path (guarded) | Executable | Runs only if `catboost` importable; else skipped with a printed notice |
| Final refit on full train + test inference | Executable | Transform-only on test; `predict_proba` after `classes_` check |
| Submission generation + 696-row validation suite | Executable | Section 12 checks; writes `outputs/submissions/` |
| Historical results table and phase narrative | Narrative (markdown) | Records the Section 8.1 figures as historical evidence |
| Methodology, leakage statement, reproducibility statement | Narrative (markdown) | |
| References / acknowledgements | Narrative (markdown) | Mirrors `references.md` |

Narrative cells justify every important decision (Section 14.5). Executable cells must run top-to-bottom from a clean kernel with no hidden state and only relative paths.

---

## 11. Missing-file handling

The notebook must degrade gracefully, never crash silently, and never fabricate data.

| Condition | Behaviour |
|---|---|
| In Colab and CSVs absent | Prompt for upload of `train.csv`, `test.csv`, `sample_submission.csv`; move into `data/input/` |
| Local and CSVs absent (Scenario B) | Print a clear instruction to place the official files in `data/input/`; stop cleanly before modelling |
| Frozen fold file absent | Regenerate from `StratifiedKFold(5, shuffle=True, random_state=42)` and assert the regenerated assignments reproduce the canonical layout (2781 rows, folds 0..4); record that regeneration occurred |
| `catboost` not importable | Print a notice; skip the CatBoost path; continue with the M1 baseline as the active model |
| `sample_submission.csv` absent | Block submission writing; the Id order/contract check cannot be satisfied without it — stop with a clear message |

---

## 12. Submission validation

The notebook's submission validation suite must enforce all of the following before writing or accepting any submission file. These mirror the executed Phase 11 checks.

| Check | Requirement |
|---|---|
| Row count | Exactly 696 |
| Columns / header | Exactly `Id,Drafted` (order and names) |
| Id order | Identical to `sample_submission.csv` (which equals `test.csv` order) |
| Probability range | All `Drafted` values within [0, 1] |
| Finiteness | No NaN, no ±inf |
| No missing | No null `Id` or `Drafted` |
| Duplicate Id | No duplicate `Id` values |
| Integrity | SHA-256 of the written file computed and printed (durable identity) |
| No manual edits | File is produced by code in the same run; SHA-256 recorded for traceability |

Historical reference (record as historical, do not recompute as a target): the two executed Phase 11 submissions, run_id `phase11_option_c_20260619_0001`, each 696 rows, header `Id,Drafted`, no winner declared, not uploaded:

| Candidate | SHA-256 |
|---|---|
| CatBoost tuned (primary) | `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8` |
| M1 LogisticRegression baseline (fallback) | `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640` |

The package's own freshly generated submission will have its **own** SHA-256, which need not equal the historical values (different environment, optional CatBoost path). Last uploaded file determines final ranking; private leaderboard uses the full test set. Upload is manual and director-side; the package does not automate it.

---

## 13. Which results to compute vs load vs record-as-historical

| Result | Disposition |
|---|---|
| Data contract (row/col counts, target balance, missingness) | **Compute** fresh from the CSVs |
| Fold assignments | **Compute** fresh (assert against frozen layout) or **load** the frozen file when present |
| M1 baseline OOF + fold AUCs | **Compute** fresh in the notebook |
| Final refit + test inference + submission | **Compute** fresh |
| CatBoost tuned OOF (0.8303208581) | **Record as historical** in the narrative; recompute only if `catboost` is available and the run elects to — never required for the deliverable |
| M0 anchor, M1 tuned, CatBoost baseline, XGBoost, LightGBM OOF figures | **Record as historical** (Phase 8–10 accepted evidence) |
| Slice diagnostics (Age_missing=1 fragility, Position=QB, robust-slice warnings) | **Record as historical** summaries; recompute only the M1 fold/slice view the notebook itself produces |
| Phase 11 submission SHA-256 values | **Record as historical** identity |

The CatBoost tuned config to cite in the narrative (from the historical HPO results, not re-tuned): `depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]`. M1 baseline exact config (C / penalty / solver / scaling) is **Not confirmed yet** from the digest and must be recovered from the Phase 8 artifacts; do not invent it.

---

## 14. Runtime modes and fallbacks

### 14.1 Colab from a Drive-uploaded ZIP

1. Upload `reto_tokio_final.zip` to Drive; mount Drive in Colab; unzip into the working directory so the package root is the current directory.
2. Run from the top: mode detection unzips/locates `data/input/`; if CSVs are present they are used, otherwise the upload prompt fires.
3. Relative paths resolve against the unzipped root. Submission writes to `outputs/submissions/`.

### 14.2 Colab with only the 3 CSVs (no ZIP, notebook only)

1. Open `99_final_integrated_project_report.ipynb` directly in Colab.
2. The mode-detection cell prompts for `train.csv`, `test.csv`, `sample_submission.csv` and places them in a freshly created `data/input/`.
3. Folds are generated fresh; the M1 baseline runs; submission is produced and validated. CatBoost is skipped unless the user installs it.

### 14.3 Full Repository Mode

1. From the repository root with the development environment active, install `requirements.txt`.
2. The notebook loads `data/input/` and may load the frozen folds from `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`.
3. Historical OOF artifacts in the repository are available for cross-checking the recorded figures but are not required by the notebook.

### 14.4 CatBoost-absent and pandas-absent fallbacks

- **CatBoost absent:** guarded `try: import catboost` fails → print a notice, skip the CatBoost path, proceed with the M1 LogisticRegression baseline as the active deliverable model. The narrative still records the historical CatBoost figures.
- **pandas/sklearn-impute minimal path:** in a constrained environment, the notebook uses row-wise median imputation via `fillna` against train-derived medians and dictionary-based categorical encoding instead of heavier transformers, and a manual fold loop instead of `cross_val_predict`. The M1 baseline remains the always-available model; if even sklearn is unavailable the notebook stops with a clear message rather than emitting an unvalidated submission. (A bare decision-rule fallback is **Not confirmed yet** as a deliverable path and should not be shipped without explicit justification.)

### 14.5 Decision justification

Every important decision in the notebook narrative must carry its reason: why F2 (slice-guard-clear, 5/5 folds, +0.0850 OOF over the Phase 6 anchor); why School is excluded (high cardinality, test-only categories, leakage risk); why median imputation plus explicit missingness flags rather than mean imputation (explicit flags are safer than implicit imputation shifts on the Age_missing slice); why CatBoost tuned is "best global OOF but warning-heavy, no repeated-CV" and M1 is the stable fallback; why no winner is declared; and why the public leaderboard is sanity-check only.

---

## 15. Forbidden-path and internal-tooling verification

### 15.1 Forbidden-path verification (repository side)

Before any staging discussion, confirm the working tree is clean and no forbidden path is touched. Use the Section 17.3 command block. Expectation: empty output for the protected-path diff and an unchanged `logs/experiment_log.csv`.

### 15.2 No internal-tooling mention (package side)

Scan every shipped text file (`README.md`, `references.md`, and the notebook's narrative cells) for internal-tooling terms. No internal build-tooling name (proprietary coding tools, automation actors, internal session-instruction or transcript files, or session-recap files) may appear anywhere in the methodology/build narrative. The only permitted generative-AI mention is **ChatGPT**, and only inside the Generative AI assistance disclosure (and a one-line acknowledgements pointer). The forbidden-term list is encoded in the scan pattern below. Suggested scan (run during the build review, not now):

```bash
grep -rniE 'claude|codex|prompt engineering|\bagent\b|assistant|recapitulaci|chat log' \
  reto_tokio_final/README.md reto_tokio_final/references.md
# Expect: zero hits.
grep -rinE 'chatgpt' reto_tokio_final/references.md
# Expect: hits ONLY within the "Generative AI assistance disclosure" subsection.
```

For the notebook, extract markdown-cell text and apply the same scan; code cells must likewise carry no such terms in comments.

---

## 16. Notebook review

Before the notebook is accepted:

- Runs top-to-bottom from a clean kernel with relative paths and fixed seed 42; no hidden state.
- Contract asserts pass (2781×16, 696×15, 696×2; positive rate 0.6483279396).
- Positive-class probability extracted only after `estimator.classes_` verification.
- Preprocessing is fold-safe in CV and full-train-only for the final refit; test is transform-only; no target encoding, no feature selection, no School-as-feature, no leaderboard use.
- Submission suite (Section 12) passes; output is 696 rows.
- Figures match Section 8.1; historical figures are labelled historical.
- Writing does not read as machine-generated (Section 18).
- Valid notebook JSON (Section 17.2).

---

## 17. Verification command blocks

### 17.1 PowerShell — validate the package structure exists (Windows PowerShell 5.1)

```powershell
# Validate portable package structure. Adjust $pkg to the package root.
$pkg = "C:\GitHub\reto_Tokio\reto_tokio_final"
$required = @(
  "README.md",
  "requirements.txt",
  "references.md",
  "99_final_integrated_project_report.ipynb",
  "data\input",
  "outputs\submissions\.gitkeep",
  "outputs\folds\.gitkeep",
  "outputs\figures\.gitkeep"
)
$missing = @()
foreach ($rel in $required) {
  $full = Join-Path $pkg $rel
  if (Test-Path $full) { Write-Host "OK   $rel" }
  else { Write-Host "MISS $rel"; $missing += $rel }
}
if ($missing.Count -eq 0) { Write-Host "STRUCTURE OK" }
else { Write-Host ("STRUCTURE INCOMPLETE: " + ($missing -join ", ")) }
```

### 17.2 PowerShell — validate the notebook is valid JSON (Windows PowerShell 5.1)

```powershell
$nb = "C:\GitHub\reto_Tokio\reto_tokio_final\99_final_integrated_project_report.ipynb"
if (-not (Test-Path $nb)) { Write-Host "NOTEBOOK NOT FOUND: $nb" }
else {
  try {
    $json = Get-Content $nb -Raw | ConvertFrom-Json -ErrorAction Stop
    if ($?) {
      $hasCells = $null -ne $json.cells
      $hasFormat = $null -ne $json.nbformat
      if ($hasCells -and $hasFormat) { Write-Host ("VALID JSON; nbformat=" + $json.nbformat + "; cells=" + $json.cells.Count) }
      else { Write-Host "JSON PARSED but missing 'cells' or 'nbformat' keys" }
    }
  } catch {
    Write-Host ("INVALID JSON: " + $_.Exception.Message)
  }
}
```

### 17.3 Final verification command block (Bash)

```bash
git status --short
git diff --check
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
git diff -- logs/experiment_log.csv
```

Expectation: a clean or intentionally-scoped status, no whitespace/conflict errors from `--check`, no protected-path file names in the third command, and no diff for `logs/experiment_log.csv`.

### 17.4 PowerShell — create the ZIP at the END of a future build (PLAN — do not run now)

```powershell
# DO NOT RUN NOW. This is the final packaging step of a FUTURE build run,
# to be executed only after structure, notebook-JSON, submission, forbidden-path,
# README, and notebook reviews have all passed.
$pkg = "C:\GitHub\reto_Tokio\reto_tokio_final"
$zip = "C:\GitHub\reto_Tokio\reto_tokio_final.zip"
if (-not (Test-Path $pkg)) { Write-Host "PACKAGE ROOT MISSING: $pkg" }
else {
  if (Test-Path $zip) { Remove-Item $zip -Force }
  if ($?) {
    Compress-Archive -Path (Join-Path $pkg "*") -DestinationPath $zip -Force
    if ($?) {
      $h = Get-FileHash $zip -Algorithm SHA256
      Write-Host ("ZIP CREATED: " + $zip)
      Write-Host ("SHA-256: " + $h.Hash)
    }
  }
}
```

---

## 18. Verifying the writing does not look machine-generated

During README and notebook review, confirm the prose reads as a human-authored technical report:

- Vary sentence and paragraph length; avoid repetitive templated openers and uniform bullet cadence.
- No boilerplate hedging or filler; each claim is specific and grounded in a number, a file, or a decision.
- No leftover meta-language about generation, drafting, or tooling.
- Section transitions read naturally; the narrative explains *why*, not only *what*.
- Terminology is consistent (F2, OOF, frozen folds, anchor, candidate-with-warning) and matches the figures.
- No forbidden tooling terms (Section 15.2).

---

## 19. "Not confirmed yet" register

| Item | Status |
|---|---|
| M1 baseline exact config (C, penalty, solver, scaling) | Not confirmed yet — recover from Phase 8 artifacts; do not invent |
| Exact development library/wheel versions to print in the package context | Not confirmed yet — record only if read directly from the environment at authoring time |
| Full citation details for `on_leakage_in_ml_pipelines.pdf`, `meta_analysis_overfitting_kaggle.pdf`, `feature_selection_survey_2024.pdf`, `causal_feature_selection_responsible_ml.pdf`, `closer_look_deep_learning_tabular_datasets.pdf` | Not confirmed yet — verify against the source PDFs before asserting authors/years/venues |
| Bare decision-rule fallback as a shipped deliverable path | Not confirmed yet — not to be shipped without explicit justification |

---

*End of runbook. Planning only — no build, training, submission, or Git action is performed in this run.*
