# Prompt — Codex Phase 10 Execution Plan (Bounded HPO and Controlled Model Selection)

```text
DO NOT RUN UNTIL THE PROJECT DIRECTOR HAS SIGNED A PHASE 10 PROJECT AUTHORIZATION NOTE.
This prompt is INERT until that note exists. It selects the authorized hash, budget mode,
candidate scope, and resolves gate 5 (experiment-log schema). Without it, do nothing.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT (Deliverable C). This is the **second brain** in the Opus → Codex → Opus separation: a reproducible executor, not a strategist. It executes only what the signed authorization note allows.
**Governing documents:** `phase10_master_planning_brief.md`, `phase10_operator_runbook.md`. On any conflict, the stricter rule and `CLAUDE.md`/`AGENTS.md`/`project_execution_plan_v3.md` win.

---

The text between the markers is the prompt to run as the Phase 10 executor (Codex), **after** the signed authorization note.

```text
================================ BEGIN PROMPT ================================

Actúa como ejecutor reproducible de ML para el proyecto Reto Tokio / GCI World NFL Draft
Prediction (repo local: C:\GitHub\reto_Tokio). Eres ejecutor, no estratega: implementas
EXACTAMENTE lo autorizado, sin convertir recomendaciones en acciones nuevas.

# 0. Precondición absoluta
Existe una Phase 10 Project Authorization Note FIRMADA que define: hash autorizado,
budget mode (Minimal/Standard/Extended), si CatBoost limited HPO está autorizado (y que
la diagnosis B5 lo precede), si hay reapertura diagnóstica XGB/LGBM (con justificación
escrita), y la resolución/waiver del gate 5 (experiment-log schema). Si la nota no existe
o algún punto no está resuelto, DETENTE y reporta. No ejecutas nada sin la nota.

NO abres Phase 11. NO creas submissions. NO usas leaderboard. NO declaras final winner ni
submission-ready model. NO ensembles/blending/stacking. NO calibración. NO threshold
tuning. NO datos externos. NO School como feature. NO modificas logs/experiment_log.csv,
data/input/, notebooks/_official/, references/, outputs/submissions/, .venv,
requirements.txt, lockfiles, .vscode/settings.json, Libros/, Prompts/, Recapitulaciones/.
NO stagear/commit/push. NO git add . NO git commit -a. NO amplías el search space tras ver
resultados. Generación y verificación están separadas: NO audites tu propia corrida como
aceptación; eso lo hace Opus después.

# 1. Estado inicial requerido (read-only)
git rev-parse --short HEAD            # == hash autorizado en la nota
git status --short                    # sin staged; solo untracked conocidos
git diff --check                      # limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # vacío
git diff -- logs/experiment_log.csv   # vacío
Confirma presentes y aceptados: phase9b_lite_transition_memo.md, phase9a_acceptance.md,
phase9a_improvement_backlog.md, validation_protocol_phase6.md, leakage_checklist_phase6.md,
el fold file outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv (SHA256[:16]
= 96937649526bcadb), y los 5 OOF baselines de Phase 8/9A. Si falta algo o el gate 5 sigue
abierto, DETENTE.

# 2. Documentos a leer (read-only)
phase10_master_planning_brief.md (eligibilidad §11, search space §13, budget §14, métricas
§15, controles §16, slices §17, notebook §18, artifacts §19, candidate log §20), el
runbook, y como contexto: phase8_acceptance.md, phase8_wave2_acceptance.md,
phase9a_acceptance.md + backlog, phase9b_lite_transition_memo.md, validation/leakage
protocols, research_notes_hpo.md.

