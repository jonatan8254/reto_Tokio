# Validation

## Purpose
Govern the validation design for the NFL Draft Prediction workflow before any new modeling, feature ablation, HPO, ensemble, or submission decision.

## Project context from Phase 3
Evidence:
- Task: binary classification; target: `Drafted`; positive class: `Drafted = 1`; ID: `Id`.
- Metric: ROC-AUC / AUC using positive-class probabilities.
- Submission format: `Id`, `Drafted`; row count: 696.
- Phase 3 confirmed: train `(2781, 16)`, test `(696, 15)`, sample submission `(696, 2)`, no duplicate rows in train/test, contract checks passed.
- Phase 3 did not train a model, generate a submission, modify raw data, select final features, select preprocessing, select imputation, select categorical encoding, or finalize validation.
- Unit of observation: Not confirmed yet.
- PDF audit gate: 34 PDFs detected, 26 Reviewed, 8 Partially readable, 0 OCR needed, 0 Extraction failed.

## Methodological evidence
Evidence:
- Reviewed sources supporting validation discipline: `the_kaggle_book_2nd_edition_2025.pdf`, `introduction_to_statistical_learning_python.pdf`, `feature_engineering_modern_ml_2024.pdf`, `hands_on_machine_learning_sklearn_pytorch_2026.pdf`, `python_machine_learning_by_example_4th_edition_2024.pdf`, `feature_engineering_and_selection_kuhn_johnson_2021.pdf`, `the_kaggle_workbook_2023.pdf`, `machine_learning_with_lightgbm_python_2023.pdf`.
- The Phase 4A report and project checklist agree that ROC-AUC must use continuous positive-class scores, not hard labels.
- Model-selection literature reviewed in the PDF audit supports conservative validation because repeated selection on the same criterion can bias performance estimates.

Inference:
- This challenge should optimize ranking quality: probability ordering for `Drafted = 1`, not threshold accuracy.
- Because the target is binary and not extremely imbalanced, a fixed stratified CV design is the safest default until grouping/dependence is confirmed.
- Slice diagnostics are mandatory because Phase 3 found role, year, measurement-completeness, and School-frequency risks.

## Inference for this challenge
Inference:
- Default validation should be `StratifiedKFold` with a fixed seed.
- Use probabilities for `Drafted = 1` in ROC-AUC.
- Public leaderboard is a sanity check only; it must never drive feature selection, HPO, model selection, or submission choice.
- Temporal/year split is diagnostic only unless official/test-distribution evidence later justifies it.

## Decision
Decision:
- Phase 5 must freeze the validation design.
- Phase 6 must implement and test the validation harness.
- Phase 7 must use exactly the same folds for feature ablations.
- Phase 8 must use exactly the same folds for model comparison.
- Phase 10 must not retune endlessly on the same CV without logging and controls.

## Techniques to consider
Decision:
- Priority 1: fixed-seed `StratifiedKFold`.
- Priority 2: out-of-fold predictions for diagnostics and future stacking guardrails.
- Priority 3: fold-by-fold ROC-AUC, mean ROC-AUC, std ROC-AUC.
- Priority 4: mandatory slice diagnostics for `Player_Type`, `Position_Type`, `Year`, measurement completeness, `Age_missing`, and frequent vs rare `School` groups.
- Conditional: `StratifiedGroupKFold` only if unit of observation or dependency/grouping is confirmed.
- Conditional: `GroupKFold` only if grouping becomes more important than class balance.

## Techniques to avoid for now
Decision:
- Do not use public leaderboard as validation.
- Do not use one holdout split as the only decision system.
- Do not use grouped CV until grouping need is confirmed.
- Do not use temporal split as default yet.
- Do not select features, models, or HPO settings using test data or leaderboard feedback.

## Leakage risks
Evidence:
- Phase 3 flagged preprocessing leakage, target encoding leakage, role-statistics leakage, public leaderboard overuse, and hidden subgroup failures.

Inference:
- Validation leakage can occur even without direct target leakage if folds change between ablations, preprocessing is fitted globally, or leaderboard feedback becomes an implicit label.

## Validation requirements
Decision:
- Report mean ROC-AUC across folds.
- Report std ROC-AUC across folds.
- Report fold-by-fold scores.
- Store OOF predictions when applicable.
- Report slice diagnostics for mandatory slices.
- Keep the same folds across Phase 7 feature blocks and Phase 8 model comparison.

## Codex instructions for future phases
Decision:
- Phase 5: document the exact fold strategy, seed, metric function, slice schema, and stop conditions.
- Phase 6: implement the validation harness before adding new feature blocks.
- Phase 7: run fixed-fold ablations only.
- Phase 8: compare model families only on the frozen folds.
- Phase 9: use OOF errors and slices for sanity checks.
- Phase 10: allow HPO only after validation and feature blocks are stable.
- Phase 11: treat public leaderboard as a sanity check, not a validation system.

## Open questions
- Unit of observation: Not confirmed yet.
- Need for grouped CV: Not confirmed yet.
- Whether Year requires a special split: Not confirmed yet.

## Phase impact
Decision:
- Primary impact: Phase 5 and Phase 6.
- Downstream guardrails: Phase 7, Phase 8, Phase 9, Phase 10, Phase 11.
