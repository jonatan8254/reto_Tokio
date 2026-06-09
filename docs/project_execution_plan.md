# Reto Tokio — Integrated Execution Plan v2

**Version:** 2.0  
**Purpose:** Context-efficient, audit-ready workflow for the GCI World NFL Draft Prediction competition.  
**Repository:** `C:\GitHub\reto_Tokio`

---

## 1. Operating Principle

This project follows a **notebook-first, reproducible, traceable, and audit-ready** workflow for the NFL Draft Prediction competition.

Core principle:

> No score matters unless it can be reproduced, explained, validated, and defended under the official competition rules.

The project will be executed through a hybrid methodology:

```text
ChatGPT here = research synthesis, methodological reasoning, prompt design, literature/web review, and phase-specific strategy.
Codex in VS Code = local execution, file editing, notebook work, environment checks, Git traceability, validation checks, and implementation.
```

Codex should not be treated as a long-document research engine by default. Codex should receive **curated context**, specific prompts, and precise phase gates.

---

## 2. Project Goal

Build a competitive, reproducible, and auditable machine learning solution for the NFL Draft Prediction competition.

Task:

```text
Binary classification: predict whether an athlete will be selected in the NFL Draft.
```

Primary metric:

```text
ROC-AUC
```

Main constraints:

```text
Use only official competition data.
Do not use external athlete, school, conference, ranking, geography, draft, or sports-outcome data.
Do not manually label examples.
Do not manually edit prediction values.
Avoid leakage.
Keep all important experiments reproducible.
```

---

## 3. Source Hierarchy

When sources conflict, use this hierarchy:

```text
1. Official README / official competition notebook.
2. Official competition CSV files and sample submission.
3. Official course PDFs, Q&A, and lecture materials.
4. Project documentation created from inspected sources.
5. Methodological books and papers.
6. Library documentation.
7. Web research, only for current technical/library information or methodology, never for external competition data.
```

If a fact cannot be confirmed, write:

```text
Not confirmed yet
```

Do not guess.

---

## 4. Research and Context-Efficiency Policy

### 4.1 General rule

Books and papers should be used as **methodological support**, not as raw context dumped into Codex.

Allowed use:

```text
validation design
leakage prevention
feature engineering methodology
model comparison methodology
hyperparameter optimization discipline
experiment tracking
notebook reproducibility
competition workflow hygiene
```

Forbidden use:

```text
external athlete-level information
school/conference/geography mappings
NFL history
real draft outcomes
external rankings
external sports statistics
```

### 4.2 Who reads what?

Use this division of labor:

```text
ChatGPT:
- Reads and synthesizes long books/papers.
- Performs targeted literature/web review.
- Produces compact research notes.
- Designs phase-specific prompts for Codex.
- Decides what evidence should be passed to Codex.

Codex:
- Reads local project files.
- Executes approved changes.
- Runs notebooks and scripts.
- Updates documentation.
- Checks Git, environment, requirements, and file structure.
- Reads short official course PDFs if they are directly needed.
- Reads targeted book/paper sections only when explicitly approved.
```

### 4.3 Codex PDF reading policy

Codex may read PDFs only under these conditions:

```text
Official short course PDFs:
Allowed when they contain rules, Q&A, baseline workflow, submission workflow, or audit requirements.

Books and long papers:
Do not read fully by default.
Only read targeted sections if approved in the phase prompt.

If Codex believes a book/paper is needed:
1. It must ask for approval.
2. It must specify the exact file.
3. It must specify the exact section/topic.
4. It must explain why that section is necessary for the current phase.
```

### 4.4 Research note files

Research should be converted into compact notes before Codex uses it.

Recommended files:

```text
docs/research_notes_validation.md
docs/research_notes_leakage.md
docs/research_notes_feature_engineering.md
docs/research_notes_tabular_models.md
docs/research_notes_hpo.md
docs/research_notes_reproducibility.md
```

Evidence note format:

```text
Topic:
Source:
Source type:
Main idea:
Application to this challenge:
Risk:
Decision:
Validation method:
Codex instruction:
```

---

## 5. Prompt Execution Methodology

Every phase should normally use two separate prompts:

```text
1. Plan Mode prompt.
2. Implementation prompt.
```

### 5.1 Plan Mode prompt

In Plan Mode, Codex must:

