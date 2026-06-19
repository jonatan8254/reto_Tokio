# Prompt — Opus Phase 10 Strategic Review (Post-Codex)

```text
DO NOT RUN UNTIL CODEX HAS EXECUTED THE AUTHORIZED PHASE 10 AND AN INDEPENDENT
RECOMPUTATION HAS PASSED. This is the third brain in the Opus → Codex → Opus separation:
a post-execution strategic review. It executes nothing, trains nothing, selects no winner,
authorizes no submission, and opens no future phase.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT (Deliverable D). It interprets Codex's Phase 10 outputs, produces a phase-gated candidate recommendation, and drafts the acceptance record for the project director.
**Governing documents:** `phase10_master_planning_brief.md`, `phase10_operator_runbook.md`, `prompt_codex_phase10_execution_plan.md`.

---

The text between the markers is the prompt to run as the post-execution strategic reviewer (Opus), after Codex's authorized run.

```text
================================ BEGIN PROMPT ================================

Actúa como científica de datos senior y revisora estratégica post-ejecución para el
proyecto Reto Tokio / GCI World NFL Draft Prediction (repo local: C:\GitHub\reto_Tokio),
con experiencia en HPO controlado, selection bias, ranking/desbalance, slice diagnostics y
cierre metodológico de fases.

# 0. Precondición absoluta
Esta revisión es válida SOLO si: (a) existió una Phase 10 Project Authorization Note
firmada; (b) Codex ya ejecutó Phase 10 y existen los artifacts
phase10_model_optimization_<run_id>_*; (c) una recomputación independiente de las métricas
pasó (ROC-AUC ±1e-9; integridad OK). Si falta cualquiera, DETENTE y reporta.

NO ejecutas notebooks. NO entrenas/reentrenas. NO HPO. NO ensembles/blending/stacking. NO
recalibras. NO threshold tuning. NO submissions. NO leaderboard. NO declaras final winner.
NO declaras submission-ready model. NO abres Phase 10 nuevas corridas ni Phase 11. NO
modificas outputs de Codex ni forbidden paths. NO stagear/commit/push (salvo instrucción
explícita y selectiva del director). Solo puedes crear/actualizar:
  docs/10_model_optimization/phase10_acceptance.md   (borrador para firma del director)
Opcionalmente, si el director lo pide, una actualización del backlog en
docs/10_model_optimization/ o docs/09_auc_ranking_diagnostics/. Por defecto, solo la
acceptance draft.

# 1. Verificación previa (read-only)
git rev-parse --short HEAD ; git status --short ; git diff --check ;
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json ;
git diff -- logs/experiment_log.csv
Confirma: HEAD coherente con la nota; sin staged; forbidden-path diff vacío; main log
unchanged; .venv/requirements.txt unchanged; sin artifact en outputs/submissions/;
artifacts phase10_* presentes; manifest hashes verificables; fold SHA = 96937649526bcadb.

# 2. Evidencia a leer (read-only, generada por Codex)
- outputs/validation/phase10_model_optimization_<run_id>_hpo_results.csv
- outputs/validation/phase10_model_optimization_<run_id>_model_summary.csv
- outputs/validation/phase10_model_optimization_<run_id>_fold_metrics.csv
- outputs/validation/phase10_model_optimization_<run_id>_slice_report.csv
- outputs/validation/phase10_model_optimization_<run_id>_topk_quantile.csv
- outputs/validation/phase10_model_optimization_<run_id>_score_distribution.csv
- outputs/oof/phase10_model_optimization_<run_id>_<candidate>_oof_predictions.csv
- outputs/reports/phase10_model_optimization_<run_id>_selection_bias_warning_report.md
- outputs/reports/phase10_model_optimization_<run_id>_validation_report.md
- outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv
- outputs/reports/phase10_model_optimization_<run_id>_artifact_manifest.csv
Y como contexto: phase8 (Wave 1 + Wave 2) acceptances, phase9a_acceptance.md + backlog,
phase9b_lite_transition_memo.md, el master planning brief de Phase 10, y los research notes
(hpo, validation, leakage, reproducibility).

# 3. Recomputación independiente mínima (verifier != generator)
Recalcula de forma independiente desde los OOF persistidos, al menos:
- ROC-AUC por candidato (rank-based stdlib) y contrasta con model_summary/hpo_results
  (±1e-9);
- positive rate global (~0.6483);
- una métrica top-k (p.ej. top-decile capture) para un candidato vs topk_quantile.csv;
- integridad OOF: schema Id/fold/y_true/y_pred_proba, 2781 filas, rango [0,1], sin NaN/inf,
  sin duplicados (Id,fold), alineación de folds vs fold file congelado;
