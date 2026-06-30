# Final Notebook Section Blueprint — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY — NOTHING IS BUILT, TRAINED, REFIT, SUBMITTED, OR COMMITTED IN THIS RUN.** This document designs the structure of the future final integrated notebook (`99_final_integrated_project_report.ipynb`) and its portable package. No model is trained, no hyperparameter search is run, no new submission is created, no existing submission is modified, no leaderboard is consulted for any decision, no final winner is declared, `logs/experiment_log.csv` is untouched, and nothing is staged, committed, or pushed. Every concrete number, file path, SHA, and reference cited below is taken from accepted project artifacts; anything not verifiable is marked "Not confirmed yet".

---

## 1. Purpose and reading guide

This blueprint specifies the section-by-section structure of the final deliverable notebook, conceived as an **executable technical report**: a single document that a reader can run top-to-bottom in three runtime modes while also reading it as a complete, professional account of the project. The notebook is the centerpiece of a minimal portable package (`README.md`, `requirements.txt`, `references.md`, `99_final_integrated_project_report.ipynb`, `data/`, `outputs/`).

The notebook to be built must be a clean, professional data-science deliverable. The portable package and all shipped files must read as a standard academic competition report. The future build run (governed by a separate build-spec file, `prompt_build_final_portable_package.md`) is referred to here neutrally as "the build run" or "the construction step".

### 1.1 Result-provenance labels (mandatory on every historical number)

Every metric, SHA, count, or threshold that the notebook displays must carry exactly one provenance label so a reader always knows whether a number was produced live or recalled:

| Label | Meaning |
|---|---|
| **Computed in this notebook** | Produced by code cells executing in the current runtime (e.g., a fresh OOF AUC computed on the spot). |
| **Loaded from repository artifact** | Read at runtime from a persisted file in the repository (e.g., an OOF CSV, a fold-assignment file). |
| **Recorded from accepted project artifact** | Quoted from an accepted phase record/report; not recomputed in this runtime (e.g., a CatBoost OOF obtained in a separate environment). |
| **Not available in current runtime** | The quantity cannot be produced or loaded in the active mode (e.g., CatBoost OOF in Colab Minimal without the package); the recorded value is shown with this label. |

### 1.2 Global prohibitions (apply to the whole notebook)

- No declaration of a final winner. CatBoost tuned is the best global OOF candidate **with warnings**; M1 logistic regression is the fallback/reference. The director chooses the upload order manually.
- No use of the public/private leaderboard to drive feature selection, model selection, hyperparameter choices, preprocessing, or submission choice. Leaderboard is sanity-check only.
- No modification of historical submissions; existing submission CSVs are identified by their SHA-256.
- No mention anywhere in the shipped narrative of internal execution tooling, code-generation aids, planning chats, or process traces. The only permitted generative-AI mention is the sober ChatGPT disclosure described in its dedicated section.

### 1.3 Per-phase closing requirement

Every phase section (Phases 1 through 11, plus 6A, 7B, the Wave 2 sub-section, 9A, and 9B-Lite) must end with a subsection titled exactly:

```
#### Key conclusions from this phase
```

This subsection states what was decided, why, what carried forward, and what was explicitly deferred or rejected.

---

## 2. Three runtime modes (planned content — described, not implemented here)

The notebook is designed to detect and adapt to three modes. These are described as planned behavior; no detection code is written in this planning run.

- **Mode 1 — Full Repository.** Runs from the cloned repository against `data/input/` and persisted artifacts in `outputs/`. Frozen folds, all persisted OOF files, and recorded phase metrics are available to load. Historical numbers appear as **Loaded from repository artifact** or **Recorded from accepted project artifact**; live recomputations appear as **Computed in this notebook**.
- **Mode 2 — Portable Package.** Runs from the minimal ZIP on a local machine. Official CSVs are present under `data/input/` (Scenario A) or replaced by placeholders with instructions (Scenario B). Frozen folds are regenerated deterministically; the M1 logistic-regression path always runs; the CatBoost path runs only if the optional package is installed, otherwise it falls back cleanly and labels CatBoost figures **Not available in current runtime**.
- **Mode 3 — Colab Minimal.** Runs in Google Colab with a core dependency set. The user supplies the three CSVs. Folds are regenerated; the M1 path computes fresh OOF and a fresh submission; CatBoost numbers are shown as **Recorded from accepted project artifact** or **Not available in current runtime**. Heavy historical evidence is shown from recorded values, never recomputed.

### 2.1 Robust path-configuration cell (planned content)

