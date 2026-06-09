# Reto Tokio — Codex Project Instructions

## 1. Project Goal

Build a reproducible, auditable, notebook-first machine learning solution for the GCI World NFL Draft Prediction competition.

The task is binary classification: predict whether an athlete will be selected in the NFL Draft.

Primary metric: ROC-AUC.

The main objective is not only to improve leaderboard performance, but to produce a clean, defensible, reproducible solution that follows the official competition rules.

---

## 2. Hard Competition Rules

Codex must follow these rules strictly:

* Use only the official competition files stored in `data/input/`.
* Do not use external athlete data.
* Do not use external school, conference, ranking, geography, draft-history, or sports-outcome data.
* Do not manually label examples.
* Do not manually edit prediction values in `submission.csv`.
* Do not fit preprocessing, imputation, encoding, feature selection, target encoding, model selection, or hyperparameter tuning on test data.
* Do not use the public leaderboard as the main validation system.
* Every important submission must be reproducible from code.
* Use fixed random seeds whenever randomness is involved.
* The final notebook must run from top to bottom without hidden state.

---

## 3. Project Structure

This is a notebook-first project.

Use the following folders:

```text
data/input/
notebooks/
notebooks/_official/
references/
docs/
outputs/submissions/
outputs/figures/
logs/
```

Folder meanings:

```text
data/input/              Official competition data only.
notebooks/_official/     Original course notebooks. Do not edit.
notebooks/               Working notebooks and final notebook.
references/              Books, papers, slides, tutorials, and course materials.
docs/                    Challenge notes, experiment notes, and submission checklists.
outputs/submissions/     Generated submission CSV files.
outputs/figures/         Figures created during EDA or reporting.
logs/                    Experiment tracking files.
```

Do not create unnecessary folders or Python modules unless the notebook becomes too long, repetitive, or hard to maintain.

---

## 4. Notebook Policy

Use these notebooks as the main workflow:

```text
notebooks/01_baseline_reproduction.ipynb
notebooks/02_eda_and_data_contract.ipynb
notebooks/03_modeling_experiments.ipynb
notebooks/99_final_submission.ipynb
```

Notebook roles:

```text
01_baseline_reproduction.ipynb
Reproduce the official baseline and generate a valid baseline submission.

02_eda_and_data_contract.ipynb
Inspect the dataset, identify target, ID column, missing values, data types, feature groups, leakage risks, and submission format.

03_modeling_experiments.ipynb
Run controlled modeling experiments: preprocessing, validation, feature engineering, model comparison, and possibly tuning.

99_final_submission.ipynb
Clean final notebook. It must run top-to-bottom and generate the final submission automatically.
```

Do not modify files inside:

```text
notebooks/_official/
```

Those files are evidence of the original course materials.

---

## 5. Required ML Discipline

Before implementing any modeling change, Codex must state:

1. The hypothesis.
2. The expected impact on ROC-AUC.
3. The leakage risk.
4. The validation strategy.
5. The files that will be modified.

After implementing any important modeling change, Codex must:

1. Run or define local validation using ROC-AUC.
2. Check that preprocessing is fitted only on training folds.
3. Check reproducibility.
4. Save candidate submissions under `outputs/submissions/`.
5. Register important experiments in `logs/experiment_log.csv`.

---

## 6. Validation Rules

Use ROC-AUC as the primary metric.

Prefer stratified validation for binary classification.

Recommended validation strategy:

```text
StratifiedKFold
fixed random_state
out-of-fold predictions when useful
mean ROC-AUC
standard deviation ROC-AUC
```

Avoid trusting a single train/validation split unless it is only used as a quick sanity check.

Do not tune repeatedly against the public leaderboard.

---

## 7. Leakage Prevention Rules

Codex must actively check for leakage.

High-risk operations:

```text
imputation
scaling
one-hot encoding
ordinal encoding
target encoding
feature selection
hyperparameter tuning
ensemble weighting
missing-value indicators
category frequency encoding
```

Safe rule:

```text
Any operation that learns from data must be fitted only on the training split or training fold.
```

For cross-validation, use fold-aware preprocessing or scikit-learn pipelines whenever possible.

Do not learn statistics from `test.csv` except for safe structural checks such as column names, row count, missingness visibility, and submission alignment.

---

## 8. Installed ECC Agents

Use these agents when relevant:

```text
mle-reviewer
python-reviewer
security-reviewer
silent-failure-hunter
doc-updater
```

Agent usage guidance:

