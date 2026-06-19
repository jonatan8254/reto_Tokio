# Prompt — Opus Phase 11 Final Submission Review (Post-Codex)

```text
DO NOT RUN UNTIL CODEX HAS EXECUTED THE AUTHORIZED PHASE 11 AND PRODUCED ARTIFACTS.
This is the third brain in the Opus → Codex → Opus separation: a post-execution submission
audit. It executes nothing, refits nothing, runs no inference, uploads nothing, uses no
leaderboard, changes no predictions, selects no winner, and opens no new modeling.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT (Deliverable D). It independently audits Codex's Phase 11 submission + artifacts, produces a phase-gated recommendation, and drafts the acceptance record for the project director.
**Governing documents:** `phase11_master_planning_brief.md`, `phase11_operator_runbook.md`, `prompt_codex_phase11_submission_readiness_execution.md`, `submission_checklist.md`, `challenge_brief.md`.

---

The text between the markers is the prompt to run as the post-execution submission reviewer (Opus), after Codex's authorized run.

```text
================================ BEGIN PROMPT ================================

Actúa como científica de datos senior y auditora de submission-readiness para el proyecto
Reto Tokio / GCI World NFL Draft Prediction (repo local: C:\GitHub\reto_Tokio), con
experiencia en final refit, leakage, formato de submission, trazabilidad de artifacts y
cierre metodológico de fases.

# 0. Precondición absoluta
Esta revisión es válida SOLO si: (a) existió una Phase 11 Project Authorization Note firmada;
(b) Codex ya ejecutó Phase 11 y existen los artifacts phase11_submission_readiness_<run_id>_*
y la(s) submission(s) bajo outputs/submissions/. Si falta cualquiera, DETENTE y reporta.

NO ejecutas el notebook. NO refiteas/reentrenas. NO inferencia nueva. NO HPO. NO
ensembles/blending/stacking. NO recalibras. NO threshold tuning. NO subes a ningún
leaderboard. NO usas leaderboard. NO cambias predicciones. NO abres nuevo modelado ni Phase
12. NO modificas outputs de Codex ni forbidden paths. NO stagear/commit/push (salvo
instrucción explícita y selectiva del director). Solo puedes crear/actualizar:
  docs/11_submission_readiness/phase11_acceptance.md   (borrador para firma del director)

# 1. Verificación previa (read-only)
git rev-parse --short HEAD ; git status --short ; git diff --check ;
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json ;
git diff -- logs/experiment_log.csv ; find outputs/submissions -maxdepth 2 -type f
Confirma: HEAD coherente con la nota; sin staged; forbidden-path diff vacío; main log
unchanged; .venv/requirements.txt unchanged; aparece SOLO la(s) submission(s) autorizada(s)
(además del baseline preexistente); artifacts phase11_* presentes; manifest hashes
verificables.

# 2. Evidencia a leer (read-only, generada por Codex)
- outputs/submissions/phase11_submission_readiness_<run_id>_<candidate>_submission.csv
- outputs/validation/phase11_submission_readiness_<run_id>_candidate_selection_report.csv
- outputs/validation/phase11_submission_readiness_<run_id>_final_refit_report.csv
- outputs/validation/phase11_submission_readiness_<run_id>_submission_validation.csv
- outputs/validation/phase11_submission_readiness_<run_id>_model_summary.csv
- outputs/reports/phase11_submission_readiness_<run_id>_validation_report.md
- outputs/reports/phase11_submission_readiness_<run_id>_artifact_manifest.csv
- outputs/reports/phase11_submission_readiness_<run_id>_experiment_log_candidate.csv
- notebooks/11_phase11_submission_readiness.ipynb (static)
Y como contexto: phase10_acceptance.md, phase10 validation/selection-bias reports,
phase9a_acceptance + backlog, submission_checklist.md, challenge_brief.md, validation/leakage
protocols, project_execution_plan_v3.md (§14, §16.7).

# 3. Auditoría independiente de la submission (verifier != generator)
Reverifica de forma independiente desde el archivo de submission y el sample oficial:
- columnas exactamente Id, Drafted;
- row count == 696 y coincide con test.csv y sample_submission.csv;
- Id set == set oficial; Id order == sample_submission.csv (= test.csv);
- Drafted numérico; todo en [0,1]; sin NaN; sin inf; sin Id duplicado;
- recomputar SHA-256 de la submission y contrastar con manifest/reporte;
- confirmar lineage: modelo + commit + run_id + feature set (F2) presentes en el reporte;
- confirmar que el candidato refiteado y sus hiperparámetros coinciden con lo recuperado de
  Phase 10 (CatBoost: depth 6 / lr 0.01 / l2 9 / iters 800 / border 128 / seed 42; M1
  baseline: la config recuperada de Phase 8);
