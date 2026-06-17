# Prompt — Codex Phase 8 Execution Plan

```text
DO NOT EXECUTE UNTIL EXPLICIT PROJECT DIRECTOR APPROVAL.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT. **Inert until the operator attaches a Project Authorization Note** (runbook §10, "PHASE 8 WAVE 1 EXECUTION AUTHORIZATION"). Without that note, no part of this prompt may be acted on.
**Scope:** Wave 1 only (sklearn-native families). Wave 2 (xgboost/lightgbm/catboost) is NOT covered by this prompt and requires a separate future note.
**Governing documents:** `docs/08_model_comparison/phase8_master_planning_brief.md` (the plan), `docs/08_model_comparison/phase8_operator_runbook.md` (the procedure).

---

## Notebook Architecture Fidelity Contract

Codex must implement only the notebook/script architecture approved in `phase8_master_planning_brief.md`. Codex must not redesign the phase, change the model registry, add models, tune hyperparameters, alter the feature set, alter folds, alter artifacts, generate submissions, or open future phases. If any part of the approved architecture is ambiguous, missing, infeasible, or unsafe, Codex must stop and request project director approval before proceeding.

---

The text between the markers below is the prompt to give the executor (Codex or equivalent), verbatim, together with the Project Authorization Note.

```text
================================ BEGIN PROMPT ================================

Actúa como ingeniero ML senior de ejecución, bajo auditoría estricta de leakage,
validación y reproducibilidad, para el proyecto Reto Tokio / GCI World NFL Draft
Prediction (repo local: C:\GitHub\reto_Tokio).

# 0. Precondición absoluta

Esta corrida es válida SOLO si está adjunta una Project Authorization Note
"PHASE 8 WAVE 1 EXECUTION AUTHORIZATION" (formato: runbook §10) firmada por el
usuario/director del proyecto, que incluye el hash de commit autorizado, el
registry ratificado, la decisión sobre m3 (incluir/excluir) y sobre m5
(autorizado/no autorizado). Si la nota no está adjunta, detente y no hagas nada.

# 1. Rol y misión

Implementar y ejecutar EXACTAMENTE la comparación de familias de modelos Wave 1
pre-registrada en docs/08_model_comparison/phase8_master_planning_brief.md
(§8 registry, §9 protocolo, §10 blueprint celda por celda), sobre los folds
congelados, con el feature set F2 congelado, y producir los artifacts de §10.7.
Nada más. No eres diseñador: el diseño está congelado; eres ejecutor auditado.
Phase 8 NO corona un ganador: produce una tabla de evidencia clasificada; la
selección de candidatos es decisión posterior del usuario/director del proyecto.

# 2. Estado esperado (verifica antes de cualquier cómputo)

