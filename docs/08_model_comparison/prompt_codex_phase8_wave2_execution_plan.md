# Prompt — Codex Phase 8 Wave 2 Execution Plan (External GBDTs)

```text
DO NOT EXECUTE UNTIL EXPLICIT PROJECT DIRECTOR APPROVAL.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT. **Inert until the operator attaches a Project Authorization Note** ("PHASE 8 WAVE 2 EXECUTION AUTHORIZATION", runbook §12). Without that note, no part of this prompt may be acted on.
**Scope:** Phase 8 Wave 2 — external GBDTs (XGBoost, LightGBM; CatBoost only if Sub-wave 2B is authorized). This prompt does NOT authorize HPO, submissions, ensembles, leaderboard use, deep tabular models, or any future phase.
**Governing documents:** `docs/08_model_comparison/phase8_wave2_master_planning_brief.md` (the plan), `docs/08_model_comparison/phase8_wave2_operator_runbook.md` (the procedure).

---

## Notebook Architecture Fidelity Contract

Codex must implement only the notebook/script architecture approved in `phase8_wave2_master_planning_brief.md`. Codex must not redesign the wave, change the model registry, add models, tune hyperparameters, alter the feature set, alter folds, alter artifacts, generate submissions, install packages, create environments, or open future phases unless the project director explicitly authorizes those actions. If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project director approval before proceeding.

---

The text between the markers below is the prompt to give the executor (Codex or equivalent), verbatim, together with the Project Authorization Note.

```text
================================ BEGIN PROMPT ================================

Actúa como ingeniera ML senior de ejecución, bajo auditoría estricta de leakage,
validación, reproducibilidad y seguridad de entorno, para el proyecto Reto Tokio /
GCI World NFL Draft Prediction (repo local: C:\GitHub\reto_Tokio).

# 0. Precondición absoluta

Esta corrida es válida SOLO si está adjunta una Project Authorization Note
"PHASE 8 WAVE 2 EXECUTION AUTHORIZATION" (formato: runbook §12) firmada por el
usuario/director del proyecto, que incluye: el hash de commit autorizado; la
estrategia de entorno (dependency check read-only; y por separado, entorno Wave 2
separado con versiones GBDT pinneadas; SIN modificar .venv/requirements); el
registry ratificado; la decisión sobre Sub-wave 2B (CatBoost). Si la nota no está
adjunta, detente y no hagas nada.

# 1. Rol y misión

Implementar y ejecutar EXACTAMENTE la comparación de GBDTs externos Wave 2
pre-registrada en docs/08_model_comparison/phase8_wave2_master_planning_brief.md
(§8 registry, §9 CatBoost double-gate, §11 protocolo, §12 blueprint celda por celda),
sobre los folds congelados, con el feature set F2 congelado, comparando contra los
comparadores m0 y m1 CARGADOS desde sus OOF persistidos de Wave 1 (NO reentrenados),
y produciendo los artifacts de §12.8. Nada más. No eres diseñadora: el diseño está
congelado; eres ejecutora auditada. Wave 2 NO corona un ganador: produce una tabla
de evidencia clasificada; la selección de candidatos es decisión posterior del
usuario/director del proyecto.

# 2. Estado esperado (verifica antes de cualquier cómputo)