A single early configuration cell is planned to establish a portable project root and resolve all input/output paths relative to it, so the same notebook runs unchanged across the three modes. It is planned to: detect whether it is running in Colab; resolve `data/input/` for train/test/sample-submission; resolve `outputs/` subfolders (`folds/`, `oof/`, `validation/`, `reports/`, `submissions/`, `figures/`) and create the ones that may be written; and degrade gracefully to "regenerate fresh" when a persisted artifact is absent. No path code is written in this planning run.

### 2.2 Optional Colab upload-fallback cell (planned content)

An optional, clearly-marked cell is planned for Colab to let the user upload the three official CSVs when they are not already mounted, moving them into `data/input/`. It is planned to be a no-op outside Colab and when the files already exist. This cell is described only; it is not implemented here.

---

## 3. Section catalogue (spec lines)

Each section below carries a compact spec line. Fields: **Purpose**; **Main evidence files**; **Portable-package dependency**; **Colab executable?** (Yes/No/Partial); **Full repo only?** (Yes/No); **Code cells required?**; **Tables required?**; **Figures required?**; **Expected conclusion**; **Decision rationale required?**; **Transition analysis required?**; **Section takeaways required?**; **Risks/caveats**. Phase sections additionally close with `#### Key conclusions from this phase`.

Ordering note: sections may be merged or subdivided for clarity during the build run, but author info, UNAL attribution, explicit Phase 1–11 coverage, decision rationale, references, the sober ChatGPT disclosure, final submission validation, and limitations/risks must never be omitted.

### 3.1 Front matter and operating instructions

#### S1. Title Page / Author Information
- **Purpose:** Identify the deliverable, author, institution, and program.
- **Main evidence files:** Not applicable (front matter).
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown only).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** No (a small identity block is acceptable).
- **Figures required?** No.
- **Expected conclusion:** Reader knows the work is authored by **Jonatan Estiven Sanchez Vargas**, **Universidad Nacional de Colombia**, **Systems and Computer Engineering (Ingenieria de Sistemas e Informatica)**, project **Reto Tokio / GCI World NFL Draft Prediction**.
- **Decision rationale required?** No.
- **Transition analysis required?** No.
- **Section takeaways required?** No.
- **Risks/caveats:** Must contain no internal-tooling mention.

#### S2. Executive Summary
- **Purpose:** One-page account of objective, method, validation discipline, final candidates, and handoff state.
- **Main evidence files:** `outputs/validation/phase11_submission_readiness_phase11_option_c_20260619_0001_model_summary.csv`; `outputs/reports/phase11_submission_readiness_phase11_option_c_20260619_0001_validation_report.md`.
- **Portable-package dependency:** Recorded values; no compute.
- **Colab executable?** Yes (Markdown; numbers labeled **Recorded from accepted project artifact**).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (compact results table: M0 0.8116502602, M1 0.8270821070, CatBoost tuned 0.8303208581, with provenance labels).
- **Figures required?** No.
- **Expected conclusion:** A leakage-safe, frozen-fold pipeline on the 21-feature F2 set yields two validated 696-row submissions; no winner is declared; upload is a manual director decision.
- **Decision rationale required?** Yes (brief).
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Must state positive rate 0.6483 and that ROC-AUC is the official metric; must not present any number as a confirmed leaderboard outcome.

#### S3. How to Run This Notebook in Google Colab
- **Purpose:** Step-by-step run instructions across the three modes, emphasizing Colab.
- **Main evidence files:** Not applicable.
- **Portable-package dependency:** `requirements.txt`; the official CSVs (Scenario A) or upload instructions (Scenario B).
- **Colab executable?** Yes.
- **Full repo only?** No.
- **Code cells required?** Yes (describe the path-config and optional upload-fallback cells; the cells are built later, not here).
- **Tables required?** Yes (mode comparison: data source, models available, runtime).
- **Figures required?** No.
- **Expected conclusion:** A reader can reproduce the M1 path and a valid 696-row submission in Colab; CatBoost numbers may be recorded-only in that mode.
- **Decision rationale required?** No.
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Must warn that CatBoost requires the optional package and a separate-environment lineage; in Colab it may be **Not available in current runtime**.

#### S4. Portable Package Overview
- **Purpose:** Describe the minimal shipped package and the Scenario A/B data-governance choice.
- **Main evidence files:** `README.md`, `references.md`, `requirements.txt` (package files, planned).
- **Portable-package dependency:** Defines it.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (file inventory: include vs exclude).
- **Figures required?** No.
- **Expected conclusion:** The package contains only `README.md`, `requirements.txt`, `references.md`, `99_final_integrated_project_report.ipynb`, `data/`, and an empty `outputs/` tree; everything else stays in the repository.
- **Decision rationale required?** Yes (why minimal).
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Must exclude `.git/`, `.venv/`, internal folders, backup notebooks, reference PDFs (cited not shipped), and all planning/build files; Scenario B must ship CSV placeholders plus instructions.

### 3.2 Problem framing and contract

