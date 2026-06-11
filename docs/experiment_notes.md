# Experiment Notes

## Phase 3 - Data Contract and Initial EDA

Date: 2026-06-10

### Executive Summary of Phase 3 Findings

Phase 3 confirms that the official CSVs pass executable data-contract checks and that the project can proceed with a reliable EDA foundation. The EDA suggests four future signal families: role context, measurement availability, physical profile, and institutional/categorical context. It also highlights the main risks that later phases must control: leakage through preprocessing, high-cardinality overfitting from `School`, low-n target-rate instability, train/test composition shift, and hidden subgroup failures.

No model was trained. No submission was generated. No raw data was modified. No final features, preprocessing rules, column drops, outlier rules, encodings, or validation policy were selected.

### Integrated Post-EDA Interpretation

The Phase 3 EDA suggests a four-layer signal architecture:

1. **Role context:** `Position`, `Position_Type`, and `Player_Type` define the context in which physical measurements should be interpreted.
2. **Measurement availability:** `Age` missingness, physical-test missingness, `available_measurement_count`, and co-missingness profiles may describe how completely an athlete was evaluated.
3. **Role-aware physical profile:** size, speed, explosiveness, agility, and strength appear most meaningful when interpreted relative to role.
4. **Institutional/categorical context:** `School`, long-tail category behavior, rare-category risk, and test-only categories may carry signal but also create overfitting risk.

Missingness has at least three subfamilies. `Age` missingness appears unusually strong in train-only diagnostics and should be tested separately from physical-test missingness. Physical-test missingness (`Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`) may reflect measurement availability, position norms, or testing context. Aggregated completeness (`available_measurement_count` and co-missingness profiles) may proxy player evaluation context.

The EDA also suggests a possible `Player_Type -> measurement completeness -> Drafted` confounding pattern. `special_teams` appears structurally different from offense and defense, with lower measurement completeness and lower target rate. This is descriptive, not causal. Future models should report global AUC plus AUC by `Player_Type`, `Position_Type`, `Year`, measurement-completeness slices, and frequent-vs-rare school groups where feasible.

Physical values should not be interpreted as raw numbers alone. A sprint, shuttle, weight, height, or jump result can mean different things for different roles. Global associations can mislead; role-aware diagnostics and slice reporting should be part of later validation.

`School` is potentially useful but high risk. Future use should be staged: no School baseline, safe frequency/count encoding, rare-category handling inside folds, and only if justified later, strictly out-of-fold target encoding with smoothing or CatBoost-style handling under careful validation.

Train/test numeric drift appears moderate rather than catastrophic. The larger concern is structural/categorical drift, especially `School` and role composition. Drift diagnostics should guide slice diagnostics, not test-tuned preprocessing.

Strategic conclusion: signal is likely less about raw physical values alone and more about role plus measurement context. Phase 3 provides a map of where signal may exist and where validation/leakage controls must be strongest.

### Data Contract Status

- Train shape recomputed in notebook: `(2781, 16)`.
- Test shape recomputed in notebook: `(696, 15)`.
- Sample submission shape recomputed in notebook: `(696, 2)`.
- Target column: `Drafted`.
- ID column: `Id`.
- Sample submission columns: `['Id', 'Drafted']`.
- Contract checks passed: `True`.
- Train duplicated rows: `0`.
- Test duplicated rows: `0`.
- Unit of observation: Not confirmed yet.

The unit of observation remains important because validation design depends on whether rows can be treated as independent.

### Target Distribution Interpretation

`Drafted = 1` is the majority class, but the target is not extremely imbalanced. Because the official metric is ROC-AUC, future models must rank players well by probability. Threshold-based accuracy is not the main goal.

### Missingness and Measurement Availability Interpretation

Missingness-prone columns are `Age, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle`. Missingness is structured by field, role, and year. It should be treated as a candidate signal family, not only as a cleaning problem. Age missingness is especially notable in train-only diagnostics and should be handled carefully as descriptive evidence, not as a final feature decision. Missingness indicators and available-measurement-count features must be tested later using fold-safe validation.

