# Reto Tokio / GCI World NFL Draft Prediction

This folder is the portable project package for the GCI World NFL Draft Prediction competition. It contains the official data, the final integrated notebook, the official baseline reproduction notebook, the reference list, and the runtime dependencies needed to reproduce the final workflow.

## What is included

- `01_baseline_reproduction.ipynb` - official baseline reproduction and historical reference
- `99_final_integrated_project_report.ipynb` - main end-to-end project report
- `data/input/train.csv`
- `data/input/test.csv`
- `data/input/sample_submission.csv`
- `references.md`
- `requirements.txt`
- `LICENSE` - MIT License
- `outputs/` skeleton folders for runtime artifacts

## Project summary

The task is binary classification: predict whether an athlete will be selected in the NFL Draft. The target is `Drafted`, and the official metric is ROC-AUC on the positive-class probability.

The project is designed to be reproducible and audit-friendly:

- official competition files only;
- no external data;
- fixed seeds and frozen folds;
- fold-safe preprocessing;
- no leaderboard-driven model selection;
- no manual edits to prediction values.

The baseline reproduction notebook is included as a historical reference and sanity check. The final integrated notebook is the primary deliverable for review and execution.

## How to run

1. Create or activate a Python 3.13 environment.
2. Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Run the baseline notebook if you want to inspect the historical reference first.
4. Open `99_final_integrated_project_report.ipynb` and run it top to bottom.

## License

This package is released under the MIT License. See [`LICENSE`](LICENSE).