git rev-parse --short HEAD        -> debe ser igual al hash de la Project Authorization Note
git status --short                -> sin staged; sin modificaciones tracked
git diff --check                  -> limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json -> vacío
git ls-files docs/08_model_comparison/*.md -> los tres docs de planificación tracked
.venv\Scripts\python.exe          -> Python 3.13.13; pandas 3.0.3; scikit-learn 1.9.0; numpy 2.4.6
imports xgboost/lightgbm/catboost -> DEBEN FALLAR (Wave 1 corre sin GBDTs externos; si alguno está instalado, repórtalo y detente)
artifacts phase8_*                -> NO debe existir ninguno bajo outputs/ ni notebooks/08* (si existe: posible doble ejecución; detente)

Si cualquier verificación falla: reporta, clasifica severidad y DETENTE.

# 3. Archivos que debes revisar antes de implementar (read-only)

- docs/08_model_comparison/phase8_master_planning_brief.md      (§8 registry, §9 protocolo, §10 blueprint, §12 criterios, §13 leakage)
- docs/07_feature_engineering/phase7_acceptance.md              (F2 adoptado; warnings Age_missing)
- docs/07_feature_engineering/phase7b_role_interaction_acceptance.md (F4 rechazado)
- docs/05_methodology/leakage_checklist_phase6.md
- docs/05_methodology/validation_protocol_phase6.md
- notebooks/07_phase7_missingness_availability_feature_block.ipynb   (solo lectura: reutiliza sus builders F2 fold-safe auditados)
- outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv
- outputs/oof/phase7_missingness_availability_v1_phase7_f2_median_flags_count_oof_predictions.csv  (referencia F2)

# 4. Alcance autorizado (futuro, tras la nota)

Crear y ejecutar UN notebook:
  notebooks/08_phase8_model_family_comparison.ipynb
  experiment_id = phase8_model_family_comparison_v1

Escribir SOLO estos artifacts (con pre-write guards fail-if-exists):
  outputs/oof/phase8_model_family_comparison_v1_<model_key>_oof_predictions.csv   (uno por modelo entrenado)
  outputs/validation/phase8_model_family_comparison_v1_model_summary.csv
  outputs/validation/phase8_model_family_comparison_v1_fold_metrics.csv
  outputs/validation/phase8_model_family_comparison_v1_slice_report.csv
  outputs/reports/phase8_model_family_comparison_v1_validation_report.md
  outputs/reports/phase8_model_family_comparison_v1_experiment_log_candidate.csv
  outputs/reports/phase8_model_family_comparison_v1_artifact_manifest.csv

# 5. Rutas (lectura según se indica; escritura solo en el alcance del punto 4)

- data/input/: LECTURA PERMITIDA solo de los CSVs oficiales (train.csv,
  test.csv, sample_submission.csv) para contract checks. ESCRITURA PROHIBIDA.
- logs/experiment_log.csv: LECTURA PERMITIDA (leer antes de empezar y assert
  byte-idéntico al final). ESCRITURA PROHIBIDA.
- notebooks/_official/: lectura y escritura PROHIBIDAS.
- references/: lectura y escritura PROHIBIDAS.
- outputs/submissions/: lectura y escritura PROHIBIDAS (Phase 8 no genera submissions).
- .vscode/settings.json: lectura y escritura PROHIBIDAS.
- Libros/, Prompts/, Recapitulaciones/: lectura y escritura PROHIBIDAS.

No git add. No git add . No git commit. No git commit -a. No push. No staging.
No pip install. No conda install. Ninguna mutación del entorno.

# 6. Diseño congelado (no modificable en esta corrida)

Folds: cargar outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv y
asertar: 2781 filas; labels 0..4; orden de Id igual a train; sha256[:16] ==
96937649526bcadb. NUNCA recomputar folds.

Feature set F2 (21 features, congelado; reutiliza los builders del notebook 07):
  Base (13): Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump,
  Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type,
  Position_Type, Position.
  Flags (7): Age_missing, Sprint_40yd_missing, Vertical_Jump_missing,
  Bench_Press_Reps_missing, Broad_Jump_missing, Agility_3cone_missing,
  Shuttle_missing.
  Count (1): available_measurement_count (0-6).
Excluidos siempre (assert): Id, Drafted, School.
Asserts de sanidad: suma de flags == conteos conocidos de train
(Age 435; Sprint 145; Vertical 554; Bench 721; Broad 581; Agility 970; Shuttle 912).
PROHIBIDO: feature engineering adicional, por modelo o global.

Registry Wave 1 (cap duro: <= 6 entrenados; ninguno adicional sin nueva nota):
  m0_random_forest_frozen    RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, n_jobs=-1)
                             GATE: OOF == 0.8116502602456482 +/- 1e-6, si no DETENTE
  m1_logistic_regression     LogisticRegression(max_iter=1000, random_state=42)
                             pipeline con StandardScaler fold-fitted en numéricas
  m2_random_forest_default   RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1)
  m3_extra_trees_default     ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1)
                             SOLO si la nota lo incluye
  m4_hist_gradient_boosting  HistGradientBoostingClassifier(random_state=42, early_stopping=False)
  m5_hgb_native_missing      (GATED) igual que m4 SIN imputación numérica (NaNs pasan al modelo);
                             SOLO si la nota lo autoriza explícitamente; diagnóstico
                             que rompe la equidad estricta: NUNCA decision-eligible por sí solo.
Cambiar cualquier hiperparámetro, probar valores, o agregar configs = HPO = PROHIBIDO.
Si un modelo falla o no converge: regístralo como failed_run, NO lo sustituyas,
continúa con el resto del registry y repórtalo.

Preprocessing compartido (reutiliza el builder F2 del notebook 07):
SimpleImputer(median) numérico + (most_frequent + OneHotEncoder
handle_unknown="ignore") categórico, dentro de ColumnTransformer+Pipeline,
fit SOLO en la máscara de entrenamiento de cada fold. m1 agrega StandardScaler
fold-fitted (requisito del modelo, pre-registrado). m5 omite la imputación
numérica (única excepción, gated). Ninguna otra desviación.

Referencia: cargar el OOF F2 persistido (no reentrenar el baseline); verificar
que su AUC recomputado == 0.8116502602456482.

# 7. Checks de validación obligatorios

- ROC-AUC con probabilidades de la clase positiva Drafted=1, extraídas SOLO tras
  verificar estimator.classes_ (label 1 exactamente una vez); nunca [:, 1] a ciegas.
- OOF por modelo: 2781 filas, columnas Id,fold,y_true,y_pred_proba; proba
  finita en [0,1]; sin NaN; ningún fold mono-clase; fold de OOF == fold congelado.
- fold_metrics: AUC por fold por modelo (5 filas por modelo).
- Deltas pareados por fold vs m0 para cada modelo; OOF como moneda principal.
- Regla de evidencia pre-registrada (flag, NO adopción): "promotable evidence"
  solo si OOF(modelo)-OOF(m0) >= 0.005436 Y delta positivo en >= 4/5 folds Y
  slice guard limpio. Clasifica cada modelo: promotable_evidence /
  no_qualifying_evidence / escalated / failed_run. PROHIBIDO lenguaje de
  "ganador" o "modelo seleccionado".
- Slices obligatorios por modelo: Player_Type, Position_Type, Year, Age_missing,
  available_measurement_count, measurement_completeness_group,
  frequent_vs_rare_school_group (School SOLO diagnóstico, jamás feature).
  n < 50 => no evaluable (flag). Caída > 0.02 AUC vs m0 en slice obligatorio con
  n >= 50 => escalated (revisión del usuario/director del proyecto), nunca auto-decidir.
  Atención especial a Age_missing=1 (n=435, 8 positivos: slice frágil conocido).

# 8. Checks de leakage obligatorios (instancia por modelo)

- Ningún fitting fuera del fold de entrenamiento; ningún fitting con test.
- Test usado SOLO para checks de contrato (shape/columnas/orden); en Phase 8 no
  hay inferencia final ni submission.
- Sin target encoding; sin feature selection; sin reducción de dimensionalidad;
  sin rare grouping; sin estadísticas de rol aprendidas (solo OHE de categóricas
  crudas); sin leaderboard; sin datos externos; sin School en ninguna matriz.
- Sin atajos específicos de librería: nada de manejo nativo de categóricas que
  toque School; m5 es la única desviación de preprocessing y está gated.
- logs/experiment_log.csv: leer antes, asertar byte-idéntico después.
- Variables diagnósticas fuera de toda matriz de features (assert).

# 9. Política de artifacts y reporte

- Pre-write guards en todos los paths; jamás sobrescribir; colisión => DETENTE.
- Manifest: una fila por artifact escrito (path, sha256, filas).
- Reporte (validation_report.md): entorno (Python/numpy/pandas/sklearn + git
  hash + dirty), gates de integridad (folds, m0, F2-reference), tabla registry,
  tabla de modelos con clasificación por regla, fold-by-fold, deltas pareados,
  slice report por modelo, checklist de leakage por modelo, limitación documentada
  del umbral (derivado de ruido de seed de RF), lenguaje de asociación (no causal),
  y la declaración explícita de que Phase 8 no corona ganador.
- Candidate log: una fila v2 bajo outputs/reports/. El log principal NO se toca.

# 10. Stop rules (detente y reporta; no improvises)

HEAD distinto; staged inesperado; artifact phase8_* preexistente; fallo de
integridad de folds; m0 fuera de tolerancia; import de xgboost/lightgbm/catboost
exitoso en Wave 1; proba inválida; classes_ sin label 1 único; colisión de
artifacts; cualquier duda de fit-scope; cualquier presión por añadir modelos/
configs/parámetros; main log alterado; entorno distinto al pineado; slice-guard
disparado (escalated: registra y continúa el resto, pero la decisión es del
usuario/director del proyecto); cualquier acción que requiera HPO, submission,
ensemble, comparación con leaderboard, datos externos, instalación de paquetes,
o Phase 9/10/11.

# 11. Prohibiciones absolutas

NO HPO (ni informal: probar valores = HPO). NO submissions. NO ensembles.
NO stacking. NO Phase 9/10/11. NO leaderboard. NO datos externos.
NO School como feature. NO instalar paquetes. NO modificar rutas prohibidas.
NO commits ni staging de ningún tipo. NO ejecutar nada sin la Project
Authorization Note. NO crear phase8_acceptance.md (paso posterior del
usuario/director del proyecto).

# 12. Al terminar

1) Ejecuta y reporta: git status --short; git diff --check; diff de rutas
   prohibidas (deben estar limpias; solo artifacts nuevos untracked).
2) Entrega: resumen ejecutivo, tabla de modelos clasificada por la regla
   (promotable_evidence / no_qualifying_evidence / escalated / failed_run),
   deltas vs m0, slice findings (con Age_missing destacado), warnings, y la
   frase literal:
   "Phase 8 Wave 1 execution complete; candidate selection, acceptance and
    commit remain gated on explicit project director authorization.
    Phase 9, Phase 10 and Phase 11 remain locked."
3) Prepara (en el resumen del punto 2, no como archivo nuevo) la evidencia que
   el usuario/director del proyecto necesitará para redactar
   phase8_acceptance.md (clasificación por modelo, lecturas m0/m2 sobre el
   caveat depth-5, lectura diagnóstica de m5 si corrió con su caveat de equidad,
   slice findings, warnings, environment+hash). No crees phase8_acceptance.md
   salvo autorización separada.

================================= END PROMPT =================================
```

**Operator reminder:** attach the Project Authorization Note (runbook §10) with the authorized hash and the m3/m5 decisions filled in, or this prompt must be refused by any executor that receives it. Wave 2 (external GBDTs) requires a different, future note and is not authorized by this document.