### Available Measurement Count Interpretation

`available_measurement_count` summarizes how many missingness-prone physical measurements are present for each row. It may capture player evaluation context because players with more complete physical profiles may have been measured more thoroughly. This is a strong future feature hypothesis, but no such feature is selected in Phase 3.

### Role and Position Interpretation

Physical metrics cannot be interpreted globally only. `Sprint_40yd`, `Weight`, `Height`, jump metrics, agility, and shuttle can have different meanings by role. `Position_Type` should be a central axis for later feature-engineering hypotheses. Role-normalized features or role interactions should be tested later, not created as final features here.

### Special Teams / Player_Type Interpretation

Player_Type target-rate and measurement-completeness tables indicate that special_teams should be treated as a distinct slice. Future models should report Player_Type slice performance because global AUC can hide weak subgroup behavior.

### School / Cardinality Risk Interpretation

`School` is potentially useful but risky. Many schools are rare, low-n school target rates can be extreme but unreliable, and test-only schools make simple encodings fragile. Future use of `School` should prioritize safe frequency/count encoding or strictly out-of-fold target encoding only if justified later. No target encoding is performed in Phase 3.

### Train/Test Shift Interpretation

Numeric train/test shift appears moderate rather than catastrophic based on descriptive diagnostics. `School` is the main categorical shift and high-cardinality concern. Drift diagnostics are descriptive only and should guide future slice diagnostics, not test-tuned preprocessing.

### Year / Cohort Effects Interpretation

Year may reflect cohort effects. Measurement availability and role composition can vary by year, so future validation should include Year slice diagnostics. This does not automatically justify a temporal split; split design is deferred to a later validation phase.

### Correlation / Redundancy Interpretation

Several physical tests are correlated, suggesting latent physical dimensions such as size, speed, explosiveness, agility, and strength. High correlation is not a reason to drop features in Phase 3. Later model families may handle redundancy differently.

### Outlier Interpretation

Physical outliers should be understood within position context. Global outlier removal can be dangerous in sports data because exceptional athletes may look like outliers. No clipping, winsorization, or row removal is selected in Phase 3.

### Contrarian Pattern Interpretation

Global associations may be misleading. A variable can look weak globally but matter inside a role group. `Height` shows evidence of direction changing across role groups, which reinforces that physical relationships should be inspected within `Position_Type`, not only globally. These contrarian patterns are hypotheses only.

### Future Signal Families

| future_signal_family | columns_or_concepts | why_it_may_matter | validation_caution |
| --- | --- | --- | --- |
| Role context | Position; Position_Type; Player_Type | Player measurements and target rates are role-dependent; global patterns can hide subgroup behavior. | Report slice performance by role and avoid overfitting rare roles. |
| Measurement availability | missingness indicators; available_measurement_count; co-missingness profiles | Measurement completeness may proxy player evaluation context and testing availability. | Any missingness feature must be tested later in fold-safe validation. |
| Physical profile | size; speed; explosiveness; agility; strength | Physical measurements are likely informative only when interpreted relative to role. | No role-normalized features or interactions are selected in Phase 3. |
| Institutional/categorical context | School; long-tail categories; rare-category behavior | School may contain signal but also strong high-cardinality overfitting risk. | Prioritize safe frequency/count encoding or strictly OOF target encoding only if justified later. |

### Key EDA Findings