#### S5. Competition Objective and ML Framing
- **Purpose:** State the binary-classification task and the official scoring.
- **Main evidence files:** `docs/00_project_contract/challenge_brief.md`.
- **Portable-package dependency:** None (narrative).
- **Colab executable?** Yes.
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Optional.
- **Figures required?** No.
- **Expected conclusion:** Predict probability of `Drafted = 1`; metric is ROC-AUC on the positive-class probability; submission is `Id,Drafted` with 696 rows.
- **Decision rationale required?** Yes (why ROC-AUC framing fits a 0.6483 positive rate).
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** No external data may be used; external data invalidates ranking.

#### S6. Official Data Contract
- **Purpose:** Verify shapes, target, balance, and missingness against the official files.
- **Main evidence files:** `data/input/train.csv`, `data/input/test.csv`, `data/input/sample_submission.csv`; `docs/00_project_contract/submission_checklist.md`.
- **Portable-package dependency:** Official CSVs (Scenario A) or placeholders (Scenario B).
- **Colab executable?** Yes (recomputes shapes and missingness live).
- **Full repo only?** No.
- **Code cells required?** Yes.
- **Tables required?** Yes (shapes 2781×16 / 696×15 / 696×2; class balance 0=978, 1=1803, positive rate 0.6483279396; per-column missing counts for train and test).
- **Figures required?** Yes (missingness comparison; target distribution).
- **Expected conclusion:** Data contract holds; Id order matches `sample_submission.csv`.
- **Decision rationale required?** Yes (why ROC-AUC, not accuracy).
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Test has no `Drafted`; test must never be used for fitting; numbers here are **Computed in this notebook**.

### 3.3 Phase narrative (Phases 1–11)

#### S7. Phase 1 — Project Contract and Rules
- **Purpose:** Document repository discipline, seeds, governance rules.
- **Main evidence files:** `docs/01_project_planning/project_execution_plan_v2_context_efficient.md`, `docs/01_project_planning/project_execution_plan_v3.md`; `README.md`.
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Optional.
- **Figures required?** No.
- **Expected conclusion:** Notebook-first, reproducible-from-clean-kernel, fixed seeds, official-files-only, selective-staging governance is established.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes (`#### Key conclusions from this phase`).
- **Risks/caveats:** Phase 1 was never formally closed in early history (closure-by-inference); environment pinning recorded later; mark unconfirmed items "Not confirmed yet".

#### S8. Phase 2 — Baseline Reproduction
- **Purpose:** Reproduce the official baseline and establish a historical reference metric.
- **Main evidence files:** `notebooks/01_baseline_reproduction.ipynb`; `docs/01_project_planning/integral_project_review_phase0_phase6.md`.
- **Portable-package dependency:** Recorded values; the notebook need not re-run RF(seed 2025) live.
- **Colab executable?** Partial (may recompute optionally; recorded by default).
- **Full repo only?** No.
- **Code cells required?** Optional.
- **Tables required?** Yes (CV ROC-AUC 0.812964 ± 0.025740; public LB 0.80792, labeled as historical record).
- **Figures required?** No.
- **Expected conclusion:** Baseline reproduced, but it is leakage-inflated by design (global imputation, global label encoding, BMI) and is a reference only, not an anchor.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** The CV↔OOF gap (~0.084 vs the later 0.726616 clean OOF) must be flagged as expected, not as a regression; LB number must not justify global preprocessing.

#### S9. Phase 3 — EDA and Data Contract
- **Purpose:** Map signal families, risks, and hypotheses without locking any feature.
- **Main evidence files:** `notebooks/02_eda_and_data_contract.ipynb`; `docs/03_eda/experiment_notes.md`; `outputs/figures/phase03_*.png`.
- **Portable-package dependency:** Official CSVs to regenerate selected figures.
- **Colab executable?** Partial (regenerate a small figure subset live; full set is recorded).
- **Full repo only?** No.
- **Code cells required?** Yes (a small, fast EDA subset).
- **Tables required?** Yes (missingness; class balance).
- **Figures required?** Yes (target distribution; missingness; role-aware contrarian association).
- **Expected conclusion:** Four signal families (role context, measurement availability, role-aware physical profile, institutional/categorical context) identified as hypotheses; diagnostic-only variables stay out of the model.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Age_missing shows a strong train-only target-rate spread (~0.747) — diagnostic only, never adopted without fold-safe validation; School high-cardinality/test-only-category risk noted.

