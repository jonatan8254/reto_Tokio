# Phase 5 Methodology Plan

## Purpose
Convert Phase 3 EDA, Phase 4A research, and the PDF audit gate into an executable methodology plan. This document still does not implement models, preprocessing pipelines, feature engineering, HPO, ensembles, or submissions.

## Inputs from Phase 3, Phase 4A and PDF Audit
Evidence:
- Phase 3 deliverables: `notebooks/02_eda_and_data_contract.ipynb` and `docs/03_eda/experiment_notes.md`.
- Phase 4A input: `Prompts/Fase 4/deep-research-report1.md` and `Recapitulaciones/recapitulacion_fase3_reto_tokio_para_fase4.md`.
- PDF audit gate: `docs/04_research/pdf_review_audit.md`, `docs/04_research/pdf_key_findings.md`, `scripts/audit_pdf_sources.py`.
- PDF audit status: 34 PDFs detected, 26 Reviewed, 8 Partially readable, 0 OCR needed, 0 Extraction failed.

Inference:
- Reviewed PDFs are acceptable methodological support for Phase 4B/5 planning.
- Partially readable PDFs may be context only.
- Keyword counts are not methodological conclusions.

Decision:
- Use the six research notes as the compact evidence layer for Phase 5-11.

## Competition contract
Evidence:
- Task: binary classification.
- Target: `Drafted`.
- Positive class: `Drafted = 1`.
- ID column: `Id`.
- Metric: ROC-AUC / AUC using positive-class probabilities.
- Submission columns: `Id`, `Drafted`.
- Submission row count: 696.
- Public leaderboard: subset of test.
- Private leaderboard: final scoring.
- Final ranking: last submitted file.
- Code may be audited for reproducibility.

Decision:
- Use only official data: `data/input/train.csv`, `data/input/test.csv`, `data/input/sample_submission.csv`.
- Do not use external athlete, school, conference, ranking, geography, draft-history, NFL outcome, external sports statistics, similar online datasets, manual labels, manually edited predictions, test data for fitting/tuning/selection, or public leaderboard as validation.

## Validation protocol
Decision:
- Freeze `StratifiedKFold` with fixed seed as the default Phase 5 validation design.
- Use ROC-AUC on positive-class probabilities for `Drafted = 1`.
- Report mean ROC-AUC, std ROC-AUC, fold scores, OOF predictions when applicable, and slice diagnostics.
- Mandatory slices: `Player_Type`, `Position_Type`, `Year`, measurement completeness, `Age_missing`, frequent vs rare `School`.
- `StratifiedGroupKFold`: only if dependency/grouping is confirmed.
- `GroupKFold`: only if grouping becomes more important than class balance.
- Temporal/year split: diagnostic only unless justified later.

## Leakage prevention protocol
Decision:
- Any transformation that learns from data must be fitted inside training folds.
- Test data is allowed only for structure checks, submission row/order checks, and final inference after the final model is trained.
- No global pandas preprocessing before CV unless purely row-wise and parameter-free.
- Block global imputation, encoding, scaling, feature selection, rare grouping, role statistics, target encoding, dimensionality reduction, and HPO.

## Preprocessing policy
Decision:
- Phase 6 must implement preprocessing as a leakage-safe validation harness.
- Use pipelines or equivalent fold-aware execution.
- Keep preprocessing minimal until baseline reproducibility under frozen folds is confirmed.
- Imputation, encoding, scaling, and category handling must be explicitly logged.

## Missingness strategy
Evidence:
- Phase 3 found missingness in `Age`, `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`.
- Phase 3 found `Age_missing` should be separated from physical-test missingness.

Decision:
- Treat missingness as candidate signal, not only cleaning.
- Test `Age_missing`, physical-test missingness indicators, `available_measurement_count`, complete-profile flag, low-profile flag, and co-missingness profiles as ablation blocks.
- No missingness feature is selected before Phase 7 ablation.

## Categorical strategy
Decision:
- Role categorical variables (`Player_Type`, `Position_Type`, `Position`) can enter earlier as controlled role-context features.
- Encoders must be fitted inside folds.
- Unknown categories must have a clear policy.
- No target encoding until strictly OOF implementation is justified.

## School strategy
Decision:
- Stage `School` in this order:
  1. no School baseline;
  2. School frequency/count encoding;
  3. rare grouping;
  4. OOF target encoding only if justified;
  5. CatBoost native categorical handling only under strict validation.
- Always monitor low-n instability, rare/frequent School slices, and fold variance.

