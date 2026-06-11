# Challenge Brief

Phase: 0 - Rules, Intake, and Competition Contract

## Purpose

Build a notebook-first, reproducible, auditable machine learning solution for the GCI World NFL Draft Prediction competition while following the official competition rules.

This phase documents the competition contract only. It does not include modeling, tuning, feature engineering, or submission generation.

## Confirmed Competition Facts

| Item | Confirmed value | Source |
|---|---|---|
| Competition | NFL Draft Prediction, GCI World 2026 April | `notebooks/_official/README.ipynb` |
| Task | Predict whether an athlete will be selected in the NFL Draft | `notebooks/_official/README.ipynb` |
| Supervised task type | Binary classification | `AGENTS.md`, `notebooks/_official/README.ipynb` |
| Target column | `Drafted` | `data/input/train.csv`, `notebooks/_official/README.ipynb` |
| Target meaning | `1` means drafted; `0` means not drafted | `notebooks/_official/README.ipynb` |
| ID column | `Id` | `data/input/train.csv`, `data/input/test.csv`, `data/input/sample_submission.csv` |
| Primary metric | AUC / ROC-AUC using predicted probabilities | `notebooks/_official/README.ipynb`, `AGENTS.md` |
| Submission columns | `Id`, `Drafted` | `data/input/sample_submission.csv`, `notebooks/_official/README.ipynb` |
| Submission row count | 696 rows | `data/input/test.csv`, `data/input/sample_submission.csv` |
| Public leaderboard | Scored on a subset of test data during the competition | `notebooks/_official/README.ipynb` |
| Private leaderboard | Final scoring uses the full test data | `notebooks/_official/README.ipynb` |
| Final ranking file | Last submitted file determines final ranking | `notebooks/_official/README.ipynb` |
| Code audit expectation | High private leaderboard participants may be asked for reproducible Google Colab code | `notebooks/_official/README.ipynb` |
| Submission workflow | Run `baseline.ipynb` to create `submission.csv`, download it, and submit it through the competition submission page | `references/course_materials/tutorials/competition_tutorial.pdf` |
| Baseline workflow | Official baseline notebook can be used as the starting point and customized for model improvements | `references/course_materials/tutorials/competition_tutorial.pdf`, `notebooks/_official/baseline_original.ipynb` |
| Baseline model information | Baseline uses `RandomForestClassifier` with 5-fold cross-validation and has approximate AUC around 0.81 | `references/course_materials/notes/GCI_sesion7.pdf`, `notebooks/_official/baseline_original.ipynb` |
| PDF timing confirmation | Competition launched April 29; ranking announcement is around July 8 | `references/course_materials/notes/GCI_sesion7.pdf`, `notebooks/_official/README.ipynb` |

## Official Files

Official competition data files inspected in Phase 0:

- `data/input/train.csv`
- `data/input/test.csv`
- `data/input/sample_submission.csv`

Official course and competition materials inspected or attempted:

- `notebooks/_official/README.ipynb`
- `notebooks/_official/baseline_original.ipynb`
- `references/course_materials/tutorials/competition_tutorial.pdf`
- `references/course_materials/qa/QA.pdf`
- `references/course_materials/notes/GCI_sesion7.pdf`
- `references/course_materials/notes/hackaton.pdf`

Phase 0B retried local PDF extraction with `.venv` Python 3.13.13 and `pypdf`. The extraction was reliable enough to confirm competition-relevant facts from `competition_tutorial.pdf`, `QA.pdf`, and `GCI_sesion7.pdf`. `hackaton.pdf` was readable but did not add useful competition-contract information.

PDF-confirmed additions:

- `competition_tutorial.pdf` confirms the practical submission workflow: download/upload the `competition` folder, run `baseline.ipynb`, create `submission.csv`, download it, and submit the CSV through the competition submission page.
- `QA.pdf` reinforces that external data usage is prohibited, code may be checked, and external data can invalidate ranking.
- `GCI_sesion7.pdf` reinforces that code must be clean, deterministic, seed-controlled, and auditable; non-compliant entries may be disqualified regardless of leaderboard position.
- `GCI_sesion7.pdf` confirms the baseline model family and validation shape at a high level: `RandomForestClassifier`, 5-fold cross-validation, and approximate AUC around 0.81.

## Data Structure

### `train.csv`

- Shape: 2,781 rows, 16 columns.
- Columns: `Id`, `Year`, `Age`, `School`, `Height`, `Weight`, `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`, `Player_Type`, `Position_Type`, `Position`, `Drafted`.
- Target column candidate confirmed: `Drafted`.
- ID column candidate confirmed: `Id`.
- Confirmed target values: `0.0`, `1.0`.
- Class balance: `0.0` = 978 rows; `1.0` = 1,803 rows.

Missing values:

| Column | Missing rows |
|---|---:|
| `Age` | 435 |
| `Sprint_40yd` | 145 |
| `Vertical_Jump` | 554 |
| `Bench_Press_Reps` | 721 |
| `Broad_Jump` | 581 |
| `Agility_3cone` | 970 |
| `Shuttle` | 912 |

### `test.csv`

- Shape: 696 rows, 15 columns.
- Columns match `train.csv` after removing `Drafted`.
- ID column candidate confirmed: `Id`.

Missing values:

| Column | Missing rows |
|---|---:|
| `Age` | 115 |
| `Sprint_40yd` | 29 |
| `Vertical_Jump` | 143 |
| `Bench_Press_Reps` | 184 |
| `Broad_Jump` | 147 |
| `Agility_3cone` | 247 |
| `Shuttle` | 228 |

### `sample_submission.csv`

- Shape: 696 rows, 2 columns.
- Columns: `Id`, `Drafted`.
- Row count matches `test.csv`.
- `Id` order matches `test.csv`.
- Example prediction values are `0.5`.

## Allowed Data

Use only the official competition files stored in `data/input/`.

The official README states that analysis must rely only on the provided training and test datasets. Project rules additionally restrict work to the official competition files under `data/input/`.

## Prohibited Actions

- Do not use external athlete data.
- Do not use external school, conference, ranking, geography, draft-history, or sports-outcome data.
- Do not manually label examples.
- Do not manually edit prediction values.
- Do not manipulate submissions outside reproducible code.
- Do not fit preprocessing, imputation, encoding, feature selection, target encoding, model selection, or hyperparameter tuning on test data.
- Do not use the public leaderboard as the main validation system.
- Do not modify official notebooks in `notebooks/_official/`.
- Do not start modeling before the competition contract and baseline reproduction steps are complete.

## Reproducibility Requirements

- Every important submission must be generated automatically from code.
- Random seeds must be fixed whenever randomness is involved.
- The final notebook must run top-to-bottom without hidden state.
- Code and predictions must be consistent enough to support audit if requested.
- Non-compliant entries may be disqualified even if they rank highly.
- Important experiments must be logged in `logs/experiment_log.csv`.
- Candidate and final submissions must be saved under `outputs/submissions/`.

## Phase 0 Stop Rule

Phase 0 ends after the competition contract and submission checklist are documented. Phase 1 must not start until explicitly approved.
