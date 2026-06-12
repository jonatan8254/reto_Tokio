# Phase 7 Acceptance Draft - Missingness / Measurement Availability

Date: 2026-06-12

Experiment ID: `phase7_missingness_availability_v1`

Planning package commit: `8b21db5`

Audit status: independent artifact audit passed with non-blocking warnings.

This document is a draft acceptance record for user/project director review. It is not signed acceptance, does not open Phase 8, and does not authorize staging or commit by itself.

## A. Executive Conclusion

Phase 7 passed independent audit for artifact integrity, metric recomputation, fold alignment, leakage controls, and scope compliance.

Recommended adopted feature block, pending user/project director sign-off: `phase7_f2_median_flags_count`.

Phase 8 status: locked.

Blockers: none found.

Warnings:

- F1, F5, and F3 triggered the pre-registered slice guard on `Age_missing = 1`.
- `leakage_checks_passed` in the candidate log is `False`, but the audit found this reflects slice-guard escalation metadata rather than evidence of actual leakage.
- During Phase 7, F4 role interactions were deferred because they were not authorized in that run.

## B. Evidence-Based Analysis

F2 is the preferred adopted feature block because it satisfies all pre-registered adoption criteria:

- OOF ROC-AUC gain vs F0 is `+0.085034`, above the `0.005436` threshold.
- Fold deltas are positive in `5/5` folds.
- Mandatory slice guard is clear.
- Feature construction is row-wise and leakage-safe.
- It keeps the incumbent median-imputation policy and avoids silently adopting mean imputation.

The Phase 6A V7 effect appears largely recoverable through explicit row-wise missingness and measurement availability features. F2 reaches OOF ROC-AUC `0.811650`, compared with F0 `0.726616` and the historical Phase 6A V7 reference `0.802271`.

F1, F5, and F3 are not automatically adopted despite strong OOF gains because the pre-registered slice guard escalated them. The degradation is concentrated in `Age_missing = 1`:

- F1: delta vs F0 `-0.044204`
- F5: delta vs F0 `-0.043033`
- F3: delta vs F0 `-0.077869`

F6 was not run because the gate stayed closed:

- F5 - F1 OOF delta = `0.001498`
- Required threshold = `0.005436`

During Phase 7, F4 was deferred because it was not authorized in that run. After Phase 7, F4 was separately authorized and executed as Phase 7B, where it was rejected by the pre-registered rule.

Mean imputation is not adopted as the default policy. F5 is diagnostic only in this acceptance draft: it has strong OOF performance but remains escalated by the slice guard and would silently encode missingness through the imputation statistic rather than through an explicit, auditable feature block.

Warnings are methodological or metadata-only, not leakage-related. The audit found no evidence of test fitting, global preprocessing leakage, School-as-feature use, external data, leaderboard use, HPO, model-family comparison, submission generation, or main-log modification.

## C. Variant Decision Table

| Variant | OOF AUC | Delta vs F0 | Same-sign folds | Slice guard status | Final decision | Rationale |
|---|---:|---:|---:|---|---|---|
| `phase7_f0_anchor_recheck` | 0.726616 | 0.000000 | 0/5 | Clear | Accepted as reproduced anchor / integrity check | Reproduces Phase 6 anchor and matches Phase 6 OOF predictions within floating-point tolerance. |
| `phase7_f1_median_flags` | 0.811568 | +0.084952 | 5/5 | Triggered | Escalated, not adopted as final Phase 7 feature set | Strong OOF gain, but `Age_missing = 1` slice degrades by more than 0.02 AUC. |
| `phase7_f5_mean_flags` | 0.813066 | +0.086450 | 5/5 | Triggered | Escalated, diagnostic only; mean imputation not adopted as default | Strong OOF gain, but slice guard triggers and mean imputation remains a diagnostic branch. |
| `phase7_f2_median_flags_count` | 0.811650 | +0.085034 | 5/5 | Clear | Adopted by rule, pending user/project director sign-off | Passes OOF gain, same-sign fold, and slice-guard criteria. |
| `phase7_f3_median_flags_count_bins` | 0.810606 | +0.083989 | 5/5 | Triggered | Escalated, not adopted | Strong OOF gain, but `Age_missing = 1` slice degradation triggers escalation. |
| `phase7_f6_mean_flags_count` | Not run | Not applicable | Not applicable | Not applicable | Not run, gate closed | F5 - F1 OOF delta `0.001498` is below the `0.005436` gate. |
| `phase7_f4_role_interactions` | Not run | Not applicable | Not applicable | Not applicable | Deferred | Not authorized in the Project Authorization Note; requires new authorization and run_id. |

