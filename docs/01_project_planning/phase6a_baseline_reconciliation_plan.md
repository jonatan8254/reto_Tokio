# Phase 6A Baseline Reconciliation Plan

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Date:** 2026-06-11
**Status:** **Design only. Execution is blocked** until (a) Phase 6 is manually reviewed and accepted, and (b) a human explicitly authorizes Phase 6A and ratifies the variant list below. This document creates no artifacts and runs nothing.
**Governing documents:** `project_execution_plan_v3.md` (§5–§9), `docs/05_methodology/validation_protocol_phase6.md`, `docs/05_methodology/leakage_checklist_phase6.md`, `CLAUDE.md`.

---

## 1. Purpose

Phase 6A exists to make Phase 7 interpretable. The project currently has two baseline scores that disagree by ~0.084 ROC-AUC on fold means (0.812964 − 0.729253 = 0.0837; on the OOF anchor the gap is 0.812964 − 0.726616 = 0.0863) and differ in five pipeline factors at once. Until that gap is decomposed:

1. No quantitative ablation threshold can be set for Phase 7 feature blocks (the threshold must be calibrated against real, observed variance on the frozen folds — currently `Not confirmed yet` in `docs/05_methodology/phase5_execution_decisions.md`).
2. The categorical-encoding policy for tree models (ordinal vs one-hot) — a *pipeline* decision hiding inside the gap — remains unsettled, which would confound every Phase 7 block result.
3. Every future result will be read against the wrong number (0.81), creating standing pressure to quietly re-adopt the leaky Phase 2 preprocessing.

`CLAUDE.md` anticipates this audit: "A future Phase 6A audit may compare Phase 2 vs Phase 6 under controlled conditions, but do not run it unless explicitly asked." This plan is the controlled-conditions design.

Phase 6A's deliverables are **knowledge and policy, not a model**: a decomposed gap, a ratified anchor score, a ratified encoding policy, and a variance-derived ablation threshold.

---

## 2. Problem statement

**Confirmed facts:**

- Phase 2 (`notebooks/01_baseline_reproduction.ipynb`, committed): CV mean ROC-AUC **0.812964** ± 0.025740; public LB 0.80792 (`logs/experiment_log.csv`).
- Phase 6 (`notebooks/03_validation_harness_phase6.ipynb`, untracked): fold mean **0.729253** ± 0.030629; OOF **0.726616** (`outputs/reports/phase6_rf_sanity_baseline_v1_validation_report.md`).
- Both use `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` — fold membership is identical.

**Why the results are not directly comparable** (repository evidence from notebook source; five simultaneous differences):

| # | Factor | Phase 2 | Phase 6 |
|---|---|---|---|
| 1 | Preprocessing fit scope | Global: mean imputation and LabelEncoder fitted on **full train before CV** (leakage by design — faithful official-baseline reproduction) | Fold-safe: all preprocessing inside per-fold `Pipeline`/`ColumnTransformer` |
| 2 | Imputation statistic | Mean (Age + 6 physical tests only) | Median (all numeric features) |
| 3 | Categorical encoding | LabelEncoder → ordinal integers | OneHotEncoder(handle_unknown="ignore") after most_frequent imputation |
| 4 | BMI feature | Included (`Weight / Height**2`, official baseline feature) | Excluded |
| 5 | RF random_state | 2025 | 42 |

Both exclude `Id` and `School`; both include `Year` and the role categoricals; both use RandomForestClassifier(n_estimators=100, max_depth=5).

**Working hypotheses** (inference — to be tested, not assumed; see review §5.2): the encoding representation under depth-5 trees and the BMI feature are the leading candidates for most of the gap; global-fit leakage inflates Phase 2 by an unknown amount; mean-vs-median and the model seed are likely second-order. Phase 6A measures these instead of arguing about them.

---

## 3. Scope

**Allowed:**

- Read existing notebooks, docs, and artifacts.
- Design and (once authorized) implement one reconciliation notebook executing the ratified variant list.
- Use the **frozen folds** loaded from the committed fold-assignment file — never recomputed.
- Produce the variant-summary, per-variant OOF files, and the reconciliation report named in §6.
- Derive and propose: definitive anchor, encoding policy, ablation threshold, minimum slice size.

**Forbidden:**

- Submissions of any kind.
- HPO of any kind (including informal "let's also try depth 7").
- Model-family comparison (RandomForestClassifier(100, depth 5) is the only estimator in Phase 6A).
- Phase 7 feature blocks or any feature work beyond the pre-registered variants below.
- Public leaderboard use — the existing 0.80792 may be mentioned as history but must not justify any conclusion.
- `logs/experiment_log.csv` modification (candidate rows only, under `outputs/reports/`).
- `data/input/` modification; `outputs/submissions/` writes; `notebooks/_official/` access beyond read-only.
- School in any feature matrix (it stays diagnostic-only).
- Adding, removing, or altering variants after ratification without a recorded human decision.

