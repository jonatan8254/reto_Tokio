# Final Package Source Inventory — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY. This document is a source-classification plan. Nothing is built, trained, refitted, optimized, submitted, committed, pushed, or staged in this planning run. No new historical artifacts are produced, no existing submission is altered, no leaderboard is consulted for selection, and no final winner is declared. The build run that consumes this inventory (see `prompt_build_final_portable_package.md`) is a separate, later step.**

---

## 1. Purpose and scope

This document is the single reasoned source inventory for the final deliverable package of the
Reto Tokio / GCI World NFL Draft Prediction project. It maps every confirmed repository source to four
destinations:

1. the comprehensive **final notebook** (`99_final_integrated_project_report.ipynb`, to be built later);
2. the **README** for the portable package;
3. the **portable package** itself (a minimal, self-contained folder for distribution);
4. the distributable **ZIP**.

It records, for each source, whether it exists today, its phase tag, its role in each destination, whether
it belongs in the ZIP, its priority, the runtime mode in which it is relevant, and notes.

Two governing constraints apply to everything downstream of this inventory:

- The portable package and every file shipped inside it (README, references, the notebook, requirements)
  must read as a professional technical data-science project. The internal construction process, internal
  planning tooling, and the build step itself must never appear in the shipped narrative.
- The only permitted generative-AI disclosure is a sober ChatGPT acknowledgement, placed solely in a
  references/acknowledgements subsection, framed strictly as auxiliary support (conceptual consultation,
  coding recommendations, debugging guidance, notebook-organization review). It is never to be described as
  having trained models, selected a winner, or executed a submission.

### Runtime-mode vocabulary

| Mode | Meaning |
|---|---|
| Full Repository | The complete repository on a local machine with the pinned environment; all 14 notebooks, all docs, all outputs, the full reference library. |
| Portable Package | The minimal distributable folder run locally (clean virtual environment or the pinned one). |
| Colab Minimal | The final notebook run in a hosted notebook environment with only core scientific packages; data uploaded by the user; CatBoost optional with a clean fallback. |
| Historical Record Only | Retained in the Full Repository as evidence; not run, not shipped. |
| Both | Relevant to Full Repository and Portable Package. |
| All | Relevant to Full Repository, Portable Package, and Colab Minimal. |
| Exclude | Not part of any runtime path for the deliverable. |

### Data governance scenarios

- **Scenario A (private / course package):** ship the three official CSVs inside the package.
- **Scenario B (restricted distribution):** exclude the official CSVs; ship placeholders plus instructions
  to obtain `train.csv`, `test.csv`, and `sample_submission.csv` from the official competition source.

The "Include in ZIP?" value `Conditional` denotes "Yes under Scenario A, Placeholder only under Scenario B."

---

## 2. Source inventory table

Columns are exactly: Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes.

### 2.1 Contract and challenge sources

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| docs/00_project_contract/challenge_brief.md | Yes | Phase 1 | Source for problem framing, target, metric | Source for challenge summary | Distilled, not shipped | No | High | Historical Record Only | Metric = ROC-AUC on positive-class probability; target Drafted=1 |
| docs/00_project_contract/submission_checklist.md | Yes | Phase 11 | Source for submission-format checks (696 rows, [Id, Drafted]) | Source for reproducibility/output statement | Distilled into validation cells | No | High | Historical Record Only | Drives the 12-check validation suite re-expressed in the notebook |