#### S10. Phase 4 — Research and Methodological Foundation
- **Purpose:** Convert literature and EDA into project rules for validation, leakage, features, models, HPO, reproducibility.
- **Main evidence files:** `docs/04_research/research_notes_validation.md`, `research_notes_leakage.md`, `research_notes_feature_engineering.md`, `research_notes_tabular_models.md`, `research_notes_hpo.md`, `research_notes_reproducibility.md`, `pdf_key_findings.md`, `pdf_review_audit.md`.
- **Portable-package dependency:** None (cites references, ships none).
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (rule → supporting reference mapping).
- **Figures required?** No.
- **Expected conclusion:** Fit-scope leakage rule, frozen fold strategy, feature-block roadmap, model order, and HPO gates are codified, each citing a real reference.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Research summaries are secondary evidence; on conflict, the official brief governs.

#### S11. Phase 5 — Frozen Execution Decisions
- **Purpose:** Formalize the frozen methodology that binds all later phases.
- **Main evidence files:** `docs/05_methodology/phase5_execution_decisions.md`, `phase5_methodology_plan.md`, `validation_protocol_phase6.md`, `leakage_checklist_phase6.md`.
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (frozen decisions list).
- **Figures required?** No.
- **Expected conclusion:** ROC-AUC via verified `estimator.classes_`, `StratifiedKFold(5, shuffle=True, random_state=42)`, OOF anchor, fold-safe fit-scope, School excluded until later, submission only in Phase 11, log governance — all frozen.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Quantitative ablation threshold, minimum slice size, and unit-of-observation were deferred to Phase 6A at freeze time (mark which remained "Not confirmed yet" until then).

#### S12. Phase 6 — Validation Harness
- **Purpose:** Establish the leakage-safe validation harness, frozen folds, OOF, and slice diagnostics.
- **Main evidence files:** `notebooks/03_validation_harness_phase6.ipynb`; `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`; `outputs/oof/phase6_rf_sanity_baseline_v1_oof_predictions.csv`; `outputs/validation/phase6_rf_sanity_baseline_v1_slice_report.csv`; `outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`; `docs/06_validation/phase6_acceptance.md`.
- **Portable-package dependency:** Frozen fold file (loaded in repo mode; regenerated deterministically otherwise).
- **Colab executable?** Yes (RF anchor recomputable; fold integrity re-asserted).
- **Full repo only?** No.
- **Code cells required?** Yes.
- **Tables required?** Yes (per-fold AUC 0.690076 / 0.751758 / 0.761581 / 0.704939 / 0.737911; fold mean 0.729253 ± 0.030629; OOF 0.726616).
- **Figures required?** Optional (fold-AUC bar).
- **Expected conclusion:** Clean OOF anchor 0.726616 established on frozen folds; fold file SHA256[:16]=96937649526bcadb over 2781 rows.
- **Decision rationale required?** Yes (why OOF over fold mean; why median imputation in-fold).
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Anchor is OOF (0.726616), not fold mean (0.729253) — consumers must read OOF; School/diagnostic flags excluded from features by design.

#### S13. Phase 6A — Baseline Reconciliation
- **Purpose:** Decompose the Phase 2↔Phase 6 gap and set the ablation threshold and duplication verdict.
- **Main evidence files:** `notebooks/04_phase6a_baseline_reconciliation.ipynb`, `05_phase6a_d1_d2_diagnostics.ipynb`, `06_phase6a_d2_refined_probe.ipynb`; `outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv`, `phase6a_d1_seed_sweep_summary.csv`, `phase6a_d2_refined_tier_summary.csv`; `outputs/reports/phase6a_*` ; `docs/06_validation/phase6a_acceptance.md`.
- **Portable-package dependency:** Recorded values (variant sweep is repo-heavy).
- **Colab executable?** No (full variant/seed sweep is repo-only; values recorded).
- **Full repo only?** Yes (for the full sweep).
- **Code cells required?** Optional (load summaries; no heavy re-sweep).
- **Tables required?** Yes (V0 0.726616 anchor; V7 mean-impute 0.802271; D1 seed std 0.002718; threshold 0.005436; D2 tiers T1→T4).
- **Figures required?** Optional.
- **Expected conclusion:** Mean imputation explains most of the gap (informative missingness), but is not silently adopted; ablation threshold set to OOF gain ≥ 0.005436 AND same-sign folds ≥ 4/5; duplication escalation cleared (T4 strict = 0%).
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** V1/V4 are leakage-inflated diagnostics, never anchors; grouped CV remains dormant; minimum slice size set to n ≥ 50.

