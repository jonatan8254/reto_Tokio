# HPO

## Purpose
Block premature hyperparameter optimization and define future Optuna/HPO activation gates.

## Project context from Phase 3
Evidence:
- Phase 3 selected no final features, no preprocessing policy, no validation policy, and no model family.
- Phase 3 risk register includes overfitting to CV, model-selection bias, public leaderboard overuse, HPO prematurity, and features derived outside folds.
- PDF audit gate confirms reviewed HPO/model-selection sources: `machine_learning_with_lightgbm_python_2023.pdf`, `the_kaggle_book_2nd_edition_2025.pdf`, `feature_engineering_modern_ml_2024.pdf`, `hands_on_machine_learning_sklearn_pytorch_2026.pdf`, `cawley_talbot_model_selection_overfitting.pdf`, `optuna_next_generation_hpo_framework.pdf`.

## Methodological evidence
Evidence:
- Reviewed model-selection literature supports that HPO can overfit the validation criterion.
- Reviewed Optuna source supports Optuna as a future HPO framework, but not before validation and model candidates are stable.
- Reviewed Kaggle-oriented sources support disciplined tuning after baseline, validation, and feature workflow are reliable.

Inference:
- HPO is a late-phase optimization tool, not a substitute for validation, feature ablations, or model comparison.
- Repeated tuning on the same CV can become implicit training on validation feedback.

## Inference for this challenge
Inference:
- Because folds, preprocessing, feature blocks, and model candidates are not frozen yet, Optuna is blocked.
- HPO should improve strong candidates, not rescue unstable methodology.

## Decision
Decision:
Optuna/HPO is not allowed until all conditions are met:
1. validation protocol frozen;
2. leakage-safe pipeline implemented;
3. feature blocks tested by ablation;
4. 1-3 model candidates selected from fair comparison;
5. `experiment_log.csv` schema active;
6. no unresolved leakage issue;
7. no dependence on public leaderboard.

## Techniques to consider
Decision:
Future Phase 10 Optuna design:
- Use `direction="maximize"` for ROC-AUC.
- Use fixed sampler seed.
- Prefer sequential deterministic runs before parallel runs.
- Use conservative `n_trials` at first.
- Use pruning only when intermediate metrics are meaningful and correctly reported.
- Keep search spaces small and justifiable.
- Do not tune every model aggressively.
- Do not reuse public leaderboard for tuning.
- Record all trials or summarize reproducibly.

## Techniques to avoid for now
Decision:
- No Optuna runs in Phase 4B, Phase 5, Phase 6, or Phase 7.
- No `GridSearchCV` / `RandomizedSearchCV` for broad search before validation gates.
- No tuning based on public leaderboard.
- No tuning many model families at once.
- No parallel nondeterministic tuning until reproducibility rules are defined.

## Leakage risks
Evidence:
- Model selection itself is a training process.
- Repeated tuning on the same CV increases selection bias.
- Nested CV is conceptually cleaner but may be expensive.

Inference:
- If nested CV is not used, the project must compensate with conservative search, fixed logging, slice diagnostics, and clear reporting.

## Validation requirements
Decision:
- HPO objective must be fixed-fold mean ROC-AUC.
- HPO report must include fold scores, std, slice metrics when feasible, search space, seed, trials, and decision.
- Any HPO improvement must be compared to the untuned candidate on the same folds.

## Codex instructions for future phases
Decision:
- Phase 5: document HPO gates.
- Phase 6: do not tune.
- Phase 7: do not tune feature blocks with HPO.
- Phase 8: select 1-3 candidates through fair comparison.
- Phase 9: sanity-check candidate robustness before tuning.
- Phase 10: run controlled HPO only after gates pass.
- Phase 11: do not choose final submission by HPO/leaderboard probing.

## Open questions
- Whether nested CV is computationally feasible: Not confirmed yet.
- Which 1-3 candidates will be eligible for HPO: Not confirmed yet.
- Final HPO budget: Not confirmed yet.

## Phase impact
Decision:
- Primary impact: Phase 10.
- Blocking guardrails: Phase 5, Phase 6, Phase 7, Phase 8, Phase 9, Phase 11.
