# Phase 5 Execution Decisions

## Purpose

Freeze the methodology decisions needed to open Phase 6: a leakage-safe validation harness and minimum preprocessing workflow.

This document does not implement models, pipelines, feature engineering, HPO, ensembles, notebooks, or submissions.

## Inputs reviewed

| Input | Use in Phase 5 |
|---|---|
| `AGENTS.md` | Project rules, notebook-first workflow, validation and leakage discipline. |
| `README.md` | Environment and project operating rules. |
| `docs/README.md` | Active documentation index after migration. |
| `docs/MIGRATION_LOG.md` | Confirms active docs were reorganized by phase. |
| `docs/00_project_contract/challenge_brief.md` | Competition contract, target, metric, official files, leaderboard rules. |
| `docs/00_project_contract/submission_checklist.md` | Submission, leakage, and reproducibility checks. |
| `docs/03_eda/experiment_notes.md` | Phase 3 data contract, EDA evidence, risks, deferred decisions. |
| `docs/04_research/pdf_review_audit.md` | PDF readability gate. |
| `docs/04_research/pdf_key_findings.md` | PDF evidence routing by topic. |
| `docs/04_research/research_notes_validation.md` | Validation methodology. |
| `docs/04_research/research_notes_leakage.md` | Leakage taxonomy and fit-scope rules. |
| `docs/04_research/research_notes_feature_engineering.md` | Feature block roadmap and ablation order. |
| `docs/04_research/research_notes_tabular_models.md` | Future model comparison guardrails. |
| `docs/04_research/research_notes_hpo.md` | HPO gates and selection-bias warnings. |
| `docs/04_research/research_notes_reproducibility.md` | Experiment log and audit requirements. |
| `docs/05_methodology/phase5_methodology_plan.md` | Consolidated Phase 5 methodology plan. |
| `logs/experiment_log.csv` | Existing Phase 2 baseline row and legacy log schema. |

## Scope boundaries

Phase 5 freezes decisions only. It does not:

- train models;
- execute notebooks;
- generate submissions;
- run HPO or Optuna;
- implement feature engineering;
- implement model comparison;
- modify official data, official notebooks, PDFs, or generated outputs;
- stage or commit files.

## Frozen decisions