#### S14. Phase 7 — Feature Engineering: Missingness / Availability
- **Purpose:** Test missingness/availability features under fixed-fold ablation and adopt F2.
- **Main evidence files:** `notebooks/07_phase7_missingness_availability_feature_block.ipynb`; `outputs/validation/phase7_missingness_availability_v1_variant_summary.csv`, `..._slice_report.csv`; `outputs/oof/phase7_missingness_availability_v1_*`; `docs/07_feature_engineering/phase7_acceptance.md`.
- **Portable-package dependency:** F2 feature build (the live pipeline path).
- **Colab executable?** Yes (F0/F1/F2 recomputable with M0 RF).
- **Full repo only?** No.
- **Code cells required?** Yes.
- **Tables required?** Yes (F0 0.726616; F1 0.811568 escalated; F2 0.811650 adopted; F3 0.810606 escalated; F5 0.813066 escalated; F6 not run, gate closed).
- **Figures required?** Optional.
- **Expected conclusion:** F2 (13 base + 7 missingness flags + available_measurement_count = 21 features) adopted by rule (delta +0.0850 > 0.005436, 5/5 folds, slice guard clear); median imputation retained; mean imputation diagnostic-only; School excluded; BMI not adopted.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** F1/F3/F5 triggered the Age_missing=1 slice guard; explicit flags preferred over implicit imputation shifts.

#### S15. Phase 7B — Role-Aware Interaction Probe
- **Purpose:** Evaluate the single deferred role interaction (available_measurement_count × Player_Type).
- **Main evidence files:** `notebooks/07b_phase7b_role_availability_interaction_probe.ipynb`; `outputs/validation/phase7b_role_availability_interaction_v1_variant_summary.csv`, `..._slice_report.csv`; `outputs/oof/phase7b_*`; `docs/07_feature_engineering/phase7b_role_interaction_acceptance.md`.
- **Portable-package dependency:** Recorded values; optional live recompute on F2.
- **Colab executable?** Partial.
- **Full repo only?** No.
- **Code cells required?** Optional.
- **Tables required?** Yes (F2 0.8116502602 vs F4 0.8093690702; delta −0.0022811901; same-sign folds 1/5).
- **Figures required?** No.
- **Expected conclusion:** F4 rejected by rule (OOF negative, 1/5 folds < 4/5); F2 retained as the final 21-feature set.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Localized slice gains (special_teams, kicking_specialist) do not survive global OOF; role-specific modeling deferred.

#### S16. Phase 8 — Model-Family Comparison (sklearn-native)
- **Purpose:** Compare five sklearn-native models on frozen F2 and frozen folds.
- **Main evidence files:** `notebooks/08_phase8_model_family_comparison.ipynb`; `outputs/oof/` Phase 8 Wave 1 files; `docs/08_model_comparison/phase8_acceptance.md`.
- **Portable-package dependency:** Recorded values; M0/M1 recomputable live.
- **Colab executable?** Partial (M0, M1 recomputable; tree variants recorded).
- **Full repo only?** No.
- **Code cells required?** Yes (M0, M1 paths).
- **Tables required?** Yes (M0 0.8116502602 anchor; M1 0.8270821070 +0.0154 4/5 candidate-with-warning; M2 0.8055237975; M3 0.7896938413; M4 0.8093293727).
- **Figures required?** Optional.
- **Expected conclusion:** M1 is the strongest non-anchor on global OOF (4/5 folds) but carries a slice warning (Age_missing=1, 8 positives, AUC 0.5442); accepted with warnings; external GBDTs deferred to Wave 2.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** M1 baseline exact config (C/penalty/solver/scaling) is **Not confirmed yet** in artifacts — recover from Phase 8 artifacts, do not invent; no winner declared.

#### S17. Phase 8 Wave 2 — External GBDT Comparison
- **Purpose:** Compare XGBoost, LightGBM, CatBoost against M0/M1 in a separate environment.
- **Main evidence files:** `notebooks/08b_phase8_wave2_dependency_environment_check.ipynb`, `08c_phase8_wave2_external_gbdt_comparison.ipynb`; `outputs/oof/` Phase 8 Wave 2 files; `docs/08_model_comparison/phase8_wave2_acceptance.md`.
- **Portable-package dependency:** CatBoost optional package; falls back when absent.
- **Colab executable?** Partial (only if the optional package is installed; otherwise recorded / Not available).
- **Full repo only?** No.
- **Code cells required?** Optional (guarded import).
- **Tables required?** Yes (xgboost 0.8113477084 dropped; lightgbm 0.8062204891 dropped; catboost baseline 0.8202943969 escalated).
- **Figures required?** Optional.
- **Expected conclusion:** XGB/LGBM show no qualifying evidence; CatBoost passes the OOF bar (4/5 vs M0) but slice guard triggers → escalated; no winner; M1 remains strongest global OOF.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** CatBoost ran in a separate environment (catboost 1.2.10), base `.venv` untouched; in Colab its numbers may be **Recorded from accepted project artifact** or **Not available in current runtime**.