| finding_type | finding | future_use |
| --- | --- | --- |
| confirmed_fact | Official CSVs load and pass executable data contract checks. | Reuse checks in later notebooks. |
| descriptive_finding | Target is not extremely imbalanced and Drafted=1 is the majority class. | Use ROC-AUC/ranking framing rather than threshold accuracy. |
| descriptive_finding | Missingness is structured by field, role, and year; Age missingness is especially notable in train-only target-rate diagnostics. | Evaluate missingness signals only with fold-safe validation. |
| descriptive_finding | Special teams appears structurally different from offense/defense, including lower measurement completeness and lower target rate. | Report future model performance by Player_Type slices. |
| potential_risk | Low-n schools and rare categories can show extreme but unreliable target rates. | Always track n and uncertainty. |
| candidate_hypothesis | Physical metrics need role-aware interpretation; global associations can be misleading. | Test role interactions or role-normalized metrics later. |
| deferred_decision | No feature engineering, preprocessing, validation policy, or model choice is finalized in Phase 3. | Carry into Phase 5/6 plans. |

### Train/Test Shift Findings

| column | max_abs_delta | total_variation_distance | test_only_categories |
| --- | --- | --- | --- |
| School | 0.0194 | 0.2438 | 17 |
| Player_Type | 0.0195 | 0.0195 | 0 |
| Position_Type | 0.0279 | 0.0456 | 0 |
| Position | 0.0246 | 0.0838 | 0 |

Top numeric shift diagnostics by descriptive max CDF distance:

| column | train_missing_pct | test_missing_pct | missing_delta_test_minus_train | train_median | test_median | median_delta_test_minus_train | descriptive_max_cdf_distance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Agility_3cone | 0.3488 | 0.3549 | 0.0061 | 7.1300 | 7.1800 | 0.0500 | 0.0718 |
| Broad_Jump | 0.2089 | 0.2112 | 0.0023 | 294.6400 | 294.6400 | 0.0000 | 0.0554 |
| Shuttle | 0.3279 | 0.3276 | -0.0004 | 4.3500 | 4.3800 | 0.0300 | 0.0541 |
| Sprint_40yd | 0.0521 | 0.0417 | -0.0105 | 4.6800 | 4.7000 | 0.0200 | 0.0396 |
| Vertical_Jump | 0.1992 | 0.2055 | 0.0063 | 83.8200 | 83.8200 | 0.0000 | 0.0343 |
| Weight | 0.0000 | 0.0000 | 0.0000 | 104.7798 | 104.7798 | 0.0000 | 0.0342 |
| Age | 0.1564 | 0.1652 | 0.0088 | 22.0000 | 22.0000 | 0.0000 | 0.0334 |
| Bench_Press_Reps | 0.2593 | 0.2644 | 0.0051 | 20.0000 | 20.0000 | 0.0000 | 0.0310 |
| Year | 0.0000 | 0.0000 | 0.0000 | 2014.0000 | 2014.0000 | 0.0000 | 0.0308 |
| Height | 0.0000 | 0.0000 | 0.0000 | 1.8796 | 1.8796 | 0.0000 | 0.0305 |

### Contrarian and Overlooked Pattern Findings

| pattern_type | variable | global_delta_drafted_minus_not_median | max_abs_within_position_type_delta | opposite_direction_groups | hypothesis |
| --- | --- | --- | --- | --- | --- |
| global_vs_within_role_direction | Height | 0.0000 | 0.0254 | line_backer (-0.025, n=309); offensive_lineman (0.025, n=435) | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Weight | 4.9895 | 3.6287 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Sprint_40yd | -0.0800 | 0.1250 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Vertical_Jump | 2.5400 | 4.4450 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Bench_Press_Reps | 1.0000 | 2.0000 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Broad_Jump | 5.0800 | 7.6200 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Agility_3cone | -0.0500 | 0.1900 | none_detected | Metric direction may depend on role; global association can be misleading. |
| global_vs_within_role_direction | Shuttle | -0.0400 | 0.1150 | none_detected | Metric direction may depend on role; global association can be misleading. |
| missingness_vs_measured_value | Age | nan | nan | not_applicable | Missingness target-rate spread=0.747; median-split value spread=0.110. Missingness may matter as much as value. |
| missingness_vs_measured_value | Sprint_40yd | nan | nan | not_applicable | Missingness target-rate spread=0.066; median-split value spread=0.095. Missingness may matter as much as value. |
| missingness_vs_measured_value | Vertical_Jump | nan | nan | not_applicable | Missingness target-rate spread=0.079; median-split value spread=0.082. Missingness may matter as much as value. |
| missingness_vs_measured_value | Bench_Press_Reps | nan | nan | not_applicable | Missingness target-rate spread=0.063; median-split value spread=0.090. Missingness may matter as much as value. |
| missingness_vs_measured_value | Broad_Jump | nan | nan | not_applicable | Missingness target-rate spread=0.069; median-split value spread=0.085. Missingness may matter as much as value. |
| missingness_vs_measured_value | Agility_3cone | nan | nan | not_applicable | Missingness target-rate spread=0.066; median-split value spread=0.044. Missingness may matter as much as value. |
| missingness_vs_measured_value | Shuttle | nan | nan | not_applicable | Missingness target-rate spread=0.071; median-split value spread=0.053. Missingness may matter as much as value. |