- confirmar, leyendo el notebook estático, que NINGÚN fit tocó test (preprocessing fit solo
  full train; test transform-only); que classes_ se verificó para label 1; que no hubo
  edición manual.
Si algo no coincide o falla un check de formato/lineage: marca BLOCKER y detente antes de
redactar la aceptación.

# 4. Interpretación estratégica (SIN seleccionar winner, SIN subir)
Responde, con lenguaje de asociación (no causal):
- ¿La submission es técnicamente válida (formato/Id/orden/rango/hash/lineage)?
- ¿El candidato refiteado es coherente con la decisión autorizada (CatBoost tuned primario /
  M1 baseline fallback / ambos)? ¿El CatBoost Stability Gate pasó o se firmó waiver?
- ¿Persisten las warnings heredadas relevantes para test (Age_missing=1 — 115/696 filas de
  test tienen Age faltante; Position=QB; CatBoost Year 2011 / avail_count 0 / OG / OLB)?
  Documenta su impacto potencial, sin poder medir AUC de test.
- ¿Hay señales de leakage, edición manual, o desalineación de Ids?
- ¿El artifact es aceptable para subida del director (con o sin warnings), requiere decisión
  del usuario, debe regenerarse, conviene usar el fallback M1, requiere más auditoría, o se
  difiere? Recuerda: un candidato optimizado NO es un winner; "best global OOF" NO implica
  "mejor en test".
Mantén roles: M0 ancla; CatBoost tuned primario warning-heavy; M1 baseline fallback; M1
tuned rechazado; XGB/LGBM dropped (no re-promover sin evidencia nueva aceptada).

# 5. Matriz de recomendación (en la acceptance draft)
Clasifica cada recomendación en EXACTAMENTE una categoría:
1 Accept Phase 11 submission artifact for user-side upload with warnings.
2 Accept Phase 11 submission artifact as technically valid but require user decision before upload.
3 Reject submission artifact; regenerate required.
4 Use M1 baseline fallback instead of CatBoost.
5 Request additional audit before upload.
6 Defer due to insufficient evidence.
7 Prohibited under current rules.
Cada recomendación con la tabla:
| Recommendation ID | Recommendation | Evidence from Phase 11 | Comparison baseline | Methodological support | Risk | Required next gate | Priority |
Priority ∈ {High, Medium, Low, Deferred, Prohibited}. NO inventes resultados de leaderboard.
Distingue "submission técnicamente válida" de "garantía de score": la validez de formato no
predice el AUC privado.

# 6. Borrador de aceptación (docs/11_submission_readiness/phase11_acceptance.md)
Redacta el borrador para firma del director, incluyendo: decisión por candidato/submission
(accept-with-warnings / accept-pending-user-decision / reject-regenerate / use-fallback /
additional-audit / defer, SIN winner); estado de la auditoría independiente de submission
(formato/Id/orden/rango/hash/lineage); candidato refiteado + fuente de hiperparámetros;
estado del CatBoost Stability Gate (pass o waiver); warnings de slice relevantes para test;
SHA-256 de la(s) submission(s); estado de upload (none / manual del director); .venv/
requirements (unchanged); main log (unchanged); matriz de recomendación §5; lista de
archivos sugeridos para commit selectivo (la submission CSV está gitignored — registrar su
SHA-256); la sección "Handoff to Manual Upload Without Automating Upload" (último archivo
subido = ranking final; private LB = full test); y campos de hash/firma en blanco para el
director. NO firmes por el director. NO subas. NO hagas commit.

# 7. Al terminar
Reporta: PASS/BLOCKER del review; checks de submission recomputados vs Codex; discrepancias;
archivos creados (acceptance draft); git status; y la frase literal:
"Phase 11 submission review complete. Submission artifact audited, not uploaded. No final
 winner declared; no leaderboard used. Acceptance is drafted for project-director signature.
 Upload remains a manual, director-only action."

================================= END PROMPT =================================
```

**What NOT to recommend:** no automatic upload; no leaderboard use for any decision; no change to predictions; no ensemble/blending/stacking/calibration/threshold tuning as an executed action (only as future-locked items); no reopening of XGB/LGBM/M1-tuned/HPO without written justification; no declaration that a submission's format validity guarantees a good private-leaderboard score; no opening of a new modeling phase. A Phase 11 validated submission is at most **technically ready for the director's manual upload decision**, never an automated submission and never a guaranteed winner.

**Operator reminder:** this prompt runs only after Codex execution produces the submission + artifacts. It produces the phase-gated recommendation matrix and the acceptance draft; the project director signs acceptance and performs any upload manually, choosing the upload order (last submitted file determines final ranking). No upload, no leaderboard selection, and no new modeling occur here.
