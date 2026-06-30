# Build Specification for the Final Portable Package — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY. Nothing is built, trained, refitted, tuned, submitted, committed, pushed, or staged in this planning run. This document is a construction brief that describes what a later build run must produce. No model is trained here; no submission is created or modified here; no leaderboard is consulted here; `logs/experiment_log.csv` is not touched here. The build run is a separate, explicitly authorized step.**

---

## 0. Status of this document

This file is an **internal planning tool**. It specifies how to construct the final portable package for the project. It is **not** itself part of the deliverable.

> **This build-specification file MUST NOT be shipped inside the portable package.** It stays under `docs/12_final_integrated_notebook/` in the working repository. It is excluded from the package contents and from any package archive.

This document refers to the future construction work neutrally as "the build run" or "the construction step". It does not describe internal execution tooling, and the shipped package must not describe it either (see §9).

---

## 1. Purpose and relationship to the other planning documents

The goal of the build run is to construct a **minimal, portable, self-contained package** that presents the entire project — from problem framing through final submission readiness — as a single professional data-science deliverable suitable for course archival and independent review.

This specification builds upon, and must be read together with, the five companion planning documents under `docs/12_final_integrated_notebook/`:

| Companion document | Role this build spec assumes for it |
|---|---|
| `final_package_integration_master_plan.md` | Overall integration strategy and scope boundaries for the package. |
| `final_package_source_inventory.md` | Authoritative inventory of which repository sources feed the package and which are excluded. |
| `final_package_structure_blueprint.md` | Target folder/file layout of the portable package. |
| `final_notebook_section_blueprint.md` | Section-by-section outline of the final integrated notebook. |
| `final_package_execution_runbook.md` | Step ordering, environment modes, and validation gates for actually running the package. |

> **Not confirmed yet:** the present on-disk status of these five companion documents (created vs. pending). The build run must read each one and reconcile it against this specification before constructing anything. Where this specification and a companion document disagree on a concrete fact, stop and flag the conflict rather than guessing.

---

## 2. What the build run MUST produce

The build run creates exactly one new top-level folder:

```
final_integrated_notebook_package/
├── README.md
├── requirements.txt
├── references.md
├── 99_final_integrated_project_report.ipynb
├── data/
└── outputs/
```

No other top-level entries. The package must stay minimal: the folder is thin, and the **notebook carries the depth**.

### 2.1 Required folder detail

```
final_integrated_notebook_package/
├── README.md                                   # full project narrative, start to finish
├── requirements.txt                            # minimal pinned-or-bounded dependency list
├── references.md                               # real bibliography + GenAI disclosure
├── 99_final_integrated_project_report.ipynb    # comprehensive, heavily documented notebook
├── data/
│   └── input/
│       ├── train.csv                           # Scenario A only (see §8)
│       ├── test.csv                            # Scenario A only (see §8)
│       └── sample_submission.csv               # Scenario A only (see §8)
└── outputs/
    ├── submissions/                            # empty at ship; runtime writes here
    └── folds/                                  # empty or frozen-fold copy (see §6.3)
```

`data/input/` is preferred over a bare `data/` so the official inputs are unambiguous and the Colab read path (`data/input/train.csv`) is obvious. Empty runtime folders are preserved with `.gitkeep`-style placeholders.

---

## 3. Hard prohibitions for the build run

The build run **must not**:

- Train heavy models, run any hyperparameter optimization, or re-run model-family comparisons for the purpose of changing results.
- Create any **new** historical/competition submission, or modify the two existing Phase 11 submission CSVs.
- Use the public or private leaderboard to drive any selection, ranking, or narrative claim.
- Modify `logs/experiment_log.csv`.
- Commit, push, or stage anything.
- Declare a final winner between the two candidates. The package presents both and records that the upload order is the director's manual decision.
- Reference any internal execution tooling anywhere in the shipped package (see §9).

The notebook **may** perform light, reproducible computation needed to render the report (load official CSVs, regenerate fold assignments under the frozen protocol, fit the fallback candidate within folds, run the validation suite, recompute documented metrics). It must not escalate beyond that into tuning or winner selection.

