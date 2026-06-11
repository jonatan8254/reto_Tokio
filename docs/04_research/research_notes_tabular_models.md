# Tabular Models

## Purpose
Define the future tabular model shortlist and comparison guardrails without implementing or selecting a model family.

## Project context from Phase 3
Evidence:
- Task is small-to-medium tabular binary classification with numeric physical metrics, categorical role fields, missingness, and high-cardinality `School`.
- Baseline context already exists with `RandomForestClassifier`; it is a reference point, not a final choice.
- Phase 3 found role-aware signal, measurement availability, and high-cardinality categorical risk.
- No model family was selected in Phase 3.
- PDF audit gate confirms reviewed tabular-model sources: `machine_learning_with_lightgbm_python_2023.pdf`, `closer_look_deep_learning_tabular_datasets.pdf`, `the_kaggle_book_2nd_edition_2025.pdf`, `catboost_unbiased_boosting_categorical_features.pdf`, `the_kaggle_workbook_2023.pdf`, `xgboost_scalable_tree_boosting_system.pdf`, `lightgbm_highly_efficient_gbdt.pdf`.

## Methodological evidence
Evidence:
- Reviewed tabular sources support gradient boosted decision trees as strong tabular candidates.
- Reviewed deep-tabular benchmark source indicates deep tabular models are not first priority unless boosted/tree baselines plateau and time allows.
- Reviewed CatBoost/LightGBM/XGBoost sources support considering missing and categorical handling as model-specific contracts, not magic leakage bypasses.

Inference:
- Model comparison must wait until validation and feature-block ablations are stable.
- A short shortlist is safer than a model zoo.

## Inference for this challenge
Inference:
- The next serious model shortlist should include interpretable sanity checks, scikit-learn candidates, and external GBDT candidates only after Phase 6/7 gates.
- `School` and missingness sensitivity must be part of model review because they are central project risks.

## Decision
Decision:
- Do not compare models before Phase 6 validation harness exists.
- Do not compare models before Phase 7 feature blocks are defined.
- Use identical folds, metrics, OOF/slice diagnostics, and logging.
- Keep baseline models simple before tuning.

## Techniques to consider
Decision:
Future shortlist:
1. Logistic Regression:
   - interpretable baseline;
   - requires imputation and encoding;
   - useful sanity check.
2. RandomForestClassifier:
   - already reproduced as baseline context;
   - reference point, not necessarily final model.
3. HistGradientBoostingClassifier:
   - strong scikit-learn tabular candidate;
   - can handle missing values natively depending on setup;
   - useful bridge before external GBDT libraries.
4. XGBoost:
   - strong general GBDT candidate;
   - good for sparse/encoded data;
   - categorical support must be handled carefully.
5. LightGBM:
   - efficient GBDT;
   - strong for tabular;
   - categorical and missing handling require precise contracts.
6. CatBoost:
   - strong candidate for categorical-heavy setting;
   - especially relevant for School;
   - still requires strict validation and ablations.
7. Deep tabular models:
   - not first priority;
   - only consider if GBDT plateau and time allows.

## Techniques to avoid for now
Decision:
- No model-family selection from one CV score.
- No HPO before fair comparison.
- No ensembles before OOF diversity is demonstrated.
- No deep tabular priority unless simpler tabular candidates plateau.
- No model comparison using public leaderboard feedback.

## Leakage risks
Inference:
- Model families that handle missing/categorical values natively can still leak if folds, encodings, category mappings, or feature selection are global.
- CatBoost-style categorical handling does not remove the need for `School` ablation and slice review.

## Validation requirements
Decision:
- Selection must consider mean ROC-AUC, std across folds, slice robustness, leakage risk, reproducibility, simplicity, final-notebook compatibility, and sensitivity to School and missingness.
- Every model comparison must be logged.
- Compare on the same feature block and same folds.

## Codex instructions for future phases
Decision:
- Phase 5: document model comparison gates only.
- Phase 6: do not compare model families yet except minimal harness sanity checks if explicitly approved.
- Phase 7: define feature blocks before model comparison.
- Phase 8: run fair shortlist comparison.
- Phase 9: review errors and suspicious wins.
- Phase 10: tune only 1-3 candidates selected from fair comparison.
- Phase 11: final model must be reproducible top-to-bottom.

## Open questions
- Which external GBDT libraries are installed and compatible: Not confirmed yet.
- Whether `School` should be handled natively by CatBoost or encoded fold-safely: Not confirmed yet.
- Whether deep tabular methods deserve time: Not confirmed yet.

## Phase impact
Decision:
- Primary impact: Phase 8.
- Guardrails: Phase 5, Phase 6, Phase 7, Phase 9, Phase 10, Phase 11.