#### S18. Phase 9A — AUC Ranking Diagnostics
- **Purpose:** Read-only AUC/PR/ranking/imbalance diagnostics over all five candidates.
- **Main evidence files:** `notebooks/09a_auc_ranking_diagnostics.ipynb`; persisted Phase 8 OOF files; `docs/09_auc_ranking_diagnostics/phase9a_acceptance.md`, `phase9a_improvement_backlog.md`.
- **Portable-package dependency:** Persisted OOF (repo mode); recorded otherwise.
- **Colab executable?** Partial (re-derivable from OOF CSVs if shipped; otherwise recorded).
- **Full repo only?** No.
- **Code cells required?** Optional.
- **Tables required?** Yes (ROC-AUC, PR-AUC, neg-class AP, Brier per model; M1 leads all global lenses; Spearman M1↔CatBoost 0.818, XGB↔LGBM 0.952).
- **Figures required?** Optional (score distributions).
- **Expected conclusion:** Complementary imbalance metrics confirm the ROC-AUC ordering; no re-ranking; M1 carry, CatBoost observe, XGB/LGBM drop; no winner, no submission.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** M1's Age_missing=1 collapse is fragile (8 positives); M1 lead stability under resampling unconfirmed.

#### S19. Phase 9B-Lite — Transition
- **Purpose:** Record the deliberate skip of a full Phase 9B cycle while preserving the evidence trail.
- **Main evidence files:** `docs/09_auc_ranking_diagnostics/phase9b_lite_transition_memo.md`.
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Optional.
- **Figures required?** No.
- **Expected conclusion:** M1 advances as primary Phase 10 candidate, CatBoost secondary, XGB/LGBM dropped; risks to monitor carried forward.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** No training, HPO, ensemble, calibration, threshold, or submission occurred here.

#### S20. Phase 10 — Controlled Model Optimization
- **Purpose:** Bounded hyperparameter search on M1 and CatBoost within pre-registered spaces; candidate recommendation without a winner.
- **Main evidence files:** `notebooks/10_phase10_model_optimization.ipynb`; `outputs/validation/phase10_*` (incl. hpo_results); `docs/10_model_optimization/phase10_acceptance.md`.
- **Portable-package dependency:** Recorded values (no search re-run in the notebook).
- **Colab executable?** No (the bounded search is repo/separate-env; values recorded).
- **Full repo only?** Yes (for the search; the recommendation is narrative).
- **Code cells required?** No (recorded only; the notebook must not re-run the search).
- **Tables required?** Yes (M1 tuned 0.8274819178 rejected, +0.0003998 vs M1 base, 3/5; CatBoost tuned 0.8303208581, +0.0186706 vs M0 5/5, +0.0032388 vs M1 base 3/5 below bar).
- **Figures required?** No.
- **Expected conclusion:** M1 tuning rejected as noise-level; CatBoost tuned is the best global OOF candidate but warning-heavy with no repeated-CV; accepted with warnings; no winner, no submission opened by this phase.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** CatBoost tuned config (depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]) ran in a separate environment; deterministic bounded search replaced Optuna-TPE; no repeated-CV stability audit for CatBoost; this section must not re-run HPO.

#### S21. Phase 11 — Final Refit and Submission Readiness
- **Purpose:** Full-train refit, test inference, and validated submissions for both candidates (Option C, dual submission).
- **Main evidence files:** `notebooks/11_phase11_submission_readiness.ipynb`; `outputs/validation/phase11_submission_readiness_phase11_option_c_20260619_0001_{candidate_selection_report,final_refit_report,model_summary,submission_validation}.csv`; `outputs/reports/phase11_submission_readiness_phase11_option_c_20260619_0001_{validation_report.md,artifact_manifest.csv,experiment_log_candidate.csv}`.
- **Portable-package dependency:** Live refit possible for M1; CatBoost refit only with the optional package.
- **Colab executable?** Partial (M1 refit + submission live; CatBoost recorded or package-gated).
- **Full repo only?** No.
- **Code cells required?** Yes (M1 full-train refit and 696-row inference path; fit-scope on train only; `classes_` check before positive-class extraction).
- **Tables required?** Yes (both candidates: 696 rows, prob ranges, SHA-256).
- **Figures required?** No.
- **Expected conclusion:** Two validated 696-row submissions produced from logged, reproducible candidates; no winner declared; manual upload.
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Submissions are gitignored — SHA-256 is durable identity (CatBoost `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8`; M1 `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640`); the notebook must not recreate or overwrite historical submissions; if it regenerates a submission live it must write to a clearly separate runtime path and never claim to reproduce a historical SHA unless byte-identical.

### 3.4 Closeout sections