```text
inspect
reason
classify risks
decide whether targeted research is necessary
propose files to modify
propose commands
propose verification checks
stop and ask for approval
```

Plan Mode must not:

```text
modify files
train models
generate submissions
commit changes
move files
delete files
start the next phase
```

### 5.2 Implementation prompt

Implementation starts only after explicit approval.

In Implementation Mode, Codex must:

```text
implement only the approved plan
modify only approved files
run only approved commands
verify the result
produce a phase report
stop before the next phase
```

### 5.3 Phase gate

Every phase ends with:

```text
Phase X is complete. I will not start Phase X+1 until you explicitly confirm.
```

---

## 6. Repository Structure

Current simplified structure:

```text
C:\GitHub\reto_Tokio\
│
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
│
├── data\
│   └── input\
│       ├── train.csv
│       ├── test.csv
│       └── sample_submission.csv
│
├── notebooks\
│   ├── _official\
│   ├── 01_baseline_reproduction.ipynb
│   ├── 02_eda_and_data_contract.ipynb
│   ├── 03_modeling_experiments.ipynb
│   └── 99_final_submission.ipynb
│
├── references\
│   ├── books\
│   ├── papers\
│   └── course_materials\
│
├── docs\
│   ├── challenge_brief.md
│   ├── experiment_notes.md
│   ├── submission_checklist.md
│   ├── project_execution_plan.md
│   └── research_notes_*.md
│
├── outputs\
│   ├── submissions\
│   └── figures\
│
└── logs\
    └── experiment_log.csv
```

Folder logic:

```text
data/input/              Official train/test/submission files.
notebooks/_official/     Original official notebooks. Do not edit.
notebooks/               Working and final notebooks.
references/              Books, papers, slides, tutorials, Q&A, and course materials.
docs/                    Synthesized decisions, notes, plans, and checklists.
outputs/submissions/     Generated CSV submissions.
outputs/figures/         EDA/modeling figures.
logs/                    Experiment tracking.
```

---

## 7. Installed Codex Agents

High-priority agents:

```text
mle-reviewer
python-reviewer
security-reviewer
silent-failure-hunter
doc-updater
```

Agent usage:

```text
mle-reviewer
Review validation strategy, leakage, metrics, model comparison, feature engineering, overfitting, and final model choice.

python-reviewer
Review Python code quality, notebook hygiene, reproducibility, imports, bugs, package compatibility, and maintainability.

security-reviewer
Check before commits, submissions, packaging, or sharing files. Detect secrets, private paths, official data, books, PDFs, ZIPs, large files, and unsafe outputs.

silent-failure-hunter
Detect hidden failures: wrong ID column, wrong target, shape mismatch, NaNs, duplicated rows, submission misalignment, wrong interpreter, missing folders, untracked large files, or silent metric errors.

doc-updater
Update README, challenge brief, research notes, experiment notes, submission checklist, and project documentation.
```

---

## 8. Installed Codex Skills

High-priority skills:

```text
mle-workflow
eval-harness
verification-loop
ai-regression-testing
security-review
```

Medium-high priority skills:

```text
documentation-lookup
nutrient-document-processing
scientific-thinking-literature-review
search-first
strategic-compact
production-audit
```

Skill usage:

```text
mle-workflow
Structure the ML process: baseline, EDA, validation, features, modeling, tuning, ensembling, and final submission.

eval-harness
Define checks before experiments: metric checks, leakage checks, reproducibility checks, submission checks, and data-contract checks.

verification-loop
Use before important submissions, commits, notebook transitions, and phase completion.

ai-regression-testing
Use after changing notebook logic to ensure previous working behavior did not silently break.

security-review
Use before committing, packaging, or submitting.

documentation-lookup
Use for official library documentation: pandas, scikit-learn, XGBoost, LightGBM, CatBoost, Optuna, and Jupyter.

nutrient-document-processing
Use for short official course PDFs and targeted document extraction. Do not use it to read full books unless explicitly approved.

scientific-thinking-literature-review
Use for targeted methodological evidence from books and papers, preferably through compact research notes.

search-first
Use for methodological or library documentation lookups. Do not use it to add external competition data.

strategic-compact
Use to summarize progress, decisions, open questions, experiment results, and next actions.

production-audit
Use near the end for final reproducibility and delivery audit.
```