## D. Adopted Feature Set Specification

If accepted by the user/project director, the post-Phase-7 feature set is:

Base Phase 6 feature set:

- `Year`
- `Age`
- `Height`
- `Weight`
- `Sprint_40yd`
- `Vertical_Jump`
- `Bench_Press_Reps`
- `Broad_Jump`
- `Agility_3cone`
- `Shuttle`
- `Player_Type`
- `Position_Type`
- `Position`

Adopted Phase 7 row-wise features:

- `Age_missing`
- `Sprint_40yd_missing`
- `Vertical_Jump_missing`
- `Bench_Press_Reps_missing`
- `Broad_Jump_missing`
- `Agility_3cone_missing`
- `Shuttle_missing`
- `available_measurement_count`

Policies retained:

- Imputation policy remains median.
- Categorical policy remains fold-safe one-hot encoding.
- `School` remains excluded from the feature matrix.
- BMI remains not adopted in Phase 7 core.
- `measurement_completeness_group` is not adopted.
- Mean imputation is not adopted as default.

## E. Interpretation and Learning

The Phase 6A V7 effect appears to be largely explainable as informative missingness / measurement availability signal.

Explicit row-wise missingness and availability features recover that signal in a cleaner, more auditable way than silently changing imputation statistics.

This is a predictive and operational interpretation, not a causal claim. The result indicates association with validation ranking performance under the frozen folds and model, not that missingness causes `Drafted`.

## F. Risk and Warning Register

| Warning / risk | Severity | Evidence | Decision | Follow-up |
|---|---|---|---|---|
| `Age_missing = 1` slice degradation for F1/F5/F3 | Warning | Deltas vs F0 below `-0.02` for F1, F5, and F3 on the `Age_missing = 1` slice. | Escalate those variants; do not adopt them automatically. | Carry the warning into future validation and error analysis. |
| Candidate log `leakage_checks_passed = False` | Warning | Candidate log field is false while notebook/report show no actual leakage evidence. | Treat as metadata wording warning caused by slice escalation mapping, not actual leakage. | Record in acceptance; do not manually edit generated artifacts without separate approval. |
| F4 role-interaction opportunity deferred | Informational | F4 was deferred during Phase 7, then evaluated in Phase 7B. | F4 rejected by Phase 7B rule; keep F2. | No further role-interaction exploration before Phase 8 unless separately authorized in a later phase. |
| Phase 8 native-missing-value learner question deferred | Informational | Missingness is clearly informative, but model-family comparison is Phase 8 and remains locked. | No model-family comparison now. | Revisit only after Phase 8 authorization. |
| No submission generated | Informational | No files under `outputs/submissions/`; Phase 7 scope forbids submissions. | Correct behavior. | Submission remains locked until a later authorized phase. |

## G. Phase 8 Dependency Notes - Phase 8 Remains Locked

F4 role-aware completeness interaction was evaluated in Phase 7B and rejected; Phase 8 should use F2 unless a separate future phase explicitly authorizes new feature exploration.

Native-missing-value models such as HistGradientBoosting may change how missingness is exploited, but no model-family comparison is authorized yet.

F4 role-aware completeness interaction was evaluated in Phase 7B and rejected; Phase 8 should use F2 unless a separate future phase explicitly authorizes new feature exploration.

HPO, submissions, model-family comparison, and leaderboard use remain prohibited.

## Post-Phase 7B Addendum

F4 was subsequently authorized and executed as Phase 7B under experiment_id `phase7b_role_availability_interaction_v1`.

Phase 7B tested exactly one deferred hypothesis: `available_measurement_count x Player_Type`.

F4 was rejected by the pre-registered rule:

- F2 OOF ROC-AUC: `0.8116502602456482`
- F4 OOF ROC-AUC: `0.8093690701818260`
- F4 - F2 OOF delta: `-0.0022811900638222`
- Same-sign folds: `1/5`
- Slice guard: clear
- Leakage verdict: pass

