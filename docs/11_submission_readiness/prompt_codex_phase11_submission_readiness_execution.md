# Prompt — Codex Phase 11 Submission Readiness Execution (Final Refit, Test Inference, Validated Submission)

```text
DO NOT RUN UNTIL THE PROJECT DIRECTOR HAS SIGNED A PHASE 11 PROJECT AUTHORIZATION NOTE.
This prompt is INERT until that note exists. The note fixes the authorized hash, the final
candidate decision (CatBoost tuned primary / M1 baseline fallback / both / block), the
CatBoost Stability Gate decision (audit passed OR written waiver), and the per-file
submission authorization. Without it, do nothing.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT (Deliverable C). This is the **second brain** in the Opus → Codex → Opus separation: a reproducible executor, not a strategist. It executes only what the signed authorization note allows.
**Governing documents:** `phase11_master_planning_brief.md`, `phase11_operator_runbook.md`. On any conflict, the stricter rule and `CLAUDE.md` / `AGENTS.md` / `project_execution_plan_v3.md` (§14, §16.7) / `submission_checklist.md` win.

---

The text between the markers is the prompt to run as the Phase 11 executor (Codex), **after** the signed authorization note.

```text
================================ BEGIN PROMPT ================================

Actúa como ejecutor reproducible de ML para el proyecto Reto Tokio / GCI World NFL Draft
Prediction (repo local: C:\GitHub\reto_Tokio). Eres ejecutor, no estratega: implementas
EXACTAMENTE lo autorizado, sin convertir recomendaciones en acciones nuevas. Esta fase
hace final refit sobre full train, inferencia sobre test y una submission validada — NO
sube nada y NO declara winner.

# 0. Precondición absoluta
Existe una Phase 11 Project Authorization Note FIRMADA que define: hash autorizado; la
decisión de candidato (CatBoost tuned primario / M1 baseline fallback / ambos / block); la
decisión del CatBoost Stability Gate (audit repeated-CV aprobado O waiver escrito que
reconoce mejores OOF global pero warnings de slice y sin repeated-CV); y la autorización
del/los archivo(s) de submission específicos. Si la nota no existe o algún punto no está
resuelto, DETENTE y reporta. No ejecutas nada sin la nota.

NO subes a ningún leaderboard. NO usas leaderboard para seleccionar. NO declaras final
winner ni submission-ready model. NO reabres HPO. NO reabres XGBoost/LightGBM. NO usas M1
tuned (rechazado). NO ensembles/blending/stacking. NO calibración. NO threshold tuning. NO
features nuevas. NO School como feature. NO datos externos. NO editas predicciones a mano.
NO modificas logs/experiment_log.csv, data/input/, notebooks/_official/, references/, .venv,
requirements.txt, lockfiles, .vscode/settings.json, Libros/, Prompts/, Recapitulaciones/.
NO stagear/commit/push. NO git add . NO git commit -a. Generación y verificación están
separadas: NO audites tu propia corrida como aceptación; eso lo hace Opus después.

# 1. Estado inicial requerido (read-only)
git rev-parse --short HEAD            # == hash autorizado en la nota (esperado de11fae o sucesor documentado)
git status --short                    # sin staged; solo untracked conocidos
git diff --check                      # limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json   # vacío
git diff -- logs/experiment_log.csv   # vacío
find outputs/submissions -maxdepth 2 -type f   # solo submission_001_baseline.csv (preexistente)
Confirma presentes y aceptados: docs/10_model_optimization/phase10_acceptance.md y los
artifacts phase10_standard_20260619_0152_* (validation_report, selection_bias_warning_report,
model_summary, slice_report, hpo_results, los 2 OOF tuned); validation_protocol_phase6.md;
leakage_checklist_phase6.md; submission_checklist.md; challenge_brief.md; los oficiales
data/input/{train,test,sample_submission}.csv (2781/696/696, columnas Id,Drafted); el fold
file congelado (SHA256[:16] = 96937649526bcadb, solo lineage). Si falta algo o un gate sin
resolver, DETENTE.

# 2. Documentos a leer (read-only)
phase11_master_planning_brief.md (candidatos §11, decisión §12, stability gate §13, fallback
§14, contrato F2 §15, refit §16, inferencia §17, validación §18, LB/upload §19, notebook
§20, artifacts §21, candidate log §22, stop rules §24), el runbook, y como contexto:
phase10_acceptance.md, phase10 validation/selection-bias reports, phase9a_acceptance + backlog,
phase8/phase8_wave2 acceptances, validation/leakage protocols, submission_checklist.md,
challenge_brief.md.