---

# 9. Integrated Work Plan

The project follows 12 phases.

Each phase includes:

```text
Goal
Research/evidence input
Codex agents and skills
Main activities
Outputs
Exit criteria
Risks
Plan Mode gate
Implementation gate
```

---

## Phase 0 — Rules, Intake, and Competition Contract

### Goal

Understand the official competition before modeling.

### Research/evidence input

Use directly in Codex because these are official and relatively short:

```text
notebooks/_official/README.ipynb
notebooks/_official/baseline_original.ipynb
references/course_materials/tutorials/competition_tutorial.pdf
references/course_materials/qa/QA.pdf
references/course_materials/notes/GCI_sesion7.pdf
references/course_materials/notes/hackaton.pdf
```

Questions:

```text
What is the target?
What is the ID column?
What is the metric?
What is the required submission format?
What data is allowed?
What data is prohibited?
What does the baseline do?
What files are official?
What can be audited?
```

### Codex skills/agents

```text
mle-workflow
eval-harness
nutrient-document-processing
mle-reviewer
doc-updater
silent-failure-hunter
```

### Main activities

```text
Inspect official notebooks.
Inspect train/test/sample_submission.
Document official rules.
Identify target and metric.
Identify possible leakage risks.
Define the competition contract.
Verify official course PDFs with local PDF tools if needed.
```

### Outputs

```text
docs/challenge_brief.md
docs/submission_checklist.md
```

### Exit criteria

```text
We can explain the competition task, target, metric, allowed data, prohibited data, baseline workflow, audit expectations, and submission format.
```

### Risks

```text
Starting modeling before understanding rules.
Using external data accidentally.
Optimizing the wrong metric.
Not reading official PDF/Q&A rules when they matter.
```

---

## Phase 1 — Operational Setup, Codex Setup, and Traceability

### Goal

Make the repository reproducible and ready for controlled experimentation.

### Research/evidence input

Default behavior:

```text
Do not read full books in Codex during Phase 1.
Use only local project files unless a specific book section is approved.
```

Optional methodological support handled by ChatGPT:

```text
python_for_data_analysis_3rd_edition_2022
hands_on_machine_learning_sklearn_pytorch_2026
the_kaggle_book_2nd_edition_2025
```

Purpose:

```text
Use books only for methodology, notebook organization, validation discipline, and reproducibility.
Do not extract external competition features from books.
```

### Codex skills/agents

```text
python-reviewer
security-reviewer
doc-updater
strategic-compact
verification-loop
security-review
silent-failure-hunter
```

### Main activities

```text
Check Python environment.
Confirm Python 3.13.13 through .venv.
Check requirements.txt.
Check .gitignore.
Confirm data/input exists.
Confirm notebooks/_official exists.
Confirm logs/experiment_log.csv exists.
Confirm outputs/submissions exists.
Inspect Git status.
Classify files into track/ignore/review/do-not-commit.
Propose clean staging plan.
Do not commit unless explicitly approved.
```

### Outputs

```text
README.md
requirements.txt
.gitignore
logs/experiment_log.csv
AGENTS.md
docs/project_execution_plan.md
```

### Exit criteria

```text
Repository can be opened in VS Code.
Codex understands AGENTS.md.
Python interpreter is correct.
Git ignores official CSVs, PDFs, ZIPs, outputs, and .venv.
Trackable project docs are identified.
No restricted or large files are staged.
```

### Risks

```text
Committing official data, books, PDFs, ZIPs, or large files.
Using wrong Python environment.
Working outside the repository root.
Accidentally tracking .venv or outputs.
Letting Codex read long books unnecessarily.
```

---

## Phase 2 — Baseline Reproduction

### Goal

Reproduce the official baseline and generate the first valid submission.

### Research/evidence input

Codex may read these because they are official and directly relevant:

```text
notebooks/_official/baseline_original.ipynb
references/course_materials/tutorials/competition_tutorial.pdf
references/course_materials/notes/GCI_sesion7.pdf
docs/challenge_brief.md
docs/submission_checklist.md
```

No book/paper reading is needed unless a specific baseline issue appears.

### Codex skills/agents

```text
mle-workflow
eval-harness
verification-loop
python-reviewer
silent-failure-hunter
mle-reviewer
```

### Main activities