---

## 4. Required qualities of the package

The build run **must** deliver all of the following.

### 4.1 A minimal, portable folder
Five files plus `data/` and `outputs/`, nothing more. Portable enough to run on a clean environment and on Google Colab.

### 4.2 A professional README documenting the whole project, start to finish
`README.md` must read as a complete, professional project record: problem statement, official metric, data governance rules, validation protocol, feature decisions, model exploration summary, final candidates, reproducibility statement, how-to-run instructions, and author attribution. It documents the project from beginning to end without internal-tooling language.

### 4.3 A heavily documented notebook
`99_final_integrated_project_report.ipynb` must be richly annotated with markdown: every major step explained, every decision justified inline, every table captioned. It is the primary deliverable and the place the project's depth lives.

### 4.4 Explicit Phase 1–11 coverage
The narrative (notebook and README) must explicitly cover Phases 1 through 11, in order, each with purpose, key decision(s), and outcome. See §7 for the verified phase-by-phase facts to ground this coverage.

### 4.5 Author and institutional attribution
The notebook and README must attribute the work to:

- **Author:** Jonatan Estiven Sanchez Vargas
- **Institution:** Universidad Nacional de Colombia
- **Program:** Systems and Computer Engineering (Ingeniería de Sistemas e Informática)
- **Project:** Reto Tokio / GCI World NFL Draft Prediction

### 4.6 Colab execution with the official files
The notebook must run in Google Colab using `train.csv`, `test.csv`, and `sample_submission.csv`. In Colab, it should detect the environment and prompt for upload of the three files (Scenario B) or read them from `data/input/` when present (Scenario A).

### 4.7 Robust path configuration
A single, robust path-configuration cell must resolve input/output locations across the local repository, the portable folder, and Colab — no hard-coded absolute paths. Reads use `data/input/`; writes use `outputs/`.

### 4.8 Final submission validation
The notebook must validate any generated submission against the contract: exactly 696 rows; header exactly `[Id, Drafted]`; `Id` set and order matching `sample_submission.csv`; probabilities in `[0, 1]`; no NaN/inf; no duplicate `Id`. Before extracting positive-class probability, it must verify `estimator.classes_` contains label `1` rather than indexing blindly.

### 4.9 SHA-256
The notebook must compute and display the SHA-256 of any submission it generates, and must record the SHA-256 identities of the two existing Phase 11 submissions as durable references (see §7.7).

### 4.10 Artifact traceability
Every result shown must be traceable: experiment/run identifiers, the frozen fold file identity, model configurations, and the lineage from OOF evaluation to final refit. Tables must cite where each number comes from.

### 4.11 Clear, professional, humanized, detailed narrative
The prose must be neutral, firm, and human — readable as the considered account of a careful practitioner, not a log dump. Detailed but disciplined.

### 4.12 Many partial conclusions
Each phase/section ends with an explicit partial conclusion capturing what was learned and what it implies for the next step.

### 4.13 Transition analyses
Between phases, an explicit transition analysis explains why the project moved from one phase to the next and what gate was satisfied.

### 4.14 Explicit per-decision rationale
Every methodological choice (validation protocol, leakage controls, feature block selection, model decisions, candidate handling) must state its rationale at the point of decision.

### 4.15 Clean tables
All comparative evidence is presented in clean, captioned Markdown tables (model comparison, fold deltas, slice diagnostics, submission validation).

### 4.16 pandas/CatBoost fallback
The notebook must degrade gracefully: if CatBoost is unavailable, fall back to the M1 logistic-regression baseline; if richer preprocessing utilities are unavailable, fall back to pandas-based median imputation and encoding. The fallback path must still produce a valid, validated submission.

### 4.17 A real bibliographic references section
`references.md` (and a references section in the notebook) must list **only** sources that physically exist in `references/` (see §10). No invented references, authors, DOIs, or years. Anything uncertain is marked "Not confirmed yet".

### 4.18 A sober ChatGPT auxiliary-support disclosure
A short, sober "Generative AI assistance disclosure" subsection in the references/acknowledgements area discloses ChatGPT only as an auxiliary support tool (see §9.2).