### 2.2 Planning sources

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| docs/01_project_planning/integral_project_review_phase0_phase6.md | Yes | Phase 6A | Context for baseline-gap narrative (collapse to "baseline reproduced") | None | None | No | Medium | Historical Record Only | Confirms Phase 2 baseline must not anchor Phase 7 (leakage-inflated) |
| docs/01_project_planning/phase6a_baseline_reconciliation_plan.md | Yes | Phase 6A | Context only | None | None | No | Low | Historical Record Only | Design for V0–V7 / D1 / D2 |
| docs/01_project_planning/project_execution_plan_v2_context_efficient.md | Yes | Phase 1 | Context only | None | None | No | Low | Historical Record Only | Plan v2 |
| docs/01_project_planning/project_execution_plan_v3.md | Yes | Phase 1 | Context only | None | None | No | Low | Historical Record Only | Plan v3; acceptance-record governance |
| docs/01_project_planning/project_execution_plan_v1.md | No | Phase 1 | None | None | None | No | Exclude | Exclude | Untracked per repo state; treat as non-source |
| docs/12_final_integrated_notebook/final_package_source_inventory.md | Yes | Package Infrastructure | None (planning doc) | None | None | No | Medium | Historical Record Only | This document |
| docs/12_final_integrated_notebook/prompt_build_final_portable_package.md | No | Package Infrastructure | None | None | None | No | High | Historical Record Only | Build-spec for the construction step; not yet created; never shipped |

### 2.3 EDA, research, and methodology sources

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| docs/03_eda/experiment_notes.md | Yes | Phase 3 | Source for EDA/data-contract narrative and missingness figures | Brief data-governance phrasing | Distilled | No | Medium | Historical Record Only | Class balance 0.6483; missingness counts; signal families |
| docs/04_research/pdf_key_findings.md | Yes | Phase 4 | Source for methodology justification text | None | None | No | Medium | Historical Record Only | Secondary evidence; official sources outrank PDFs |
| docs/04_research/pdf_review_audit.md | Yes | Phase 4 | None | None | None | No | Low | Historical Record Only | PDF audit log |
| docs/04_research/research_notes_validation.md | Yes | Phase 4 | Source for validation-protocol prose | None | None | No | Medium | Historical Record Only | Underpins ROC-AUC + frozen folds |
| docs/04_research/research_notes_leakage.md | Yes | Phase 4 | Source for leakage-safety prose | Brief no-leakage statement | None | No | High | Historical Record Only | Fit-scope rule; fold-safe preprocessing |
| docs/04_research/research_notes_feature_engineering.md | Yes | Phase 4 | Source for F2 feature-block rationale | None | None | No | Medium | Historical Record Only | Blocks 0–6 design |
| docs/04_research/research_notes_tabular_models.md | Yes | Phase 4 | Source for model-family ordering rationale | None | None | No | Medium | Historical Record Only | RF → LR → HGB → XGB → LGBM → CatBoost order |
| docs/04_research/research_notes_hpo.md | Yes | Phase 4 | Source for bounded-HPO rationale | None | None | No | Medium | Historical Record Only | Seven HPO activation gates |
| docs/04_research/research_notes_reproducibility.md | Yes | Phase 4 | Source for reproducibility statement | Source for reproducibility statement | Distilled | No | Medium | Historical Record Only | Seeds, clean-kernel, commit anchoring |
| docs/05_methodology/phase5_execution_decisions.md | Yes | Phase 5 | Source for frozen-methodology summary | None | None | No | High | Historical Record Only | ~17 frozen decisions |
| docs/05_methodology/phase5_methodology_plan.md | Yes | Phase 5 | Context only | None | None | No | Medium | Historical Record Only | Feature/model/HPO roadmaps |
| docs/05_methodology/validation_protocol_phase6.md | Yes | Phase 5 | Source for validation-setup cells | None | None | No | High | Historical Record Only | StratifiedKFold(5, shuffle, 42); OOF anchor |
| docs/05_methodology/leakage_checklist_phase6.md | Yes | Phase 5 | Source for leakage-safety cells | None | None | No | High | Historical Record Only | 14-item reusable checklist |