```text
Open notebooks/01_baseline_reproduction.ipynb.
Adapt paths to data/input/.
Run all cells.
Generate baseline submission.
Save submission under outputs/submissions/.
Register baseline in logs/experiment_log.csv.
Verify submission shape, ID order, probability range, and reproducibility.
```

### Outputs

```text
notebooks/01_baseline_reproduction.ipynb
outputs/submissions/submission_001_baseline.csv
logs/experiment_log.csv updated
```

### Exit criteria

```text
A valid CSV is generated.
The notebook runs from top to bottom.
Baseline score is recorded.
Submission checklist passes.
```

### Risks

```text
Wrong path.
Wrong submission columns.
Notebook depends on hidden state.
CSV saved in the wrong folder.
Submitting before checks.
```

---

## Phase 3 — Data Contract and Initial EDA

### Goal

Understand the dataset technically before creating features.

### Research/evidence input

Codex can use course slides if needed, but should not read long books by default.

```text
references/course_materials/slides/lec3_slides.pdf
references/course_materials/slides/lec4_slides.pdf
docs/challenge_brief.md
docs/submission_checklist.md
```

ChatGPT may prepare compact EDA/data-contract notes from books if needed.

Questions:

```text
What is the unit of observation?
What is the target distribution?
What columns exist in train and test?
What columns are numeric?
What columns are categorical?
What columns have missing values?
What columns have high cardinality?
Are there suspicious columns?
Are train and test structurally aligned?
```

### Codex skills/agents

```text
mle-workflow
eval-harness
python-reviewer
silent-failure-hunter
mle-reviewer
```

### Main activities

```text
Create/update notebooks/02_eda_and_data_contract.ipynb.
Load train/test/sample_submission.
Inspect shape, columns, dtypes.
Inspect missing values.
Inspect target imbalance.
Inspect cardinality.
Inspect train/test column alignment.
Inspect possible ID columns.
Inspect submission format.
Document only structural and EDA findings.
```

### Outputs

```text
notebooks/02_eda_and_data_contract.ipynb
docs/experiment_notes.md updated
outputs/figures/EDA figures if useful
```

### Exit criteria

```text
We know target, ID, feature groups, missingness, cardinality, class imbalance, and train/test structure.
```

### Risks

```text
Using test target information.
Overinterpreting test distributions.
Dropping columns without evidence.
Creating features too early.
```

---

## Phase 4 — Directed Research and Methodological Knowledge Base

### Goal

Use books, papers, course materials, library documentation, and targeted web research to define the modeling strategy.

This phase is the main research phase, but research is still context-efficient.

### Research/evidence input

Primary research is done here in ChatGPT and then passed to Codex as compact notes.

Potential sources:

```text
references/books/the_kaggle_book_2nd_edition_2025.pdf
references/books/the_kaggle_workbook_2023.pdf
references/books/introduction_to_statistical_learning_python.pdf
references/books/hands_on_machine_learning_sklearn_pytorch_2026.pdf
references/books/feature_engineering_and_selection_kuhn_johnson_2021.pdf
references/books/machine_learning_with_lightgbm_python_2023.pdf

references/papers/on_leakage_in_ml_pipelines.pdf
references/papers/leakage_and_reproducibility_crisis_ml_science.pdf
references/papers/cawley_talbot_model_selection_overfitting.pdf
references/papers/feature_selection_survey_2024.pdf
references/papers/xgboost_scalable_tree_boosting_system.pdf
references/papers/lightgbm_highly_efficient_gbdt.pdf
references/papers/catboost_unbiased_boosting_categorical_features.pdf
references/papers/optuna_next_generation_hpo_framework.pdf
```

Research questions:

```text
What validation strategy is appropriate for binary tabular classification?
How should ROC-AUC be interpreted?
How can leakage happen in preprocessing and feature engineering?
How should categorical variables be encoded?
When should CatBoost, LightGBM, or XGBoost be used?
How should hyperparameter optimization be controlled?
How should public leaderboard feedback be handled?
When are ensembles useful?
```

### Codex skills/agents

```text
scientific-thinking-literature-review
nutrient-document-processing
documentation-lookup
search-first
mle-reviewer
doc-updater
strategic-compact
```

### Main activities

```text
Use ChatGPT to synthesize long sources into compact research notes.
Let Codex read only the compact research notes unless targeted source verification is approved.
Create docs/research_notes_*.md.
Convert research into actionable modeling decisions.
Document risks and validation methods.
```