# 3. Alcance autorizado (futuro, exacto)
Feature set: SOLO F2 (base Phase 6 + 7 missing flags + available_measurement_count).
Sin features nuevas. School excluida (assert raise-on-violation). Imputación mediana +
one-hot fold-safe.
Folds: cargar el fold file congelado y ASERTAR integridad (SHA, 2781 filas, folds 0..4).
No recomputar folds para selección.
Candidatos:
  - M1 LogisticRegression = PRIMARIO. HPO acotado en el espacio pre-registrado §13
    (C log-uniform [1e-3,1e2]; penalty {l2,l1}; class_weight {None,balanced}; solver
    compatible; max_iter fijo para converger). Objetivo = OOF/fold-mean ROC-AUC.
  - CatBoost = SECUNDARIO, limited HPO SOLO si la nota lo autoriza y tras diagnosis B5;
    cat_features=[]; entorno Wave 2 SEPARADO (no tocar .venv); sin early stopping basado en
    test; espacio pequeño §13 (depth {4,6,8}; learning_rate [0.01,0.2]; l2_leaf_reg
    {1,3,5,9}; iterations {200,400,800}; border_count {64,128}; random_seed=42).
  - M0 RandomForest = ANCLA. NO se tunea; se carga desde OOF persistido (config 100,
    depth 5, seed 42) para deltas pareados.
  - XGBoost / LightGBM = DROPPED. NO deep HPO por defecto; solo diagnóstico minúsculo
    pre-registrado si la nota adjunta justificación escrita.

# 4. Rutas permitidas (escritura)
notebooks/10_phase10_model_optimization.ipynb
outputs/oof/phase10_model_optimization_<run_id>_<candidate>_oof_predictions.csv
outputs/validation/phase10_model_optimization_<run_id>_hpo_results.csv
outputs/validation/phase10_model_optimization_<run_id>_model_summary.csv
outputs/validation/phase10_model_optimization_<run_id>_fold_metrics.csv
outputs/validation/phase10_model_optimization_<run_id>_slice_report.csv
outputs/validation/phase10_model_optimization_<run_id>_topk_quantile.csv
outputs/validation/phase10_model_optimization_<run_id>_score_distribution.csv
outputs/reports/phase10_model_optimization_<run_id>_selection_bias_warning_report.md
outputs/reports/phase10_model_optimization_<run_id>_validation_report.md
outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv
outputs/reports/phase10_model_optimization_<run_id>_artifact_manifest.csv
experiment_id = phase10_model_optimization_v<K>; run_id obligatorio; check-and-fail si la
ruta existe (nunca sobrescribir). Rutas con forward slashes.

# 5. Rutas prohibidas
Todo lo de §0 (logs/experiment_log.csv, data/input/, notebooks/_official/, references/,
outputs/submissions/, .venv, requirements.txt, lockfiles, .vscode/settings.json, Libros/,
Prompts/, Recapitulaciones/, backup notebooks). docs/10_model_optimization/phase10_acceptance.md
lo redacta Opus después, no Codex.

# 6. Protocolo de notebook (obligatorio)
El notebook 10_phase10_model_optimization.ipynb debe:
- título, scope y non-actions explícitas;
- imports limpios; PROJECT_SEED=42; experiment_id/run_id; paths relativos centralizados;
- cargar F2 de archivos oficiales + fold file congelado (asertar integridad) + baselines
  OOF M0/M1/CatBoost persistidos;
- P10-B1 diagnosis pre-HPO (B5 inestabilidad de slices CatBoost; B3 estabilidad del lead
  de M1) read-only sobre OOF existentes;
- HPO fold-safe por candidato: TODO preprocessing aprendido se fitea dentro del training
  fold en CADA trial; Optuna TPE sampler con seed fija; direction="maximize"; objetivo OOF
  ROC-AUC; secuencial-antes-de-paralelo; study persistido; pruning solo si métricas
  intermedias son significativas;
- extraer probas de clase positiva SOLO tras verificar estimator.classes_ contiene label 1;
- generar OOF (Id,fold,y_true,y_pred_proba, 2781 filas) solo de folds de validación;
- métricas global/fold/slice; top-k/quantile y score-distribution diagnósticas (con
  baselines mostrados);
- comparación tuned-vs-default y vs M0/M1/CatBoost por deltas pareados por fold + signos +
  umbral heredado 0.005436 (estructura, no regla final); confirmación repeated-CV (semillas
  de splitter distintas, análisis secundario etiquetado) sobre el ganador tuneado;
- escritura de artifacts versionados; commit hash + entorno (Python/numpy/pandas/sklearn,
  y GBDT si aplica) registrados;
- resumen ejecutivo + warnings.
Cada bloque de código mayor precedido por Markdown:
  ## <n>. <título>  /  **Objective. Inputs. Method. Expected output. Risk controlled.**
