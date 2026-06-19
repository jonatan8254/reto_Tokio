# Phase 9A — Diagnostic-Driven Improvement Hypothesis Backlog

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Phase:** 9A — AUC-Oriented Imbalance and Ranking Diagnostics (post-Codex Opus strategic review)
**Date:** 2026-06-18
**Source commit (planning-inclusive):** `0207436` (*planning: refine phase 9a diagnostics package*); diagnostics artifacts `phase9a_auc_ranking_diagnostics_v1_*` (untracked at review time)
**Status:** Non-executive backlog. **Nothing here is implemented or authorized.** Phase 9A selects no winner and authorizes no submission. Phase 10 and Phase 11 remain locked.

---

## 0. Basis and Guardrails

This backlog derives **only** from: the five persisted OOF files; the Phase 9A diagnostics (integrity, AUC reproduction, global metrics, top-k/quantile, fold-paired, slice, score-distribution, disagreement); the Phase 7/8 accepted records; and the repository methodology references. It was produced after an **independent recomputation passed** (ROC-AUC ≤ 1.11e-16; average precision ≤ 1.4e-15; top-k positive counts exact; integrity 0 mismatches).

Frozen roles preserved: **m0 = reference anchor; m1 = candidate-with-warning (strongest global ranker); catboost = escalated / candidate-with-warning; xgboost & lightgbm = no_qualifying_evidence.** No item promotes any model, declares a winner, or authorizes a submission. Every ensemble / blending / stacking / HPO / calibration-fitting / threshold-tuning / submission idea is **future-locked**. Expected rationale is qualitative (no invented numeric gains).

Categories: **(1)** Safe diagnostic recommendation for Phase 9A execution · **(2)** Hypothesis for Phase 9B or later diagnostic phase · **(3)** Hypothesis for Phase 10 HPO (locked) · **(4)** Hypothesis for future ensemble/blending (locked) · **(5)** Hypothesis for Phase 11 submission strategy (locked) · **(6)** Deferred — insufficient evidence · **(7)** Prohibited under current rules.

---

## 1. Evidence Snapshot Driving the Backlog

| model | ROC-AUC | PR-AUC (AP) | neg-class AP | Brier | top-500 capture | folds + vs M0 | folds + vs M1 | warning slices | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| m0 | 0.811650 | 0.863811 | 0.778719 | 0.158603 | 0.2496 | — | 1/5 | 0 | anchor |
| **m1** | **0.827082** | **0.874184** | **0.790499** | **0.141434** | **0.2551** | 4/5 | — | 6 | carry |
| catboost | 0.820294 | 0.870463 | 0.788618 | 0.147291 | 0.2524 | 4/5 | 2/5 | 8 | observe |
| xgboost | 0.811348 | 0.864025 | 0.781012 | 0.157459 | 0.2524 | 1/5 | 1/5 | 9 | drop-candidate |
| lightgbm | 0.806220 | 0.858134 | 0.777041 | 0.166400 | 0.2496 | 1/5 | 0/5 | 13 | drop-candidate |

(AP baseline = positive rate 0.6483; neg-class AP baseline = 0.3517.) Rank correlations: M1↔CatBoost Spearman 0.818; M1↔M0 0.819; CatBoost↔M0 0.835; **XGB↔LGBM 0.952 (near-duplicate).** Consistency finding: M1 leads on ROC **and** PR **and** neg-AP **and** Brier **and** top-k — **no ROC-vs-imbalance-metric conflict**; the majority-positive base rate does not reorder candidates.

---

## 2. Backlog Table