### 4.19 No invented references
Every cited source must correspond to a real file in `references/`. If a citation cannot be grounded, it is omitted or flagged, never fabricated.

### 4.20 A minimal requirements.txt
`requirements.txt` lists only what the notebook needs to run end to end (see §11). CatBoost is optional, behind the fallback.

### 4.21 Zero references to internal execution tooling
No shipped file mentions any internal build or execution tooling in its methodology or build narrative (see §9).

---

## 5. Ground-truth project facts (verified)

| Item | Value |
|---|---|
| Repository | `C:\GitHub\reto_Tokio`, branch `master`, HEAD `e5ea4e8` |
| Target | `Drafted` (1 = drafted) |
| Official metric | ROC-AUC on positive-class probability |
| Train | 2781 rows × 16 cols (includes `Drafted`, `School`, `Id`) |
| Test | 696 rows × 15 cols (no `Drafted`) |
| Sample submission | 696 rows × 2 cols `[Id, Drafted]` |
| Train class balance | 0 = 978, 1 = 1803 → positive rate 0.6483279396 |
| Submission row count | Exactly 696; `Id` order matches `sample_submission.csv` |
| Final ranking rule | Last submitted file determines final ranking; private LB uses full test set |

### 5.1 Train/test missingness (verified)

| Column | Train missing | Test missing |
|---|---:|---:|
| Age | 435 | 115 |
| Sprint_40yd | 145 | 29 |
| Vertical_Jump | 554 | 143 |
| Bench_Press_Reps | 721 | 184 |
| Broad_Jump | 581 | 147 |
| Agility_3cone | 970 | 247 |
| Shuttle | 912 | 228 |

### 5.2 F2 feature set (21 features, frozen)

- **Base 13:** Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump, Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type, Position_Type, Position
- **7 missingness flags:** Age_missing, Sprint_40yd_missing, Vertical_Jump_missing, Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing, Shuttle_missing
- **+ available_measurement_count**
- **School excluded** as a feature.
- Median imputation + one-hot encoding fitted **inside training folds** (Phases 6–10) and **on full train** (Phase 11).

### 5.3 Frozen validation protocol