### Outputs

```text
docs/research_notes_validation.md
docs/research_notes_leakage.md
docs/research_notes_feature_engineering.md
docs/research_notes_tabular_models.md
docs/research_notes_hpo.md
docs/research_notes_reproducibility.md
docs/experiment_notes.md updated
```

### Exit criteria

```text
We have evidence-based decisions for validation, leakage prevention, feature engineering, model selection, tuning, and submission strategy.
Codex has compact notes instead of full-book context.
```

### Risks

```text
Using literature as decoration.
Extracting external sports knowledge.
Letting research delay implementation.
Overloading Codex with full books.
```

---

## Phase 5 — Final Methodological Plan Before Modeling

### Goal

Convert rules + EDA + evidence notes into an executable modeling plan.

### Research/evidence input

Use compact sources:

```text
docs/challenge_brief.md
docs/submission_checklist.md
docs/experiment_notes.md
docs/research_notes_*.md
notebooks/02_eda_and_data_contract.ipynb
```

Do not read books/papers unless a specific gap remains.

### Codex skills/agents

```text
strategic-compact
mle-workflow
mle-reviewer
eval-harness
doc-updater
```

### Main activities

```text
Define validation protocol.
Define initial preprocessing.
Define safe feature engineering candidates.
Define candidate model families.
Define what we will not do.
Define experiment naming convention.
Define submission naming convention.
Define first modeling experiment sequence.
```

### Outputs

```text
docs/experiment_notes.md updated
docs/submission_checklist.md updated
logs/experiment_log.csv ready
```

### Exit criteria

```text
There is a clear sequence of experiments before modifying 03_modeling_experiments.ipynb deeply.
```

### Risks

```text
Jumping directly to Optuna.
Testing too many things at once.
No experimental hypothesis.
Ignoring research notes.
```

---

## Phase 6 — Leakage-Safe Preprocessing and Local Validation

### Goal

Build the first reliable validation pipeline.

### Research/evidence input

Use compact notes first:

```text
docs/research_notes_validation.md
docs/research_notes_leakage.md
docs/research_notes_reproducibility.md
docs/submission_checklist.md
```

Only read original books/papers if a precise implementation gap appears.

### Codex skills/agents

```text
mle-workflow
eval-harness
mle-reviewer
python-reviewer
silent-failure-hunter
ai-regression-testing
verification-loop
```

### Main activities

```text
Create/update notebooks/03_modeling_experiments.ipynb.
Implement StratifiedKFold.
Use ROC-AUC.
Define numeric/categorical preprocessing.
Use fit only on training folds.
Compare with baseline.
Generate OOF predictions if useful.
Register experiments.
```

### Outputs

```text
notebooks/03_modeling_experiments.ipynb
logs/experiment_log.csv updated
docs/experiment_notes.md updated
```

### Exit criteria

```text
We can compare models locally with stable CV ROC-AUC.
```

### Risks

```text
Preprocessing fitted on full train before CV.
Feature selection outside CV.
Changing folds between experiments.
```

---

## Phase 7 — Feature Engineering, Feature Selection, and Ablations

### Goal

Improve signal using only official internal data.

### Research/evidence input

Use compact notes first:

```text
docs/research_notes_feature_engineering.md
docs/research_notes_leakage.md
docs/research_notes_validation.md
references/course_materials/slides/lec8_slides.pdf
references/course_materials/readings/Lectura Feature Engineering.pdf
```

Feature families:

```text
missing indicators
safe numeric transformations
safe ratios
position-based internal interactions
age/year internal interactions
rare category grouping
frequency/count encoding
one-hot encoding for low-cardinality variables
out-of-fold target encoding only if justified and implemented safely
```

### Codex skills/agents

```text
mle-workflow
mle-reviewer
python-reviewer
eval-harness
ai-regression-testing
scientific-thinking-literature-review
```

### Main activities

```text
Add features in blocks.
Run ablation tests.
Record CV mean and std.
Reject features that increase variance or look suspicious.
Document feature rationale.
```

### Outputs

```text
feature block notes in docs/experiment_notes.md
logs/experiment_log.csv updated
outputs/figures/feature diagnostics if useful
```

### Exit criteria