#### S22. Final Submission Validation
- **Purpose:** Re-assert that the produced/recorded submissions satisfy the official format.
- **Main evidence files:** `outputs/validation/phase11_submission_readiness_phase11_option_c_20260619_0001_submission_validation.csv`; `data/input/sample_submission.csv`.
- **Portable-package dependency:** Sample submission for Id-order check.
- **Colab executable?** Yes (validate any locally produced submission live).
- **Full repo only?** No.
- **Code cells required?** Yes.
- **Tables required?** Yes (12-check summary: header [Id, Drafted]; 696 rows; Id set/order match; probs ∈ [0,1]; no NaN/inf/duplicates; SHA-256 recorded; no manual edits).
- **Figures required?** No.
- **Expected conclusion:** Both recorded submissions pass; any live M1 submission also passes the same checks.
- **Decision rationale required?** Yes.
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Last uploaded file determines final ranking; private LB uses the full test set; leaderboard is sanity-check only.

#### S23. Final Recommendation and Manual Upload Handoff
- **Purpose:** State the recommendation and hand the upload decision to the director.
- **Main evidence files:** `outputs/validation/phase11_submission_readiness_phase11_option_c_20260619_0001_candidate_selection_report.csv`; `docs/11_submission_readiness/phase11_operator_runbook.md`.
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (primary vs fallback summary).
- **Figures required?** No.
- **Expected conclusion:** Primary = CatBoost tuned (best global OOF, with explicit slice/stability caveats); fallback = M1 baseline (simpler, 4/5 folds vs M0); no winner declared; upload order is the director's manual choice (last-file-wins).
- **Decision rationale required?** Yes.
- **Transition analysis required?** Yes (Phase 11 → final recommendation).
- **Section takeaways required?** Yes.
- **Risks/caveats:** No automated upload; the leaderboard must not be used to choose between the two.

#### S24. Limitations and Risks
- **Purpose:** State honest constraints and residual risks.
- **Main evidence files:** Phase 9A/10/11 reports (as cited above).
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Optional.
- **Figures required?** No.
- **Expected conclusion:** Key limitations enumerated: CatBoost slice fragility (Age_missing=1, ~16.5% of test rows Age-missing) and absence of a repeated-CV stability audit; M1 QB-slice loss; School excluded by policy; unit-of-observation only partially probed.
- **Decision rationale required?** Yes.
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Must avoid overclaiming; numbers carry provenance labels.

#### S25. Reproducibility Register
- **Purpose:** Pin everything needed to reproduce results.
- **Main evidence files:** `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`; `outputs/reports/phase11_submission_readiness_phase11_option_c_20260619_0001_artifact_manifest.csv`; `requirements.txt`.
- **Portable-package dependency:** `requirements.txt`; frozen fold file.
- **Colab executable?** Yes (print versions and the fold SHA live).
- **Full repo only?** No.
- **Code cells required?** Yes.
- **Tables required?** Yes (seed 42; fold SHA256[:16]=96937649526bcadb; HEAD e5ea4e8; environment versions where available).
- **Figures required?** No.
- **Expected conclusion:** Seeds, folds, environment, and artifact lineage are pinned and verifiable.
- **Decision rationale required?** No.
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** Separate-environment CatBoost versions must be recorded, not assumed; mark any unpinned version "Not confirmed yet".

#### S26. Bibliographic References
- **Purpose:** List the real reference library actually used.
- **Main evidence files:** `references.md`; `references/books/*`, `references/papers/*` (cited, not shipped).
- **Portable-package dependency:** `references.md` ships; PDFs do not.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Yes (reference → project decision supported).
- **Figures required?** No.
- **Expected conclusion:** Each load-bearing decision maps to a real source (e.g., Cawley & Talbot 2010; Kapoor & Narayanan 2022; Kuhn & Johnson 2021; Chen & Guestrin 2016; Ke et al. 2017; Prokhorenkova et al. 2019; Akiba et al. 2019; Ye et al. 2025).
- **Decision rationale required?** No.
- **Transition analysis required?** No.
- **Section takeaways required?** No.
- **Risks/caveats:** Cite only PDFs that physically exist in `references/`; entries with uncertain citation details are marked "Not confirmed yet" (e.g., the Sasse et al. and a small number of edition/year details).

#### S27. Generative AI Assistance Disclosure
- **Purpose:** Sober, bounded disclosure of auxiliary ChatGPT support.
- **Main evidence files:** Not applicable.
- **Portable-package dependency:** Lives in `references.md` / acknowledgements.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** No.
- **Figures required?** No.
- **Expected conclusion:** ChatGPT is disclosed as an auxiliary support tool for conceptual consultation, coding recommendations, debugging guidance, and notebook-organization review; it did not train, tune, or select models, run hyperparameter optimization, choose submissions, or make methodological decisions.
- **Decision rationale required?** No.
- **Transition analysis required?** No.
- **Section takeaways required?** No.
- **Risks/caveats:** This is the only permitted generative-AI mention; tone must be factual and restrained; no other internal tooling may be named anywhere.