---

## 4. Proposed reconciliation variants

Eight pre-registered variants. **V0 is the existing Phase 6 result (reused, not re-run, unless fold-integrity verification requires a re-run — which would itself be a finding).** All variants use the frozen folds, RandomForestClassifier(n_estimators=100, max_depth=5, n_jobs as available), and the §7.10 leakage checklist instantiated per variant.

Design logic: V1 reproduces Phase 2 inside Phase 6-style reporting (bridge validity check: it must land near 0.813). Then two **decomposition ladders** walk between the endpoints, changing one factor at a time — V2/V3 strip factors from the Phase 2 replica, V5/V6/V7 add factors to the clean Phase 6 pipeline. Comparing rungs isolates each factor twice (once in a leaky context, once in a clean context), which also reveals interaction effects between leakage and representation.

- **V0 — `phase6a_v0_phase6_current`** — the accepted Phase 6 result, carried in as the clean endpoint. *Methodologically acceptable.*
- **V1 — `phase6a_v1_phase2_replica`** — exact Phase 2 behavior (global mean imputation on the 7 columns, global LabelEncoder, BMI, seed 2025) executed under Phase 6 reporting (OOF, slices, checklist — with the leakage items deliberately marked FAILED, by design). Purpose: verify the bridge (≈ 0.813 expected). *Diagnostic-only: contains deliberate leakage.*
- **V2 — `phase6a_v2_replica_no_bmi`** — V1 minus BMI. Isolates BMI's contribution in the leaky context. *Diagnostic-only.*
- **V3 — `phase6a_v3_replica_seed42`** — V1 with RF random_state=42. Isolates/dismisses the seed factor (expected: within noise). *Diagnostic-only.*
- **V4 — `phase6a_v4_foldsafe_ordinal_mean_bmi`** — fold-fitted mean imputation + fold-fitted OrdinalEncoder (handle_unknown via encoded placeholder) + BMI + seed 42. This is "Phase 2's recipe made leakage-safe": the cleanest measure of how much of Phase 2's score was leakage inflation vs legitimate signal. *Methodologically acceptable in construction; its BMI/encoding choices are policy questions, not defaults.*
- **V5 — `phase6a_v5_phase6_plus_bmi`** — Phase 6 current pipeline + BMI (row-wise, parameter-free per `docs/05_methodology/leakage_checklist_phase6.md` allowed-transformations logic). Isolates BMI in the clean context. *Methodologically acceptable as a measurement; BMI **adoption** remains a Phase 7 Block 0 human decision.*
- **V6 — `phase6a_v6_phase6_ordinal`** — Phase 6 current pipeline with fold-fitted OrdinalEncoder replacing OneHotEncoder. Isolates the encoding representation in the clean context — the single most decision-relevant variant. *Methodologically acceptable.*
- **V7 — `phase6a_v7_phase6_mean_impute`** — Phase 6 current pipeline with SimpleImputer(strategy="mean") replacing median. Isolates the imputation statistic. *Methodologically acceptable.*

Optional addendum (run only if V1–V7 leave a large unexplained residual, and only with human approval): **V8 — `phase6a_v8_phase6_ordinal_bmi`** (V6 + BMI) to close the ladder to V4. Hard cap: **no more than 8 executed variants total** without a new human authorization.

**Diagnostic-only secondary analyses** (no model training, no features):

- **D1 — variance calibration:** seed-sweep of the final candidate-anchor pipeline (e.g., RF seeds {42, 2025, 7, 123, 2026} on frozen folds) to measure pure seed noise on OOF AUC. This number, with per-fold paired deltas across variants, derives the Phase 7 ablation threshold.
- **D2 — unit-of-observation probe:** read-only near-duplicate scan of train rows across `Year` (similar Height/Weight/physical profiles, same Position) to inform the dormant grouped-CV question. Purely descriptive; output is a count and examples in the report, not a feature and not an automatic protocol change.

---

## 5. Variant matrix