| Decision item | Options considered | Recommended decision | Rationale | Evidence source | Risk controlled | Impact on Phase 6 | Status |
|---|---|---|---|---|---|---|---|
| Metric | ROC-AUC, accuracy, log loss | ROC-AUC | Official metric is ROC-AUC/AUC. | `docs/00_project_contract/challenge_brief.md` | Wrong optimization target. | Harness must compute ROC-AUC. | Frozen |
| Score input | Hard labels, probabilities | Positive-class probabilities for `Drafted = 1` | ROC-AUC evaluates ranking from continuous scores. | `docs/00_project_contract/submission_checklist.md`, `docs/04_research/research_notes_validation.md` | Invalid local validation. | Hard labels are not acceptable for ROC-AUC. | Frozen |
| Class index | Assume `predict_proba(X)[:, 1]`, verify classes | Verify `estimator.classes_` and locate label `1` | Class order can silently differ by estimator or encoding. | Phase 5 prompt, leakage discipline | Silent metric bug. | Harness must assert class index before scoring. | Frozen |
| Metric function | Custom AUC, scikit-learn | `sklearn.metrics.roc_auc_score` | Standard library already available through `scikit-learn`. | `requirements.txt` | Metric drift. | Use one standard metric function. | Frozen |
| CV splitter | Holdout, `StratifiedKFold`, `GroupKFold` | `StratifiedKFold` | Binary classification with unconfirmed grouping. | `AGENTS.md`, `docs/04_research/research_notes_validation.md` | Class imbalance and fold instability. | Use stratified folds by default. | Frozen |
| `n_splits` | 3, 5, 10, Not confirmed yet | `5` | 3 is less stable, 10 is costlier with smaller validation folds, and Phase 2 baseline used 5. | `logs/experiment_log.csv`, `docs/00_project_contract/challenge_brief.md` | Variance/cost imbalance. | Use 5 folds for Phase 6 harness. | Frozen |
| Shuffle | `False`, `True` | `shuffle=True` | Row order has no confirmed temporal meaning; Year remains diagnostic. | `docs/03_eda/experiment_notes.md` | Order artifacts. | Randomized stratified folds. | Frozen |
| Fold seed | `42`, `2025`, new seed | `PROJECT_SEED = 42` for folds | Existing baseline fold config uses 42; docs require fixed seeds. | `logs/experiment_log.csv`, `AGENTS.md` | Irreproducible folds. | Same fold assignments across phases. | Frozen |
| Grouped CV | Activate, block, conditional | Conditional only | Unit/group dependency is not confirmed. | `docs/03_eda/experiment_notes.md` | False group assumptions. | Do not activate grouped CV in Phase 6. | Frozen |
| Temporal CV | Default, diagnostic | Diagnostic only | Year effects exist, but no official temporal split requirement is confirmed. | `docs/03_eda/experiment_notes.md` | Overconstrained validation. | Report Year slices, do not use temporal split by default. | Frozen |
| Public leaderboard | Validation system, sanity check | Sanity check only | Public leaderboard is a subset and can cause selection leakage. | `docs/00_project_contract/challenge_brief.md`, `docs/00_project_contract/submission_checklist.md` | Leaderboard leakage. | Not used for Phase 6 decisions. | Frozen |
| Phase 6 submission policy | Allow, block | Block submissions | Phase 6 is validation/preprocessing harness work. | `docs/01_project_planning/project_execution_plan_v2_context_efficient.md` | Premature submission. | No Phase 6 submission CSV. | Frozen |
| First Phase 6 baseline | Competitive model, sanity baseline | Validation harness sanity baseline | Purpose is to verify folds, metric, preprocessing scope, and logging. | Phase 6 goal | Premature model selection. | One reference harness run only. | Frozen |
| First baseline columns | Include all, exclude `Id`/`Drafted`/`School` | Exclude `Id`, `Drafted`, and `School`; use raw official non-School features | `Id` is identifier, `Drafted` is target, `School` is high-risk. | `docs/03_eda/experiment_notes.md`, `docs/04_research/research_notes_feature_engineering.md` | Leakage and overfitting. | Simple first harness input set. | Frozen |
| Year handling | Drop, numeric feature, split driver | Use `Year` as raw numeric feature and mandatory slice; not a split driver | Year may encode cohort effects but temporal split is not justified. | `docs/03_eda/experiment_notes.md` | Temporal overinterpretation. | Include Year diagnostics. | Frozen |
| Role categoricals | Exclude, include | Include `Player_Type`, `Position_Type`, and `Position` | Role context is a core Phase 3 signal family. | `docs/03_eda/experiment_notes.md` | Hidden subgroup failure. | Must be fold-safely encoded. | Frozen |
| No causal interpretation | Omit, add policy | Add predictive-only wording | EDA and later models are descriptive/predictive, not causal. | `docs/03_eda/experiment_notes.md` | Causal overclaim. | Reports use association/ranking language. | Frozen |
| Artifact overwrite | Allow, forbid | Forbid overwrites without `experiment_id` or `run_id` | Audit traceability requires stable artifact lineage. | `docs/04_research/research_notes_reproducibility.md` | Lost audit trail. | Future artifacts must be uniquely named. | Frozen |

## Provisional decisions

| Decision item | Provisional value | Why provisional | Verification needed |
|---|---|---|---|
| Exact model for Phase 6 sanity run | Reproduce Phase 2 `RandomForestClassifier` as historical reference under frozen folds | Avoids introducing a new model-family decision, but fold-safe implementation must be checked. | Confirm clean Phase 6 harness can reproduce reference behavior without leakage. |
| Minimum slice size | Not confirmed yet | Baseline variance under frozen folds is not measured. | Measure fold and slice stability in Phase 6. |
| Feature-block quantitative threshold | Not confirmed yet | Need baseline mean/std before setting thresholds. | Define after first frozen-fold baseline. |
| Experiment log v2 migration | Defer | Current CSV has a real Phase 2 row using the legacy schema. | Create a separate approved migration plan before changing the CSV schema. |
| Measurement-completeness cutoffs | Not confirmed yet | Candidate features are Phase 7 hypotheses. | Define fold-safe buckets during Phase 7. |