# 3. Alcance autorizado (exacto)
Feature set: SOLO F2 (13 base + 7 missing flags + available_measurement_count = 21 features).
Sin features nuevas. School excluida (assert raise-on-violation). available_measurement_count
y los *_missing recomputados row-wise/deterministas. Imputación mediana + one-hot fold-safe,
PERO en Phase 11 el "fit" del preprocessing es sobre FULL TRAIN (no folds), aplicado a test.
Candidato final segun la nota:
  - CatBoost tuned = PRIMARIO si la nota lo autoriza y el Stability Gate pasó/waiver.
    Hiperparámetros recuperados de hpo_results.csv: depth=6, learning_rate=0.01,
    l2_leaf_reg=9, iterations=800, border_count=128, random_seed=42, cat_features=[].
    Entorno Wave 2 SEPARADO (catboost 1.2.10), sin tocar .venv. Sin HPO, sin early stopping
    basado en test.
  - M1 baseline = FALLBACK. Configuración recuperada de los artifacts aceptados de Phase 8/9A
    (NO inventar C/penalty/solver/scaling; recuperarlos del notebook 10 / artifacts). NUNCA
    usar M1 tuned.
  - Si la nota pide AMBOS (Option C), generar dos submissions validadas por separado, sin
    elegir winner; el director decide el orden de subida.
Folds: el fold file congelado es solo lineage. El refit final NO usa folds; usa full train.
La SELECCIÓN ya está decidida por la nota (evidencia OOF de Phase 10), no por test ni LB.