| Variant | Purpose | Feature set | Preprocessing | Model seed | Leakage risk | Diagnostic-only? | Methodologically acceptable? | Expected interpretation |
|---|---|---|---|---|---|---|---|---|
| V0 phase6_current | Clean endpoint / provisional anchor | 13 raw (no School, no BMI) | fold-fitted median impute + most_frequent + OneHot | 42 | None | No | **Yes** | Reference point 0.7266 OOF |
| V1 phase2_replica | Bridge validity: reproduce 0.813 under new reporting | 13 raw + BMI | **global** mean impute + **global** LabelEncoder | 2025 | **Deliberate (by design)** | **Yes** | No | If ≉0.813, the bridge itself is broken → stop condition |
| V2 replica_no_bmi | BMI effect, leaky context | 13 raw | global mean + global LabelEncoder | 2025 | Deliberate | **Yes** | No | V1−V2 ≈ BMI contribution (leaky context) |
| V3 replica_seed42 | Seed effect | 13 raw + BMI | global mean + global LabelEncoder | 42 | Deliberate | **Yes** | No | V1−V3 ≈ seed noise; expect ≪ fold std |
| V4 foldsafe_ordinal_mean_bmi | Phase 2 recipe, made leakage-safe | 13 raw + BMI | fold-fitted mean + fold-fitted Ordinal | 42 | Low | No | Yes (construction) | V1−V4 ≈ pure leakage inflation of Phase 2 |
| V5 phase6_plus_bmi | BMI effect, clean context | 13 raw + BMI | fold-fitted median + OneHot | 42 | Low | Boundary (measurement yes; adoption is Phase 7) | Yes (as measurement) | V5−V0 ≈ BMI contribution (clean context) |
| V6 phase6_ordinal | Encoding effect, clean context | 13 raw | fold-fitted median + fold-fitted Ordinal | 42 | Low | No | **Yes** | V6−V0 ≈ ordinal-vs-onehot effect → encoding policy input |
| V7 phase6_mean_impute | Imputation statistic | 13 raw | fold-fitted mean + OneHot | 42 | Low | No | Yes | V7−V0 ≈ mean-vs-median effect |
| (V8 optional) phase6_ordinal_bmi | Ladder closure if residual large | 13 raw + BMI | fold-fitted median + Ordinal | 42 | Low | No | Yes | V8 vs V4 isolates mean-vs-median within the acceptable family |
| D1 seed sweep | Noise floor for threshold | anchor pipeline | as anchor | {5 seeds} | None | Yes (analysis) | — | Distribution of OOF deltas under pure noise |
| D2 near-duplicate probe | Grouped-CV evidence | none (no model) | none | — | None | Yes (analysis) | — | Count/examples of plausible repeat athletes |

All comparisons use **OOF ROC-AUC on the frozen folds** as the primary number, with per-fold paired deltas reported for every pair cited in the report (paired deltas on identical folds are far more sensitive than comparing two fold-means under std ≈ 0.03).

---

## 6. Required artifacts for Phase 6A

**Future names only — nothing is created until Phase 6A is authorized.**

```text
notebooks/04_phase6a_baseline_reconciliation.ipynb
outputs/reports/phase6a_baseline_reconciliation_report.md
outputs/reports/phase6a_baseline_reconciliation_experiment_log_candidate.csv
outputs/validation/phase6a_baseline_reconciliation_variant_summary.csv
outputs/oof/phase6a_<variant_id>_oof_predictions.csv        (one per executed variant V1–V7/V8)
outputs/folds/phase6a_fixed_fold_assignments.csv            (verification copy of the frozen folds; must be byte-equivalent in content to the committed Phase 6 fold file)
```