#### S28. Conclusion
- **Purpose:** Close the report.
- **Main evidence files:** Not applicable (synthesis).
- **Portable-package dependency:** None.
- **Colab executable?** Yes (Markdown).
- **Full repo only?** No.
- **Code cells required?** No.
- **Tables required?** Optional.
- **Figures required?** No.
- **Expected conclusion:** A leakage-safe, frozen-fold, fully auditable pipeline delivered two validated submissions; the project prioritized reproducibility and discipline over leaderboard chasing; the upload decision remains a manual director choice.
- **Decision rationale required?** Yes (brief synthesis).
- **Transition analysis required?** No.
- **Section takeaways required?** Yes.
- **Risks/caveats:** No winner declared; no leaderboard-driven claim.

---

## 4. Mandatory transition list

Each phase section must contain an explicit transition paragraph that closes the prior phase and motivates the next. The one-line examples below illustrate the expected style; they are not to be copied verbatim.

| Transition | Expected transition style (illustrative, do not copy verbatim) |
|---|---|
| Phase 1 → 2 | "With governance, seeds, and the official-files-only rule fixed, the project moves to reproducing the documented baseline as a historical reference." |
| Phase 2 → 3 | "Because the reproduced baseline is leakage-inflated by design, it is treated as reference only, and exploration shifts to leakage-aware EDA that locks no feature." |
| Phase 3 → 4 | "The four hypothesized signal families and their risks are carried into a literature synthesis that turns observations into enforceable rules." |
| Phase 4 → 5 | "The synthesized rules are formalized into a frozen methodology that binds every subsequent phase." |
| Phase 5 → 6 | "The frozen protocol is implemented as a leakage-safe validation harness producing the canonical OOF anchor on frozen folds." |
| Phase 6 → 6A | "With a clean anchor in hand, the gap to the historical baseline is decomposed and the ablation threshold and duplication verdict are established." |
| Phase 6A → 7 | "Having attributed most of the gap to informative missingness, the project tests missingness and availability features explicitly and fold-safely." |
| Phase 7 → 7B | "With F2 adopted, the single deferred role interaction is probed under the same adoption rule." |
| Phase 7B → 8 | "After the role interaction is rejected and F2 confirmed, the fixed feature set enters a fair, frozen-fold model-family comparison." |
| Phase 8 → 8 Wave 2 | "Having compared the sklearn-native families, the comparison extends to external gradient-boosted trees in a separate, isolated environment." |
| Phase 8 Wave 2 → 9A | "With five candidates characterized, a read-only diagnostic pass examines AUC, ranking, and imbalance behavior without altering any model." |
| Phase 9A → 9B-Lite | "Because the imbalance lenses confirm the existing ordering, a full diagnostic cycle is deliberately skipped while the evidence trail is preserved." |
| Phase 9B-Lite → 10 | "The carried-forward candidates enter a bounded, pre-registered optimization pass under selection-bias and leakage control." |
| Phase 10 → 11 | "With the optimization candidate and the fallback identified, both are refit on full train and validated for submission readiness." |
| Phase 11 → Final recommendation | "With two format-valid submissions on disk, the project states a caveated recommendation and hands the upload-order decision to the director." |

---

## 5. Coverage and compliance checklist (for the build run)

The construction step must verify, before the notebook is considered complete, that:

- Author info, UNAL attribution, and program are present in S1 and not contradicted elsewhere.
- Phases 1 through 11 are each explicitly covered, plus 6A, 7B, Wave 2, 9A, and 9B-Lite, and each phase section ends with `#### Key conclusions from this phase`.
- Decision rationale and a transition paragraph appear in every phase section per the table in Section 4.
- The references section lists only real sources from `references/`, and the ChatGPT disclosure appears once, soberly, in the references/acknowledgements area.
- Final submission validation (S22) and limitations/risks (S24) are present.
- Every historical number carries one provenance label from Section 1.1.
- No final winner is declared; no leaderboard is used for any decision; no historical submission is recreated or modified.
- No internal execution tooling is named anywhere in the shipped narrative.

---

## 6. Items marked "Not confirmed yet"

- M1 baseline exact configuration (C, penalty, solver, scaling) is not confirmed in artifacts; it must be recovered from Phase 8 artifacts during the build run and never invented.
- Exact pinned environment versions for the separate CatBoost environment beyond `catboost 1.2.10`, and the full base-environment version matrix for the Reproducibility Register, are not fully confirmed and must be read at build time.
- A small number of bibliographic details flagged as uncertain in the reference library (notably the Sasse et al. leakage entry and a few edition/year fields) remain "Not confirmed yet" pending verification against the source PDFs.
- The final uploaded submission and any resulting leaderboard outcome are not confirmed; the package ships in a no-winner, not-uploaded state by design.