### 2.4 Phase acceptance records

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| docs/06_validation/phase6_acceptance.md | Yes | Phase 6 | Source for harness/anchor narrative | None | None | No | Medium | Historical Record Only | OOF anchor 0.726616; frozen folds canonical |
| docs/06_validation/phase6a_acceptance.md | Yes | Phase 6A | Source for ablation-threshold and baseline-gap narrative | None | None | No | Medium | Historical Record Only | Threshold 0.005436; duplication cleared |
| docs/07_feature_engineering/phase7_acceptance.md | Yes | Phase 7 | Source for F2 adoption narrative | None | None | No | High | Historical Record Only | F2 adopted; OOF 0.8116502602 |
| docs/07_feature_engineering/phase7b_role_interaction_acceptance.md | Yes | Phase 7B | Source for F4-rejection narrative | None | None | No | Medium | Historical Record Only | F4 rejected; F2 retained |
| docs/08_model_comparison/phase8_acceptance.md | Yes | Phase 8 | Source for Wave 1 model-comparison narrative | Source for results table | None | No | High | Historical Record Only | M1 candidate-with-warning; M0 anchor |
| docs/08_model_comparison/phase8_wave2_acceptance.md | Yes | Phase 8 Wave 2 | Source for external-GBDT narrative | Source for results table | None | No | High | Historical Record Only | CatBoost escalated; XGB/LGBM dropped |
| docs/09_auc_ranking_diagnostics/phase9a_acceptance.md | Yes | Phase 9B-Lite | Source for ranking-diagnostics narrative | None | None | No | Medium | Historical Record Only | M1 leads all global lenses; diagnostic-only |
| docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md | Yes | Phase 9B-Lite | Context only | None | None | No | Low | Historical Record Only | 11 phase-gated backlog items |
| docs/09_auc_ranking_diagnostics/phase9b_lite_transition_memo.md | Yes | Phase 9B-Lite | Context only | None | None | No | Low | Historical Record Only | Intentional skip to Phase 10 planning |
| docs/10_model_optimization/phase10_acceptance.md | Yes | Phase 10 | Source for bounded-HPO outcome narrative | Source for results table | None | No | High | Historical Record Only | CatBoost tuned best OOF; warning-heavy |
| docs/10_model_optimization/phase10_master_planning_brief.md | Yes | Phase 10 | Context only | None | None | No | Low | Historical Record Only | Planning brief |
| docs/10_model_optimization/phase10_project_authorization_note.md | Yes | Phase 10 | Context only | None | None | No | Low | Historical Record Only | Authorization note |
| docs/11_submission_readiness/phase11_master_planning_brief.md | Yes | Phase 11 | Source for submission-readiness narrative | None | None | No | Medium | Historical Record Only | Option C dual submission |
| docs/11_submission_readiness/phase11_operator_runbook.md | Yes | Phase 11 | Context for refit/inference/validation flow | None | None | No | Medium | Historical Record Only | Operator runbook; manual upload only |
| docs/11_submission_readiness/phase11_project_authorization_note.md | Yes | Phase 11 | Context only | None | None | No | Low | Historical Record Only | Authorization note |
| docs/README.md | Yes | Package Infrastructure | None | None | None | No | Low | Historical Record Only | Caveat: not fully current after Phase 5 |
| docs/MIGRATION_LOG.md | Yes | Package Infrastructure | None | None | None | No | Low | Historical Record Only | Docs reorganization log |
| README.md (repo root) | Yes | README | Reference for repo-level framing | Basis to be rewritten for the package | Rewritten, not copied | No | High | Historical Record Only | Package README is a fresh, narrative-clean rewrite |

