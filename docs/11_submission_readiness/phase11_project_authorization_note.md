# Phase 11 Project Authorization Note — Final Refit, Test Inference and Validated Submission

## 1. Executive Authorization
This note authorizes a future Phase 11 execution only after this document is reviewed and accepted by the project director.
This note does not execute Phase 11.
This note does not create submissions.
This note does not authorize automatic upload.
This note does not declare a final winner.

## 2. Authorized Starting Commit
Authorized starting commit:
`6ffb66d7165361a7c3247757edad7da134eba2ad`

Short:
`6ffb66d`

Commit message:
`planning: add phase 11 submission readiness package`

Future Codex execution must verify this hash before doing anything.

## 3. Governing Planning Package
Phase 11 must follow the planning package committed at `6ffb66d`:

- `docs/11_submission_readiness/phase11_master_planning_brief.md`
- `docs/11_submission_readiness/phase11_operator_runbook.md`
- `docs/11_submission_readiness/prompt_codex_phase11_submission_readiness_execution.md`
- `docs/11_submission_readiness/prompt_opus_phase11_final_submission_review.md`

The note also inherits the accepted Phase 10 evidence and the Phase 6 methodology contract.

## 4. Phase 10 Evidence Carried Forward
Phase 10 remains the governing evidence base for the final-refit decision.

- CatBoost tuned has the best global OOF ROC-AUC, but it remains warning-heavy and is not a final winner.
- M1 Logistic Regression baseline remains the fallback/reference candidate.
- M1 tuned was rejected because its improvement over M1 baseline was noise-level.
- M0 RandomForest frozen remains the anchor/reference only.
- XGBoost and LightGBM remain dropped.
- No final winner was selected in Phase 10.
- No submission was authorized in Phase 10.

## 5. Candidate Decision
Authorized candidate decision:
Option C — generate both validated candidate submission artifacts.

Candidate 1:
CatBoost tuned — primary final-refit candidate, warning-heavy, not final winner.

Candidate 2:
M1 Logistic Regression baseline — fallback/reference candidate.

Rejected:
M1 tuned, because its improvement over M1 baseline was noise-level.

Anchor only:
M0 RandomForest frozen.

Dropped:
XGBoost and LightGBM.

## 6. CatBoost Stability Gate Decision
CatBoost Stability Gate decision:
Written waiver granted for Phase 11 execution.

The project director acknowledges that CatBoost tuned:
- has the best global Phase 10 OOF ROC-AUC;
- does not clear the historical promotion bar over M1 baseline;
- has only 3/5 positive folds vs M1 baseline;
- lacks repeated-CV stability confirmation;
- retains slice warnings;
- may underperform on private test despite being best on global OOF;
- is allowed as a primary final-refit candidate under time/resource constraints.

This waiver does not make CatBoost tuned the final winner.
This waiver only permits generating a validated CatBoost candidate submission artifact.

## 7. Authorized Future Execution Scope
Future Codex execution is authorized to:

- create `notebooks/11_phase11_submission_readiness.ipynb`;
- refit CatBoost tuned on full train using the accepted Phase 10 tuned hyperparameters;
- refit M1 baseline on full train using the recovered accepted baseline configuration;
- generate test predictions for both authorized candidates;
- create two validated submission CSV artifacts;
- validate schema, row count, Id order, probability range, NaN/inf, duplicates and SHA-256;
- create validation reports, model summary, final refit report, submission validation report, artifact manifest and candidate experiment log;
- leave upload to the project director manually.

## 8. Authorized Submission Artifacts
Authorized future submission families:

- `outputs/submissions/phase11_submission_readiness_<run_id>_catboost_tuned_submission.csv`
- `outputs/submissions/phase11_submission_readiness_<run_id>_m1_logistic_regression_baseline_submission.csv`

No other submission files are authorized.

## 9. Feature and Data Contract
Use F2 only.
School is prohibited as a feature.
No external data.
Train data may be used for full-train refit.
Test data may be used only for inference.
Sample submission may be used only for schema, Id set and Id order validation.

## 10. Forbidden Actions
Explicitly prohibited:

- leaderboard use for model selection;
- automatic upload;
- final winner declaration;
- submission-ready declaration before Opus review and director acceptance;
- HPO;
- ensembles;
- blending;
- stacking;
- calibration fitting;
- threshold tuning;
- XGBoost reopening;
- LightGBM reopening;
- M1 tuned usage;
- School as feature;
- external data;
- manual prediction editing;
- modifying `logs/experiment_log.csv`;
- modifying forbidden paths;
- `git add .`;
- `git commit -a`;
- push.

## 11. Required Execution Artifacts
Future Codex execution must produce the following artifacts only under the Phase 11 namespace:

- `notebooks/11_phase11_submission_readiness.ipynb`
- `outputs/validation/phase11_submission_readiness_<run_id>_candidate_selection_report.csv`
- `outputs/validation/phase11_submission_readiness_<run_id>_final_refit_report.csv`
- `outputs/validation/phase11_submission_readiness_<run_id>_submission_validation.csv`
- `outputs/validation/phase11_submission_readiness_<run_id>_model_summary.csv`
- `outputs/reports/phase11_submission_readiness_<run_id>_validation_report.md`
- `outputs/reports/phase11_submission_readiness_<run_id>_artifact_manifest.csv`
- `outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv`
- `outputs/submissions/phase11_submission_readiness_<run_id>_catboost_tuned_submission.csv`
- `outputs/submissions/phase11_submission_readiness_<run_id>_m1_logistic_regression_baseline_submission.csv`

## 12. Required Submission Validation Suite
The submission validation suite must confirm:

- columns exactly `Id, Drafted`;
- row count exactly 696;
- Id set matches the official test/sample Id set;
- Id order matches `sample_submission.csv` and `test.csv`;
- `Drafted` is numeric and every value lies in `[0, 1]`;
- no NaN values;
- no infinite values;
- no duplicate Id values;
- no manual prediction edits;
- SHA-256 recorded in the manifest and validation report;
- the report identifies model, commit hash, run_id and feature set (F2);
- no automatic upload.

## 13. Required Post-Codex Opus Review
After Codex execution, Opus must run:

`docs/11_submission_readiness/prompt_opus_phase11_final_submission_review.md`

Opus must independently audit:

- submission schema;
- 696 rows;
- Id set;
- Id order;
- probability range;
- NaN/inf;
- duplicates;
- SHA-256;
- artifact manifest;
- no manual edits;
- no leakage;
- no leaderboard use;
- no automatic upload.

## 14. Manual Upload Policy
No agent uploads.
The project director manually decides whether to upload.
If both submissions are generated, the project director manually decides upload order.
The last uploaded file determines final ranking.
Leaderboard feedback must not be used to start an upload loop.

## 15. Git and Log Safety
`logs/experiment_log.csv` must remain unchanged during Phase 11 execution.
The submission candidate log is written only to `outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv`.
No forbidden path may be modified.
No stage, commit, or push may occur during execution.

## 16. Stop Rules
Stop immediately if any of the following occurs:

- HEAD does not match the authorized starting commit;
- the candidate decision gate is unresolved;
- the CatBoost Stability Gate is neither passed nor waived;
- a required predecessor document is missing;
- F2 would be violated by a new feature or School usage;
- external data would be introduced;
- HPO would be used;
- test would be used for fitting;
- `classes_` does not contain label 1;
- row count, Id set or Id order cannot be verified;
- probabilities are outside `[0, 1]` or contain NaN/inf;
- manual editing is detected;
- leaderboard is used for selection;
- any automatic upload is attempted;
- a winner is declared.

## 17. Explicit Non-Decisions
This authorization note does not:

- execute Phase 11;
- train or refit any model;
- run test inference;
- create or upload any submission;
- use the leaderboard for selection;
- declare a final winner;
- declare a submission-ready model;
- reopen Phase 10;
- reopen HPO;
- reopen XGBoost or LightGBM;
- change the Phase 10 acceptance record.

## 18. Project Director Signature
- Decision: Authorized for future Phase 11 execution under Option C.
- CatBoost Stability Gate: Written waiver granted.
- Authorized by:
- Date:
- Signature:
- Authorization commit hash:
