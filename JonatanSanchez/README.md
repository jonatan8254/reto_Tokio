# Reto Tokio / GCI World NFL Draft Prediction

**A reproducible, leakage-safe machine-learning solution for predicting NFL Draft selection.**

- **Author:** Jonatan Estiven Sanchez Vargas
- **Institution:** Universidad Nacional de Colombia
- **Program:** Systems and Computer Engineering (Ingeniería de Sistemas e Informática)
- **Project:** Reto Tokio / GCI World NFL Draft Prediction
- **Primary deliverable:** [`99_final_integrated_project_report.ipynb`](99_final_integrated_project_report.ipynb)

---

## 1. What this project is

This package is the final, self-contained record of a binary-classification project: given a
college athlete's combine measurements and categorical profile, predict the probability that the
athlete is **drafted** (`Drafted = 1`). The work was carried out as a disciplined, phase-gated
machine-learning study that prioritises **reproducibility, leakage safety, and auditability** over
leaderboard chasing.

The package is deliberately minimal on the outside and comprehensive on the inside: a thin folder
with a single, heavily documented notebook that tells the whole story from problem framing to two
validated, submission-ready prediction files.

## 2. The task in one screen

| Item | Value |
|---|---|
| Task | Binary classification |
| Target | `Drafted` (1 = drafted, 0 = not drafted) |
| Identifier | `Id` |
| Official metric | ROC-AUC on the positive-class probability |
| Training rows | 2,781 |
| Test rows | 696 |
| Submission format | `Id,Drafted`, exactly 696 rows, `Id` order matching `sample_submission.csv` |
| Class balance (train) | 978 negative / 1,803 positive → positive rate ≈ 0.6483 |
| Data policy | Official competition files only; **no external data** |

The positive class is the majority class, so the project reports **ROC-AUC on probabilities**
(threshold-free ranking quality) rather than accuracy, in line with the official metric.

## 3. Package contents

```
final_integrated_notebook_package/
├── README.md                                   # this file
├── requirements.txt                            # minimal dependencies
├── references.md                               # real bibliography + AI-assistance disclosure
├── 99_final_integrated_project_report.ipynb    # the full, executable report
├── data/
│   └── input/
│       ├── train.csv                           # official training data (2781 × 16)
│       ├── test.csv                            # official test data (696 × 15)
│       └── sample_submission.csv               # official submission template (696 × 2)
└── outputs/                                     # created/overwritten at runtime
    ├── submissions/                            # generated submission(s) land here
    ├── folds/
    ├── figures/
    └── tables/
```

This package ships under **Scenario A** (private/course distribution): the three official CSV files
are included so the notebook runs with zero setup. For restricted distribution (**Scenario B**),
remove the three files from `data/input/` and supply them at run time (the notebook detects their
absence and offers an upload step in Google Colab).

## 4. How to run

The notebook is designed to run top-to-bottom, unchanged, in three environments.

### 4.1 Google Colab (recommended for review)

1. Upload this package folder to Google Drive (or upload the ZIP and unzip it), **or** open the
   notebook directly and upload only the three CSV files when prompted.
2. Open `99_final_integrated_project_report.ipynb` in Colab.
3. Run **Runtime → Run all**.

The notebook resolves its own paths, loads the official files from `data/input/` (or from the
upload), reproduces the validation and feature pipeline, refits the reproducible candidate, and
writes a validated submission into `outputs/submissions/`.