### Leakage and Validation Risk Register

| risk | severity | likelihood | evidence | safeguard | owner_future_phase |
| --- | --- | --- | --- | --- | --- |
| Target-aware analysis accidentally uses test data | High | Medium | Target exists only in train; many plots compare rates. | All target-rate helpers use train-only data. | Phase 3/All future notebooks |
| Preprocessing leakage through global imputation or encoding | High | High | Missingness and categorical structure are prominent. | Future imputers/encoders must be fitted inside CV folds. | Phase 6 |
| High-cardinality School overfitting | High | High | School has long-tail frequency and many low-n rates. | No target encoding in Phase 3; later encodings must be fold-aware. | Phase 7 |
| Low-n target-rate instability | Medium | High | Wilson intervals and sample-size scatter show unstable categories. | Always show n and uncertainty. | Phase 5/7 |
| Train/test composition shift hidden by aggregates | Medium | Medium | Frequency deltas and composition plots show possible shifts. | Use as validation hypotheses, not test-tuning targets. | Phase 5/6 |
| Outlier removal based on EDA aesthetics | Medium | Medium | Physical metrics include global and within-position outliers. | No removal/winsorization in Phase 3. | Phase 7 |
| Correlation mistaken for feature selection | Medium | Medium | High-correlation physical metrics identified. | Correlation table is descriptive. | Phase 7/8 |
| Public leaderboard over-trust | High | Medium | Baseline leaderboard score exists in log. | Use leaderboard only as sanity check. | Phase 11 |
| Notebook hidden state | High | Medium | Notebook-first workflow can hide execution-order dependencies. | Execute top-to-bottom from repo root. | All phases |
| Promising signal families are implemented without leakage controls | High | Medium | The strongest candidate signals involve missingness, School, role context, and target-rate summaries. | Treat EDA findings as hypotheses; require fold-safe implementation and ablation before adoption. | Phase 5/6/7 |
| Age_missing is over-trusted because its train-only association is strong | High | Medium | Age missingness appears unusually strong in train-only target-rate diagnostics. | Test Age missingness separately from physical-test missingness with fixed folds and slice checks. | Phase 7 |
| School encodings overfit rare categories | High | High | School has long-tail behavior, low-n target-rate instability, and test-only categories. | Stage School ablations; use only fold-safe frequency/count, rare handling, or strictly OOF target encoding if later justified. | Phase 7/8 |
| Role-normalized features leak fold statistics | High | Medium | Role-specific physical interpretation suggests possible role-normalized metrics. | Compute any role statistics inside training folds only; report role-slice AUC. | Phase 7 |
| Rare grouping is learned globally instead of inside folds | Medium | Medium | Long-tail categorical behavior suggests possible rare-category handling. | Learn rare-category thresholds and mappings inside training folds only. | Phase 7 |
| Public leaderboard becomes an implicit validation system | High | Medium | Baseline public leaderboard score is known and easy to overuse. | Use public leaderboard only as a sanity check; use local CV and slice diagnostics for decisions. | Phase 11 |

### Hypothesis Register