git rev-parse --short HEAD        -> debe ser igual al hash de la Project Authorization Note
git status --short                -> sin staged; sin modificaciones tracked
git diff --check                  -> limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json -> vacío
git ls-files docs/08_model_comparison/*wave2*.md -> los tres docs Wave 2 tracked
.venv y requirements              -> NO modificados (verifica byte-idénticos)
artifacts phase8_wave2_*          -> NO debe existir ninguno (si existe: posible doble ejecución; detente)

Entorno de ejecución de 08c (entorno SEPARADO Wave 2, NO .venv):
python -c "import sys,sklearn,pandas,numpy; print(sys.version.split()[0], sklearn.__version__, pandas.__version__, numpy.__version__)"
  -> 3.13.13 / 1.9.0 / 3.0.3 / 2.4.6  (espejo del stack pineado)
python -c "import xgboost,lightgbm; print(xgboost.__version__, lightgbm.__version__)"  -> versiones pinneadas
import catboost -> SOLO si Sub-wave 2B autorizado

Si cualquier verificación falla: reporta, clasifica severidad y DETENTE.

# 3. Archivos que debes revisar antes de implementar (read-only)

- docs/08_model_comparison/phase8_wave2_master_planning_brief.md  (§8 registry, §9 gate, §11 protocolo, §12 blueprint, §14 criterios, §15 leakage)
- docs/08_model_comparison/phase8_acceptance.md                   (Wave 1 cierre; m0/m1 clasificaciones)
- docs/05_methodology/leakage_checklist_phase6.md
- docs/05_methodology/validation_protocol_phase6.md
- notebooks/08_phase8_model_family_comparison.ipynb               (solo lectura: reutiliza sus builders F2 fold-safe auditados)
- outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv
- outputs/oof/phase8_model_family_comparison_v1_m0_random_forest_frozen_oof_predictions.csv   (comparador m0, NO reentrenar)
- outputs/oof/phase8_model_family_comparison_v1_m1_logistic_regression_oof_predictions.csv    (comparador m1, NO reentrenar)

# 4. Alcance autorizado (futuro, tras la nota)

Crear y ejecutar DOS notebooks:
  notebooks/08b_phase8_wave2_dependency_environment_check.ipynb   (read-only; NO instala; NO entrena)
  notebooks/08c_phase8_wave2_external_gbdt_comparison.ipynb       (entorno SEPARADO; experiment_id = phase8_wave2_external_gbdt_v1)

Escribir SOLO estos artifacts (con pre-write guards fail-if-exists):
  outputs/oof/phase8_wave2_external_gbdt_v1_<model_key>_oof_predictions.csv   (uno por GBDT entrenado)
  outputs/validation/phase8_wave2_external_gbdt_v1_model_summary.csv
  outputs/validation/phase8_wave2_external_gbdt_v1_fold_metrics.csv
  outputs/validation/phase8_wave2_external_gbdt_v1_slice_report.csv
  outputs/validation/phase8_wave2_external_gbdt_v1_dependency_report.csv
  outputs/reports/phase8_wave2_external_gbdt_v1_validation_report.md
  outputs/reports/phase8_wave2_external_gbdt_v1_experiment_log_candidate.csv
  outputs/reports/phase8_wave2_external_gbdt_v1_artifact_manifest.csv
  outputs/reports/phase8_wave2_external_gbdt_v1_environment_report.md

# 5. Estrategia de entorno y dependencias (crítico)

- .venv: NO instalar, NO modificar, NO mutar. requirements/lockfiles: NO editar.
- 08b es READ-ONLY: registra Python/OS, versiones del stack, y disponibilidad de
  xgboost/lightgbm/catboost. NO instala nada. NO entrena nada.
- La instalación (si la nota la autoriza) ocurre SOLO en un entorno SEPARADO Wave 2
  que espeja sklearn 1.9.0 / pandas 3.0.3 / numpy 2.4.6 y agrega versiones GBDT
  pinneadas. 08c se ejecuta en ese entorno separado.
- Comparadores m0/m1: cargados desde OOF persistido de Wave 1, NUNCA reentrenados.

# 6. Rutas (lectura según se indica; escritura solo en el alcance del punto 4)

- data/input/: LECTURA PERMITIDA solo de los CSVs oficiales. ESCRITURA PROHIBIDA.
- logs/experiment_log.csv: LECTURA PERMITIDA (leer antes; assert byte-idéntico al final). ESCRITURA PROHIBIDA.
- notebooks/_official/, references/, outputs/submissions/, .vscode/settings.json,
  Libros/, Prompts/, Recapitulaciones/: lectura y escritura PROHIBIDAS.
- Artifacts existentes de Wave 1 (notebook 08, outputs phase8_model_family_comparison_v1_*,
  docs/08_model_comparison/phase8_acceptance.md): SOLO LECTURA. No modificar.

No git add. No git add . No git commit. No git commit -a. No push. No staging.
No pip install en .venv. No conda. No mutación del entorno pineado.

# 7. Diseño congelado (no modificable en esta corrida)

Folds: cargar outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv y
asertar: 2781 filas; labels 0..4; orden de Id igual a train; sha256[:16] ==
96937649526bcadb. NUNCA recomputar folds.

Anchor M0: cargar el OOF persistido de m0 y verificar OOF AUC ==
0.8116502602456482 (± 1e-9). Si no coincide, DETENTE (deriva de baseline).

Feature set F2 (21 features, congelado; reutiliza los builders del notebook 08):
  Base (13): Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump,
  Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type,
  Position_Type, Position.
  Flags (7): Age_missing, Sprint_40yd_missing, Vertical_Jump_missing,
  Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing, Shuttle_missing.
  Count (1): available_measurement_count (0-6).
Excluidos siempre (assert): Id, Drafted, School.
Asserts de sanidad: suma de flags == conteos conocidos de train
(Age 435; Sprint 145; Vertical 554; Bench 721; Broad 581; Agility 970; Shuttle 912).

Registry Wave 2 (cap duro: <= 3 GBDTs entrenados; ninguno adicional sin nueva nota):
  xgboost   XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1, subsample=1.0,
                          colsample_bytree=1.0, reg_lambda=1.0, random_state=42, n_jobs=1,
                          tree_method="hist", eval_metric="logloss")   # SIN eval_set, SIN early stopping
  lightgbm  LGBMClassifier(n_estimators=300, num_leaves=31, learning_rate=0.1, subsample=1.0,
                          colsample_bytree=1.0, reg_lambda=1.0, random_state=42, n_jobs=1,
                          deterministic=True, force_col_wise=True, verbose=-1)   # categorical_feature SIN usar
  catboost  (GATED, Sub-wave 2B) CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1,
                          random_seed=42, thread_count=1, cat_features=[], verbose=0,
                          allow_writing_files=False)   # SOLO si 2B autorizado + School reconfirmado
Comparadores (NO entrenar): m0_random_forest_frozen, m1_logistic_regression (cargados de OOF Wave 1).
Cambiar cualquier hiperparámetro, probar valores, agregar eval_set/early stopping = HPO = PROHIBIDO.
Si un GBDT no importa, no converge o falla: regístralo como failed_run, NO lo
sustituyas, continúa con el resto del registry y repórtalo.

CatBoost double-gate (§9): ejecutar SOLO si (1) Gate 1 Wave 2 autorizado;
(2) Gate 2 Sub-wave 2B autorizado explícitamente; (3) School-exclusion reconfirmada
en la nota; (4) cat_features == [] (assert). Si algún gate falla, OMITE CatBoost;
XGBoost + LightGBM siguen siendo un Wave 2 completo.

Preprocessing compartido (reutiliza el builder F2 del notebook 08):
SimpleImputer(median) numérico + (most_frequent + OneHotEncoder
handle_unknown="ignore") categórico, dentro de ColumnTransformer+Pipeline,
fit SOLO en la máscara de entrenamiento de cada fold. TODOS los GBDTs reciben la
MISMA matriz numérica codificada. Sin native categorical (LightGBM categorical_feature
sin usar; CatBoost cat_features=[]). Sin tuning, sin target encoding, sin external data.

# 8. Checks de validación obligatorios

- ROC-AUC con probabilidades de la clase positiva Drafted=1, extraídas SOLO tras
  verificar estimator.classes_ (label 1 exactamente una vez); nunca [:, 1] a ciegas.
- OOF por GBDT: 2781 filas, columnas Id,fold,y_true,y_pred_proba; proba finita en
  [0,1]; sin NaN; ningún fold mono-clase; fold de OOF == fold congelado.
- fold_metrics: AUC por fold por GBDT (5 filas por modelo).
- Deltas pareados por fold vs m0 (regla principal) Y vs m1 (lectura informativa);
  conteo same-sign para ambos.
- Regla de evidencia pre-registrada (flag, NO adopción): "promotable_evidence" solo
  si OOF(GBDT)-OOF(m0) >= 0.005436 Y delta positivo en >= 4/5 folds vs m0 Y slice
  guard limpio. Clasifica: promotable_evidence / no_qualifying_evidence / escalated /
  failed_run. PROHIBIDO lenguaje de "ganador" o "modelo seleccionado".
- Slices obligatorios por GBDT: Player_Type, Position_Type, Year, Age_missing,
  available_measurement_count, measurement_completeness_group,
  frequent_vs_rare_school_group (School SOLO diagnóstico, jamás feature).
  n < 50 => no evaluable (flag). Caída > 0.02 AUC vs m0 en slice obligatorio con
  n >= 50 => escalated (revisión del usuario/director), nunca auto-decidir.
- Age_missing=1 (n=435, 8 positivos): registra explícitamente el AUC de cada GBDT
  frente a M0 (0.6917447306791569) y m1 (0.5442037470725996). Slice frágil conocido.

# 9. Checks de leakage obligatorios (instancia por GBDT)

- Ningún fitting fuera del fold de entrenamiento; ningún fitting con test.
- Test usado SOLO para checks de contrato; en Wave 2 no hay inferencia ni submission.
- Sin target encoding (CatBoost cat_features=[]); sin feature selection; sin reducción
  de dimensionalidad; sin rare grouping; sin estadísticas de rol aprendidas; sin
  leaderboard; sin datos externos; sin School en ninguna matriz; sin native categorical.
- .venv / requirements byte-idénticos. logs/experiment_log.csv leer antes, assert idéntico después.
- Variables diagnósticas fuera de toda matriz de features (assert).

# 10. Política de artifacts y reporte

- Pre-write guards en todos los paths; jamás sobrescribir; colisión => DETENTE.
- Manifest: una fila por artifact escrito (path, sha256, filas).
- dependency_report (08b) + environment_report: versiones exactas de Python/stack/GBDTs.
- Reporte (validation_report.md): entorno (versiones + git hash + dirty), gates de
  integridad (folds, M0 anchor, F2), tabla registry, tabla de GBDTs con clasificación
  por regla, fold-by-fold, deltas pareados vs m0 y vs m1, slice report por GBDT con
  Age_missing=1 destacado, checklist de leakage por GBDT, registro del CatBoost gate
  (si corrió), limitación documentada del umbral (ruido de seed de RF), lenguaje de
  asociación (no causal), y la declaración explícita de que Wave 2 no corona ganador.
- Candidate log: filas v2 bajo outputs/reports/. El log principal NO se toca.

# 11. Stop rules (detente y reporta; no improvises)

HEAD distinto; staged inesperado; artifact phase8_wave2_* preexistente; instalación
en .venv o edición de requirements; fallo de integridad de folds; M0 anchor fuera de
tolerancia; proba inválida; classes_ sin label 1 único; colisión de artifacts;
CatBoost sin gate 2B o con cat_features no vacío; cualquier duda de fit-scope;
cualquier presión por añadir modelos/configs/parámetros/eval_set; main log alterado;
entorno distinto al espejo pineado; import GBDT resolviendo contra .venv; slice-guard
disparado (escalated: registra y continúa el resto, decisión del director); cualquier
acción que requiera HPO, submission, ensemble, leaderboard, datos externos,
instalación adicional, o Phase 9/10/11.

# 12. Prohibiciones absolutas

NO instalar en .venv. NO modificar requirements/entorno pineado. NO HPO (ni informal:
probar valores o eval_set = HPO). NO submissions. NO ensembles. NO stacking. NO deep
tabular. NO Phase 9/10/11. NO leaderboard. NO datos externos. NO School como feature.
NO CatBoost native categorical. NO modificar artifacts de Wave 1. NO modificar rutas
prohibidas. NO commits ni staging. NO ejecutar nada sin la Project Authorization Note.
NO crear phase8_wave2_acceptance.md (paso posterior del usuario/director).

# 13. Al terminar

1) Ejecuta y reporta: git status --short; git diff --check; diff de rutas prohibidas
   (deben estar limpias; solo artifacts nuevos untracked); confirma .venv/requirements
   byte-idénticos.
2) Entrega: resumen ejecutivo, tabla de GBDTs clasificada por la regla
   (promotable_evidence / no_qualifying_evidence / escalated / failed_run), deltas vs
   m0 y vs m1, slice findings (con Age_missing=1 destacado), registro del CatBoost gate,
   environment/dependency record, warnings, y la frase literal:
   "Phase 8 Wave 2 execution complete; candidate selection, acceptance and commit
    remain gated on explicit project director authorization. Phase 9, Phase 10 and
    Phase 11 remain locked."
3) Prepara (en el resumen del punto 2, no como archivo nuevo) la evidencia que el
   usuario/director necesitará para redactar phase8_wave2_acceptance.md. No crees
   phase8_wave2_acceptance.md salvo autorización separada.

================================= END PROMPT =================================
```

**Operator reminder:** attach the Project Authorization Note (runbook §12) with the authorized hash, the environment decision, the ratified registry, and the CatBoost (2B) decision filled in, or this prompt must be refused by any executor that receives it. The dependency install (separate env) is itself a gated decision; if the note authorizes only the read-only dependency check, the executor must stop after `08b`.
