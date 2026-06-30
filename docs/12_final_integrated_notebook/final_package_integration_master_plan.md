# Final Package Integration Master Plan — Reto Tokio / GCI World NFL Draft Prediction

**PLANNING ONLY — NOTHING IS BUILT, TRAINED, OR COMMITTED IN THIS RUN.** This document is an internal planning artifact. It does not create the portable package, does not author the final notebook, does not train or retune any model, does not generate or modify submissions, does not touch `logs/experiment_log.csv`, and does not stage, commit, or push anything. It describes how a later build run should assemble the deliverables, grounded strictly in verified repository evidence. Every concrete number, path, SHA, and reference below is taken from the project ground truth; anything not verifiable is marked **Not confirmed yet**.

---

## Scope and Non-Scope

### Scope (what this plan governs)

This master plan governs the design of three coordinated deliverables and the rules that bind them together:

1. A **comprehensive final notebook** (`99_final_integrated_project_report.ipynb`) that tells the whole technical story end-to-end and regenerates the validated final artifacts from official data.
2. A **minimal portable package** (a small ZIP) that lets a third party run the final notebook locally or in a hosted environment without cloning the full repository history.
3. A **professional README** plus a **`references.md`** bibliography that present the work as a self-contained, auditable data-science project.

It also defines: integration rules across phases, evidence admissibility (what may and may not be cited), leakage controls (narrative and technical), the strategy for avoiding heavy retraining, preservation of the executed Phase 11 submissions, the three runtime modes (Full Repository / Portable Package / Colab Minimal), the documentation/writing-quality bar, the real bibliographic policy, and the sober generative-assistance disclosure.

### Non-Scope (explicitly out of bounds for this plan and the build run it describes)

| Out of scope | Reason |
|---|---|
| Training heavy models or running any HPO | Optimization concluded at Phase 10; the package reuses recorded results and only does light, reproducible inference |
| Declaring a final winner among candidates | Project policy keeps both Phase 11 candidates valid; the director chooses upload order |
| Creating new historical submissions or editing existing ones | The two Phase 11 submissions are frozen by SHA-256 identity |
| Using the public leaderboard to drive any decision | Leaderboard is sanity-check only |
| Modifying `logs/experiment_log.csv`, staging, committing, or pushing | Hard git governance; build run is a separate, later, explicitly authorized step |
| Shipping internal planning, tooling, or process traces | The package is a clean technical deliverable |

---

## Phase-Vision Statement (Phase 1 → 11)

The project advanced through a disciplined, gated sequence. The final package must reflect this arc faithfully but compactly:

- **Phases 1–5 — Foundation.** Establish the problem, the data contract, a reproduced baseline, exploratory analysis, a research synthesis, and a frozen methodology. These phases fix the rules (ROC-AUC metric, `StratifiedKFold(5, shuffle=True, random_state=42)`, leakage-safe fit-scope, School excluded until later, submission discipline).
- **Phases 6–7B — Operationalization.** Stand up the leakage-safe validation harness with frozen folds, reconcile the baseline gap, and engineer the leakage-safe feature set. This produces the frozen **F2** feature set (21 features) after a role-interaction probe (F4) is rejected by rule.
- **Phases 8–9A — Comparison and diagnosis.** Compare model families on identical folds and the identical F2 feature set, then run read-only ranking, imbalance, and slice diagnostics. No winner is declared; M1 emerges as the strongest global ranker (candidate-with-warning) and CatBoost as a genuine but warning-heavy second.
- **Phase 10 — Controlled optimization.** Bounded, pre-registered hyperparameter search on the carried candidates. M1 tuning is rejected as noise-level; CatBoost tuned reaches the best global OOF but remains warning-heavy with no repeated-CV stability confirmation.
- **Phase 11 — Final refit and validated submissions.** Full-train refit, leakage-safe test inference, a full validation suite, and two format-compliant 696-row submissions (Option C, dual submission). No winner declared; not uploaded.

---

## Evidence Used vs Evidence That Must NOT Be Used

The final notebook and README narrate the project from recorded results. This table fixes admissibility.