### 2.5 Notebooks (14 confirmed)

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| notebooks/01_baseline_reproduction.ipynb | Yes | Phase 2 | Collapsed to "baseline reproduced" summary | None | None | No | Medium | Historical Record Only | RF(100, depth 5, seed 2025); CV 0.812964; leakage by design |
| notebooks/02_eda_and_data_contract.ipynb | Yes | Phase 3 | Source for EDA/data-contract cells | None | None | No | Medium | Historical Record Only | Class balance, missingness, signal families |
| notebooks/03_validation_harness_phase6.ipynb | Yes | Phase 6 | Source for frozen-fold/OOF harness cells | None | None | No | High | Historical Record Only | Defines canonical folds + OOF anchor |
| notebooks/04_phase6a_baseline_reconciliation.ipynb | Yes | Phase 6A | Collapsed to one-line reconciliation note | None | None | No | Low | Historical Record Only | V0–V7 variants |
| notebooks/05_phase6a_d1_d2_diagnostics.ipynb | Yes | Phase 6A | Context only | None | None | No | Low | Historical Record Only | Seed sweep + duplication probe |
| notebooks/06_phase6a_d2_refined_probe.ipynb | Yes | Phase 6A | Context only | None | None | No | Low | Historical Record Only | T1–T4b; duplication cleared |
| notebooks/07_phase7_missingness_availability_feature_block.ipynb | Yes | Phase 7 | Source for F2 feature-engineering cells | None | None | No | High | Historical Record Only | F0–F6; F2 adopted |
| notebooks/07b_phase7b_role_availability_interaction_probe.ipynb | Yes | Phase 7B | Collapsed to "F4 rejected" note | None | None | No | Low | Historical Record Only | Single interaction probe |
| notebooks/08_phase8_model_family_comparison.ipynb | Yes | Phase 8 | Source for Wave 1 comparison cells | None | None | No | High | Historical Record Only | M0–M4; M1 candidate-with-warning |
| notebooks/08b_phase8_wave2_dependency_environment_check.ipynb | Yes | Phase 8 Wave 2 | Context only | None | None | No | Low | Historical Record Only | Separate-environment dependency check |
| notebooks/08c_phase8_wave2_external_gbdt_comparison.ipynb | Yes | Phase 8 Wave 2 | Source for external-GBDT cells | None | None | No | High | Historical Record Only | XGB/LGBM/CatBoost in separate env |
| notebooks/09a_auc_ranking_diagnostics.ipynb | Yes | Phase 9B-Lite | Source for ranking-diagnostics cells | None | None | No | Medium | Historical Record Only | Read-only AUC/PR/Brier/top-k |
| notebooks/10_phase10_model_optimization.ipynb | Yes | Phase 10 | Source for bounded-HPO + CatBoost config cells | None | None | No | High | Historical Record Only | CatBoost tuned config; M1 tuning rejected |
| notebooks/11_phase11_submission_readiness.ipynb | Yes | Phase 11 | Source for refit/inference/validation/submission cells | None | None | No | Critical | Historical Record Only | Option C; both submissions PASS |
| 99_final_integrated_project_report.ipynb (to be built) | No | Package Infrastructure | The deliverable itself | Primary "how to run" target | Centerpiece artifact | Yes | Critical | All | Comprehensive, self-contained, three runtime modes; built by the construction step |

### 2.6 Outputs (by family)

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv | Yes | Phase 6 | Canonical frozen folds; integrity-asserted in Full Repository | None | Regenerated fresh from seed 42 in package | Optional | High | Both | SHA256[:16]=96937649526bcadb; 2781 rows, folds 0..4; package recreates rather than ships |
| outputs/oof/ (Phase 6–10 OOF families) | Yes | Phase 8 Wave 2 | Loaded for diagnostics in Full Repository; values recorded in notebook markdown | None | Not shipped; OOF computed fresh | No | Medium | Historical Record Only | OOF schema Id,fold,y_true,y_pred_proba; persisted families across Phases 6–10 |
| outputs/validation/ (slice + variant summaries) | Yes | Phase 8 Wave 2 | Source for slice/variant tables; summaries embedded in notebook | None | Not shipped | No | Medium | Historical Record Only | Includes Phase 11 candidate_selection/final_refit/model_summary/submission_validation reports |
| outputs/reports/ (validation reports, manifests, candidate logs) | Yes | Phase 11 | Source for results narrative; not shipped | None | Not shipped | No | Medium | Historical Record Only | Includes Phase 11 validation_report.md, artifact_manifest.csv, experiment_log_candidate.csv |
| outputs/figures/ (Phase 3 EDA figures) | Yes | Phase 3 | Figures regenerated in-notebook, not copied | None | Regenerated at runtime | No | Low | Full Repository | phase03_*.png set; the notebook recomputes its own visuals |
| outputs/submissions/phase11_…_catboost_tuned_submission.csv | Yes | Phase 11 | Referenced by SHA-256 only; never edited | None | Regenerated by final refit, not shipped | No | Critical | Historical Record Only | 696 rows; SHA-256 a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8; gitignored |
| outputs/submissions/phase11_…_m1_logistic_regression_baseline_submission.csv | Yes | Phase 11 | Referenced by SHA-256 only; never edited | None | Regenerated by final refit, not shipped | No | Critical | Historical Record Only | 696 rows; SHA-256 0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640; gitignored |
| logs/experiment_log.csv | Yes | Package Infrastructure | None; not touched | None | None | No | Exclude | Exclude | Legacy schema; must not be modified, migrated, or shipped |