- ancla M0 (≤1e-9 vs OOF Phase 7 F2 persistido) y M1 baseline = 0.8270821069632867.
Si algo no coincide dentro de tolerancia: marca BLOCKER y detente.

# 4. Interpretación estratégica (SIN seleccionar winner)
Responde, con lenguaje de asociación (no causal):
- ¿El HPO de M1 mejoró ROC-AUC OOF de forma real (delta tuned-vs-default > noise floor) y
  same-sign en mayoría de folds, o está dentro del ruido? Si está en el ruido, recomienda
  conservar defaults.
- ¿El tuneo de M1 alivió, ignoró o empeoró las warnings heredadas (Age_missing=1 frágil;
  Position=QB robusto)? HPO no debe usarse para esconder un problema de slice.
- Si CatBoost se tuneó: ¿la diagnosis B5 justificó el tuneo? ¿mejoró estabilidad de slices
  robustos (Year 2009/2011, avail_count) o solo ganancia global? ¿supera o no a M1?
- ¿Hay evidencia de selection bias / overfitting de CV (confirmación repeated-CV)?
- ¿Distribuciones de score degeneradas/comprimidas? ¿Conflictos ROC-vs-PR/top-k o
  global-vs-slice?
- ¿Qué candidatos merecen accept-with-warnings / observe / reject / defer, recordando que
  NO hay winner y que M0 sigue ancla?
Mantén roles: M0 ancla; M1 primario candidate-with-warning; CatBoost secundario/observe;
XGB/LGBM dropped no_qualifying_evidence (no re-promover sin evidencia nueva aceptada).

# 5. Matriz de recomendación (en la acceptance draft)
Clasifica cada recomendación en EXACTAMENTE una categoría:
1 Accept Phase 10 result with warnings.
2 Accept Phase 10 result as candidate for Phase 11 planning (not submission execution).
3 Reject optimized variant; keep M1 baseline.
4 Keep CatBoost under observation.
5 Request additional audit before Phase 11.
6 Defer due to insufficient evidence.
7 Prohibited under current rules.
Cada recomendación con la tabla:
| Recommendation ID | Recommendation | Evidence from Phase 10 | Comparison baseline | Methodological support | Risk | Required next gate | Priority |
Priority ∈ {High, Medium, Low, Deferred, Prohibited}. NO inventes ganancias numéricas; usa
solo evidencia de los artifacts. Distingue explícitamente "optimized candidate" de "final
winner": un candidato optimizado NO es un winner ni submission-ready.

# 6. Borrador de aceptación (docs/10_model_optimization/phase10_acceptance.md)
Redacta el borrador para firma del director, incluyendo: decisión (accept-with-warnings /
defer / reject por candidato, SIN winner); estado del audit independiente; reproducción
ROC-AUC (±1e-9) y anclas; resumen tuned-vs-default por candidato; deltas vs M0/M1/CatBoost;
estabilidad fold + repeated-CV; hallazgos de slice (incl. Age_missing=1, QB, Year);
selection-bias report; warnings; matriz de recomendación §5; estado de submission (none);
.venv/requirements (unchanged); main log (unchanged); locks Phase 11; campos de
hash/firma en blanco para el director; lista de archivos sugeridos para commit selectivo;
y la sección "Handoff to Phase 11 Without Opening Phase 11". NO firmes por el director. NO
hagas commit.

# 7. Al terminar
Reporta: PASS/BLOCKER del review; valores recomputados vs Codex; discrepancias; archivos
creados (acceptance draft); git status; y la frase literal:
"Phase 10 strategic review complete. No final winner selected, no submission authorized.
 Candidates remain phase-gated. Acceptance is drafted for project-director signature.
 Phase 11 remains locked."

================================= END PROMPT =================================
```

**What NOT to recommend:** no submission; no leaderboard use; no ensemble/blending/stacking/calibration/threshold tuning as an executed action (only as future-locked items); no reopening of XGB/LGBM deep HPO without written justification; no declaration of a final winner or submission-ready model; no opening of Phase 11. A Phase 10 "optimized candidate" is at most a **candidate for future Phase 11 planning**, never a submission decision.

**Operator reminder:** this prompt runs only after Codex execution + a passing independent recomputation. It produces the phase-gated recommendation matrix and the acceptance draft; the project director signs acceptance and authorizes any selective commit. No winner, no submission, no future-phase opening occurs here.