| ID | Hypothesis | Evidence motivating it | Methodological support | Expected AUC/ranking rationale (qualitative) | Required future phase | Required artifacts | Main risk | Gate before execution | Priority | Category |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | Characterize M1's `Age_missing=1` collapse (AUC 0.544 ≈ random, −0.1475 vs M0) — separate "8-positive fragility" from a genuine LogisticRegression weakness on age-missing rows | slice report: m1 Age_missing=1 warn+fragile; on Age_missing=0 (n=2346) m1 is best (+0.0281) | Kuhn & Johnson (subgroup divergence); validation note | M1's global lead is intact; the risk is localized — understanding it protects any future selection | Phase 9B diagnostic | slice + score-distribution on the slice; n_pos-aware fragility study | Over-reading 8 positives; or ignoring a real weakness | Phase 9B authorization; min-n discipline | **High** | 2 |
| B2 | Investigate M1's robust-size `Position=QB` underperformance (n=162, −0.046 vs M0) | slice report: m1 QB warning, not fragile (n_pos≥20) | Kuhn & Johnson | A robust-size slice loss is more decision-relevant than the fragile one | Phase 9B diagnostic | per-position slice deep-dive | Multiplicity (many positions) | Phase 9B; report all positions | **Medium** | 2 |
| B3 | Quantify whether M1's global lead is stable under resampling/seed variation before any selection | single OOF realization; threshold provenance is RF-seed-noise | ISLP; Cawley & Talbot | Stability would strengthen "carry"; instability would caution it | Phase 9B diagnostic | bootstrap CIs on AUC/PR (seed-fixed) over the existing OOF | CI misused as a selection rule | Phase 9B; CIs descriptive only | **High** | 1/2 |
| B4 | Treat XGBoost and LightGBM as near-duplicate, sub-M0 rankers — keep as diagnostic reference, do not carry as active candidates | ROC xgb −0.0003 / lgbm −0.0054 vs M0; XGB↔LGBM Spearman 0.952; most slice warnings (9/13) | Kaggle Book (diversity ≠ count) | Removing redundant weak rankers reduces multiplicity and focus dilution | Phase 9B / decision note | disagreement + global tables (existing) | Re-promoting weak models without new evidence | none to *record*; promotion locked | **Low** | 6 |
| B5 | Understand CatBoost's robust-slice instability (Year 2009/2011, OG/OLB, avail_count 0) before any CatBoost tuning | slice report: catboost 8 warnings incl. robust-size | hpo note; Cawley & Talbot | Tuning before understanding risks overfitting the escalations | Phase 10 HPO (locked) | slice + fold artifacts (existing) | HPO-by-stealth | Phase 10 authorization + diagnosis first | **Medium** | 3 |
| B6 | Note that XGB/LGBM *out-rank* M0/M1/CatBoost on `Age_missing=1` (xgb +0.0117, lgbm +0.0261 vs M0) — possible age-missing handling signal | slice report Age_missing=1 row | research_notes_tabular_models (native missing handling) | Only a hypothesis — the slice has 8 positives | Phase 9B diagnostic | age-missing-focused slice study | Fragile-slice over-reading | Phase 9B; fragility flag | **Deferred** | 6 |
| B7 | Record M1↔CatBoost moderate complementarity (Spearman 0.818) as a *future* ensemble candidate-pair — NOT now | disagreement: M1↔CatBoost 0.818 (vs XGB↔LGBM 0.952 redundant) | Kaggle Book (ensemble diversity) | Diversity *may* help, but CatBoost is the weaker partner and 2/5 vs M1 | Future ensemble phase (locked) | disagreement (existing); future OOF blend study | Implicit ensemble / gate jumping | Explicit future ensemble authorization | **Deferred** | 4 |
| B8 | Defer all hyperparameter optimization of M1 and CatBoost | M1 strongest but warned; CatBoost escalated | research_notes_hpo (7 conditions) | HPO should improve a *selected, understood* candidate, not rescue methodology | Phase 10 HPO (locked) | — | HPO-by-stealth; LB-free tuning discipline | Phase 10 authorization (7 conditions) | **Deferred** | 3 |
| B9 | Do not design any submission / threshold strategy | no final winner exists; Phase 9A is diagnostic | challenge brief; submission checklist | n/a — ranking metric is threshold-free | Phase 11 (locked) | — | Leaderboard chasing | Phase 11 authorization | **Prohibited (now)** | 5 |
| B10 | Deepen negative-class (minority, base rate 0.352) retrieval analysis — the harder side where AP is lowest (~0.78) | global metrics neg-class AP; §6 framing | ISLP; §6 of brief | Where ranking utility is most discriminating here | Phase 9B diagnostic | bottom-k / neg-AP extensions (existing seed) | Over-interpretation | Phase 9B authorization | **Medium** | 2 |
| B11 | Keep M1's strong Brier (0.1414, best) as a *diagnostic* calibration note; do not recalibrate | score-distribution + Brier | Kuhn & Johnson (calibration as diagnostic) | Good probability quality supports trust, not selection | Future (calibration fitting locked) | calibration bins (existing, diagnostic) | Recalibration temptation | Explicit future authorization | **Low** | 2 |

---

## 3. Strategic Reading (no winner)

- **M1 carries** as the strongest local ranker on every global lens (ROC, PR, neg-AP, Brier, top-k) and 4/5 folds vs M0 — but it remains **candidate-with-warning**, not a winner, because of the concentrated `Age_missing=1` collapse (B1) and the robust-size QB-slice loss (B2). Its lead's stability is unconfirmed (B3).
- **CatBoost stays under observation** — a genuine second-best that beats M0 but trails M1 and carries more robust-slice instability (B5). Its only forward role beyond observation is a *future-locked* diversity-pair hypothesis with M1 (B7).
- **XGBoost and LightGBM** add no new evidence; they are near-duplicate, sub-M0 rankers and should not be carried as active candidates (B4), though one fragile-slice curiosity is noted (B6).
- The **imbalance diagnostics confirmed rather than challenged the ROC ordering** — an important negative result: no metric conflict forces a re-ranking.

The highest-value, *safe* next questions are B1, B3, B10 (diagnostic, Phase 9B). Everything touching tuning, ensembling, calibration fitting, thresholds, or submissions is future-locked. **Phase 10 and Phase 11 remain locked. No final winner. No submission-ready model.**