# 4. Rutas permitidas (escritura)
notebooks/11_phase11_submission_readiness.ipynb
outputs/validation/phase11_submission_readiness_<run_id>_candidate_selection_report.csv
outputs/validation/phase11_submission_readiness_<run_id>_final_refit_report.csv
outputs/validation/phase11_submission_readiness_<run_id>_submission_validation.csv
outputs/validation/phase11_submission_readiness_<run_id>_model_summary.csv
outputs/reports/phase11_submission_readiness_<run_id>_validation_report.md
outputs/reports/phase11_submission_readiness_<run_id>_artifact_manifest.csv
outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv
outputs/submissions/phase11_submission_readiness_<run_id>_<candidate>_submission.csv
experiment_id = phase11_submission_readiness_v<K>; run_id obligatorio; check-and-fail si la
ruta existe (nunca sobrescribir). Rutas con forward slashes. La submission CSV está
gitignored (outputs/submissions/*.csv): su SHA-256 en el manifest/reporte es su única
identidad durable.

# 5. Rutas prohibidas
logs/experiment_log.csv, data/input/, notebooks/_official/, references/, .venv,
requirements.txt, lockfiles, .vscode/settings.json, Libros/, Prompts/, Recapitulaciones/,
backup notebooks. docs/11_submission_readiness/phase11_acceptance.md lo redacta Opus
después, no Codex. No crear más de la(s) submission(s) autorizada(s) por la nota.

# 6. Protocolo de notebook (obligatorio)
El notebook 11_phase11_submission_readiness.ipynb debe:
- título, scope y non-actions explícitas;
- imports limpios; PROJECT_SEED; experiment_id/run_id; paths relativos centralizados;
- validar hash autorizado; cargar SOLO data oficial + artifacts aceptados de Phase 10;
- P11-B0 gate check; P11-B1 candidate selection gate (registrar candidato + deltas OOF de
  Phase 10, sin LB); P11-B2 CatBoost stability gate (verificar audit aprobado o waiver de la
  nota; si CatBoost no autorizado, usar fallback o detener);
- P11-B3 construir F2 para full train y test de forma idéntica; assert School ausente;
  recomputar *_missing y available_measurement_count row-wise;
- P11-B4 fit del preprocessing (imputación/one-hot/scaling si M1) SOLO sobre full train;
  fit del modelo seleccionado SOLO sobre full train (sin HPO); seeds fijas;
- verificar estimator.classes_ contiene label 1 ANTES de extraer probas;
- P11-B5 inferencia sobre test: transform-only con preprocessing de train; probas de
  Drafted=1; validar shape (696) y rango [0,1]; sin acceso a target; sin edición manual;
- P11-B6 construir submission (Id, Drafted) alineada al orden de sample_submission.csv;
  correr la suite de validación §7; escribir submission solo si TODAS pasan;
- P11-B7 escribir artifacts versionados; hash SHA-256 de la submission; manifest; reporte;
  candidate log; registrar commit hash + entorno (Python/numpy/pandas/sklearn; catboost si
  aplica);
- resumen ejecutivo + warnings (incl. Age_missing=1 frágil, QB, Year 2011, avail_count 0).
Cada bloque de código mayor precedido por Markdown:
  ## <n>. <título>  /  **Objective. Inputs. Method. Expected output. Risk controlled.**
Cada celda de código inicia con comentario (p.ej. # 5.2 Validate official sample submission alignment).
Tras resultados relevantes, Markdown ### Interpretation con Main result / Methodological
reading / Risk or warning / Decision.

# 7. Suite de validación de submission (obligatoria, stop on fail)
- columnas exactamente Id, Drafted;
- row count == 696; coincide con test.csv y sample_submission.csv;
- Id set == set oficial de test/sample;
- Id order == sample_submission.csv (= test.csv);
- Drafted numérico; todo en [0,1]; sin NaN; sin inf;
- sin Id duplicado (696 únicos);
- sin edición manual (generada por código; regenerar y comparar / hash);
- SHA-256 registrado en manifest y reporte;
- reporte identifica modelo, commit hash, run_id y feature set (F2);
- NO subida automática.

# 8. Jerarquía de métricas y dirección de probabilidad
La métrica oficial es ROC-AUC sobre probas de clase positiva Drafted=1. En Phase 11 NO se
recalcula AUC de test (no hay labels de test). La validación es de formato/lineage, no de
score. Extraer SIEMPRE la columna de predict_proba correspondiente a label 1 tras verificar
estimator.classes_. Threshold tuning prohibido (AUC es threshold-free). Calibración no se
fitea.

# 9. Controles de leakage / overfitting / submission-risk
- todo transform aprendido fitea SOLO sobre full train; test solo se transforma;
- test nunca se usa para fit/selección; sin labels de test; sin datos externos; sin LB;
- sin School como feature (assert); F2 exacto (assert column-set);
- candidato ya seleccionado por la nota (OOF), no por test ni LB;
- sin edición manual de predicciones; generación 100% por código;
- check-and-fail en rutas; sin sobrescrituras sin run_id;
- main log read-before / assert byte-identical-after;
- registrar nº de submissions generadas (1 o 2 si Option C); sin loop de subida.

# 10. Controles de leaderboard y upload
NO subes. NO usas LB para seleccionar. La subida es manual y del director. Si se generan dos
submissions válidas, el director decide el orden (último archivo subido = ranking final). No
reordenas por el usuario. No afirmas que hubo subida.

# 11. Candidate log (no el main log)
Escribir solo outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv
con campos: experiment_id, run_id, authorized_commit, phase10_acceptance_commit,
candidate_family, candidate_variant, final_refit_candidate, fallback_candidate, features_used,
School_used_as_feature=False, external_data_used=False, leaderboard_used_for_selection=False,
submission_created, submission_uploaded=False, model_hyperparameters_source, feature_contract,
preprocessing_contract, train_rows, test_rows, submission_rows, submission_path,
submission_sha256, artifact_manifest_path, validation_report_path, submission_validation_status,
manual_edit_detected=False, notes.

# 12. Git policy
Nunca git add . / git commit -a / commit / push. No stagear. Terminar con bloque de
verificación: git status --short; git diff --check; git diff --name-only de forbidden paths;
git diff -- logs/experiment_log.csv; find outputs/submissions. Reportar archivos creados,
estado git, si diff --check pasó, si forbidden paths cambiaron, si el main log quedó intacto,
blockers y warnings.

# 13. Stop rules
Detente y reporta si: HEAD != hash autorizado; gate de candidato sin resolver; CatBoost
requerido pero stability gate ni pasó ni tiene waiver; falta un doc predecesor o el sample
submission; se violaría el contrato F2 (feature nueva/School); datos externos; HPO; test
usado para fit; classes_ sin label 1; row count/Id set/Id order no verificables;
NaN/inf/fuera de rango en predicciones; edición manual detectada; LB usado para selección;
cualquier intento de subida automática; se declararía un winner. Stop = detente, reporta,
espera al director.

# 14. Al terminar (NO acceptance)
Reporta: candidato(s) refiteado(s) y fuente de hiperparámetros; integridad de F2 y exclusión
de School; resultado de la suite de validación de submission; SHA-256 de la(s) submission(s);
artifacts creados; warnings de slice (Age_missing=1, QB, Year 2011, avail_count 0); git
status; y la frase literal:
"Phase 11 execution complete. Submission generated and validated, not uploaded. No final
 winner declared. Awaiting independent Opus submission review and project-director acceptance.
 Leaderboard not used for selection."
La aceptación la redacta Opus después (Deliverable D) y la firma el director. La subida la
hace el director manualmente.

================================= END PROMPT =================================
```

**Operator reminder:** this prompt is inert until a signed Phase 11 Project Authorization Note exists. Codex is a reproducible executor — it implements only the authorized scope, never converts a recommendation into an unapproved action, never uploads, never uses the leaderboard for selection, never declares a winner, never reopens HPO/XGBoost/LightGBM, and never edits predictions by hand. Independent Opus review (Deliverable D) and director acceptance follow; the director performs any upload manually.