### 2.7 References (cite only; do not ship the PDFs)

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| references/books/ (10 PDFs) | Yes | References | Cited in references section | Cited / pointed to references.md | references.md bibliography entries | No | Medium | Historical Record Only | Cite by full bibliographic entry; PDFs not shipped (size/licensing) |
| references/papers/ (11 PDFs) | Yes | References | Cited for load-bearing decisions | Cited / pointed to references.md | references.md bibliography entries | No | High | Historical Record Only | Cawley & Talbot, Kapoor & Narayanan, XGBoost, LightGBM, CatBoost, Optuna, etc. |
| references/course_materials/ (notes, qa, readings, slides, tutorials) | Yes | References | Referenced through project summaries only | None | None | No | Low | Historical Record Only | Course PDFs; not central evidence; not shipped |
| references.md (to be built) | No | References | Companion bibliography | Linked from README | Shipped bibliography file | Yes | High | Both | Lists real references only; hosts the ChatGPT disclosure subsection |

### 2.8 Official data

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| data/input/train.csv | Yes | Data | Loaded for training/refit | "Place under data/input/" instruction | Shipped (A) or placeholder (B) | Conditional | Critical | All | 2781 x 16; includes Drafted, School, Id |
| data/input/test.csv | Yes | Data | Loaded for inference | "Place under data/input/" instruction | Shipped (A) or placeholder (B) | Conditional | Critical | All | 696 x 15; no Drafted |
| data/input/sample_submission.csv | Yes | Data | Loaded for Id order + format check | "Place under data/input/" instruction | Shipped (A) or placeholder (B) | Conditional | Critical | All | 696 x 2 [Id, Drafted]; defines Id order |

### 2.9 Package infrastructure and disclosure

| Source path | Exists? | Phase | Role in final notebook | Role in README | Role in portable package | Include in ZIP? | Priority | Runtime mode | Notes |
|---|---|---|---|---|---|---|---|---|---|
| README.md (package, to be built) | No | README | Points readers to the notebook | The package front page | Required front page | Yes | Critical | Both | Narrative-clean rewrite; no internal tooling mentioned |
| requirements.txt (package, to be built) | No | Package Infrastructure | Declares core dependencies | Referenced in setup steps | Required for local runs | Yes | High | Both | Core scientific stack; CatBoost optional |
| outputs/ (package skeleton: submissions/, folds/, figures/) | No | Package Infrastructure | Write targets at runtime | Mentioned as output location | Empty dirs with placeholders | Placeholder only | Medium | Both | Created empty; populated at runtime |
| Generative AI assistance disclosure (subsection of references.md) | No | Disclosure | None | Linked from references | One sober subsection | Yes | Medium | Both | ChatGPT only; auxiliary support framing; no training/selection/submission claims |
| AGENTS.md | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Internal; never shipped, never mentioned |
| CLAUDE.md | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Internal; never shipped, never mentioned |
| notebooks/_official/ | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Source evidence; repo-only; never executed |
| notebooks/02_*_before_*.ipynb (backups) | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Untracked backups; excluded |
| Libros/, Prompts/, Recapitulaciones/ | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Internal/private; never shipped, never mentioned |
| .git/, .venv/, .obsidian/, .claude/ | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Tooling/state; never shipped |
| Sin título.canvas | Yes | Package Infrastructure | None | None | None | No | Exclude | Exclude | Stray canvas file; excluded |

