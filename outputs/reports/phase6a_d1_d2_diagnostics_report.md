# Phase 6A Diagnostics Report - D1 Seed Sweep + D2 Unit-of-Observation Probe

## Scope

Authorized diagnostic extension of Phase 6A. Strictly limited to:

- D1: RF seed sweep of the two methodologically-acceptable anchor-candidate pipelines on the frozen folds.
- D2: read-only near-duplicate / unit-of-observation probe (no model, no features, no protocol change).

Boundary checks:

- No Phase 7, no HPO, no V8, no model-family comparison, no submissions, no public-leaderboard use.
- `logs/experiment_log.csv` not modified (candidate row only, under `outputs/reports/`).
- `School` used in D2 for duplicate detection only; it is never a model feature.
- Frozen folds loaded from the committed Phase 6 file and integrity-checked; never recomputed.

## Environment

| Item | Value |
|---|---|
| Git status | dbc2efc4ba77cd1e8eac638bb00c4cfd7fa44440 (dirty) |
| Python | 3.13.13 |
| Platform | Windows-11-10.0.26200-SP0 |
| numpy | 2.4.6 |
| pandas | 3.0.3 |
| scikit-learn | 1.9.0 |

## Integrity gates (all passed)

| Gate | Value |
|---|---|
| Frozen-folds sha256[:16] | 96937649526bcadb (== 96937649526bcadb) |
| v0median @ seed 42 OOF | 0.726616 (anchor 0.726616) |
| v7mean @ seed 42 OOF | 0.802271 (anchor 0.802271) |
| v0median@42 OOF vector vs accepted Phase 6 OOF, max|diff| | 4.44e-16 |

## D1 seed sweep (per pipeline x seed)

`v0median` = fold-safe median impute + one-hot, no BMI (incumbent V0 anchor).
`v7mean` = fold-safe mean impute + one-hot, no BMI (clean-upgrade candidate; isolates the dominant factor).

| pipeline | seed | oof_auc | fold_mean | fold_std |
|---|---|---|---|---|
| v0median | 7 | 0.722429 | 0.724626 | 0.033863 |
| v0median | 42 | 0.726616 | 0.729253 | 0.030629 |
| v0median | 123 | 0.727378 | 0.728678 | 0.032257 |
| v0median | 2025 | 0.723812 | 0.725616 | 0.034801 |
| v0median | 2026 | 0.729133 | 0.732583 | 0.030696 |
| v7mean | 7 | 0.800369 | 0.803593 | 0.029331 |
| v7mean | 42 | 0.802271 | 0.805851 | 0.026861 |
| v7mean | 123 | 0.802747 | 0.805447 | 0.030851 |
| v7mean | 2025 | 0.801970 | 0.805507 | 0.029376 |
| v7mean | 2026 | 0.803264 | 0.806897 | 0.025608 |

## D1 noise floor (OOF ROC-AUC across 5 seeds)

| pipeline | mean | std_sample | min | max | range |
|---|---|---|---|---|---|
| v0median | 0.725873 | 0.002718 | 0.722429 | 0.729133 | 0.006704 |
| v7mean | 0.802124 | 0.001097 | 0.800369 | 0.803264 | 0.002895 |

Seed-noise std (OOF, max of the two pipelines): **0.002718**.

## D1 paired contrast (v7mean - v0median, same seed)

| seed | v0median_oof | v7mean_oof | delta_v7_minus_v0 |
|---|---|---|---|
| 42.000000 | 0.726616 | 0.802271 | 0.075655 |
| 2025.000000 | 0.723812 | 0.801970 | 0.078158 |
| 7.000000 | 0.722429 | 0.800369 | 0.077940 |
| 123.000000 | 0.727378 | 0.802747 | 0.075369 |
| 2026.000000 | 0.729133 | 0.803264 | 0.074131 |

Paired OOF delta: mean **0.076251**, min **0.074131**, range 0.004028.
Same-sign positive fold pairs: **25/25**.
Mean-imputation effect exceeds 2.0 x seed-noise std on every seed: **True**.

## D1 per-fold seed noise (std of each fold AUC across seeds)

| pipeline | fold | fold_auc_std_across_seeds |
|---|---|---|
| v0median | 0 | 0.006001 |
| v0median | 1 | 0.003792 |
| v0median | 2 | 0.004492 |
| v0median | 3 | 0.006400 |
| v0median | 4 | 0.002917 |
| v7mean | 0 | 0.004817 |
| v7mean | 1 | 0.005530 |
| v7mean | 2 | 0.002151 |
| v7mean | 3 | 0.003909 |
| v7mean | 4 | 0.001741 |

## Proposed ablation threshold (for human ratification - NOT auto-adopted)

Proposed rule for Phase 7 feature-block acceptance:

> A block is accepted only if its OOF ROC-AUC gain over the anchor is **>= 0.005436**
> (= max(2.0 x seed_std 0.002718, floor 0.005)),
> **and** the per-fold delta is the same sign in **>= 4/5** folds.

