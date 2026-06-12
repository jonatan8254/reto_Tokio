# Phase 7B Role Interaction Acceptance Draft

Date: 2026-06-12

Experiment ID: `phase7b_role_availability_interaction_v1`

Run ID: `phase7b_f4_single_probe_20260612`

Starting commit: `8b21db5`

This document is a draft acceptance record for user/project director review. It does not sign on behalf of the user/project director, does not authorize staging or commit, and does not open Phase 8.

## A. Executive Conclusion

Phase 7B passed execution and independent audit.

F4 decision: rejected by the pre-registered rule; keep F2 as the post-Phase-7 feature set.

Phase 8 status: locked.

Blockers: none.

Primary result:

- F2 OOF ROC-AUC: `0.8116502602456482`
- F4 OOF ROC-AUC: `0.8093690701818260`
- F4 - F2 OOF delta: `-0.0022811900638222`
- Same-sign folds: `1/5`
- Slice guard: clear
- Leakage verdict: pass

F4 does not meet the required OOF gain threshold and does not meet the same-sign fold criterion.

## B. Hypothesis and Design

Phase 7B tested exactly one deferred F4 hypothesis:

`available_measurement_count x Player_Type`

F4 was compared against the persisted Phase 7 F2 OOF baseline, not against F0.

No other features or interactions were tested:

- no `Position_Type` interactions;
- no `Position` interactions;
- no missingness-flag interactions;
- no pairwise physical interactions;
- no `School` features;
- no BMI;
- no `measurement_completeness_group` model feature;
- no co-missingness patterns;
- no HPO;
- no model-family comparison.

The interaction was implemented fold-safely: `Player_Type` one-hot categories were fitted only inside each training fold, then multiplied by the row-wise `available_measurement_count`.

## C. Metric and Decision Table

| Baseline | Candidate | F2 OOF AUC | F4 OOF AUC | Delta F4 - F2 | Same-sign folds | Slice guard | Final decision | Rationale |
|---|---|---:|---:|---:|---:|---|---|---|
| `phase7_f2_median_flags_count` | `phase7b_f4_role_count_player_type` | 0.811650 | 0.809369 | -0.002281 | 1/5 | Clear | Reject F4; keep F2 | Global OOF delta is negative and same-sign fold count is below 4/5. |

Acceptance rule result:

- OOF gain over F2 >= `0.005436`: failed.
- Same-sign fold deltas vs F2 >= `4/5`: failed.
- Slice guard clear: passed.
- Leakage warning: none.
- Artifact/path/log violation: none.

## D. Fold-Level Evidence

| Fold | F2 AUC | F4 AUC | Delta F4 - F2 | Sign |
|---:|---:|---:|---:|---|
| 0 | 0.789389 | 0.786025 | -0.003364 | non_positive |
| 1 | 0.832382 | 0.827928 | -0.004453 | non_positive |
| 2 | 0.825854 | 0.838923 | 0.013069 | positive |
| 3 | 0.773724 | 0.767900 | -0.005825 | non_positive |
| 4 | 0.840930 | 0.837018 | -0.003912 | non_positive |

Only fold 2 improved. Four of five folds moved against F4.

## E. Slice Findings

Mandatory slices were present:

- `Player_Type`
- `Position_Type`
- `Year`
- `Age_missing`
- `available_measurement_count`
- `measurement_completeness_group`
- `frequent_vs_rare_school_group`

Slice guard status: clear. No mandatory slice with `n >= 50` degraded by more than `0.02` AUC versus F2.

Most positive slice movements:

| Slice | Value | n | Delta F4 - F2 |
|---|---|---:|---:|
| `Player_Type` | `special_teams` | 95 | +0.030286 |
| `Year` | `2013` | 256 | +0.020695 |
| `Position_Type` | `kicking_specialist` | 82 | +0.019516 |
| `available_measurement_count` | `3` | 137 | +0.009700 |
| `Position_Type` | `line_backer` | 309 | +0.007619 |

Most negative slice movements:

| Slice | Value | n | Delta F4 - F2 |
|---|---|---:|---:|
| `measurement_completeness_group` | `0` | 56 | -0.018100 |
| `available_measurement_count` | `0` | 56 | -0.018100 |
| `Year` | `2017` | 274 | -0.015062 |
| `Year` | `2011` | 278 | -0.010757 |
| `Year` | `2016` | 260 | -0.010404 |

Interpretation:

- `Player_Type = special_teams` and `Position_Type = kicking_specialist` improved, suggesting the hypothesis has localized signal.
- The global OOF result and fold consistency are not sufficient to adopt F4.
- Player_Type or Position_Type heterogeneity exists, but the evidence is inconclusive for adoption because the improvement is not stable across folds.

## F. Leakage and Scope Verdict

Leakage verdict: pass.

Confirmed:

- no test fitting;
- no global preprocessing;
- no `School` as feature;
- no external data;
- no leaderboard use;
- no HPO;
- no model-family comparison;
- no submission generated;
- `logs/experiment_log.csv` unchanged;
- F2 was loaded from persisted OOF and was not silently retrained;
- F4 positive-class probabilities were extracted after verifying `estimator.classes_`.

## G. Final Feature-Set Recommendation

Keep F2 as the post-Phase-7 feature set:

- base Phase 6 features;
- seven missingness flags;
- `available_measurement_count`;
- median imputation;
- fold-safe one-hot encoding;
- `School` excluded from the feature matrix.

Do not adopt F4 in the current feature set.

Final post-Phase-7 / Phase-7B feature set: F2. F4 is not adopted. Phase 8 remains locked.

## H. Phase 8 Dependency Note

Phase 8 remains locked.

If Phase 8 is later authorized, it should use F2 as the post-Phase-7 feature set unless the user/project director makes a separate decision.

Native-missing-value learners remain a future Phase 8 question only.

HPO, submissions, leaderboard use, and model-family comparison remain prohibited until separately authorized.

## Files Recommended for Future Selective Commit

- `notebooks/07b_phase7b_role_availability_interaction_probe.ipynb`
- `outputs/oof/phase7b_role_availability_interaction_v1_phase7b_f4_role_count_player_type_oof_predictions.csv`
- `outputs/validation/phase7b_role_availability_interaction_v1_variant_summary.csv`
- `outputs/validation/phase7b_role_availability_interaction_v1_slice_report.csv`
- `outputs/reports/phase7b_role_availability_interaction_v1_validation_report.md`
- `outputs/reports/phase7b_role_availability_interaction_v1_experiment_log_candidate.csv`
- `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md`

## I. Final Closure Status

Do not mark Phase 7B fully closed until the user/project director reviews this acceptance record, authorizes selective commit, and records the resulting commit hash.

REJECT F4 — KEEP F2