---

## 3. Sources critical for the notebook

The comprehensive notebook is the centerpiece. Its non-negotiable inputs are:

- The three official CSVs (`data/input/train.csv`, `test.csv`, `sample_submission.csv`) — every cell that
  loads, validates, trains, infers, or writes a submission depends on them.
- The frozen validation protocol from `docs/05_methodology/validation_protocol_phase6.md` and
  `notebooks/03_validation_harness_phase6.ipynb` — `StratifiedKFold(n_splits=5, shuffle=True,
  random_state=42)`, OOF ROC-AUC as the canonical anchor, and class-index verification before extracting
  positive-class probabilities.
- The F2 feature definition from `notebooks/07_phase7_missingness_availability_feature_block.ipynb` and
  `docs/07_feature_engineering/phase7_acceptance.md` — the 21-feature set (13 base + 7 missingness flags +
  `available_measurement_count`), median imputation and one-hot encoding fitted inside training folds (and
  on full train at refit), with School excluded.
- The model definitions and accepted results: M0 RandomForest anchor (OOF 0.8116502602), M1 Logistic
  Regression baseline/fallback (OOF 0.8270821070), and CatBoost tuned (OOF 0.8303208581; config depth=6,
  learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]).
- The Phase 11 refit/inference/validation flow from `notebooks/11_phase11_submission_readiness.ipynb` and
  the Phase 11 reports/validation outputs — the basis for the notebook's submission-generation and
  twelve-check validation suite.

The frozen fold file is High priority but is regenerated from seed 42 inside the package rather than shipped,
so the notebook remains self-contained.

## 4. Sources critical for the README

The README is a fresh, narrative-clean rewrite. Its essential inputs are the problem framing and metric
(from `docs/00_project_contract/challenge_brief.md`), the data-governance and reproducibility statements
(from `docs/04_research/research_notes_leakage.md`, `research_notes_reproducibility.md`, and
`docs/03_eda/experiment_notes.md`), the final results table (from the Phase 8, Phase 8 Wave 2, and Phase 10
acceptance records), and the bibliography pointer to `references.md`. The README must state how to run the
notebook, how to install dependencies, the expected output (a 696-row, two-column submission), the
reproducibility guarantees (seed 42, frozen folds, fold-safe preprocessing), and author attribution
(Jonatan Estiven Sanchez Vargas; Universidad Nacional de Colombia; Systems and Computer Engineering).

## 5. Sources critical for the ZIP

The ZIP must contain exactly: `README.md`, `requirements.txt`, `references.md`,
`99_final_integrated_project_report.ipynb`, a `data/` tree, and an empty `outputs/` skeleton
(`submissions/`, `folds/`, `figures/` with placeholders). Under Scenario A the `data/input/` CSVs are
included; under Scenario B they are replaced by placeholders plus retrieval instructions. The frozen fold
file is Optional in the ZIP because the notebook recreates it deterministically. Nothing else from the
repository belongs in the ZIP.

## 6. Context-only sources

These inform the notebook narrative and the README results table but are not themselves shipped and are not
run in the package: all `docs/01_project_planning/` plans, all `docs/04_research/` notes, the
`docs/05_methodology/` documents beyond the validation/leakage protocols, every phase acceptance record
(Phases 6 through 11), and the thirteen non-final notebooks. They are retained as Historical Record Only in
the Full Repository. Their function is to let the notebook and README state confirmed facts (metrics,
deltas, fold counts, decisions) without re-deriving the full project history; exploratory phases collapse to
single summary lines (for example, "baseline reproduced", "F4 rejected, F2 retained").

## 7. LOCAL sources that must not be used as central evidence

The course materials under `references/course_materials/` (session notes, Q&A, readings, slides, tutorials)
are local supporting material. They may be referenced only through existing project summaries and must never
be presented as primary, load-bearing evidence in the shipped narrative. The load-bearing citations are the
peer-reviewed and book references under `references/books/` and `references/papers/`. Likewise, any value
that is "Not confirmed yet" (see Section 12) must not be asserted as fact in the package.

