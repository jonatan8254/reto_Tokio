# Phase 6A Acceptance Record

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Phase:** Phase 6A - Baseline Reconciliation
**Date drafted:** 2026-06-11
**Status:** Accepted with warnings - pending selective commit.

---

## 1. Purpose

Record the manual review and the acceptance decision for the Phase 6A baseline reconciliation phase.

Phase 6A was scoped to:
- reconcile Phase 2 and Phase 6;
- decompose the validation gap;
- validate which changes were diagnostic-only versus methodologically acceptable;
- run D1 seed sweep to estimate the seed-noise floor and define a Phase 7 ablation threshold;
- evaluate the D2 unit-of-observation / near-duplicate risk and whether grouped CV should remain dormant;
- establish the gate conditions before opening Phase 7.

---

## 2. Evidence reviewed

The following artifacts have been reviewed to support this acceptance decision:

* `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`
* `outputs/reports/phase6a_baseline_reconciliation_report.md`
* `outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv`
* `outputs/reports/phase6a_d1_d2_diagnostics_report.md`
* `outputs/validation/phase6a_d1_seed_sweep_summary.csv`
* `outputs/reports/phase6a_d2_refined_probe_report.md`
* `outputs/validation/phase6a_d2_refined_tier_summary.csv`
* `notebooks/04_phase6a_baseline_reconciliation.ipynb`
* `notebooks/05_phase6a_d1_d2_diagnostics.ipynb`
* `notebooks/06_phase6a_d2_refined_probe.ipynb`
* `outputs/reports/phase6a_baseline_reconciliation_experiment_log_candidate.csv`
* `outputs/reports/phase6a_d1_d2_experiment_log_candidate.csv`
* `outputs/reports/phase6a_d2_refined_experiment_log_candidate.csv`
* `docs/06_validation/phase6_acceptance.md`
* `docs/01_project_planning/phase6a_baseline_reconciliation_plan.md`
* `docs/01_project_planning/project_execution_plan_v3.md`

---

## 3. Numerical Evidence Summary

**Phase 6A reconciliation:**
- V0 OOF ROC-AUC = 0.726616.
- V0 fold mean ROC-AUC = 0.729253.
- V1 Phase 2 replica fold mean = 0.812964.
- V1 successfully bridged the Phase 2 CV mean target.
- V1-V3 are diagnostic-only, deliberate-leakage variants and are ineligible as anchors.
- V4 OOF ROC-AUC = 0.809010.
- V4 fold mean ROC-AUC = 0.812399.
- V4 is a methodologically acceptable construction but is not adopted as anchor because it conflates ordinal encoding, mean imputation, and BMI.
- V5 BMI clean-context delta vs V0 = +0.000332.
- V6 ordinal clean-context delta vs V0 = -0.000804.
- V7 OOF ROC-AUC = 0.802271.
- V7 fold mean ROC-AUC = 0.805851.
- V7 is the clean upgrade candidate but is not automatically adopted as the Phase 7 anchor.

**D1 seed sweep:**
- v0median mean OOF = 0.725873.
- v0median seed std = 0.002718.
- v0median range = 0.006704.
- v7mean mean OOF = 0.802124.
- v7mean seed std = 0.001097.
- v7mean range = 0.002895.
- Paired v7mean - v0median mean delta = 0.076251.
- Paired v7mean - v0median min delta = 0.074131.
- Paired v7mean - v0median range = 0.004028.
- Same-sign fold pairs = 25/25.
- Mean-imputation effect exceeds 2 x seed-noise std on every seed.

**D2 / refined D2:**
- First-pass D2 was an upper-bound heuristic and triggered escalation.
- T1 loose D2: 119 clusters, 252 rows, 220 fold-spanning rows, 7.91% fold-spanning.
- T2 exact build: 23 clusters, 47 rows, 41 fold-spanning rows, 1.47% fold-spanning.
- T3 build + age: 8 clusters, 16 rows, 16 fold-spanning rows, 0.58% fold-spanning.
- T4 full measurement signature: 0 clusters, 0 rows, 0 fold-spanning rows, 0.00%.
- T4b full signature without School: 0 clusters, 0 rows, 0 fold-spanning rows, 0.00%.
- Refined D2 escalation = False.
- No material same-athlete duplication confirmed.

---

## 4. Boundary Compliance

Explicit boundaries maintained during Phase 6A evaluation:
- No Phase 7 was opened.
- No HPO was run.
- No submissions were generated.
- No V8 was run.
- No model-family comparison was performed.
- No public leaderboard feedback was used.
- `logs/experiment_log.csv` was not modified.
- `data/input` was not modified.
- `notebooks/_official` was not modified.
- `references` was not modified.
- `outputs/submissions` was not modified.
- `School` was not used as a model feature.
- Frozen StratifiedKFold folds were retained.
- Grouped CV remains dormant.
- Positive-class probability extraction policy remains based on estimator.classes_ where applicable.
- No causal interpretation is made.

---

## 5. Ratified Decisions

The following policy and baseline elements are explicitly recorded and ratified:

* **Anchor:** V0 retained as the incumbent Phase 7 baseline anchor.
* **Clean upgrade candidate:** V7.
* **V4:** not adopted as anchor despite high OOF because it conflates ordinal encoding, mean imputation, and BMI.
* **Encoding policy:** one-hot retained.
* **Imputation policy:** median retained in the incumbent anchor.
* **Mean imputation:** not silently adopted as anchor; it becomes the strongest Phase 7 Block 1 lead / explicit missingness hypothesis.
* **BMI:** deferred to Phase 7 Block 0 / feature-block review, not adopted automatically.
* **Ablation threshold:** OOF ROC-AUC gain >= 0.005436 and same-sign fold deltas in >= 4/5 folds.
* **Minimum slice size:** n >= 50.
* **Unit of observation:** no material same-athlete duplication confirmed under refined D2.
* **Grouped CV:** dormant.
* **StratifiedKFold** frozen folds retained.
* **Experiment Logs:** Main experiment log migration/update remains deferred.

---

## 6. Warnings and Limitations

- The mean-imputation effect is robust but likely reflects informative missingness, not a harmless nuisance parameter.
- V7 is not automatically adopted as anchor.
- V4 is not adopted as anchor despite its high OOF ROC-AUC because it conflates multiple changes.
- BMI and ordinal encoding effects are below the D1 seed-noise floor.
- Refined D2 clears material duplication, but it remains a heuristic and cannot prove athlete identity perfectly.
- School remains excluded from the feature matrix.
- Phase 7 must test missingness / measurement availability explicitly and fold-safely.
- No causal interpretation is made.

---

## 7. Phase 7 Gate

Phase 7 remains blocked until:
- this acceptance record is reviewed and signed by the human reviewer;
- the Phase 6A artifacts are selectively committed;
- no forbidden-path diffs are present;
- no files are staged unexpectedly;
- the accepted baseline policy is frozen.

Recommended first Phase 7 work:
- Block 0: freeze accepted baseline policy.
- Block 1: missingness / measurement availability.

Do not start Phase 7 from this document alone.

---

## Acceptance Status
**Decision:** ACCEPT PHASE 6A WITH WARNINGS
**Review status:** Reviewed and accepted for Phase 6A closure
**Date:** 2026-06-11
**Acceptance commit hash:** f1fb717
