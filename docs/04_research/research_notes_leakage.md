# Leakage

## Purpose
Define the leakage taxonomy and fold-safe rules that govern all preprocessing, feature engineering, model comparison, HPO, and submission decisions.

## Project context from Phase 3
Evidence:
- Only official data may be used: `data/input/train.csv`, `data/input/test.csv`, and `data/input/sample_submission.csv`.
- Test data may not be used for fitting, tuning, selection, target encoding, or model choice.
- Phase 3 risk register flagged preprocessing leakage, target encoding leakage, role-statistics leakage, rare grouping leakage, public leaderboard overuse, and drift misuse.
- Phase 3 selected no final features, no imputation, no categorical encoding, no validation policy, and no model family.
- PDF audit gate confirmed reviewed leakage sources: `leakage_and_reproducibility_crisis_ml_science.pdf`, `on_leakage_in_ml_pipelines.pdf`, `feature_engineering_modern_ml_2024.pdf`, `the_kaggle_book_2nd_edition_2025.pdf`, `catboost_unbiased_boosting_categorical_features.pdf`, `machine_learning_with_lightgbm_python_2023.pdf`.

## Methodological evidence
Evidence:
- Reviewed leakage papers support a pipeline-wide leakage taxonomy, not only direct target leakage.
- Reviewed model-selection literature supports treating model selection and HPO as part of the training process.
- Reviewed feature-engineering sources emphasize that learned transformations, feature selection, and encodings must be estimated only inside the training data available to that fold.

Inference:
- The most promising Phase 3 signal families are also the easiest to contaminate: `School`, `Age_missing`, measurement completeness, role statistics, rare categories, and target-rate summaries.

## Inference for this challenge
Inference:
- The safe default is: if a transformation learns any statistic from rows, it must be fitted inside each training fold.
- Test data is allowed only for structure checks, submission row/order checks, and final inference after the final model is trained.
- Train/test drift diagnostics are descriptive only; they must not tune preprocessing toward the test distribution.

## Decision
Decision:
- Phase 6 must implement leakage-safe preprocessing before Phase 7 feature blocks.
- No global pandas preprocessing is allowed before CV unless the transformation is purely row-wise and learns no parameters from other rows.
- Any target-aware or group-statistic transform must be blocked until it can be implemented fold-safely.

## Techniques to consider
Decision:
- Scikit-learn `Pipeline` / `ColumnTransformer` style execution.
- Fold-aware imputers, encoders, scalers, rare-category mappers, and feature selectors.
- Row-wise features that do not learn from other rows.
- Explicit leakage checklist before every experiment and submission.

## Techniques to avoid for now
Decision:
- Global imputation before CV.
- Global encoding before CV.
- Global scaling before CV.
- Global rare-category grouping before CV.
- Global role mean/std, role z-score, role percentile, or role rank computation.
- Global feature selection.
- Target encoding without strict OOF logic.
- Test-informed preprocessing or drift correction.

## Leakage risks
Evidence:
Layered leakage taxonomy for this project:
1. data leakage;
2. test-to-train leakage;
3. preprocessing leakage;
4. imputation leakage;
5. encoding leakage;
6. target encoding leakage;
7. feature selection leakage;
8. role-statistics leakage;
9. rare-grouping leakage;
10. HPO/model-selection leakage;
11. leaderboard leakage;
12. confound/group leakage;
13. drift misuse leakage.

Decision:
- Test data may be used only for structure checks, submission row/order checks, and final inference after the final model is trained.
- Test data may not be used for fitting imputers, encoders, scalers, rare grouping, target encoding, feature selection, model selection, HPO, or choosing submissions.
- Transformations that must be fitted inside training folds include `SimpleImputer`, `OneHotEncoder`, `OrdinalEncoder`, `StandardScaler`, `TargetEncoder`, rare category mapping, role mean/std, role z-score statistics, role percentile/rank mapping, feature selection, dimensionality reduction, and HPO.

## Validation requirements
Decision:
- Each experiment must document what learns from data and where it is fitted.
- Each feature block must be tested under the frozen folds from Phase 5/6.
- Slice diagnostics must check whether apparent gains are only subgroup or rare-category artifacts.

## Codex instructions for future phases
Decision:
- Phase 5: freeze leakage checklist and allowed/disallowed test-data uses.
- Phase 6: implement only fold-safe preprocessing.
- Phase 7: implement feature blocks only as leakage-reviewed ablations.
- Phase 8: compare models only after the same leakage-safe pipeline is available.
- Phase 9: audit suspicious gains and dominant variables.
- Phase 10: treat HPO as model-selection risk.
- Phase 11: do not use public leaderboard as an optimization loop.

Allowed row-wise transformations:
- simple arithmetic ratios from columns in the same row;
- missingness indicators from the same row;
- `available_measurement_count` from the same row;
- boolean flags based only on current row values.

Potentially dangerous transformations:
- any group statistic;
- any target statistic;
- any normalization learned from data;
- rare category grouping learned globally;
- feature selection learned globally.

## Open questions
- Unit of observation: Not confirmed yet.
- Whether grouping by School, Year, Position, or Position_Type is required for CV: Not confirmed yet.

## Phase impact
Decision:
- Primary impact: Phase 5, Phase 6, Phase 7.
- Guardrails: Phase 8, Phase 9, Phase 10, Phase 11.