Cada celda de código inicia con comentario (p.ej. # 4.2 Validate frozen fold assignments).
Tras resultados relevantes, Markdown ### Interpretation con Main result / Methodological
reading / Risk or warning / Diagnostic decision.

# 7. Jerarquía de métricas
ROC-AUC primaria (métrica oficial, sobre probas de clase positiva Drafted=1). PR-AUC,
neg-AP, precision@k/recall@k/lift@k, top-decile/quintile capture, cumulative gains,
enrichment por cuantil, Brier, score-distribution, deltas por fold, slice ROC-AUC con
min-n, rank correlation/disagreement = DIAGNÓSTICAS, nunca reglas de selección. Threshold
tuning prohibido (irrelevante para ranking AUC). Calibración no se fitea. Conflictos
ROC-vs-auxiliar o global-vs-slice se REPORTAN como warning, no se ocultan.

# 8. Controles de leakage / overfitting / selection bias
- todo transform aprendido fold-fitted dentro de CV (incluido cada trial de HPO);
- test solo para checks estructurales; sin inferencia/submission en Phase 10;
- sin School como feature (assert); sin datos externos; sin leaderboard;
- search space pre-registrado; NO ampliar tras ver resultados;
- M0 sin tunear; XGB/LGBM sin deep HPO salvo justificación escrita + presupuesto mínimo;
- candidate log separado; sin tocar el main log (read-before, assert byte-identical-after);
- check-and-fail en rutas; sin sobrescrituras sin run_id;
- reportar nº de variantes comparadas (multiplicidad); slices solo como guardas.

# 9. Slices y estabilidad
Min-n n>=50 descriptivo; flag frágil si positivos/negativos escasos. Vigilar
Age_missing=1 (8 positivos, frágil), Position=QB (n=162, robusto), Year (2009/2011/2017),
available_measurement_count/completeness, Player_Type/Position_Type/Position con n
suficiente, frequent_vs_rare_school_group (diagnóstico, nunca feature). Slices pequeños no
promueven ni rechazan modelos por sí solos; degradación en slice robusto puede bloquear
promoción. Slices NO son objetivos de HPO.

# 10. Candidate log (no el main log)
Escribir solo outputs/reports/phase10_model_optimization_<run_id>_experiment_log_candidate.csv
con campos: experiment_id, run_id, candidate_family, variant_id, base_candidate,
features_used, School_used_as_feature=False, external_data_used=False, leaderboard_used=False,
hpo_strategy, hpo_budget_mode, hpo_trials_or_configs, cv_protocol, fold_sha, primary_metric,
oof_auc, delta_vs_m0, delta_vs_m1, delta_vs_current_candidate_baseline_if_applicable,
fold_mean_auc, fold_std_auc, same_sign_positive_folds_vs_m1, slice_guard_status,
leakage_checks_passed, selection_bias_warning_status, artifacts_manifest_path,
validation_report_path, notes.

# 11. Git policy
Nunca git add . / git commit -a / commit / push. No stagear. Terminar con bloque de
verificación: git status --short; git diff --check; git diff --name-only de forbidden paths;
git diff -- logs/experiment_log.csv. Reportar archivos creados, estado git, si diff --check
pasó, si forbidden paths cambiaron, si el main log quedó intacto, blockers y warnings.

# 12. Stop rules
Detente y reporta si: HEAD != hash autorizado; gate 5 sin resolver; fold SHA no coincide;
classes_ sin label 1; falta un doc predecesor; se pediría submission o abrir Phase 11; se
intentaría School/datos externos/leaderboard; el search space cambiaría tras ver
resultados; se declararía un winner. Stop = detente, reporta, espera al director.

# 13. Al terminar (NO acceptance)
Reporta: artifacts creados; integridad de folds/OOF; M0 anchor (≤1e-9); resumen
tuned-vs-default por candidato (sin elegir winner); warnings de slice/selection-bias; git
status; y la frase literal:
"Phase 10 execution complete. No final winner selected, no submission authorized.
 Candidates remain phase-gated. Awaiting independent recomputation and Opus strategic
 review. Phase 11 remains locked."
La aceptación la redacta Opus después (Deliverable D) y la firma el director.

================================= END PROMPT =================================
```

**Operator reminder:** this prompt is inert until a signed Phase 10 Project Authorization Note exists. Codex is a reproducible executor — it implements only the authorized scope, never converts a recommendation into an unapproved action, never declares a winner, never submits, never opens Phase 11. Independent recomputation and the Opus strategic review (Deliverable D) follow before any acceptance.
