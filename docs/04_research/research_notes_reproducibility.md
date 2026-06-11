# Reproducibility

## Purpose
Define notebook-first, audit-ready reproducibility requirements for future modeling, submissions, and final package work.

## Project context from Phase 3
Evidence:
- Project is notebook-first and audit-oriented.
- Official notebooks in `notebooks/_official/` must not be modified.
- Every important submission must be reproducible from code.
- Phase 3 notebook executed as an EDA/data-contract report and did not train models or generate submissions.
- PDF audit gate confirms reviewed reproducibility sources: `leakage_and_reproducibility_crisis_ml_science.pdf`, `the_kaggle_book_2nd_edition_2025.pdf`, `feature_engineering_modern_ml_2024.pdf`, `fundamentals_of_data_engineering_2022.pdf`, `on_leakage_in_ml_pipelines.pdf`, `hands_on_machine_learning_sklearn_pytorch_2026.pdf`.

## Methodological evidence
Evidence:
- Reviewed reproducibility and leakage sources support explicit reporting of data, preprocessing, validation, seeds, model selection, and audit checks.
- Reviewed workflow sources support notebooks only when they run cleanly, have stable paths, and produce traceable outputs.

Inference:
- Reproducibility is part of competition compliance, not cosmetic documentation.
- Notebook hidden state, manual prediction editing, and unlogged submissions are direct audit risks.

## Inference for this challenge
Inference:
- The final solution must be regenerated from official files with relative paths and fixed seeds.
- Any submitted file must link back to a notebook/script, experiment log row, validation evidence, and leakage checks.

## Decision
Decision:
- Notebook-first workflow.
- Clean kernel run.
- Use relative paths.
- Fixed seeds.
- Keep versioned docs.
- Maintain experiment log.
- Maintain submission traceability.
- No manual prediction editing.
- Prohibit hidden state.
- Prohibit modifying official notebooks.

## Techniques to consider
Decision:
- Reproducible notebooks from repo root.
- Stable random seed policy.
- Experiment log rows for important experiments.
- Saved outputs under `outputs/`.
- Diff/status checks before staging.
- Submission checklist before any candidate CSV.

## Techniques to avoid for now
Decision:
- No hidden notebook state.
- No local absolute paths in deliverable notebooks.
- No manual CSV edits.
- No unlogged submissions.
- No modifying raw official data or official notebooks.
- No committing PDFs, official CSVs, ZIPs, generated outputs, or `.venv`.

## Leakage risks
Inference:
- Reproducibility failures can hide leakage because an experiment cannot be re-run to inspect fold fitting, preprocessing, or submission generation.

## Validation requirements
Decision:
Required experiment log fields:
- `experiment_id`
- `date`
- `phase`
- `notebook_or_script`
- `git_commit_or_status`
- `data_version`
- `fold_strategy`
- `random_seed`
- `feature_block`
- `preprocessing_summary`
- `model_family`
- `model_params_summary`
- `hpo_status`
- `cv_auc_mean`
- `cv_auc_std`
- `fold_scores`
- `slice_metrics_available`
- `leakage_checks_passed`
- `submission_created`
- `submission_path`
- `public_lb_score_if_submitted`
- `notes`
- `decision`

Required audit checklist:
- Can the notebook run top-to-bottom?
- Can predictions be regenerated?
- Are all random seeds fixed?
- Are official notebooks untouched?
- Are data files untouched?
- Was test used only for allowed operations?
- Were preprocessing steps fitted inside folds?
- Were submissions generated automatically?
- Is the submitted file linked to an experiment?

## Codex instructions for future phases
Decision:
- Phase 5: freeze reproducibility checklist and experiment log schema.
- Phase 6: make the validation harness reproducible.
- Phase 7: log every feature ablation.
- Phase 8: log every model comparison.
- Phase 9: preserve OOF diagnostics and error analysis.
- Phase 10: log HPO trials or summaries reproducibly.
- Phase 11: final notebook must run top-to-bottom and generate final submission automatically.

## Open questions
- Final experiment log schema migration needs: Not confirmed yet.
- Whether additional environment lock files are needed: Not confirmed yet.

## Phase impact
Decision:
- All future phases: Phase 5 through Phase 11.