Notebook contract (binding on the future implementation): runs top-to-bottom from repo root; relative paths; loads the frozen folds from file and **asserts** integrity (2781 rows, expected per-fold class counts) before any training; one variant = one declarative config entry; pre-write guards (fail if target artifact exists); per-variant §7.10 leakage checklist instantiated (with V1–V3's deliberate-leakage items explicitly marked as by-design failures); records commit hash + environment versions; writes the candidate log row(s) to `outputs/reports/` only; never touches `logs/experiment_log.csv`.

Report contract: variant matrix with results; gap-decomposition table (factor → estimated contribution → context(s) measured); D1 noise-floor analysis with the proposed ablation threshold and its derivation; D2 findings; explicit *diagnostic vs decision* labeling (§5.2.8 of Plan v3); proposed anchor; proposed encoding policy; open items.

---

## 7. Acceptance criteria

Phase 6A closes only when **all** of the following are true and recorded in a human-signed acceptance record:

1. **Bridge verified:** V1 reproduces Phase 2's score within tolerance (suggested: |V1 fold-mean − 0.812964| < 0.005, folds being identical; tolerance ratified at authorization). If not → stop condition 9.1.
2. **Gap decomposed:** factor contributions (leakage inflation, encoding, BMI, imputation statistic, seed) are quantified with paired per-fold evidence, and the unexplained residual is small (suggested: |residual| < 1 × seed-noise std from D1; ratified at authorization).
3. **Anchor ratified:** the human selects the definitive Phase 7 anchor pipeline and its OOF number from the *methodologically acceptable* variants only (V0/V5/V6/V7/V4-family). Diagnostic-only variants are ineligible by construction.
4. **Encoding policy ratified:** ordinal vs one-hot for role categoricals under tree models is decided from V6-vs-V0 (and V4/V8) evidence and recorded as a frozen pipeline decision.
5. **Ablation threshold ratified:** a concrete numeric rule for Phase 7 block acceptance (e.g., "OOF delta ≥ X with same-sign fold deltas in ≥ k/5 folds"), derived from D1 + paired-delta variance, is recorded.
6. **Minimum slice size set:** from observed slice variance across variants, a minimum-n flag threshold for slice diagnostics is recorded.
7. **BMI disposition recorded:** the V5 measurement is recorded and the adoption decision is explicitly *deferred to Phase 7 Block 0* (or decided now by the human, either way in writing).
8. **D2 disposition recorded:** grouped-CV stays dormant or escalates to a protocol-change decision (escalation = stop condition, not an automatic change).
9. **All artifacts** exist per §6, conform to the artifact contract, and are commit-anchored; candidate log rows written; main log untouched (verified).
10. **No forbidden action occurred** (verified against §3): no submissions, no HPO, no other model families, no LB input, no feature work beyond the ratified list.

---

## 8. Risks

| Risk | Description | Control |
|---|---|---|
| Leakage (re-introduced) | V1–V3 deliberately contain leakage; their code patterns must never migrate into acceptable variants or Phase 7 | Deliberate-leakage variants are quarantined in config + named `replica`; checklist marks them by-design-failed; acceptable variants independently checked |
| Comparability | Any variant silently recomputing folds, changing n_estimators/depth, or altering row order breaks pairing | Frozen-folds file + integrity asserts; single estimator config; paired-delta computations keyed by `Id` |
| Accidental feature selection | "While we're here, try dropping Year / adding flags" | Pre-registered variant list; hard cap of 8; anything else → Phase 7 backlog |
| Overinterpretation | Reading small deltas as real effects | All conclusions sized against D1 noise floor; paired evidence required |
| Scope creep | Variant list grows, "one more run" syndrome | Human ratification required for any addition; V8 pre-authorized as the only optional extension |
| Premature Phase 7 | Starting blocks before acceptance record is signed | Plan v3 §8 gate; Phase 7 prompts require the 6A acceptance record to exist |
| Leaderboard chasing | Using 0.80792 to argue for the leaky pipeline or to pick the anchor | §3 prohibition; anchor must be argued from internal evidence only |
| Log schema drift | Writing v2-schema rows into the legacy main log | Candidate rows only; schema assert before any log write; migration separately gated |
| Artifact overwrite | Re-runs clobbering earlier variant outputs | Pre-write guards (fail-if-exists); re-runs require new run_id/v-bump |

---

## 9. Stop conditions

Stop immediately, report findings, and await human input if any of the following occurs:

1. **Bridge failure:** V1 does not reproduce ≈ 0.813 on identical folds — the reconciliation premise is wrong (data drift, environment effect, or a notebook defect) and everything downstream is uninterpretable.
2. **Fold-integrity failure:** the frozen-folds file fails its asserts, or recomputation from the frozen splitter spec does not reproduce it.
3. **Too-good-to-be-true:** any acceptable-variant OOF jumps far above the plausible range (suspect leakage first, always).
4. **Large unexplained residual:** factor contributions don't approximately compose to the observed gap (interaction effects beyond V8's reach) — human decides whether deeper decomposition is worth it.
5. **D2 escalation:** the near-duplicate probe suggests material athlete repetition across rows — grouped-CV becomes a live protocol question; no further experiments until the human rules on it.
6. **Any §3 forbidden action becomes necessary-seeming** to proceed — it isn't; stop.
7. **Artifact path collision, schema mismatch, or environment anomaly** (e.g., scikit-learn version differs from the version recorded in Phase 6's run, if recorded).
8. **Variant-list pressure:** any participant (human or agent) proposes mid-run changes to the variant list — pause for a recorded decision rather than absorbing the change.

---

## 10. Recommended next action

1. **Now:** Human performs the Phase 6 manual review (Plan v3 §8, Phase 6 task list) and signs the Phase 6 acceptance record.
2. **Then:** Human decides whether to authorize Phase 6A, and in the same decision **ratifies**: the variant list (V0–V7, optional V8), the V1 bridge tolerance, the residual tolerance, and the D1 seed list.
3. **Only after that:** implement `notebooks/04_phase6a_baseline_reconciliation.ipynb` per §6's notebook contract, have it independently reviewed (two-role rule), execute it, and bring the report back for the Phase 6A acceptance decision (§7).

**Recommendation:** treat Phase 6A as **mandatory before Phase 7**. It is cheap (one notebook, ≤ 8 single-model variants on existing folds), it converts an unexplained ~0.08–0.09 gap into ratified policy (anchor, encoding, threshold, slice minimums), and every later phase becomes interpretable because of it. Execution remains blocked until the human authorizations above are recorded.
