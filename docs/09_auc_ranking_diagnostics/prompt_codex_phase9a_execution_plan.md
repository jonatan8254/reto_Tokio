# Prompt — Codex Phase 9A Execution Plan (AUC-Oriented Imbalance and Ranking Diagnostics)

```text
DO NOT EXECUTE UNTIL EXPLICIT PROJECT DIRECTOR APPROVAL.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT. **Inert until the operator attaches a signed authorization note** ("PHASE 9A EXECUTION AUTHORIZATION", runbook §10). Without that note, no part of this prompt may be acted on.
**Scope:** Phase 9A — read-only OOF ranking/imbalance diagnostics. This prompt does NOT authorize training, HPO, ensembles, calibration fitting, threshold tuning, submissions, leaderboard use, winner declaration, or any future phase.
**Governing documents:** `docs/09_auc_ranking_diagnostics/phase9a_master_planning_brief.md` (the plan), `docs/09_auc_ranking_diagnostics/phase9a_operator_runbook.md` (the procedure).

---

## Notebook Architecture Fidelity Contract

Codex must implement only the notebook/script architecture approved in `phase9a_master_planning_brief.md`. Codex must not redesign the phase, change the candidate set, add models, train or retrain anything, tune hyperparameters, create ensembles, calibrate or threshold-tune, alter the metric set into a selection rule, alter folds, alter artifacts, generate submissions, use the leaderboard, declare a final winner, or open future phases unless the project director explicitly authorizes those actions. If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project-director approval before proceeding. Codex produces a technical diagnostic report only; strategic prioritization is the later Opus step.
Codex may include a technical backlog seed section inside the validation report, but Codex must not create `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md`. The final improvement backlog is produced only by the post-Codex Opus strategic review after Codex execution and independent recomputation have passed.

---

The text between the markers below is the prompt to give the executor (Codex or equivalent), verbatim, together with the signed authorization note.

```text
================================ BEGIN PROMPT ================================

Actúa como ingeniera ML senior de ejecución, bajo auditoría estricta de leakage,
validación, reproducibilidad y disciplina de ranking metrics, para el proyecto
Reto Tokio / GCI World NFL Draft Prediction (repo local: C:\GitHub\reto_Tokio).

# 0. Precondición absoluta

Esta corrida es válida SOLO si está adjunta una nota de autorización firmada
"PHASE 9A EXECUTION AUTHORIZATION" (formato: runbook §10), que incluye el hash de
commit autorizado. Si la nota no está adjunta, detente y no hagas nada.

# 1. Rol y misión

Implementar y ejecutar EXACTAMENTE los diagnósticos de ranking/desbalance OOF
pre-registrados en docs/09_auc_ranking_diagnostics/phase9a_master_planning_brief.md
(§8 métricas, §9 bloques, §11 slices, §12 blueprint celda por celda, §13 artifacts).
TODO es read-only sobre OOF persistidos. NO entrenas nada. NO seleccionas modelo.
Produces un reporte técnico diagnóstico, no una recomendación estratégica.

# 2. Estado esperado (verifica antes de cualquier cómputo)

git rev-parse --short HEAD        -> debe ser igual al hash de la nota de autorización
git status --short                -> sin staged; sin modificaciones tracked
git diff --check                  -> limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json -> vacío
.venv\Scripts\python.exe          -> Python 3.13.13; pandas 3.0.3; scikit-learn 1.9.0; numpy 2.4.6
# If package versions differ from the expected versions, classify this as a warning unless metric reproduction, OOF integrity checks, or notebook execution fail.
artifacts phase9a_*               -> NO debe existir ninguno (si existe: posible doble ejecución; detente)

Si cualquier verificación falla: reporta, clasifica severidad y DETENTE.

# 3. Archivos que debes revisar antes de implementar (read-only)

- docs/09_auc_ranking_diagnostics/phase9a_master_planning_brief.md   (§6 imbalance, §8 métricas, §11 slices, §12 blueprint, §13 artifacts, §14 stop rules)
- docs/08_model_comparison/phase8_acceptance.md                      (Wave 1: m0 ref, m1 candidate_with_warning)
- docs/08_model_comparison/phase8_wave2_acceptance.md                (Wave 2: catboost escalated; xgb/lgbm no_qualifying_evidence)
- docs/05_methodology/validation_protocol_phase6.md                  (ROC-AUC; ranking quality; not threshold accuracy)
- docs/05_methodology/leakage_checklist_phase6.md
- outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv    (frozen folds; sha256[:16]=96937649526bcadb)
- outputs/oof/phase8_model_family_comparison_v1_m0_random_forest_frozen_oof_predictions.csv
- outputs/oof/phase8_model_family_comparison_v1_m1_logistic_regression_oof_predictions.csv
- outputs/oof/phase8_wave2_external_gbdt_v1_xgboost_oof_predictions.csv
- outputs/oof/phase8_wave2_external_gbdt_v1_lightgbm_oof_predictions.csv
- outputs/oof/phase8_wave2_external_gbdt_v1_catboost_oof_predictions.csv

# 4. Alcance autorizado (futuro, tras la nota)

Crear y ejecutar UN notebook:
  notebooks/09a_auc_ranking_diagnostics.ipynb
  experiment_id = phase9a_auc_ranking_diagnostics_v1
  PROJECT_SEED = 42 (para cualquier bootstrap/sampling; NO se entrena nada)

Escribir SOLO estos artifacts (con pre-write guards fail-if-exists):
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_oof_integrity_report.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_auc_reproduction.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_global_metrics.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_topk_quantile.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_fold_paired.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_slice_report.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_score_distribution.csv
  outputs/validation/phase9a_auc_ranking_diagnostics_v1_disagreement.csv
  outputs/reports/phase9a_auc_ranking_diagnostics_v1_validation_report.md
  outputs/reports/phase9a_auc_ranking_diagnostics_v1_artifact_manifest.csv
  outputs/reports/phase9a_auc_ranking_diagnostics_v1_experiment_log_candidate.csv
  (opcional, solo si aportan valor) outputs/figures/phase9a_auc_ranking_diagnostics_v1_*.png
NO crees phase9a_acceptance.md ni el backlog final: son pasos posteriores (Opus + director).

# 5. Rutas (lectura según se indica; escritura solo en el alcance del punto 4)

- data/input/: LECTURA solo de CSVs oficiales para contract checks. ESCRITURA PROHIBIDA.
- logs/experiment_log.csv: LECTURA (leer antes; assert byte-idéntico al final). ESCRITURA PROHIBIDA.
- notebooks/_official/, references/, outputs/submissions/, .vscode/settings.json,
  Libros/, Prompts/, Recapitulaciones/: lectura y escritura PROHIBIDAS.
- Outputs existentes de Phase 7/8 y acceptance docs: SOLO LECTURA. No modificar.

No git add. No git add . No git commit. No git commit -a. No push. No staging.

# 6. Diseño congelado (no modificable en esta corrida)

Candidatos (5; read-only OOF; NUNCA reentrenar):
  m0_random_forest_frozen  (anchor/reference)
  m1_logistic_regression   (candidate_with_warning, foco diagnóstico)
  catboost                 (escalated/candidate_with_warning, foco diagnóstico)
  xgboost                  (no_qualifying_evidence, diagnostic-only)
  lightgbm                 (no_qualifying_evidence, diagnostic-only)
Roles congelados: NO re-promover xgboost/lightgbm; NO declarar winner; m0 sigue anchor.

Métrica principal congelada: ROC-AUC sobre y_pred_proba (clase positiva Drafted=1).
Imbalance: positive rate global = 0.6483 (1803/2781), MAYORÍA positiva. Reporta
positive rate global + por fold + por slice. PR-AUC/top-k/lift son DIAGNÓSTICOS,
siempre con baseline mostrado; conflictos ROC-vs-PR/top-k = WARNING, nunca re-ranking.

Folds: cargar el fold file y asertar 2781 filas, labels 0..4, sha256[:16]=96937649526bcadb.
El fold de cada OOF es autoritativo; NUNCA recomputar folds.

# 7. Orden obligatorio de ejecución (gates duros)

GATE 1 — Integridad OOF (Bloque 1; ANTES de cualquier métrica):
  Por cada uno de los 5 OOF: schema == [Id,fold,y_true,y_pred_proba]; 2781 filas;
  proba en [0,1]; sin NaN/inf; sin (Id,fold) duplicados; 0 mismatch de Id->fold y
  Id->y_true contra m0; positive rate ~0.6483. Si algo falla: DETENTE (no calcules métricas).
GATE 2 — Reproducción ROC-AUC (Bloque 2):
  Recalcula ROC-AUC por modelo desde OOF y contrasta con los reports aceptados de
  Phase 8 (m0 0.8116502602; m1 0.8270821070; xgb 0.8113477084; lgbm 0.8062204891;
  cat 0.8202943969) dentro de ±1e-9. Si no coincide: DETENTE.
Solo si GATE 1 y GATE 2 pasan, procede a métricas (Bloques 3-8).

# 8. Diagnósticos obligatorios (desde OOF; sin entrenar)

- Global (Bloque 3): ROC-AUC; PR-AUC/Average Precision (con baseline 0.6483);
  Brier diagnóstico (etiquetar "no oficial"); positive rate; retrieval de clase
  negativa (minoría) como lente adicional.
- Top-k/quantile (Bloque 4): precision@k, recall@k, lift@k (con techo ~1.54),
  top-decile y top-quintile capture, cumulative gains, enrichment por quantile;
  SIEMPRE con baseline aleatorio. Grilla k/quantile pre-registrada y registrada.
- Fold-level (Bloque 5): ROC-AUC (y PR-AUC si útil) por fold; deltas pareados vs
  m0 y vs m1; conteo same-sign con magnitudes. Folds alineados (verificado en GATE 1).