## 8. Historical artifacts NOT needed for Colab Minimal mode

Colab Minimal computes everything fresh from the three CSVs: folds, F2 features, OOF predictions for the
fallback path, the fold-level table, the final refit, and the validated submission. It therefore does not
need the persisted `outputs/oof/` families, `outputs/validation/` summaries, `outputs/reports/` artifacts,
`outputs/figures/`, the persisted Phase 11 submission CSVs, or the frozen fold file. The accepted OOF
metrics for M0, M1, and CatBoost tuned are embedded as recorded values in notebook markdown for the
results comparison, because they cannot be recomputed in a minimal environment without the heavier models
and the full pipeline. CatBoost is optional in this mode, with a clean fallback to the M1 baseline when the
package is unavailable.

## 9. Files to EXCLUDE

Permanently excluded from both the ZIP and the shipped narrative: `.git/`, `.venv/`, `.obsidian/`,
`.claude/`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `AGENTS.md`, `CLAUDE.md`, `notebooks/_official/`,
all backup notebooks (`notebooks/02_*_before_*.ipynb` and similar), the reference PDFs themselves (cited,
not shipped), `logs/experiment_log.csv` (legacy, must not be modified or shipped), `Sin título.canvas`,
caches, temporary files, and every internal planning or build-spec document including this inventory and
`prompt_build_final_portable_package.md`. The thirteen historical notebooks and the `docs/` tree stay in the
repository but are not placed in the ZIP.

## 10. Files that must NEVER be mentioned in the final notebook

The final notebook (and every shipped file) must never reference, by name or by description, any internal
construction or planning machinery: `CLAUDE.md`, `AGENTS.md`, the `docs/` planning and prompt files, the
build-spec `prompt_build_final_portable_package.md`, the `Prompts/`, `Recapitulaciones/`, and `Libros/`
folders, `notebooks/_official/`, the experiment log, or the build run itself. The shipped prose must not
contain the words associated with internal tooling or automated authoring. The narrative presents a
professional, reproducible data-science project authored by the named author; exploratory phases are
summarized as ordinary methodology, not as a tooling trace.

## 11. Permitted ChatGPT auxiliary disclosure

Exactly one generative-AI disclosure is permitted, and only inside a "Generative AI assistance disclosure"
subsection of `references.md` (optionally cross-linked from the README acknowledgements). It states, soberly,
that ChatGPT was used in an auxiliary capacity for conceptual consultation on validation, leakage, and
feature-engineering frameworks; for coding recommendations and debugging guidance; and for
notebook-organization and documentation-structure review. It must explicitly state that it did not train,
tune, or select models, did not execute hyperparameter optimization, did not make submission decisions, and
did not influence the methodological trajectory beyond advisory consultation. No other generative-AI or
internal-tooling reference is permitted anywhere in the package.

---

## 12. "Not confirmed yet" items

- M1 baseline exact configuration (C, penalty, solver, scaling) is **Not confirmed yet** in the artifacts;
  it must be recovered from the Phase 8 artifacts during the build run and never invented. (Phase 11 ground
  truth lists a recovered candidate config — C=1.0, class_weight=None, max_iter=1000, random_state=42,
  StandardScaler, solver=lbfgs — which the build run must verify against the persisted artifacts before
  asserting it in any shipped file.)
- `docs/12_final_integrated_notebook/prompt_build_final_portable_package.md` does **not yet exist**; it is
  referenced here by name only.
- `99_final_integrated_project_report.ipynb`, the package `README.md`, `requirements.txt`, `references.md`,
  and the `outputs/` package skeleton do **not yet exist**; they are deliverables of the later build run.
- `docs/01_project_planning/project_execution_plan_v1.md` is untracked in the repository state and is treated
  here as a non-source (Exists?=No for inventory purposes).
- Exact pinned versions for the portable `requirements.txt` are **Not confirmed yet** and must be set during
  the build run (CatBoost is recorded as having run in a separate environment at version 1.2.10; the base
  pinned environment remained GBDT-free).