```text
We know which feature blocks help, which hurt, and which are suspicious.
```

### Risks

```text
Feature explosion.
Target encoding leakage.
External sports/domain knowledge leakage.
Overfitting to CV.
```

---

## Phase 8 — Model Comparison

### Goal

Compare model families under the same validation strategy.

### Research/evidence input

Use compact notes first:

```text
docs/research_notes_tabular_models.md
docs/research_notes_validation.md
docs/research_notes_leakage.md
```

Candidate models:

```text
Logistic Regression
Random Forest
ExtraTrees
HistGradientBoosting
XGBoost
LightGBM
CatBoost
```

### Codex skills/agents

```text
mle-workflow
mle-reviewer
python-reviewer
eval-harness
silent-failure-hunter
documentation-lookup
```

### Main activities

```text
Compare models with identical folds.
Use ROC-AUC mean and std.
Keep baseline visible.
Track training time.
Save candidate submissions only for meaningful improvements.
```

### Outputs

```text
model comparison section in notebooks/03_modeling_experiments.ipynb
logs/experiment_log.csv updated
candidate submissions in outputs/submissions/
```

### Exit criteria

```text
We identify 2-3 strong model candidates.
```

### Risks

```text
Tuning too early.
Choosing a model from one lucky fold.
Ignoring simple baselines.
```

---

## Phase 9 — Error Analysis, Sanity Checks, and Model Review

### Goal

Determine whether improvements are real and defensible.

### Research/evidence input

Use compact notes first:

```text
docs/research_notes_validation.md
docs/research_notes_leakage.md
docs/research_notes_reproducibility.md
docs/experiment_notes.md
```

### Codex skills/agents

```text
mle-reviewer
silent-failure-hunter
verification-loop
ai-regression-testing
strategic-compact
```

### Main activities

```text
Compare fold stability.
Inspect prediction distributions.
Check feature importance.
Check suspiciously dominant variables.
Check train/test alignment.
Check submission alignment.
Check if leaderboard and CV disagree strongly.
Run ablations on top features.
```

### Outputs

```text
docs/experiment_notes.md updated
sanity check notes
logs/experiment_log.csv updated
```

### Exit criteria

```text
We can explain why a model improved and why it is not obviously leaking.
```

### Risks

```text
Trusting leaderboard jumps blindly.
Keeping suspicious features.
Ignoring CV variance.
```

---

## Phase 10 — Controlled Hyperparameter Optimization and Ensembles

### Goal

Improve strong candidates without overfitting.

### Research/evidence input

Use compact notes first:

```text
docs/research_notes_hpo.md
docs/research_notes_tabular_models.md
docs/research_notes_validation.md
docs/research_notes_leakage.md
```

### Codex skills/agents

```text
mle-workflow
eval-harness
mle-reviewer
python-reviewer
ai-regression-testing
verification-loop
```

### Main activities

```text
Tune only 1-3 strong candidates.
Use controlled search spaces.
Use fixed seeds.
Avoid huge trial counts initially.
Save best parameters.
Revalidate tuned models.
Create simple ensembles only if OOF predictions show useful diversity.
```

### Outputs

```text
best parameter notes in docs/experiment_notes.md
candidate tuned submissions
candidate ensemble submissions
logs/experiment_log.csv updated
```

### Exit criteria

```text
Tuning or ensembling improves CV without suspicious instability.
```

### Risks

```text
Overfitting to CV.
Using leaderboard as objective.
Too many trials.
Overly complex ensemble.
```

---

## Phase 11 — Strategic Submissions and Final Package

### Goal

Submit strong candidates strategically and prepare final reproducible delivery.

### Research/evidence input

Use:

```text
references/course_materials/tutorials/competition_tutorial.pdf
references/course_materials/qa/QA.pdf
docs/submission_checklist.md
docs/experiment_notes.md
logs/experiment_log.csv
```

No long book/paper reading should be needed.

### Codex skills/agents

```text
verification-loop
production-audit
security-reviewer
security-review
mle-reviewer
python-reviewer
silent-failure-hunter
doc-updater
```

### Main activities

```text
Generate final candidate submissions.
Avoid excessive probing.
Record leaderboard scores.
Select final model using CV + leaderboard sanity.
Create/update notebooks/99_final_submission.ipynb.
Run notebook top-to-bottom.
Generate final submission automatically.
Review .gitignore.
Review no external data used.
Review no secrets/private paths.
```