Proposed minimum slice size for diagnostics: **n >= 50** (smallest fold has 360 positives / 195 negatives; final value to be cross-checked against the Phase 6 slice-report variance). These are proposals; the Phase 6A acceptance record ratifies the final numbers.

## D2 unit-of-observation probe (read-only)

Heuristic: rows sharing identical (`School`, `Position`, `Player_Type`, `Position_Type`, Height rounded to 0.1, Weight rounded to 1) are flagged as the same-athlete / duplicate-record candidates. Descriptive only.

| Metric | Value |
|---|---|
| Identical-profile clusters (size >= 2) | 119 |
| Rows in such clusters | 252 (9.06% of train) |
| Cross-year clusters | 115 (rows 244) |
| Clusters spanning >= 2 CV folds | 103 (rows 220) |
| Escalation threshold (fold-spanning rows) | > 2% of train |
| **D2 escalation** | **True** |

Examples (largest clusters):

| cluster_id | cluster_size | n_distinct_years | n_folds_spanned | cross_year | Id | Year | School | Position | Player_Type | Position_Type | Height | Weight | Drafted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 67 | 4 | 3 | 3 | True | 52 | 2014 | Ohio St. | CB | defense | defensive_back | 1.803400 | 87.996920 | 1 |
| 67 | 4 | 3 | 3 | True | 2143 | 2017 | Ohio St. | CB | defense | defensive_back | 1.828800 | 87.543327 | 1 |
| 67 | 4 | 3 | 3 | True | 2441 | 2017 | Ohio St. | CB | defense | defensive_back | 1.828800 | 88.450512 | 1 |
| 67 | 4 | 3 | 3 | True | 1164 | 2019 | Ohio St. | CB | defense | defensive_back | 1.803400 | 87.543327 | 1 |
| 2 | 3 | 3 | 2 | True | 1369 | 2010 | Alabama | CB | defense | defensive_back | 1.778000 | 88.904105 | 1 |
| 2 | 3 | 3 | 2 | True | 928 | 2016 | Alabama | CB | defense | defensive_back | 1.778000 | 89.357697 | 1 |
| 2 | 3 | 3 | 2 | True | 2211 | 2017 | Alabama | CB | defense | defensive_back | 1.828800 | 89.357697 | 1 |
| 16 | 3 | 2 | 2 | True | 772 | 2011 | Boston Col. | OT | offense | offensive_lineman | 2.032000 | 142.881597 | 0 |
| 16 | 3 | 2 | 2 | True | 1442 | 2013 | Boston Col. | OT | offense | offensive_lineman | 2.006600 | 143.335189 | 0 |
| 16 | 3 | 2 | 2 | True | 2281 | 2013 | Boston Col. | OT | offense | offensive_lineman | 2.006600 | 142.881597 | 0 |
| 21 | 3 | 3 | 2 | True | 2050 | 2010 | Clemson | CB | defense | defensive_back | 1.828800 | 86.636143 | 1 |
| 21 | 3 | 3 | 2 | True | 100 | 2015 | Clemson | CB | defense | defensive_back | 1.828800 | 86.636143 | 0 |
| 21 | 3 | 3 | 2 | True | 1259 | 2019 | Clemson | CB | defense | defensive_back | 1.778000 | 87.089735 | 0 |
| 27 | 3 | 3 | 2 | True | 2592 | 2010 | Florida | CB | defense | defensive_back | 1.803400 | 87.543327 | 1 |
| 27 | 3 | 3 | 2 | True | 2602 | 2012 | Florida | CB | defense | defensive_back | 1.778000 | 87.543327 | 1 |
| 27 | 3 | 3 | 2 | True | 2018 | 2014 | Florida | CB | defense | defensive_back | 1.803400 | 87.996920 | 1 |
| 34 | 3 | 3 | 2 | True | 965 | 2010 | Florida St. | OLB | defense | line_backer | 1.854200 | 108.862169 | 1 |
| 34 | 3 | 3 | 2 | True | 1342 | 2012 | Florida St. | OLB | defense | line_backer | 1.879600 | 109.315761 | 1 |
| 34 | 3 | 3 | 2 | True | 2282 | 2014 | Florida St. | OLB | defense | line_backer | 1.905000 | 108.862169 | 0 |
| 40 | 3 | 3 | 3 | True | 659 | 2010 | Iowa | OT | offense | offensive_lineman | 1.955800 | 142.428004 | 1 |

Interpretation: identical-profile rows that land in different CV folds would let the same athlete's identity leak across folds, optimistically biasing every absolute AUC. Because all D1/V0-V7 contrasts share the same folds, this bias is common-mode and largely cancels in paired deltas; the decomposition conclusions are unaffected. D2 escalation triggered: grouped-CV is now a live protocol question - STOP and obtain a human ruling before Phase 7.

## Closure status

D1 and D2 are executed and ready for human review. They do not by themselves close Phase 6A: the anchor, encoding policy, BMI disposition, ablation threshold, and minimum slice size are ratified in `docs/06_validation/phase6a_acceptance.md` (not created here).

## Next gate

Do not start Phase 7 until the Phase 6A acceptance record is signed.