```text
mle-reviewer
Use for ML methodology review: leakage, validation, metrics, feature engineering, overfitting, model comparison, and final model selection.

python-reviewer
Use for Python code quality: readability, reproducibility, imports, function design, notebook hygiene, and avoidable bugs.

security-reviewer
Use before packaging, sharing, committing, or submitting files. Check secrets, paths, private data, large files, and unsafe outputs.

silent-failure-hunter
Use to detect hidden bugs: wrong target, wrong ID column, misaligned predictions, NaNs, duplicated rows, shape mismatches, and submission-format errors.

doc-updater
Use when updating README, docs, experiment notes, challenge brief, or submission checklist.
```

---

## 9. Installed ECC Skills

Use these skills when relevant:

```text
mle-workflow
eval-harness
verification-loop
ai-regression-testing
search-first
strategic-compact
production-audit
security-review
documentation-lookup
nutrient-document-processing
scientific-thinking-literature-review
```

Skill usage guidance:

```text
mle-workflow
Use to structure the ML process: baseline, EDA, validation, feature engineering, model comparison, tuning, ensembling, and final submission.

eval-harness
Use to define checks before experiments: metric checks, submission checks, leakage checks, reproducibility checks, and sanity checks.

verification-loop
Use before any important submission or major commit. Verify data paths, notebook execution, metrics, predictions, and submission format.

ai-regression-testing
Use after modifying notebook logic to make sure previous working behavior has not silently broken.

search-first
Use for documentation and methodology lookup. Do not use it to bring external data into the competition.

strategic-compact
Use to summarize progress, decisions, experiment results, and next steps during long sessions.

production-audit
Use near the end to audit reproducibility, file organization, final notebook quality, and submission readiness.

security-review
Use before committing or sharing files to ensure no secrets, private paths, unnecessary large files, or restricted materials are included.

documentation-lookup
Use to consult technical documentation for libraries such as pandas, scikit-learn, XGBoost, LightGBM, CatBoost, Optuna, and Jupyter.

nutrient-document-processing
Use for processing course documents, PDFs, slides, tutorials, and reference materials when needed.

scientific-thinking-literature-review
Use to extract methodological insights from books and papers, especially about validation, leakage, feature engineering, overfitting, tabular models, and hyperparameter optimization.
```

---

## 10. Priority Order

High-priority agents and skills:

```text
mle-workflow
mle-reviewer
python-reviewer
eval-harness
verification-loop
ai-regression-testing
security-reviewer
security-review
silent-failure-hunter
```

Medium-high priority agents and skills:

```text
documentation-lookup
nutrient-document-processing
scientific-thinking-literature-review
search-first
strategic-compact
production-audit
doc-updater
```

---

## 11. Modeling Strategy

Start simple and improve gradually.

Recommended model path:

```text
1. Official baseline reproduction.
2. Logistic Regression or simple scikit-learn baseline.
3. Random Forest / ExtraTrees / HistGradientBoosting.
4. XGBoost / LightGBM / CatBoost if installed and compatible.
5. Controlled hyperparameter tuning only after stable validation.
6. Simple ensemble only if it improves local validation consistently.
```

Do not jump to complex models before reproducing the baseline.

Do not use Optuna before having a clean validation pipeline.

---

## 12. Experiment Tracking

Important experiments must be recorded in:

```text
logs/experiment_log.csv
```

Each important experiment should include:

```text
experiment_id
date
phase
notebook
features_version
model
params_summary
cv_auc_mean
cv_auc_std
leaderboard_auc
submission_file
risk_flags
notes
```

If an experiment is not reproducible, do not treat it as a real improvement.

---

## 13. Final Submission Requirements

The final notebook must:

* Load data from `data/input/`.
* Train the selected model.
* Use a defensible validation strategy.
* Generate `submission.csv` automatically.
* Save the final submission under `outputs/submissions/`.
* Avoid hidden notebook state.
* Run from top to bottom.
* Use fixed random seeds.
* Clearly explain the modeling decisions.
* Avoid external data.
* Avoid leakage.

Before final submission, run a verification pass using:

```text
verification-loop
mle-reviewer
python-reviewer
silent-failure-hunter
security-reviewer
```

---

## 14. Communication Style for Codex

When proposing changes, be concise but explicit.

Always explain:

```text
what will change
why it helps
what risk it introduces
how it will be validated
```

Prefer robust, simple, reproducible solutions over clever but fragile solutions.

The goal is a solution that can be defended under audit.