Final joint decision after Phase 7 and Phase 7B:

- Final post-Phase-7 / Phase-7B feature set: F2.
- F4 is not adopted.
- Phase 8 remains locked.

## H. Required Acceptance Metadata

Audit status: passed with non-blocking warnings.

Artifacts reviewed:

- `notebooks/07_phase7_missingness_availability_feature_block.ipynb`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f0_anchor_recheck_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f1_median_flags_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f5_mean_flags_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f2_median_flags_count_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f3_median_flags_count_bins_oof_predictions.csv`
- `outputs/validation/phase7_missingness_availability_v1_variant_summary.csv`
- `outputs/validation/phase7_missingness_availability_v1_slice_report.csv`
- `outputs/reports/phase7_missingness_availability_v1_validation_report.md`
- `outputs/reports/phase7_missingness_availability_v1_experiment_log_candidate.csv`
- `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`
- `outputs/oof/phase6_rf_sanity_baseline_v1_oof_predictions.csv`
- `logs/experiment_log.csv` read-only diff check

Independent OOF recomputation results:

- F0: `0.7266161714116555`
- F1: `0.8115677460991508`
- F5: `0.8130660442094350`
- F2: `0.8116502602456482`
- F3: `0.8106056481642162`
- Maximum absolute difference versus variant summary: `0.0`

F0 anchor verification:

- F0 OOF AUC equals `0.726616` within planned tolerance.
- F0 predictions match `outputs/oof/phase6_rf_sanity_baseline_v1_oof_predictions.csv` with max absolute probability difference `5.551115123125783e-16`.

Fold-integrity verification:

- Every trained OOF file has `2781` rows.
- Every trained OOF file includes `Id`, `fold`, `y_true`, and `y_pred_proba`.
- Fold labels match `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`.
- Probabilities are finite, non-null, and in `[0, 1]`.
- No validation fold is one-class.

Adopted feature set:

- Base Phase 6 features plus seven missingness flags and `available_measurement_count`.

Rejected/escalated variants and reasons:

- F1: escalated for `Age_missing = 1` slice degradation.
- F5: escalated for `Age_missing = 1` slice degradation and not adopted as default imputation policy.
- F3: escalated for `Age_missing = 1` slice degradation; binning not adopted.
- F6: not run, gate closed.
- F4: originally deferred in Phase 7; subsequently evaluated in Phase 7B and rejected; keep F2.

F5 / mean imputation decision:

- Not adopted as default policy.

F3 / binning decision:

- Not adopted.

F6:

- Not run, gate closed.

F4:

- Evaluated in Phase 7B and rejected by the pre-registered rule; not adopted.

BMI disposition:

- Not adopted in Phase 7 core.

Leakage verdict:

- PASS. No evidence found of test fitting, global preprocessing leakage, `School` as feature, external data, leaderboard use, HPO, model-family comparison, submission generation, or main-log modification.

Metadata warning:

- `leakage_checks_passed` is `False` in the candidate log, apparently because at least one variant was escalated by slice guard. This should be treated as a metadata wording warning, not as actual leakage evidence.

Files recommended for future selective commit:

- `notebooks/07_phase7_missingness_availability_feature_block.ipynb`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f0_anchor_recheck_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f1_median_flags_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f5_mean_flags_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f2_median_flags_count_oof_predictions.csv`
- `outputs/oof/phase7_missingness_availability_v1_phase7_f3_median_flags_count_bins_oof_predictions.csv`
- `outputs/validation/phase7_missingness_availability_v1_variant_summary.csv`
- `outputs/validation/phase7_missingness_availability_v1_slice_report.csv`
- `outputs/reports/phase7_missingness_availability_v1_validation_report.md`
- `outputs/reports/phase7_missingness_availability_v1_experiment_log_candidate.csv`
- `docs/07_feature_engineering/phase7_acceptance.md`

Phase 8 remains locked until this acceptance is reviewed, signed by the user/project director, selectively committed, hash-recorded, and separately authorized.

## I. Final Closure Recommendation

Do not mark Phase 7 fully closed until the user/project director reviews this acceptance record, authorizes selective commit, and the resulting commit hash is recorded.

ACCEPT WITH WARNINGS