## Not confirmed yet

| Item | Why unresolved | How to resolve |
|---|---|---|
| Unit of observation | Official docs do not confirm whether rows are statistically independent. | Keep marked and inspect only official sources if needed. |
| Need for grouped CV | No confirmed grouping or dependency is documented. | Use Phase 6/9 slice diagnostics; activate only if evidence supports it. |
| Minimum slice size | No frozen-fold variance exists yet. | Measure baseline fold and slice stability. |
| Quantitative ablation threshold | Baseline variance under frozen folds is unknown. | Set after Phase 6 baseline. |
| Final `School` encoding | High-risk variable has not been safely tested. | Use Phase 7 staged ablations. |
| Log schema migration | Existing real row uses legacy schema. | Require separate approval before migration. |

## Phase 6 readiness

Phase 6 is not ready until:

- this document is reviewed and accepted;
- `docs/05_methodology/validation_protocol_phase6.md` is reviewed and accepted;
- `docs/05_methodology/leakage_checklist_phase6.md` is reviewed and accepted;
- the validation splitter, fold seed, metric policy, and slice schema are accepted;
- leakage fit-scope rules are accepted;
- the first Phase 6 baseline policy is accepted;
- `logs/experiment_log.csv` migration is explicitly deferred or separately approved;
- unit of observation remains explicitly marked `Not confirmed yet`.

## Artifact paths and naming conventions

Future phases may create these directories only when implementation requires them:

| Artifact type | Directory | Naming convention |
|---|---|---|
| Experiment log | `logs/` | `experiment_log.csv` |
| Fold assignments | `outputs/folds/` | `{experiment_id}_fold_assignments.csv` |
| OOF predictions | `outputs/oof/` | `{experiment_id}_oof_predictions.csv` |
| Slice reports | `outputs/validation/` | `{experiment_id}_slice_report.csv` |
| Validation reports | `outputs/reports/` | `{experiment_id}_validation_report.md` |
| Submissions | `outputs/submissions/` | `{experiment_id}_submission.csv` |

No artifact should overwrite another artifact without an `experiment_id` or `run_id`.

## Experiment log policy

Current status:

- `logs/experiment_log.csv` exists.
- It has a legacy schema.
- It contains one real Phase 2 baseline row.

Decision:

- Do not overwrite, truncate, or migrate `logs/experiment_log.csv` during Phase 5.
- Document the future v2 schema only.
- Any future schema migration must preserve the existing baseline row.

Proposed v2 schema:

```text
experiment_id,date,phase,notebook_or_script,git_commit_or_status,data_version,fold_strategy,random_seed,feature_block,preprocessing_summary,model_family,model_params_summary,hpo_status,cv_auc_mean,cv_auc_std,fold_scores,slice_metrics_available,leakage_checks_passed,submission_created,submission_path,public_lb_score_if_submitted,notes,decision
```

Optional future fields requiring separate approval:

```text
run_id,parent_experiment_id,fold_file,oof_path,test_prediction_path,data_rows_train,data_rows_test,positive_rate_train,preprocessing_fit_scope,school_strategy,leakage_review_status,slice_report_path,environment_summary,duration_seconds
```

## Phase transition policy

| Phase | Entry gate |
|---|---|
| Phase 6 | Phase 5 methodology docs accepted; validation and leakage rules frozen. |
| Phase 7 | Phase 6 harness tested; fold-safe preprocessing working; baseline reproducible under frozen folds. |
| Phase 8 | Phase 7 feature block ablations complete enough to compare model families fairly. |
| Phase 10 | Stable validation, leakage-safe pipeline, tested feature blocks, and 1-3 candidate models selected. |
| Phase 11 | Final candidate is reproducible, logged, verified, and submission-ready. |

## Restrictions respected

Phase 5 documentation must not:

- train models;
- generate submissions;
- run notebooks;
- use Optuna or HPO;
- implement feature engineering;
- modify raw data;
- modify official notebooks;
- modify PDFs;
- stage or commit files.