### 4.2 Local machine

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook 99_final_integrated_project_report.ipynb
```

### 4.3 Dependencies and graceful fallback

The notebook needs only **pandas, numpy, and scikit-learn**. CatBoost is **optional**: the tuned
CatBoost candidate is reproduced only if `catboost` is installed; otherwise the notebook falls back
to the logistic-regression candidate and clearly labels the CatBoost figures as recorded values.
The fallback path still produces a fully validated 696-row submission.

## 5. Methodology at a glance (Phases 1–11)

The project advanced through eleven gated phases. Each gate had to be satisfied before the next
phase began; no phase was closed without explicit acceptance evidence.

| Phase | Focus | Outcome |
|---|---|---|
| 1 | Contract, rules, reproducibility | Notebook-first, fixed seeds, official-files-only governance. |
| 2 | Baseline reproduction | Official RandomForest baseline reproduced as a historical reference (leakage-inflated by design). |
| 3 | EDA and data contract | Shapes/target/missingness verified; four signal families hypothesised; `School` flagged as high-cardinality/leakage risk. |
| 4 | Research synthesis | Validation, leakage, feature, model, and HPO rules distilled from the reference library. |
| 5 | Methodology freeze | ROC-AUC on probabilities, `StratifiedKFold(5, shuffle=True, random_state=42)`, fold-safe fit scope, `School` excluded, submissions only in Phase 11 — frozen. |
| 6 | Validation harness | Clean out-of-fold (OOF) anchor established on frozen folds. |
| 6A | Baseline reconciliation | The gap to the historical baseline attributed mostly to informative missingness; the feature-adoption threshold set. |
| 7 | Feature engineering | The **F2** feature set (21 features) adopted under fixed-fold ablation; `School` excluded; BMI not adopted. |
| 7B | Role-interaction probe | The single deferred interaction rejected; F2 confirmed as final. |
| 8 | Model-family comparison | Logistic regression emerged as the strongest non-anchor (with a slice warning); external gradient-boosting trees compared in an isolated environment; XGBoost/LightGBM dropped, CatBoost escalated. |
| 9A | Ranking diagnostics | Complementary imbalance metrics confirmed the ranking; no re-ranking; no winner. |
| 10 | Controlled optimization | Bounded hyperparameter search; logistic-regression tuning rejected as noise-level; tuned CatBoost is the best global OOF candidate but warning-heavy. |
| 11 | Submission readiness | Both candidates refit on full train, inferred on test, and validated; **two** format-valid 696-row submissions produced. |

A complete, decision-by-decision account — with partial conclusions and transition analyses between
phases — lives in the notebook.

## 6. Validation and leakage discipline

- **Metric.** ROC-AUC computed on the positive-class probability, obtained only after verifying that
  the fitted estimator's `classes_` actually contains the label `1` (never by blind column indexing).
- **Cross-validation.** `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` on a single
  frozen fold assignment shared by every comparison, so all models are judged on identical splits.
- **Fit scope.** Every learned transform — median imputation, one-hot encoding, scaling — is fitted
  **inside the training folds** during comparison, and **on the full training set only** at the final
  refit. Test data is used solely for structure checks and final inference; it never informs fitting,
  feature selection, or model choice.
- **Feature policy.** `School` is excluded as a model feature (high cardinality, instability,
  test-only-category and leakage risk). No external data of any kind is used.
- **Leaderboard policy.** The public leaderboard is a post-submission sanity check only; it never
  drives feature, model, preprocessing, or submission decisions.

## 7. Feature set (F2)

- **Base measurements and profile (13):** `Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump,
  Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type, Position_Type, Position`.
- **Missingness flags (7):** one binary flag per physical measurement that can be missing.
- **Availability count (1):** `available_measurement_count` (how many physical measurements a row has).
- **Excluded:** `School` (diagnostic only), `Id`, `Drafted`.

Missingness is informative in this dataset (some measurements are recorded only for certain roles),
so the project models *the pattern of missingness explicitly* rather than letting an imputation
strategy silently encode it.

## 8. Final candidates and submissions

The project produced **two** validated candidates and deliberately **does not declare a single
winner**:

| Candidate | Role | Internal OOF ROC-AUC | Notes |
|---|---|---|---|
| Tuned CatBoost | Primary (warning-heavy) | 0.830321 | Best global out-of-fold score; carries documented slice warnings and lacks a repeated-CV stability audit. |
| Logistic regression (baseline) | Fallback / reference | 0.827082 | Simpler, more stable, reproduces with the standard stack. |

Both candidates were refit on the full training set and produced format-valid 696-row submissions.
Each generated submission is validated against the official contract (header, row count, `Id` set
and order, probability bounds, no missing/duplicate values) and identified by its SHA-256 checksum.
**The choice of which file to submit — and, where multiple submissions are allowed, in what order —
is a manual decision; the last submitted file determines the final ranking.**

## 9. Reproducibility

- Fixed random seed (`42`) for fold generation and model fitting.
- A single frozen fold assignment shared across all comparisons.
- Deterministic, code-only prediction generation — predictions are never edited by hand.
- Every reported number is labelled by provenance (computed live, loaded from a stored artifact, or
  recorded from an accepted project result), so a reader always knows how each figure was obtained.

## 10. Limitations

- The primary candidate (tuned CatBoost) is the strongest on the global out-of-fold score but is
  **warning-heavy**: it underperforms on some role and year slices, and on rows with missing `Age`
  (about one in six test rows), and it was not subjected to a repeated-cross-validation stability
  audit. The simpler logistic-regression candidate is retained precisely as a stable fallback.
- The dataset's unit of observation (possible athlete repetition across years) was probed and found
  not to warrant grouped cross-validation, but it was not exhaustively resolved.
- `School` may carry real signal but was excluded on leakage-risk grounds; recovering it safely is
  left as future work.

## 11. References and AI-assistance disclosure

See [`references.md`](references.md) for the full bibliography and a sober disclosure of the auxiliary
use of generative AI (ChatGPT) for conceptual consultation, coding recommendations, debugging
guidance, and documentation-structure review. All methodological decisions, validation criteria,
modelling choices, and final interpretation are the author's own.

## 12. Data and usage note

The official competition files are included here for course/private execution only and must be used
under the competition's terms. No external athlete, school, ranking, geography, draft-history, or
online-statistics data is used anywhere in this project.