- Slices (Bloque 6): 8 dims (Age_missing, Year, available_measurement_count,
  measurement_completeness_group, Player_Type, Position_Type, Position as an optional
  fine-grained diagnostic slice with stricter min-n (`Position` n>=100),
  frequent_vs_rare_school_group diagnostic-only). The 7 established slice dimensions
  remain intact; `Position` is additive and optional. n>=50 (Position n>=100). Reporta
  n, n_positive, positive_rate, AUC, delta_vs_m0, delta_vs_m1, warning flag (>0.02
  caída vs m0). Flag de fragilidad si n_positive<20 (p.ej. Age_missing=1, 8 pos).
  Reporta TODOS los niveles que cumplan min-n (sin selección); registra nº de comparaciones.
- Distribución/calibración (Bloque 7): quantiles de score, separación por y_true,
  flags de compresión/degeneración; Brier; curva de calibración DIAGNÓSTICA. PROHIBIDO
  recalibrar.
- Disagreement (Bloque 8): rank correlation (Spearman/Kendall) m1<->catboost (y vs m0);
  casos m1-alto/catboost-bajo y viceversa. DIAGNÓSTICO; PROHIBIDO ensamblar/blendear.

# 9. Síntesis y veredicto (Bloques 9-10; técnico, no estratégico)

- Warning synthesis: conflictos global-vs-slice, ROC-vs-top-k, inestabilidad fold,
  small-n, multiplicidad.
- Veredicto por candidato: carry / observe / drop-candidate. PROHIBIDO "winner",
  "best", "submission-ready". Sin lenguaje causal injustificado.
- Semilla de backlog (solo ideas basadas en evidencia, clasificadas por fase futura;
  NO ejecutar). El backlog final y la priorización los hace Opus después.

# 10. Política de artifacts y reporte

- Pre-write guards en todos los paths; jamás sobrescribir; colisión => DETENTE.
- Manifest: una fila por artifact (path, sha256, filas).
- Candidate log: filas v2 bajo outputs/reports/. El log principal NO se toca
  (leer antes, assert byte-idéntico al final).
- validation_report.md: entorno + git hash; resultados GATE 1/2; tablas de cada
  bloque; positive rates; baselines; warnings; veredictos por candidato; lenguaje
  de asociación (no causal); declaración explícita de que Phase 9A NO corona winner
  y NO autoriza submission; recordatorio de locks Phase 10/11.
- Estándar de notebook (§12 del brief): cada bloque importante precedido por celda
  Markdown (Objetivo/Inputs/Método/Output esperado/Riesgo controlado) y seguido por
  celda Interpretation (Resultado/Lectura/Riesgo/Decisión diagnóstica). El notebook
  debe leerse como un informe técnico ejecutable.

# 11. Checks de leakage/seguridad obligatorios

- Solo OOF persistidos aceptados como fuente; sin test fitting; sin datos externos;
  sin School como feature (School solo aparece como dimensión de slice diagnóstica).
- Sin entrenamiento; sin HPO; sin ensembles/blending/stacking; sin recalibración;
  sin threshold tuning; sin submissions; sin leaderboard; sin inferir private LB.
- Probas ya son positivas (Drafted=1) en y_pred_proba; no reinterpretar columnas.
- logs/experiment_log.csv byte-idéntico antes/después.

# 12. Stop rules (detente y reporta; no improvises)

HEAD distinto; staged inesperado; artifact phase9a_* preexistente; GATE 1 falla
(schema/filas/range/NaN/dupes/misalignment); GATE 2 falla (AUC no reproduce ±1e-9);
proba inválida; colisión de artifacts; cualquier intento de entrenar/reentrenar,
HPO, ensemble, recalibrar, threshold-tune o submission; uso de leaderboard o datos
externos; main log alterado; presión por declarar winner o abrir Phase 10/11;
presión por añadir métricas/slices que funcionen como regla de selección.
Un slice con n<min-n NO es stop: márcalo non-evaluable/fragile y continúa.

# 13. Al terminar

1) Ejecuta y reporta: git status --short; git diff --check; diff de rutas
   prohibidas (limpias; solo artifacts nuevos untracked); main log byte-idéntico.
2) Entrega: resumen técnico, resultados GATE 1/2, tablas globales/top-k/fold/slice/
   distribución/disagreement, warnings, veredictos por candidato (carry/observe/drop),
   y la frase literal:
   "Phase 9A diagnostics complete; this is technical evidence only. No final winner
    was selected and no submission was authorized. Strategic prioritization and
    acceptance remain for the project director. Phase 10 and Phase 11 remain locked."
3) NO redactes phase9a_acceptance.md ni `docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md`: son pasos
   posteriores de Opus + director.

================================= END PROMPT =================================
```

**Operator reminder:** attach the signed authorization note (runbook §10) with the authorized hash filled in, or this prompt must be refused by any executor that receives it. After Codex finishes and an independent recomputation passes, run `prompt_opus_phase9a_strategic_recommendation_review.md` for backlog prioritization and acceptance drafting.
