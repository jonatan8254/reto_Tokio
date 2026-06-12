# Prompt — Codex Phase 7 Execution Plan (INERT UNTIL PROJECT AUTHORIZATION NOTE IS ATTACHED)

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT. **Inert until the operator attaches a Project Authorization Note** (runbook §9). Without that note, no part of this prompt may be acted on.
**Governing documents:** `docs/07_feature_engineering/phase7_master_planning_brief.md` (the plan), `docs/07_feature_engineering/phase7_operator_runbook.md` (the procedure).

---

The text between the markers below is the prompt to give the executor (Codex or equivalent), verbatim, together with the Project Authorization Note.

```text
================================ BEGIN PROMPT ================================

Actúa como ingeniero ML senior de ejecución, bajo auditoría estricta de leakage,
validación y reproducibilidad, para el proyecto Reto Tokio / GCI World NFL Draft
Prediction (repo local: C:\GitHub\reto_Tokio).

# 0. Precondición absoluta

Esta corrida es válida SOLO si está adjunta una Project Authorization Note
(formato: runbook §9) firmada por el usuario/director del proyecto, que
incluye el hash de commit autorizado. Si la nota no está adjunta, detente y no
hagas nada.

# 1. Rol y misión

Implementar y ejecutar EXACTAMENTE el bloque de features de missingness /
measurement availability pre-registrado en
docs/07_feature_engineering/phase7_master_planning_brief.md §9, sobre los folds
congelados, con el modelo congelado, y producir los artifacts de §13 del brief.
Nada más. No eres diseñador: el diseño está congelado; eres ejecutor auditado.

# 2. Estado esperado (verifica antes de cualquier cómputo)

git rev-parse --short HEAD        -> debe ser igual al hash de la Project Authorization Note
git status --short                -> sin staged; sin modificaciones tracked
git diff --check                  -> limpio
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json -> vacío
.venv\Scripts\python.exe          -> Python 3.13.13; pandas 3.0.3; scikit-learn 1.9.0; numpy 2.4.6

Si cualquier verificación falla: reporta, clasifica severidad y DETENTE.

# 3. Archivos que debes revisar antes de implementar (read-only)

- docs/07_feature_engineering/phase7_master_planning_brief.md   (§9 ladder, §10 contrato, §11 criterios, §12 leakage)
- docs/06_validation/phase6a_acceptance.md                      (decisiones ratificadas)
- docs/06_validation/phase6_acceptance.md
- docs/05_methodology/leakage_checklist_phase6.md
- docs/05_methodology/validation_protocol_phase6.md
- notebooks/04_phase6a_baseline_reconciliation.ipynb            (solo lectura: reutiliza sus builders fold-safe auditados)
- notebooks/05_phase6a_d1_d2_diagnostics.ipynb                  (solo lectura: patrón de integrity gates)
- outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv
- outputs/oof/phase6_rf_sanity_baseline_v1_oof_predictions.csv
- outputs/oof/phase6a_v7_phase6_mean_impute_oof_predictions.csv

# 4. Alcance autorizado (futuro, tras la nota)

Crear y ejecutar UN notebook:
  notebooks/07_phase7_missingness_availability_feature_block.ipynb
  experiment_id = phase7_missingness_availability_v1

Escribir SOLO estos artifacts (con pre-write guards fail-if-exists):
  outputs/oof/phase7_missingness_availability_v1_<variant_id>_oof_predictions.csv  (uno por variante entrenada)
  outputs/validation/phase7_missingness_availability_v1_variant_summary.csv
  outputs/validation/phase7_missingness_availability_v1_slice_report.csv
  outputs/reports/phase7_missingness_availability_v1_validation_report.md
  outputs/reports/phase7_missingness_availability_v1_experiment_log_candidate.csv

# 5. Rutas prohibidas (no escribir jamás; lectura según se indica)

- data/input/: LECTURA PERMITIDA solo de los CSVs oficiales (train.csv,
  test.csv, sample_submission.csv) para contract checks. ESCRITURA PROHIBIDA.
- notebooks/_official/: lectura y escritura PROHIBIDAS.
- references/: lectura y escritura PROHIBIDAS.
- outputs/submissions/: lectura y escritura PROHIBIDAS (Phase 7 no genera submissions).
- logs/experiment_log.csv: LECTURA PERMITIDA (leer antes de empezar y assert
  sin cambios al final). ESCRITURA PROHIBIDA.
- .vscode/settings.json: lectura y escritura PROHIBIDAS.
- Libros/, Prompts/, Recapitulaciones/: lectura y escritura PROHIBIDAS.

No git add. No git add . No git commit. No git commit -a. No push. No staging.

# 6. Diseño congelado (no modificable en esta corrida)

Folds: cargar outputs/folds/phase6_rf_sanity_baseline_v1_fold_assignments.csv y
asertar: 2781 filas; labels 0..4; orden de Id igual a train; sha256[:16] ==
96937649526bcadb. NUNCA recomputar folds.

Modelo único: RandomForestClassifier(n_estimators=100, max_depth=5,
random_state=42, n_jobs=-1). Cambiar cualquier hiperparámetro = HPO = prohibido.

Features base (13): Year, Age, Height, Weight, Sprint_40yd, Vertical_Jump,
Bench_Press_Reps, Broad_Jump, Agility_3cone, Shuttle, Player_Type,
Position_Type, Position. Excluidos siempre: Id, Drafted, School (assert).

Features nuevas (row-wise, sin fitting):
  Age_missing; Sprint_40yd_missing; Vertical_Jump_missing;
  Bench_Press_Reps_missing; Broad_Jump_missing; Agility_3cone_missing;
  Shuttle_missing; available_measurement_count (no-NaN entre los 6 tests, 0-6);
  measurement_completeness_group = bins fijos {0:none,1-3:low,4-5:partial,6:complete}
  codificados como enteros ordenados 0-3 (mapeo constante, sin quantiles).
Asserts de sanidad: suma de flags == conteos conocidos de train
(Age 435; Sprint 145; Vertical 554; Bench 721; Broad 581; Agility 970; Shuttle 912).

Escalera de variantes (cap duro: <= 8 entrenadas; ninguna adicional sin nueva nota):
  F0  phase7_f0_anchor_recheck        13 features, median            GATE: OOF == 0.726616 +/- 1e-6, si no DETENTE
  F1  phase7_f1_median_flags          13 + 7 flags, median
  F5  phase7_f5_mean_flags            13 + 7 flags, mean
  F2  phase7_f2_median_flags_count    F1 + available_measurement_count, median
  F3  phase7_f3_median_flags_count_bins  F2 + completeness bins, median
  F6  (GATED) phase7_f6_mean_flags_count  SOLO si F5-F1 OOF >= 0.005436
  F4  (GATED) phase7_f4_role_interactions SOLO si: (1) una variante anterior pasa
      el umbral; (2) los slices muestran heterogeneidad relevante por
      Player_Type o Position_Type; Y (3) el usuario/director del proyecto
      autoriza F4 explícitamente en la Project Authorization Note inicial. Si
      F4 no fue autorizado inicialmente, activarlo requiere detener la corrida
      y emitir una nueva Project Authorization Note con un nuevo run_id.
Lecturas de referencia (sin entrenar): copia de V0 OOF y V7 OOF para deltas pareados.

Pipelines: SimpleImputer(median|mean) numérico + (most_frequent + OneHotEncoder
handle_unknown="ignore") categórico, dentro de ColumnTransformer+Pipeline,
fit SOLO en la máscara de entrenamiento de cada fold. Reutiliza los builders del
notebook 04 (auditados); no reescribas la lógica desde cero.

# 7. Checks de validación obligatorios

- ROC-AUC con probabilidades de la clase positiva Drafted=1, extraídas SOLO tras
  verificar estimator.classes_ (label 1 exactamente una vez); nunca [:, 1] a ciegas.
- OOF por variante: 2781 filas, columnas Id,fold,y_true,y_pred_proba; proba
  finita en [0,1]; sin NaN; ningún fold mono-clase; fold de OOF == fold congelado.
- Deltas pareados por fold vs F0 para cada variante; OOF como moneda principal.
- Regla de aceptación pre-registrada (no modificable): adoptar solo si
  OOF(variante)-OOF(F0) >= 0.005436 Y delta positivo en >= 4/5 folds Y guardia
  de slices (abajo). Clasifica cada variante: adopted / rejected / escalated.
- Slices obligatorios: Player_Type, Position_Type, Year, Age_missing,
  available_measurement_count, measurement_completeness_group,
  frequent_vs_rare_school_group (School SOLO diagnóstico, jamás feature).
  n < 50 => no evaluable (flag). Caída > 0.02 AUC en slice obligatorio con
  n >= 50 => escalated (revisión del usuario/director del proyecto), nunca auto-adoptar.

# 8. Checks de leakage obligatorios (instancia por variante)

- Ningún fitting fuera del fold de entrenamiento; ningún fitting con test.
- Test usado SOLO para checks de contrato (shape/columnas/orden); en Phase 7 no
  hay inferencia final ni submission.
- Sin target encoding; sin feature selection; sin reducción de dimensionalidad;
  sin rare grouping; sin estadísticas de rol aprendidas (solo OHE de categóricas
  crudas); sin leaderboard; sin datos externos.
- logs/experiment_log.csv: leer antes, asertar idéntico después.
- Variables diagnósticas fuera de la matriz de features (assert).

# 9. Política de artifacts y reporte

- Pre-write guards en todos los paths; jamás sobrescribir; colisión => DETENTE.
- Reporte (validation_report.md): entorno (Python/numpy/pandas/sklearn + git
  hash + dirty), gates de integridad, tabla de variantes, fold-by-fold, deltas
  pareados, lectura vs V7 (cuánto del +0.0757 recuperan los features explícitos),
  slice report, checklist de leakage por variante, clasificación
  adopted/rejected/escalated por regla, lenguaje de asociación (no causal).
- Candidate log: una fila v2 (23 columnas) bajo outputs/reports/. El log
  principal NO se toca.

# 10. Stop rules (detente y reporta; no improvises)

HEAD distinto; staged inesperado; fallo de integridad de folds; F0 fuera de
tolerancia; proba inválida; classes_ sin label 1 único; colisión de artifacts;
cualquier duda de fit-scope; cualquier presión por añadir variantes/features/
parámetros; main log alterado; entorno distinto al pineado; slice-guard
disparado (escalated); cualquier acción que requiera HPO, submission,
comparación de familias de modelos, leaderboard, datos externos o Phase 8.

# 11. Prohibiciones absolutas

NO HPO (ni informal). NO submissions. NO Phase 8. NO model-family comparison.
NO ensembles. NO leaderboard. NO datos externos. NO School como feature.
NO modificar rutas prohibidas. NO commits ni staging de ningún tipo.
NO ejecutar nada sin la Project Authorization Note.

# 12. Al terminar

1) Ejecuta y reporta: git status --short; git diff --check; diff de rutas
   prohibidas (deben estar limpias; solo artifacts nuevos untracked).
2) Entrega: resumen ejecutivo, tabla de variantes con clasificación por regla,
   hallazgo F1-vs-F5-vs-V7, slice findings, warnings, y la frase literal:
   "Phase 7 execution complete; acceptance and commit remain gated on explicit
    user/project director authorization. Phase 8 remains locked."
3) NO redactes phase7_acceptance.md ni hagas commit: ambos son pasos
   posteriores del usuario/director del proyecto (runbook §§11-12).
4) Prepara (en el resumen del punto 2, no como archivo nuevo) la evidencia que
   el usuario/director del proyecto necesitará para redactar
   phase7_acceptance.md (clasificación por rung, lecturas F1/F5/Vref7, slice
   findings, warnings, environment+hash). No crees phase7_acceptance.md salvo
   autorización separada.

================================= END PROMPT =================================
```

**Operator reminder:** attach the Project Authorization Note (runbook §9) with the authorized hash filled in, or this prompt must be refused by any executor that receives it.