## Role-aware feature engineering roadmap
Decision:
- Test role-aware hypotheses only after Phase 6 harness is stable.
- Candidate blocks: role interactions, speed-size interactions, strength-size interactions, explosiveness proxies, agility-speed interactions, BMI-like feature from `Height`/`Weight`, role-normalized z-scores, within-role ranks/percentiles, role-specific outlier flags.
- Role statistics must be learned inside folds.
- No global outlier deletion or winsorization.

## Feature block ablation plan
Decision:
- A0: baseline reproduction context only.
- A1: raw features without School.
- A2: missingness indicators.
- A3: `available_measurement_count` / completeness flags.
- A4: role context and role interactions.
- A5: role-aware numeric transformations.
- A6: School frequency/count.
- A7: rare grouping.
- A8: OOF target encoding or CatBoost categorical strategy only if previous steps are stable.

## Model comparison roadmap
Decision:
- No model comparison until Phase 6 and Phase 7 gates pass.
- Future shortlist: Logistic Regression, RandomForestClassifier reference, HistGradientBoostingClassifier, XGBoost, LightGBM, CatBoost, and deep tabular only if GBDT plateau and time allows.
- Use identical folds, features, metrics, OOF/slice diagnostics, and logging.
- Do not choose a model family from one CV score.

## HPO activation gates
Decision:
Optuna/HPO is blocked until:
1. validation protocol frozen;
2. leakage-safe pipeline implemented;
3. feature blocks tested by ablation;
4. 1-3 model candidates selected from fair comparison;
5. `experiment_log.csv` schema active;
6. no unresolved leakage issue;
7. no dependence on public leaderboard.

Future Phase 10 defaults: `direction="maximize"`, fixed sampler seed, conservative trials, sequential deterministic runs first, small justified search spaces, reproducible trial logging.

## Ensemble activation gates
Decision:
- No ensembles before fair model comparison and error analysis.
- Ensembles require real OOF diversity, not only close scores.
- Blending/stacking must use OOF predictions and remain reproducible.
- No leaderboard-driven ensemble weight search.

## Submission discipline
Decision:
- Generate submissions only after a logged, reproducible experiment with validated CV evidence.
- Public leaderboard is a sanity check only.
- Submission CSV must be generated automatically, saved under `outputs/submissions/`, have columns `Id`, `Drafted`, 696 rows, test/sample ID order, finite probabilities in `[0, 1]`, and no manual edits.
- Final ranking depends on last submitted file, so Phase 11 must control submission order.

## Experiment logging schema
Decision:
Use these fields for future important experiments:
- `experiment_id`
- `date`
- `phase`
- `notebook_or_script`
- `git_commit_or_status`
- `data_version`
- `fold_strategy`
- `random_seed`
- `feature_block`
- `preprocessing_summary`
- `model_family`
- `model_params_summary`
- `hpo_status`
- `cv_auc_mean`
- `cv_auc_std`
- `fold_scores`
- `slice_metrics_available`
- `leakage_checks_passed`
- `submission_created`
- `submission_path`
- `public_lb_score_if_submitted`
- `notes`
- `decision`

## Phase 6 entry criteria
Decision:
- validation protocol approved;
- leakage checklist approved;
- feature block roadmap approved;
- experiment log schema approved;
- no unresolved contradiction in challenge constraints;
- unit of observation explicitly marked Not confirmed yet if still unresolved.

## Phase 7 entry criteria
Decision:
- Phase 6 validation harness implemented and tested;
- preprocessing pipeline leakage-safe;
- baseline model reproducible under fixed folds;
- slice diagnostics available;
- feature block ablation protocol approved.

## Phase 8 guardrails
Decision:
- No model comparison until Phase 6 and Phase 7 gates are satisfied.
- Use identical folds, identical metrics, identical OOF/slice diagnostics, and experiment logging.
- Keep baseline models simple before tuning.

## Open questions
- Unit of observation: Not confirmed yet.
- Need for grouped CV: Not confirmed yet.
- Final validation split beyond default stratified CV: Not confirmed yet.
- Which external GBDT libraries are installed and stable: Not confirmed yet.
- Final School encoding strategy: Not confirmed yet.
- Final HPO budget: Not confirmed yet.

## Stop/go decision
Decision:
- Phase 4B documentation can close when all six research notes and this plan exist and pass acceptance checks.
- Phase 5 can start in Plan Mode after reviewing these docs.
- Phase 5 must not implement models; it must freeze methodology and prepare Phase 6.