| Evidence class | Status in package | Notes |
|---|---|---|
| Official data (`data/input/train.csv`, `test.csv`, `sample_submission.csv`) | **Used** | 2781×16, 696×15, 696×2; only official files |
| Frozen fold file `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` | **Used** (cited / optionally shipped) | SHA256[:16] `96937649526bcadb`, 2781 rows, folds 0..4 |
| Recorded OOF ROC-AUC values (Phase 8–10, accepted) | **Used** (recorded, not recomputed end-to-end) | M0 0.8116502602, M1 0.8270821070, CatBoost tuned 0.8303208581, etc. |
| Phase 11 validation reports and manifests | **Used** as lineage evidence | Reports under `outputs/reports/` and `outputs/validation/` |
| Phase 11 submission SHA-256 identities | **Used** as durable identity | CatBoost `a6f14ef1…`, M1 `0804613d…` |
| Real reference library under `references/` | **Cited** as bibliography | Cite by title/author/year; do not ship large PDFs |
| Public leaderboard scores | **NOT used** for any decision | Sanity-check only; never drives selection |
| School column as a model feature | **NOT used** | Excluded by frozen policy; diagnostic-only |
| Any external athlete/school/draft/NFL/online dataset | **NOT used** | Forbidden by competition rules |
| Internal planning docs, process traces, tooling notes | **NOT used** in narrative | Excluded from package and prose |
| Leakage-inflated diagnostic variants (e.g., Phase 6A V1 global-preprocessing replica) | **NOT presented as results** | May be referenced only as a documented diagnostic, never as a competitive metric |

---

## Files That Enter vs Do Not Enter the ZIP

### Enter the ZIP (minimal portable package)

| Path in ZIP | Purpose |
|---|---|
| `README.md` | Project overview, rules, run instructions, results, attribution |
| `requirements.txt` | Core dependencies (numpy, pandas, scikit-learn); CatBoost optional |
| `references.md` | Real bibliography + generative-assistance disclosure |
| `99_final_integrated_project_report.ipynb` | Comprehensive, self-contained final notebook |
| `data/input/train.csv`, `test.csv`, `sample_submission.csv` | Official data — **Scenario A only** |
| `data/input/` placeholders + instructions | **Scenario B only** (CSVs excluded) |
| `outputs/submissions/.gitkeep`, `outputs/folds/.gitkeep`, `outputs/figures/.gitkeep` | Preserve runtime output structure |
| `outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv` | Optional: ship frozen folds for exact reproducibility |

### Do NOT enter the ZIP

`.git/`, `.venv/`, `.claude/`, `.obsidian/`, `Libros/`, `Prompts/`, `Recapitulaciones/`, `AGENTS.md`, `CLAUDE.md`, the 14 phase notebooks under `notebooks/` (only the new `99_*` notebook ships), `notebooks/_official/`, backup notebooks (`notebooks/02_*_before_*.ipynb`, etc.), all of `docs/` (including this plan), `references/` PDFs (cited, not shipped), `outputs/oof/`, `outputs/validation/`, `outputs/reports/`, `logs/experiment_log.csv`, caches, temp files, and `Sin título.canvas`.

---

## How Phases 1 → 11 Connect (Integration Rules)

The final notebook is a single linear narrative that compresses eleven phases into one reproducible document while preserving the gated logic. Integration rules:

1. **One frozen validation spine.** Every metric in the narrative refers to the same fold definition: `StratifiedKFold(5, shuffle=True, random_state=42)`, fold file SHA256[:16] `96937649526bcadb`. OOF ROC-AUC is the canonical anchor.
2. **One frozen feature set.** The competitive results all rest on F2 (21 features). Earlier feature experiments (F0–F6, F4) appear as a compact decision trail, not as parallel pipelines.
3. **Recorded results, light recomputation.** Phase 8–10 comparative AUCs are presented as recorded values with their decision rationale. The notebook recomputes only what is cheap and leakage-safe (M1-style CV, final refit, inference, validation).
4. **No phase is re-litigated.** Acceptances (with warnings) from Phases 6, 6A, 7, 7B, 8, 8 Wave 2, 9A, 10, 11 are treated as settled inputs.
5. **Narrative boundaries map to phase boundaries.** Each notebook section header corresponds to a phase or phase group so a reader can audit the arc without reading internal docs.

