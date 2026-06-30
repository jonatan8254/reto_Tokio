# Reto Tokio / GCI World NFL Draft Prediction

This repository contains the full, auditable machine-learning workflow for the GCI World NFL Draft Prediction competition. The project predicts whether an athlete will be selected in the NFL Draft using only the official competition files and a leakage-safe validation design.

## Project summary

- Task: binary classification
- Target: `Drafted`
- Official metric: ROC-AUC on the positive-class probability
- Data policy: official files only, no external data
- Validation policy: frozen `StratifiedKFold(5, shuffle=True, random_state=42)`
- Core feature set: F2, which adds row-wise missingness flags and `available_measurement_count` to the base feature block

The repository is organized to support reproducible experimentation, documented phase gates, and a clear path from baseline reproduction to final submission readiness.

## Key deliverables

- `notebooks/01_baseline_reproduction.ipynb` - historical baseline reproduction and reference point
- `notebooks/11_phase11_submission_readiness.ipynb` - final refit, test inference, and validated candidate submissions
- `JonatanSanchez/99_final_integrated_project_report.ipynb` - portable integrated package notebook
- `JonatanSanchez/README.md` - portable package guide in English
- `docs/` - planning, methodology, acceptance, and runbook documents
- `outputs/` - OOF predictions, validation reports, manifests, and validated submissions
- `logs/experiment_log.csv` - main experiment log, kept stable and unchanged during controlled phases

The baseline reproduction notebook is included as a historical reference. It remains part of the repository evidence trail, even though the main analytical path later moved to leakage-safe validation and the F2 feature set.

## Repository layout

```text
data/input/                  Official competition CSV files only
notebooks/                   Working notebooks and final execution notebooks
notebooks/_official/         Original official notebooks. Do not edit.
docs/                        Plans, methodology, acceptance, and runbooks
references/                  Real papers, books, slides, and course materials
outputs/folds/               Frozen fold assignments and fold artifacts
outputs/oof/                 Out-of-fold predictions by experiment
outputs/validation/          Tabular validation outputs
outputs/reports/             Narrative validation reports and manifests
outputs/submissions/         Generated submission CSV files
logs/                        Experiment tracking
JonatanSanchez/              Portable package for final delivery
```

## Reproducibility and leakage control

The project was built with strict controls:

- no external athlete, school, or draft-history data;
- no manual editing of predictions;
- no fitting on test data;
- no leaderboard-driven model selection;
- fold-safe preprocessing inside the training folds;
- fixed random seeds whenever randomness is used;
- `School` excluded as a model feature;
- positive-class probability extracted only after verifying `estimator.classes_`.

## Portable package

The `JonatanSanchez/` folder is a portable delivery package. It includes:

- a baseline reproduction notebook;
- the final integrated project report notebook;
- the official data files;
- a license file;
- a compact English README;
- runtime dependencies and output skeleton folders.

This package is designed for portable review and execution without needing the full repository history.

## How to run

For the main workflow, use the notebooks in `notebooks/` from the repository root.

For the portable package, open `JonatanSanchez/99_final_integrated_project_report.ipynb` and run it top to bottom after installing the listed dependencies.

## Results summary

Key recorded validation results from the accepted phases are summarized in the project documentation and final reports. The final submission-ready candidates were validated without upload and without a final-winner declaration.

## License

This repository is released under the MIT License. See [`LICENSE`](LICENSE).