| hypothesis | eda_evidence_source | potential_future_feature_or_action | leakage_risk | validation_requirement | priority | future_phase |
| --- | --- | --- | --- | --- | --- | --- |
| Missingness indicators may improve ranking quality. | Missingness indicator vs Drafted-rate table; co-missingness heatmap. | Add fold-safe missingness indicators. | Medium | Fixed StratifiedKFold ablation and slice checks. | High | Phase 7 |
| Available measurement count captures player evaluation context. | Available count distribution and train-only target-rate plot. | Test available measurement count as a simple numeric feature. | Low/Medium | Ablation with and without measurement-count feature. | High | Phase 7 |
| Physical metrics have role-specific directionality. | Position_Type profiles; global vs within-role scan. | Test role interactions or role-normalized metrics. | Medium | Fold-aware preprocessing and slice-level AUC by Position_Type. | High | Phase 7/8 |
| School contains signal but is high overfitting risk. | School coverage curve and target-rate instability plot. | Test safe school frequency or carefully fold-aware target encoding only if justified. | High | Strict OOF encoding and ablation. | Medium | Phase 7 |
| Year/cohort differences affect validation reliability. | Year distribution, Year x missingness, Year x Position_Type composition. | Evaluate year-slice diagnostics or year-aware robustness reporting. | Medium | Compare standard StratifiedKFold with slice diagnostics. | Medium | Phase 5/6 |
| Rare category handling may reduce noise. | Categorical long-tail and low-n Wilson intervals. | Test rare-category grouping inside fold-aware preprocessing. | Medium | Ablation and fold variance monitoring. | Medium | Phase 7 |
| Correlated physical tests may be redundant for some models but complementary for others. | Pearson/Spearman heatmaps and high-correlation pair table. | Compare model families and optional regularized preprocessing. | Low/Medium | Same folds across model comparisons. | Low/Medium | Phase 8 |
| Age_missing should be tested separately from physical-test missingness. | Age missingness shows unusually strong train-only target-rate diagnostics. | Test an Age_missing indicator as its own ablation block. | Medium - selection must not be based on test or leaderboard feedback. | Fixed folds; compare global AUC and AUC by Player_Type, Position_Type, and Year. | High | Phase 7 |
| Available measurement count should be tested as raw count, complete-profile indicator, and low-profile indicator. | Available measurement count plot and train-only target-rate table. | Ablate raw count, is_complete_measurement_profile, and has_low_measurement_profile. | Low/Medium - safe if computed only from row-level official fields and selected via CV. | Fixed-fold ablation and slice diagnostics by Player_Type and Position_Type. | High | Phase 7 |
| Missingness/completeness effects should be tested within Player_Type and Position_Type slices. | Player_Type measurement completeness and role missingness summaries. | Report missingness-feature lift and AUC by role slices. | Medium - global gains may reflect subgroup composition rather than stable signal. | Slice-level validation for offense, defense, special_teams, and Position_Type groups. | High | Phase 7/9 |
| Player_Type slice performance should be reported because special teams may behave differently. | Special teams has lower measurement completeness and lower target-rate diagnostics. | Add Player_Type slice metrics to model review reports. | Low - reporting risk is interpretation, not leakage, if labels remain train/validation only. | OOF or validation predictions with AUC by Player_Type. | High | Phase 6/9 |
| Role-aware physical metrics should be tested via interactions, role-normalized values, and within-role percentiles/ranks. | Position_Type physical profiles and global-vs-within-role association scan. | Test raw metrics, role interactions, role z-scores, and within-role ranks. | High - role statistics must be computed inside training folds. | Fold-aware transformers plus role-slice AUC. | High | Phase 7/8 |
| Variables with weak global association but strong within-role association should be scanned systematically. | Contrarian section, including Height direction changes across role groups. | Build a controlled diagnostic for low-global/high-within-role associations. | Medium - scanning many candidates can overfit if used for selection without validation. | Predeclare candidate block and validate by fixed-fold ablation. | Medium | Phase 7 |
| School should be ablated in staged fashion. | School coverage, target-rate instability, and test-only school diagnostics. | Compare no School, frequency/count encoding, rare grouping, and possible OOF target encoding only if justified. | High - School can overfit and target encoding can leak labels. | Strict fold-aware encoding; monitor fold variance and rare/frequent-school slices. | Medium/High | Phase 7/8 |
| Numeric train/test drift should be checked conditionally by role before making modeling decisions. | Global numeric drift is moderate, while role composition can differ. | Add role-conditioned drift diagnostics and slice model reporting. | Medium - do not tune preprocessing to test distributions. | Use drift as diagnostic context, not selection objective. | Medium | Phase 5/6 |
| Year-slice diagnostics should be included in future validation reporting. | Year distribution, Year x missingness, and Year x Position_Type composition. | Report validation AUC and calibration-style summaries by Year where feasible. | Medium - do not automatically switch to temporal split without justification. | Combine standard StratifiedKFold with Year-slice reporting unless later evidence changes split design. | Medium | Phase 5/6 |
| Within-position outlier flags may be tested later, but no outlier deletion is selected. | Outlier diagnostics by position show role-contextual extremes. | Ablate within-position outlier flags or robust transforms versus no outlier handling. | Medium - outlier thresholds must be learned inside folds if estimated from data. | Compare against no-outlier-handling baseline and inspect role slices. | Low/Medium | Phase 7 |

