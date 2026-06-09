# Reto Tokio

Notebook-first machine learning workspace for the GCI World NFL Draft Prediction competition.

The goal is to build a reproducible and auditable binary classification solution that predicts whether an athlete will be selected in the NFL Draft. The primary metric is ROC-AUC.

## Rules

- Use only the official competition files in `data/input/`.
- Do not use external athlete, school, conference, ranking, geography, draft-history, or sports-outcome data.
- Do not manually label examples or manually edit prediction values.
- Do not fit preprocessing, imputation, encoding, feature selection, model selection, or tuning on test data.
- Do not use the public leaderboard as the main validation system.

## Environment

This project uses Python 3.13.13 in a local virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies with:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the project interpreter directly when running checks:

```powershell
.\.venv\Scripts\python.exe
```

## Notebook Workflow

Run notebooks from the repository root and keep them reproducible from a clean kernel.

Recommended order:

1. `notebooks/01_baseline_reproduction.ipynb`
2. `notebooks/02_eda_and_data_contract.ipynb`
3. `notebooks/03_modeling_experiments.ipynb`
4. `notebooks/99_final_submission.ipynb`

Do not edit notebooks in `notebooks/_official/`; they are source evidence for the course materials.

## Outputs and Logs

- Generated submissions: `outputs/submissions/`
- Generated figures: `outputs/figures/`
- Experiment tracking: `logs/experiment_log.csv`
- Project notes and checklists: `docs/`

Important experiments should be reproducible from code and logged in `logs/experiment_log.csv`.

## Git Safety

Do not commit official CSVs, PDFs, ZIP archives, generated outputs, or `.venv/`.

The repository is configured to ignore official input CSVs, reference PDFs/slides/text files, generated submissions, figures, virtual environments, caches, secrets, and ZIP archives.
