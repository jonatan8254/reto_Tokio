# Feature Engineering

## Purpose
Define feature hypotheses, feature blocks, and ablation order without approving final features or executable feature engineering.

## Project context from Phase 3
Evidence:
- Four future signal families from EDA: role context; measurement availability; role-aware physical profile; institutional/categorical context.
- Missingness-prone columns: `Age`, `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`.
- `School` is high-cardinality, long-tail, and has test-only categories.
- Physical metrics must be interpreted by role; global interpretation is risky.
- Phase 3 selected no final features, no imputation, no categorical encoding, no outlier policy, no validation policy.
- PDF audit gate confirms reviewed feature-engineering sources: `feature_engineering_modern_ml_2024.pdf`, `feature_selection_survey_2024.pdf`, `feature_engineering_and_selection_kuhn_johnson_2021.pdf`, `python_machine_learning_by_example_4th_edition_2024.pdf`, `the_kaggle_book_2nd_edition_2025.pdf`, `machine_learning_with_lightgbm_python_2023.pdf`.

## Methodological evidence
Evidence:
- Reviewed feature-engineering sources support structured feature blocks, high-cardinality caution, missing-data handling, interaction effects, and fold-safe feature selection.
- Reviewed leakage sources warn that feature engineering can leak when group statistics, target statistics, rare mappings, or feature selection are learned globally.
- Reviewed tabular model sources support testing missingness/categorical handling as model-dependent hypotheses rather than as global preprocessing assumptions.

Inference:
- The correct next step is block-level ablation, not unbounded feature creation.
- Features that look row-wise safe are lower risk; features that learn role/category statistics require fold-safe implementation.

## Inference for this challenge
Inference:
- Missingness and role context are strong candidates, but they must remain hypotheses until fixed-fold ablations prove value.
- `School` may be useful but should enter late and in staged form because it is the highest-cardinality/overfitting risk.
- Outliers should be interpreted within role; global clipping or deletion is not justified.

## Decision
Decision:
- No final feature is approved in Phase 4B.
- Features are hypotheses.
- Each block must be tested by fixed-fold ablation.
- Do not select features based on public leaderboard.
- Do not trust global feature importance alone.
- Do not remove outliers globally.
- Do not winsorize globally.
- Do not create group-normalized features outside folds.

## Techniques to consider
Decision:
Feature block roadmap:

Block 0 - Raw baseline features:
- numeric physical measurements;
- categorical role variables;
- no School variant.

Block 1 - Missingness and measurement availability:
- `Age_missing`;
- `Sprint_40yd_missing`;
- `Vertical_Jump_missing`;
- `Bench_Press_Reps_missing`;
- `Broad_Jump_missing`;
- `Agility_3cone_missing`;
- `Shuttle_missing`;
- `available_measurement_count`;
- `is_complete_measurement_profile`;
- `has_low_measurement_profile`;
- `physical_missing_count`;
- age missingness separated from physical-test missingness.

Block 2 - Role context:
- `Player_Type`;
- `Position_Type`;
- `Position`;
- role-slice diagnostics;
- possible role interactions later.

Block 3 - Role-aware physical profile:
- speed-size interactions;
- strength-size interactions;
- explosiveness proxies;
- agility-speed interactions;
- BMI-like feature if derivable only from `Height` and `Weight`;
- role-normalized z-scores;
- within-role ranks or percentiles;
- role-specific outlier flags.

Block 4 - School safe encodings:
- no School baseline;
- School frequency/count encoding;
- rare grouping;
- unknown category handling;
- OOF target encoding only if justified;
- CatBoost native categorical handling only under strict validation.

Block 5 - Interaction features:
- simple predeclared interactions;
- interactions with `Position_Type` or `Player_Type`;
- avoid combinatorial explosion.

Block 6 - Feature selection:
- no global feature selection;
- only fold-safe feature selection inside CV if later justified;
- prefer ablation by blocks before RFE or wrapper search.

## Techniques to avoid for now
Decision:
- No OOF target encoding until earlier blocks are stable.
- No CatBoost categorical strategy until `School` ablation justifies it.
- No global role normalization.
- No global rare grouping.
- No global feature selection.
- No unsupervised or supervised dimensionality reduction before Phase 6/7 gates.
- No external sports, school, conference, geography, draft history, ranking, or NFL outcome data.

## Leakage risks
Inference:
- Missingness indicators are row-wise safe, but selecting them because of unstable CV or leaderboard feedback is still a selection risk.
- Role-normalized features, role percentiles, and rare grouping are learned statistics and must be fitted inside training folds.
- `School` target rates are high risk because low-n categories can look extreme but be unreliable.

## Validation requirements
Decision:
Ablation order:
- A0: baseline reproduction context only.
- A1: raw features without School.
- A2: missingness indicators.
- A3: `available_measurement_count` / completeness flags.
- A4: role context and role interactions.
- A5: role-aware numeric transformations.
- A6: School frequency/count.
- A7: rare grouping.
- A8: OOF target encoding or CatBoost categorical strategy only if previous steps are stable.

Each ablation must use the same fixed folds, ROC-AUC, fold scores, mean/std, and mandatory slice diagnostics.

## Codex instructions for future phases
Decision:
- Phase 5: approve the block roadmap and ablation order only.
- Phase 6: implement leakage-safe preprocessing before feature blocks.
- Phase 7: implement feature blocks one at a time with fixed-fold ablations.
- Phase 8: compare model families only after blocks are defined.
- Phase 9: review whether gains are real by slice and error analysis.
- Phase 10: do not tune features via HPO.
- Phase 11: submit only traceable, logged feature/model combinations.

## Open questions
- Unit of observation: Not confirmed yet.
- Whether role-normalized statistics are stable enough: Not confirmed yet.
- Whether `School` improves validation after safe encoding: Not confirmed yet.

## Phase impact
Decision:
- Primary impact: Phase 5 and Phase 7.
- Dependency impact: Phase 6, Phase 8, Phase 9, Phase 10, Phase 11.