---

## How to Avoid Heavy Retraining

The package must run quickly and deterministically in modest environments. Strategy:

- **Reuse recorded comparative metrics.** The model-family comparison and HPO outcomes are stated from recorded results (e.g., M0 0.8116502602, M1 0.8270821070, CatBoost tuned 0.8303208581). The notebook does not re-run XGBoost/LightGBM/CatBoost tuning.
- **Recompute only the inexpensive paths.** A leakage-safe LogisticRegression CV (M1-style) and the final full-train refit + test inference are cheap enough to run live.
- **CatBoost is optional, not mandatory.** Where CatBoost is unavailable, the notebook degrades gracefully to the M1 baseline path. The tuned CatBoost config is recorded (`depth=6, learning_rate=0.01, l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[]`) so the result is reproducible where the library is present, and explained where it is not.
- **No HPO anywhere in the package.** Optimization is historical; the package consumes its conclusions.

---

## How to Preserve the Final Phase 11 Submissions

Two validated submissions were produced under run_id `phase11_option_c_20260619_0001`. They must be preserved by identity, not by shipping the gitignored CSVs.

| Candidate | Rows | Header | SHA-256 |
|---|---|---|---|
| CatBoost tuned (primary) | 696 | `[Id, Drafted]` | `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8` |
| M1 LogisticRegression baseline (fallback) | 696 | `[Id, Drafted]` | `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640` |

Preservation rules: the existing CSVs are never edited; their SHA-256 values are the durable identity recorded in the README/notebook lineage. When the notebook regenerates a submission, it writes to `outputs/submissions/` and reports the produced SHA-256 for comparison against the recorded identity. No winner is declared; the director chooses upload order (last submitted file determines final ranking; private leaderboard uses the full test set). Row count must be exactly 696 with Id order matching `sample_submission.csv`.

---

## How to Avoid Narrative AND Technical Leakage

**Technical leakage controls (carried from frozen policy):**
- Imputation, encoding, and any learned statistic fit only inside training folds during CV, or on full train for the final refit; test is transform-only.
- Test data used only for structure/shape checks and final inference — never for fitting, tuning, selection, or drift correction.
- Positive-class probability extracted only after verifying `estimator.classes_` contains label 1; never blind `[:, 1]`.
- School never used as a feature; no target encoding, no global rare grouping, no global scaling before CV.
- The frozen fold file is the single source of fold truth; if folds are regenerated, the seed and splitter must reproduce the recorded SHA256[:16] `96937649526bcadb`.

**Narrative leakage controls:**
- Report leakage-inflated diagnostics (e.g., the Phase 6A global-preprocessing replica) only as labeled diagnostics, never as competitive scores, so a reader cannot mistake an inflated number for a real result.
- Do not let any leaderboard number appear as a justification for a modeling choice.
- Keep the storyline honest about warnings (Age_missing=1 fragility, QB-slice losses, CatBoost robust-slice instability, missing repeated-CV stability) rather than narrating a clean victory.

---

## Three-Mode Balance: Full Repository / Portable Package / Colab Minimal

| Aspect | Full Repository | Portable Package | Colab Minimal |
|---|---|---|---|
| Location | Local repo + `.venv` | Local, ZIP contents only | Hosted notebook |
| Data source | `data/input/` in repo | `data/input/` in ZIP (Scenario A) or user-supplied (Scenario B) | User upload |
| Models shown | Full evidence (M0–M4, GBDTs, CatBoost) | M1 always; CatBoost if installed | M1 always; CatBoost optional |
| Folds | Load frozen file | Load shipped file or regenerate with seed 42 | Regenerate with seed 42 |
| Heavy deps | Full suite | Core + optional CatBoost | Core only |
| Output | Full diagnostics + submission | Submission + validation report | Single validated submission |

