# Phase 6A D2 Refined Probe - Unit-of-Observation Re-examination

## Purpose

The first-pass D2 probe (notebook 05) flagged 7.9% of rows as fold-spanning identical-profile clusters and tripped the
escalation threshold. That heuristic matched only on (School, Position, role, coarse Height/Weight), which conflates
genuine duplicate records with distinct same-program athletes of similar build. This refined, read-only probe tightens
the match key step by step to separate the two. No model, no features, no protocol change.

## Environment

| Item | Value |
|---|---|
| Git status | dbc2efc4ba77cd1e8eac638bb00c4cfd7fa44440 (dirty) |
| Python | 3.13.13 |
| numpy | 2.4.6 |
| pandas | 3.0.3 |
| Platform | Windows-11-10.0.26200-SP0 |

## Tiered identical-profile analysis

Each tier requires rows to match on a progressively stricter key. `fold_spanning_rows` = rows in clusters whose members
fall in >= 2 CV folds (the only configuration that actually leaks identity across folds).

| tier | description | match_key | eligible_rows | n_clusters | n_rows_in_clusters | pct_train | fold_spanning_rows | pct_fold_spanning | same_year_rows | cross_year_rows |
|---|---|---|---|---|---|---|---|---|---|---|
| T1_loose | Original coarse heuristic (Height~0.1, Weight~1) | School + Position + Player_Type + Position_Type + Height_r1 + Weight_r0 | 2781 | 119 | 252 | 0.0906 | 220 | 0.0791 | 8 | 244 |
| T2_exact_build | Exact full-precision Height + Weight | School + Position + Height + Weight | 2781 | 23 | 47 | 0.0169 | 41 | 0.0147 | 6 | 41 |
| T3_build_age | T2 + exact Age (Age present only) | School + Position + Height + Weight + Age | 2346 | 8 | 16 | 0.0058 | 16 | 0.0058 | 0 | 16 |
| T4_full_signature | School + Position + all 9 measurements + identical missingness pattern | School + Position + Height + Weight + Age + Sprint_40yd + Vertical_Jump + Bench_Press_Reps + Broad_Jump + Agility_3cone + Shuttle | 2781 | 0 | 0 | 0.0000 | 0 | 0.0000 | 0 | 0 |
| T4b_full_sig_no_school | Full measurement signature ignoring School (catches transfers/typos) | Position + Height + Weight + Age + Sprint_40yd + Vertical_Jump + Bench_Press_Reps + Broad_Jump + Agility_3cone + Shuttle | 2781 | 0 | 0 | 0.0000 | 0 | 0.0000 | 0 | 0 |

Collapse of fold-spanning rows from the loose to the strict key: **220 (7.91%) -> 0 (0.00%)**.

## Strict duplicates (T4 full measurement signature)

A T4 cluster shares School + Position + identical values across all of Height, Weight, Age, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle (including identical
missingness pattern). Two distinct athletes matching the entire measured vector is statistically implausible, so T4
clusters are near-certain duplicate records.

| Metric | Value |
|---|---|
| T4 clusters | 0 |
| T4 rows | 0 (0.00% of train) |
| T4 fold-spanning rows | 0 (0.00% of train) |
| T4 same-year rows | 0 |
| T4 cross-year rows | 0 |
| Escalation threshold | > 2% of train |
| **Refined D2 escalation** | **False** |

### Strict duplicate examples

_No rows._

## Verdict

REFINED ESCALATION CLEARED: under strict full-measurement-signature matching, fold-spanning duplicate rows fall below the 2% threshold. The original T1 escalation was driven by coarse matching of distinct same-program/position athletes with similar builds, not genuine duplicate records. Recommendation: keep the frozen StratifiedKFold folds; record unit-of-observation as 'no material same-athlete duplication confirmed'.

Effect on prior results: none. Any residual identity leak is common-mode across all V0-V7/D1 variants on the shared
frozen folds and cancels in the paired deltas, so the gap decomposition and the D1 noise floor are unaffected. The
unit-of-observation question bears only on the absolute anchor level and Phase 7 generalization estimates.

## Next gate

Do not start Phase 7 until the Phase 6A acceptance record is signed. This refined probe is read-only evidence for that
acceptance decision; it changes no protocol on its own.