- `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
- Frozen fold file: `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv`, SHA256[:16] = `96937649526bcadb`, 2781 rows, folds 0..4.
- OOF schema: `Id, fold, y_true, y_pred_proba`.
- Always verify `estimator.classes_` contains label `1` before extracting positive-class probability.

---

## 6. Model evidence to present (verified, read-only)

### 6.1 Accepted OOF ROC-AUC values

| Model | OOF ROC-AUC | Role |
|---|---:|---|
| M0 RandomForest (frozen) | 0.8116502602456482 | Anchor / reference |
| M1 LogisticRegression (baseline) | 0.8270821069632867 | Fallback / reference |
| CatBoost baseline | 0.8202943968641223 | Diagnostic |
| CatBoost tuned | 0.8303208581017550 | Best global OOF; warning-heavy primary candidate |
| M1 tuned | 0.8274819177762125 | Rejected (noise-level +0.0003998 vs M1 base, 3/5 folds) |
| XGBoost | 0.8113477083751576 | Dropped (no qualifying evidence) |
| LightGBM | 0.8062204891415921 | Dropped (no qualifying evidence) |

Pre-registered promotion bar: delta ≥ 0.005436 **AND** same-sign positive folds ≥ 4/5 **AND** slice guard clear. CatBoost tuned: +0.0186706 vs M0 (5/5 folds), but +0.0032388 vs M1 baseline (3/5 folds, below the 0.005436 bar), no repeated-CV stability audit, warning-heavy on robust slices. **No winner is declared.**

### 6.2 Candidate configurations

- **CatBoost tuned (from HPO results):** `depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]`. CatBoost ran in a separate environment (catboost 1.2.10); the base `.venv` was untouched.
- **M1 LogisticRegression baseline:** **Not confirmed yet** — exact `C` / `penalty` / `solver` / scaling must be recovered from the Phase 8 artifacts before the notebook fixes them. Do not invent these values; if not recoverable, mark "Not confirmed yet" in the notebook and use the documented Phase 11 recovery (`C=1.0, class_weight=None, max_iter=1000, random_state=42, StandardScaler, solver=lbfgs`) only if it is confirmed against the artifacts.

### 6.3 Frozen folds in the package
The notebook regenerates folds under the frozen protocol (`StratifiedKFold(5, shuffle=True, random_state=42)`). If the construction step chooses to ship the canonical fold file under `outputs/folds/`, it must be the verified file with SHA256[:16] = `96937649526bcadb`; otherwise the notebook asserts the regenerated assignments reproduce that identity.

---

## 7. Phase 1–11 coverage map (verified facts to ground the narrative)

The narrative must cover each phase explicitly, with a partial conclusion and a transition analysis. Anchor each section on these verified facts.

| Phase | Purpose | Verified key fact(s) | Partial-conclusion seed |
|---|---|---|---|
| 1 | Setup & reproducibility | Notebook-first workflow; seed 42 (StratifiedKFold); hard governance rules; environment recorded. (Phase 1 never formally closed.) | Reproducible infrastructure established. |
| 2 | Baseline reproduction | RandomForest(n_estimators=100, max_depth=5, random_state=2025); global mean imputation + LabelEncoder + BMI (leakage by design); CV ROC-AUC 0.812964 ± 0.025740; public LB 0.80792. | Historical reference only; not a clean anchor. |
| 3 | EDA & data contract | Contract verified (2781×16 / 696×15 / 696×2); positive rate 0.6483279396; missingness mapped; four signal families; 24 figures; School flagged high-cardinality. | Hypotheses logged; nothing locked. |
| 4 | Research synthesis | Rules for validation, leakage, feature blocks, model order, HPO, reproducibility distilled from real references. | Policy inputs ready for freeze. |
| 5 | Methodology freeze | ~17 decisions frozen: StratifiedKFold(5,42); OOF ROC-AUC anchor; fold-safe fit-scope; School excluded until later; HPO gates; submissions Phase 11 only. | Governing policy fixed. |
| 6 | Validation harness | Leakage-safe harness; frozen folds (`96937649526bcadb`); OOF ROC-AUC 0.726616 (provisional anchor); fold mean 0.729253 ± 0.030629. | Clean local baseline established. |
| 6A | Baseline reconciliation | Mean-imputation effect dominates the Phase 2 gap (V7 OOF 0.802271); ablation threshold 0.005436; duplication probe cleared (T4 strict 0%). | Anchor retained; threshold set. |
| 7 | Missingness / availability features | F2 adopted (21 features), OOF 0.8116502602, slice guard clear, 5/5 folds; F1/F3/F5 escalated on Age_missing=1 slice. | F2 is the frozen feature set. |
| 7B | Role-interaction probe | F4 rejected (OOF 0.8093690702, −0.0023 vs F2, 1/5 folds). | F2 retained. |
| 8 (Wave 1) | sklearn model comparison | M1 LR candidate-with-warning (OOF 0.8270821070, 4/5 folds vs M0); M2/M3/M4 rejected. | M1 strongest global, warned. |
| 8 (Wave 2) | External GBDTs | CatBoost escalated (OOF 0.8202943969); XGBoost/LightGBM dropped; separate env, `.venv` untouched. | CatBoost second-best, warned. |
| 9A | AUC / ranking diagnostics | Read-only; M1 leads on ROC, PR-AUC, neg-class AP, Brier, top-k; Age_missing=1 fragility (8 positives); audit max abs diff ~1.11e-16. | M1 carry; no winner. |
| 10 | Bounded optimization | M1 tuning rejected (noise-level); CatBoost tuned best OOF 0.8303208581 but warning-heavy, no repeated-CV; accept with warnings. | CatBoost tuned candidate; M1 fallback. |
| 11 | Submission readiness | Option C dual submission; full-train refit + test inference; 12-check validation suite all pass; two valid 696-row submissions; no winner; not uploaded. | Both candidates submission-ready. |

### 7.7 Existing Phase 11 submissions (durable identities; do not modify)

| Candidate | Rows | SHA-256 |
|---|---:|---|
| CatBoost tuned (primary) | 696 | `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8` |
| M1 LogisticRegression baseline (fallback) | 696 | `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640` |

Phase 11 run_id: `phase11_option_c_20260619_0001`. Submission CSVs live under `outputs/submissions/` and are gitignored; the SHA-256 values above are their durable identity. Phase 10 acceptance commit `fc7a625`; Phase 11 execution commit `e5ea4e8`.

---

## 8. Data governance: Scenario A vs Scenario B

The build run must support both, selected at construction time:

| Scenario | Use case | `data/input/` contents | Notebook behavior |
|---|---|---|---|
| **A** | Private / course package | Ship `train.csv`, `test.csv`, `sample_submission.csv` | Read directly from `data/input/`. |
| **B** | Restricted distribution | Ship placeholders + instructions only (no CSVs) | Prompt for the three official files (upload in Colab / local copy), then proceed. |

Only the official competition files are permitted. No external athlete, school, ranking, geography, draft-history, or online-statistics data, in either scenario.

---

## 9. Tooling-language and disclosure constraints (binding on the shipped package)

### 9.1 Prohibited in all shipped files
No shipped file (README, references, notebook, any other) may mention, in its methodology or build narrative, any internal execution tooling, autonomous orchestration framework, conversational-interface tooling, or instruction-construction process. Present the work strictly as a professional technical data-science project authored by the named author.

### 9.2 Permitted disclosure
A single sober subsection titled "Generative AI assistance disclosure" in the references/acknowledgements area may state that **ChatGPT** was used in an auxiliary capacity for conceptual consultation on validation/leakage/feature-engineering frameworks, coding recommendations and debugging guidance, and notebook-organization and documentation-structure review. It must explicitly state that this tool **did not** train models, tune models, run optimization, select winners, or execute submissions. Keep the tone factual and compliance-focused. No other tool names appear.

---

## 10. Real bibliography (the only citable sources)

Cite **only** files that physically exist under `references/`. Ship the bibliography as text; do not ship the PDFs.

**Books (`references/books/`):** feature_engineering_and_selection_kuhn_johnson_2021.pdf; feature_engineering_modern_ml_2024.pdf; fundamentals_of_data_engineering_2022.pdf; hands_on_machine_learning_sklearn_pytorch_2026.pdf; introduction_to_statistical_learning_python.pdf; machine_learning_with_lightgbm_python_2023.pdf; python_for_data_analysis_3rd_edition_2022.pdf; python_machine_learning_by_example_4th_edition_2024.pdf; the_kaggle_book_2nd_edition_2025.pdf; the_kaggle_workbook_2023.pdf

**Papers (`references/papers/`):** catboost_unbiased_boosting_categorical_features.pdf; causal_feature_selection_responsible_ml.pdf; cawley_talbot_model_selection_overfitting.pdf; closer_look_deep_learning_tabular_datasets.pdf; feature_selection_survey_2024.pdf; leakage_and_reproducibility_crisis_ml_science.pdf; lightgbm_highly_efficient_gbdt.pdf; meta_analysis_overfitting_kaggle.pdf; on_leakage_in_ml_pipelines.pdf; optuna_next_generation_hpo_framework.pdf; xgboost_scalable_tree_boosting_system.pdf

**Course materials (`references/course_materials/`):** notes/GCI_sesion7.pdf, notes/hackaton.pdf; qa/QA.pdf; readings/Lectura Feature Engineering.pdf; slides/lec{1,2,3,4,5,6,8}_slides.pdf; tutorials/competition_tutorial.pdf, tutorials/final_assignment_tutorial.pdf

The construction step must format full citations from these files. Where a citation's bibliographic detail (exact edition year, DOI) cannot be confirmed from the source, mark it "Not confirmed yet" rather than inventing it. The vetted citation strings prepared during research may be used, but every entry must map to a file above.

---

## 11. requirements.txt specification

Keep it minimal. The notebook must run end to end with:

- `pandas`
- `numpy`
- `scikit-learn`

`catboost` is **optional** and reached only through the fallback (§4.16); if listed, mark it optional in a comment. Do **not** require `xgboost`, `lightgbm`, `scipy`, `optuna`, or any heavy stack — those models are dropped or diagnostic and must not gate execution. Pin or bound versions conservatively; if exact pins cannot be confirmed against the working environment, leave bounded constraints and note "Not confirmed yet" for unconfirmed pins.

---

## 12. Notebook construction outline (defer to `final_notebook_section_blueprint.md`)

The notebook `99_final_integrated_project_report.ipynb` must, at minimum:

1. **Header** — title, author/institution/program attribution, project, official metric, run date.
2. **Environment & path configuration** — robust local/portable/Colab path resolution; soft imports with fallbacks (§4.16); seed fixing.
3. **Data load & contract** — read official CSVs; assert 2781/696/696 shapes; class balance; missingness summary (§5).
4. **Validation protocol** — frozen StratifiedKFold(5,42); fold-identity assertion (§5.3, §6.3).
5. **Feature engineering** — F2 construction with leakage-safe fit scope (§5.2).
6. **Phase 1–11 narrative** — explicit per-phase coverage, partial conclusions, transition analyses, per-decision rationale, clean tables (§7).
7. **Model evidence** — comparison and fold-delta tables; CatBoost-tuned and M1-baseline candidates; explicit no-winner statement (§6).
8. **Final refit & inference** — full-train fit; test transform-only; `classes_` check before positive-class probability.
9. **Submission validation** — 696 rows, `[Id, Drafted]`, Id match/order, probability bounds, no NaN/inf/dups (§4.8).
10. **SHA-256 & traceability** — compute new SHA-256; record the two Phase 11 SHA-256 identities (§7.7).
11. **References & GenAI disclosure** — real bibliography (§10) + sober ChatGPT disclosure (§9.2).
12. **Closing** — overall conclusions; final candidates; director-decides-upload-order statement; leaderboard is sanity-check only.

Section structure and depth ultimately defer to `final_notebook_section_blueprint.md`; resolve any conflict in its favor unless it contradicts a verified fact in §5–§7, in which case stop and flag.

---

## 13. Build-run acceptance checklist

Before the package is considered built, confirm every item:

- [ ] Folder is exactly `final_integrated_notebook_package/` with the five files plus `data/` and `outputs/`; nothing extra.
- [ ] README documents the project start to finish, professionally, with author/institution/program attribution.
- [ ] Notebook is heavily documented and covers Phases 1–11 explicitly with partial conclusions and transition analyses.
- [ ] Notebook runs in Colab with the three official files; path configuration robust across all modes.
- [ ] Submission validation enforces 696 rows, `[Id, Drafted]`, Id match/order, probability bounds, no NaN/inf/dups; `classes_` verified.
- [ ] SHA-256 computed for any generated submission; the two Phase 11 SHA-256 identities recorded.
- [ ] Every result is traceable (run ids, fold identity `96937649526bcadb`, model configs, OOF→refit lineage).
- [ ] pandas/CatBoost fallback present and produces a valid submission without CatBoost.
- [ ] `requirements.txt` minimal (pandas, numpy, scikit-learn; CatBoost optional).
- [ ] `references.md` cites only real files under `references/`; no invented references; sober ChatGPT disclosure present.
- [ ] No shipped file mentions internal execution tooling in its methodology/build narrative.
- [ ] No winner declared; both candidates presented; upload order left to the director.
- [ ] Scenario (A or B) selected and applied consistently to `data/input/`.
- [ ] No training of heavy models, no HPO, no new/modified historical submissions, no leaderboard-driven selection, no commit/push/stage, `logs/experiment_log.csv` untouched.
- [ ] **This build-spec file is NOT inside the package.**

---

## 14. Open items marked "Not confirmed yet"

- Present on-disk status of the five companion planning documents (§1).
- M1 LogisticRegression baseline exact configuration (`C`, `penalty`, `solver`, scaling) — recover from Phase 8 artifacts; do not invent (§6.2).
- Exact dependency pins for `requirements.txt` if they cannot be confirmed against the working environment (§11).
- Specific bibliographic details (edition year, DOI) for any reference where the source PDF does not confirm them (§10).