Balancing rule: the **same notebook** serves all three modes via environment auto-detection and soft dependency fallbacks. The narrative and recorded results are identical across modes; only the live-computed portions scale down. The full repository remains the auditable source of truth; the portable package is the clean redistributable; the minimal mode guarantees a valid 696-row submission with core libraries only.

---

## Minimal Portable Package Plan

**Objective of the portable package:** allow any reviewer to reproduce the final validated result from official data with minimal setup, without the full repository, internal documentation, or large reference PDFs.

**Target structure (kept deliberately small):**

```
reto_tokio_final/
├── README.md
├── requirements.txt
├── references.md
├── 99_final_integrated_project_report.ipynb
├── data/
│   └── input/                # Scenario A: official CSVs; Scenario B: placeholders + instructions
│       ├── train.csv
│       ├── test.csv
│       └── sample_submission.csv
└── outputs/
    ├── submissions/          # .gitkeep (generated at runtime)
    ├── folds/                # frozen folds (optional) or .gitkeep
    └── figures/              # .gitkeep (generated at runtime)
```

**Data governance scenarios:**
- **Scenario A (private/course package):** include `train.csv`, `test.csv`, `sample_submission.csv`.
- **Scenario B (restricted distribution):** exclude the CSVs; ship placeholders plus instructions to place official files in `data/input/`.

**Size budget:** target a compact archive (notebook plus optional CSVs ~1.5 MB if included). Keep output cells lean.

**Quality gates for the package:** runs top-to-bottom from a clean kernel; produces a 696-row submission with header `[Id, Drafted]`; fold integrity reproduces SHA256[:16] `96937649526bcadb` when folds are regenerated; no internal-tooling references anywhere; references cited rather than shipped.

---

## README Plan

**Objective of the README:** present the work as a professional, self-contained technical project a reviewer can understand and run in minutes.

**Required sections:**

| Section | Content |
|---|---|
| Title and summary | Reto Tokio / GCI World NFL Draft Prediction; binary classification; target `Drafted`; metric ROC-AUC on positive-class probability |
| Data and governance | Official files only; no external data; no leaderboard-driven decisions; `StratifiedKFold(5, seed 42)`; School excluded as a feature |
| Feature set | F2: base 13 + 7 missingness flags + `available_measurement_count` (21 features) |
| How to run | `pip install -r requirements.txt`; open `99_final_integrated_project_report.ipynb`; run top-to-bottom |
| Expected output | Validated submission CSV, 696 rows, `[Id, Drafted]` |
| Results summary | Recorded OOF ROC-AUC table (below) |
| Reproducibility | Fixed seed 42, frozen folds, leakage-safe fit-scope, no HPO at run time |
| Author attribution | Jonatan Estiven Sanchez Vargas — Universidad Nacional de Colombia — Systems and Computer Engineering |
| References and disclosure | Pointer to `references.md`, including the generative-assistance disclosure |

**Recorded results table to include (verbatim from accepted records):**

| Model | OOF ROC-AUC | Role |
|---|---:|---|
| M0 RandomForest (frozen) | 0.8116502602 | Reference anchor |
| M1 LogisticRegression (baseline) | 0.8270821070 | Fallback / reference candidate |
| CatBoost (baseline) | 0.8202943969 | Comparison |
| CatBoost (tuned) | 0.8303208581 | Best global OOF (warning-heavy; primary Phase 11 candidate) |

The README must **not** mention any internal build tooling. It presents methodology and engineering only. The build run (construction step) may consult the build-spec file `prompt_build_final_portable_package.md`, but no trace of that tooling appears in shipped text.

---

## Documentation, Humanized Writing and Analytical Depth Plan

**Objective of the final notebook:** be the single comprehensive, reproducible record of the project — from data contract to validated submissions — readable by a technical reviewer end-to-end.

**Abundant documentation and transitional analysis.** Every code section is preceded by prose that states purpose, inputs, decision, and the transition to the next step. The notebook explicitly narrates the phase arc (foundation → operationalization → comparison/diagnosis → optimization → final refit) with transitional paragraphs between sections so the reader follows *why* each step follows the last, not just *what* runs.