### Outputs

```text
notebooks/99_final_submission.ipynb
outputs/submissions/final_submission.csv
README.md updated
docs/submission_checklist.md completed
logs/experiment_log.csv final
```

### Exit criteria

```text
Final notebook runs from top to bottom.
Final CSV is generated automatically.
Experiment is recorded.
Submission is reproducible.
No forbidden data used.
```

### Risks

```text
Submitting the wrong CSV.
Final notebook depends on hidden state.
Files missing from final package.
Forgetting the last submitted file is what counts.
```

---

# 10. Experiment Rules

Every important experiment must answer:

```text
What changed?
Why should it help?
What is the expected ROC-AUC impact?
What leakage risk exists?
How will it be validated?
What files changed?
```

Every important experiment must be logged in:

```text
logs/experiment_log.csv
```

Minimum columns:

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

---

# 11. Submission Rules

Generate submissions only when:

```text
[ ] The experiment has a clear hypothesis.
[ ] CV ROC-AUC improved or gave useful evidence.
[ ] The notebook generating it is saved.
[ ] The CSV was generated automatically.
[ ] Prediction shape matches sample_submission.
[ ] ID alignment is checked.
[ ] No NaNs exist.
[ ] No external data was used.
[ ] The experiment is logged.
```

Suggested naming:

```text
submission_001_baseline.csv
submission_002_sklearn_pipeline.csv
submission_003_lgbm_features_v1.csv
submission_004_catboost_features_v2.csv
submission_005_ensemble_final.csv
```

---

# 12. Final Checklist

Before final delivery:

```text
[ ] Official baseline was reproduced.
[ ] First valid submission was generated.
[ ] Target and metric are documented.
[ ] Data contract is documented.
[ ] EDA is documented.
[ ] Validation uses ROC-AUC.
[ ] Validation is stratified or otherwise justified.
[ ] Seeds are fixed.
[ ] No external data was used.
[ ] No manual labels were created.
[ ] No manual prediction editing was done.
[ ] Preprocessing does not fit on test.
[ ] Feature engineering is documented.
[ ] Model comparison is logged.
[ ] Tuning is controlled.
[ ] Ensemble, if used, is justified.
[ ] Every important submission has an experiment log entry.
[ ] Final notebook runs top-to-bottom.
[ ] Final submission is generated automatically.
[ ] Final files are audited.
```

---

# 13. Standard Codex Phase Prompt Pattern

Each phase prompt should follow this pattern:

```text
1. State current phase.
2. State that Codex is in Plan Mode.
3. Read AGENTS.md and docs/project_execution_plan.md.
4. Read only phase-relevant docs.
5. State allowed files.
6. State forbidden actions.
7. State required skills/agents.
8. Ask Codex to decide whether targeted research is needed.
9. Ask Codex to produce a plan only.
10. Require approval gate.
```

Implementation prompt pattern:

```text
1. Reference approved plan.
2. Allow only approved changes.
3. Run approved commands.
4. Verify outputs.
5. Report changed files.
6. Stop before next phase.
```

---

# 14. First Codex Prompt

Use this prompt in VS Code/Codex only before starting a new phase or when the state is uncertain:

```text
Read AGENTS.md and docs/project_execution_plan.md. Inspect the project structure. Do not modify files yet.

Confirm:
1. The available folders.
2. The official data files in data/input/.
3. The official notebooks in notebooks/_official/.
4. The current working notebooks.
5. The available references in references/.
6. The experiment log in logs/.

Then propose the safest next phase-specific step. Do not start implementation until approved.
```

---

# 15. Execution Philosophy

The execution philosophy is:

```text
Use ChatGPT here to research, synthesize, design prompts, and curate evidence.
Use Codex to implement approved changes locally.
Use ECC skills to structure and verify.
Use agents to review methodology, code, security, and silent failures.
Use literature as compact evidence, not raw context overload.
Use notebooks to experiment.
Use logs to preserve traceability.
Use verification before every important submission.
Use phase gates to prevent uncontrolled scope creep.
```

Final operating sentence:

> ChatGPT researches and curates, Codex implements, ECC structures and audits, literature informs decisions, validation protects against illusion, and the final notebook proves reproducibility.