### Saved High-Value Figures

- `outputs/figures/phase03_target_distribution.png`
- `outputs/figures/phase03_missingness_train_test_comparison.png`
- `outputs/figures/phase03_available_measurement_count_distribution.png`
- `outputs/figures/phase03_available_measurement_count_vs_target_rate.png`
- `outputs/figures/phase03_missingness_indicator_vs_target_rate.png`
- `outputs/figures/phase03_position_missingness_heatmap.png`
- `outputs/figures/phase03_year_missingness_heatmap.png`
- `outputs/figures/phase03_missingness_comissingness_heatmap.png`
- `outputs/figures/phase03_player_type_available_measurement_count.png`
- `outputs/figures/phase03_train_test_numeric_distribution_overlays.png`
- `outputs/figures/phase03_position_type_physical_metric_median_heatmap.png`
- `outputs/figures/phase03_outlier_diagnostics_by_position.png`
- `outputs/figures/phase03_position_target_rate_with_uncertainty.png`
- `outputs/figures/phase03_position_type_target_rate_with_uncertainty.png`
- `outputs/figures/phase03_school_frequency_cumulative_coverage.png`
- `outputs/figures/phase03_school_target_rate_instability.png`
- `outputs/figures/phase03_train_test_categorical_frequency_deltas.png`
- `outputs/figures/phase03_year_position_type_composition.png`
- `outputs/figures/phase03_train_test_year_distribution.png`
- `outputs/figures/phase03_role_target_rates_with_uncertainty.png`
- `outputs/figures/phase03_physical_relationships_by_position_type.png`
- `outputs/figures/phase03_numeric_correlations_pearson.png`
- `outputs/figures/phase03_numeric_correlations_spearman.png`
- `outputs/figures/phase03_contrarian_global_vs_within_role_associations.png`

### Deferred Decisions

- No imputation method selected.
- No categorical encoding selected.
- No missingness feature selected.
- No complete-profile or low-profile measurement-completeness feature selected.
- No role-normalized feature, role percentile, or role interaction selected.
- No `School` encoding strategy selected.
- No outlier clipping/removal selected.
- No outlier flag selected.
- No feature interaction selected.
- No temporal split selected.
- No validation split policy finalized beyond preserving the existing need for leakage-safe local validation.
- No model family selected for improvement beyond the previously reproduced baseline context.

### Verification Note

The refactored notebook is designed to run top-to-bottom from the repository root, recompute structural facts from the official CSV files, keep target-aware analysis train-only, and avoid modeling or submission-generation logic.