**Analytical depth (honest, not triumphant).** The narrative must surface the real findings and warnings, including: the baseline reconciliation (Phase 6 OOF 0.726616 vs the leakage-inflated Phase 2 replica), the adoption of F2 by rule (OOF 0.8116502602, 5/5 positive folds, slice guard clear) and rejection of F4 (OOF −0.0023, 1/5 folds), the model-family comparison, the diagnostic confirmation that imbalance-aware metrics agreed with the ROC-AUC ordering, and the Phase 10 outcome (M1 tuning rejected as noise; CatBoost tuned best-but-warned, no repeated-CV stability). The class balance (positive rate 0.6483) and missingness profile are documented from the data contract.

**Humanized, professional, firm writing.** Prose is direct, confident, and free of filler; it states decisions and their evidence plainly, acknowledges limitations without hedging into vagueness, and reads as the work of an engineer who owns the conclusions.

**Section map for the notebook:**

| Section | Phase mapping | Core content |
|---|---|---|
| 1. Problem and data contract | 1–3 | Target, metric, official files, class balance, missingness |
| 2. Validation spine | 5–6 | Frozen folds, OOF anchor, leakage-safe fit-scope |
| 3. Feature engineering | 6A–7B | F2 derivation; F4 rejection; School excluded |
| 4. Model comparison | 8–9A | Recorded family comparison; ranking/slice diagnostics |
| 5. Optimization | 10 | Bounded HPO outcome; M1 noise-level; CatBoost tuned warnings |
| 6. Final refit and submission | 11 | Full-train refit, inference, validation suite, dual submissions |
| 7. Results, limitations, references | — | Summary table, honest warnings, bibliography |

---

## Colab Portability Plan

**Objective:** the final notebook runs in a hosted minimal environment with only core scientific Python, and still produces a valid submission.

**Mechanics:**
- **Environment auto-detection** selects a hosted path versus a local path and prompts for the three official CSVs when files are not present, placing them under `data/input/`.
- **Soft dependency fallbacks.** CatBoost is attempted; if unavailable, the notebook proceeds on the M1 baseline path and records that CatBoost results are reported from recorded values rather than recomputed. Core dependencies are numpy, pandas, scikit-learn.
- **Leakage-safe minimal compute.** Folds regenerated in memory with `StratifiedKFold(5, shuffle=True, random_state=42)`; imputation and encoding fit inside folds; final refit on full train; test transform-only; positive-class probability via verified `classes_`.
- **Submission integrity in minimal mode.** Output is a 696-row CSV with header `[Id, Drafted]`, Id order matching `sample_submission.csv`, probabilities finite and within [0, 1], validated before writing.
- **Determinism.** Seed 42 throughout; the regenerated fold assignment must reproduce SHA256[:16] `96937649526bcadb`.

**Known constraint:** **Not confirmed yet** — the exact M1 baseline configuration (C, penalty, solver, scaling) is to be recovered from Phase 8 artifacts and must not be invented; the Colab path must use the recovered config, not a guessed one.

---

## Bibliographic References and ChatGPT Disclosure Plan

**Objective:** guarantee that every cited source is real and physically present in the project reference library, and that auxiliary generative-assistance is disclosed soberly and only here.

**Real bibliographic references.** `references.md` cites only sources that exist under `references/`. The load-bearing set maps directly to project decisions:

| Reference | Supports |
|---|---|
| Cawley & Talbot (2010), *On over-fitting in model selection…*, JMLR 11 | Selection-bias guard; frozen validation; M1-tuning rejection rationale |
| Kapoor & Narayanan (2022), *Leakage and the reproducibility crisis in ML-based science* (arXiv:2207.07048) | Leakage taxonomy; fold-safe preprocessing |
| Kuhn & Johnson (2021), *Feature Engineering and Selection* | Leakage-safe feature blocks |
| James, Witten, Hastie, Tibshirani & Taylor (2021), *An Introduction to Statistical Learning with Applications in Python* | k-fold CV, ROC-AUC foundations |
| Géron (2026), *Hands-On Machine Learning with Scikit-Learn and PyTorch* | Pipeline validation harness |
| Chen & Guestrin (2016), *XGBoost* (arXiv:1603.02754) | GBDT candidate |
| Ke et al. (2017), *LightGBM* (NeurIPS 2017) | GBDT candidate |
| Prokhorenkova et al. (2019), *CatBoost: Unbiased boosting with categorical features* (arXiv:1706.09516) | CatBoost candidate; categorical-leakage mitigation |
| Akiba et al. (2019), *Optuna* (KDD '19) | HPO governance reference |
| Ye et al. (2025), *A closer look at deep learning methods on tabular datasets* (arXiv:2407.00956) | Tree ensembles as strong tabular baseline |
| Massaron, Tunguz & Banachewicz (2025), *The Kaggle Book, 2nd ed.* | Competition validation/leaderboard hygiene |

Additional real items present in `references/` (e.g., `feature_selection_survey_2024.pdf`, `causal_feature_selection_responsible_ml.pdf`, `on_leakage_in_ml_pipelines.pdf`, `meta_analysis_overfitting_kaggle.pdf`, `closer_look_deep_learning_tabular_datasets.pdf`, the LightGBM-practitioner and Python-data books, and the GCI course materials) may be cited as supporting reading. **Citation-completeness caveat — Not confirmed yet:** exact author lists, years, DOIs, page ranges, and edition details must be transcribed from the actual PDFs at build time and must not be fabricated. Any field that cannot be verified from the source is written as **Not confirmed yet**.

**Sources policy.** Cite, do not ship: the large PDFs stay out of the ZIP. The reference list draws only from titles that physically exist in `references/`. No external dataset is cited or used.

**Generative-assistance disclosure (sober, references/acknowledgements only).** `references.md` includes one short, factual subsection titled "Generative AI assistance disclosure." It states that ChatGPT was used in an auxiliary capacity for conceptual consultation on validation/leakage/feature-engineering framing, coding recommendations and debugging guidance, and notebook-organization and documentation-structure review. It states explicitly that it did **not** train, tune, or select models, did **not** execute hyperparameter optimization, and did **not** make submission decisions or determine the methodological trajectory. The disclosure names ChatGPT only; no other tooling is referenced anywhere in the package.

**Writing-quality firewall for shipped text.** Across README, `references.md`, and the notebook, the prose must read as a professional technical project. It must not reference internal execution tooling of any kind as part of the methodology or build narrative; the only permitted generative-assistance mention is the sober ChatGPT disclosure described above.

---

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| A reviewer mistakes a leakage-inflated diagnostic for a real score | Label all diagnostics; present only leakage-safe metrics as results |
| CatBoost unavailable in a target environment | Soft fallback to M1 baseline; CatBoost results reported from recorded values |
| Submission identity drift | Compare regenerated SHA-256 against recorded identities; never edit existing CSVs |
| Over-claiming a winner | Keep dual-candidate framing; director chooses upload order |
| Fabricated citation fields | Transcribe from real PDFs at build; mark unverifiable fields **Not confirmed yet** |
| Internal-tooling leakage into shipped text | Writing-quality firewall; single permitted ChatGPT disclosure |
| M1 config guessed rather than recovered | Recover exact M1 config from Phase 8 artifacts before the build run |
| Heavy compute in minimal environments | No HPO; reuse recorded metrics; light inference only |

---

## Open Items Marked "Not confirmed yet"

- Exact M1 LogisticRegression baseline configuration (C, penalty, solver, scaling) — recover from Phase 8 artifacts; do not invent.
- Exact citation metadata (author lists, years, DOIs, pages, editions) for several `references/` items — transcribe from the actual PDFs at build time.
- Whether the frozen fold file is shipped inside the ZIP or regenerated in-notebook — to be fixed at build time; both must reproduce SHA256[:16] `96937649526bcadb`.
- Final selection between Scenario A and Scenario B for distribution — a governance decision made at package time.

---

*End of plan. This is an internal planning document only; no code, model, submission, or commit is produced by writing it.*
