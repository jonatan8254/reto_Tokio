# Prompt — Opus Phase 9A Strategic Recommendation Review (Post-Codex)

```text
DO NOT RUN UNTIL CODEX HAS EXECUTED PHASE 9A AND AN INDEPENDENT RECOMPUTATION HAS PASSED.
```

**Project:** Reto Tokio / GCI World NFL Draft Prediction
**Status:** PREPARED PROMPT. This is the **third brain** in the Opus → Codex → Opus separation: a post-execution strategic review. It interprets Codex's diagnostic outputs, prioritizes a phase-gated improvement backlog, and drafts the acceptance record for the project director. **It executes nothing, trains nothing, selects no winner, and authorizes no submission or future phase.**
**Governing documents:** `phase9a_master_planning_brief.md`, `phase9a_operator_runbook.md`, `prompt_codex_phase9a_execution_plan.md`.

---

The text between the markers below is the prompt to run as the post-execution strategic reviewer (Opus or equivalent), after Codex's run.

```text
================================ BEGIN PROMPT ================================

Actúa como científica de datos senior y revisora estratégica post-ejecución para el
proyecto Reto Tokio / GCI World NFL Draft Prediction (repo local: C:\GitHub\reto_Tokio),
con experiencia en ranking metrics, desbalance, slice diagnostics, selection bias y
cierre metodológico de fases.

# 0. Precondición absoluta

Esta revisión es válida SOLO si:
- Codex ya ejecutó Phase 9A y existen los artifacts phase9a_auc_ranking_diagnostics_v1_*;
- una recomputación independiente de las métricas pasó (ROC-AUC ±1e-9; integridad OK).
Si los artifacts no existen o el audit independiente no pasó, detente y reporta.

NO ejecutas notebooks. NO entrenas. NO reentrenas. NO HPO. NO ensembles/blending/
stacking. NO recalibras. NO threshold-tuning. NO submissions. NO leaderboard. NO
declaras final winner. NO declaras submission-ready model. NO abres Phase 10/11. NO
modificas outputs de Codex. NO stagear/commit/push (salvo instrucción explícita y
selectiva del director). Solo puedes crear/actualizar:
  docs/09_auc_ranking_diagnostics/phase9a_improvement_backlog.md
  docs/09_auc_ranking_diagnostics/phase9a_acceptance.md   (borrador para firma del director)

# 1. Verificación previa (read-only)

git rev-parse --short HEAD ; git status --short ; git diff --check ;
git diff --name-only -- data/input notebooks/_official references outputs/submissions logs/experiment_log.csv .vscode/settings.json
Confirma: HEAD coherente; sin staged; forbidden-path diff vacío; main log unchanged;
artifacts phase9a_* presentes; manifest hashes verificables.

# 2. Evidencia a leer (read-only, generada por Codex)

- outputs/validation/phase9a_auc_ranking_diagnostics_v1_oof_integrity_report.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_auc_reproduction.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_global_metrics.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_topk_quantile.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_fold_paired.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_slice_report.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_score_distribution.csv
- outputs/validation/phase9a_auc_ranking_diagnostics_v1_disagreement.csv
- outputs/reports/phase9a_auc_ranking_diagnostics_v1_validation_report.md
- outputs/reports/phase9a_auc_ranking_diagnostics_v1_artifact_manifest.csv
- outputs/reports/phase9a_auc_ranking_diagnostics_v1_experiment_log_candidate.csv
Y, como contexto: ambos phase8 acceptance docs y el master planning brief de Phase 9A.

# 3. Recomputación independiente mínima (verifier ≠ generator)

Recalcula de forma independiente, desde los OOF persistidos, al menos:
- ROC-AUC por candidato (rank-based stdlib) y contrasta con auc_reproduction.csv (±1e-9);
- positive rate global (debe ser ~0.6483);
- una métrica top-k (p.ej. top-decile capture) para un candidato, y contrasta con topk_quantile.csv.
Also independently verify OOF schema, row count, probability range, absence of NaN/inf values, duplicate checks, and Id/fold/y_true alignment across all five OOF files, or directly validate the integrity report against raw OOF reads.
Si algo no coincide dentro de tolerancia documentada: marca BLOCKER y detente.

# 4. Interpretación estratégica (sin seleccionar winner)

Interpreta la evidencia respondiendo a las preguntas diagnósticas del brief §7:
- ¿M1 mantiene superioridad en ranking útil (top-k) y estabilidad fold, no solo ROC global?
- ¿CatBoost aporta complementariedad real vs M1 o solo ganancia local con warnings?
- ¿Hay distribuciones de score degeneradas/comprimidas?
- ¿Qué slices son frágiles (Age_missing=1, Year, completeness, roles)?
- ¿Qué conflictos ROC-vs-PR/top-k o global-vs-slice aparecieron?
- ¿Qué candidatos merecen carry / observe / drop, recordando que NO hay winner?
Mantén roles congelados: m0 anchor; m1 candidate_with_warning; catboost escalated/
candidate_with_warning; xgboost/lightgbm no_qualifying_evidence (no re-promover sin
evidencia nueva aceptada). Lenguaje de asociación, no causal.

# 5. Backlog priorizado (docs/.../phase9a_improvement_backlog.md)

Construye el backlog final de hipótesis de mejora AUC/ranking, derivado SOLO de:
artifacts aceptados, OOF, fold/slice reports, validation reports, evidencia Phase 7/8,
referencias del repo y los diagnósticos de Phase 9A. NO implementes nada.

Cada item con la tabla:
| Recommendation ID | Hypothesis | Evidence motivating it | Methodological support | Expected AUC/ranking rationale | Required future phase | Required artifacts | Main risk | Gate before execution | Priority |
Clasifica cada item en EXACTAMENTE una categoría:
1 Safe diagnostic recommendation for Phase 9A execution.
2 Hypothesis for Phase 9B or later diagnostic phase.
3 Hypothesis for Phase 10 HPO (locked).
4 Hypothesis for future ensemble/blending (locked).
5 Hypothesis for Phase 11 submission strategy (locked).
6 Deferred — insufficient evidence.
7 Prohibited under current rules.
Priority ∈ {High, Medium, Low, Deferred, Prohibited}. Expected rationale CUALITATIVO
salvo evidencia aceptada (no inventes ganancias numéricas). Recordatorios: M1 sigue
candidate_with_warning; CatBoost escalated/candidate_with_warning; XGB/LGBM
no_qualifying_evidence; cualquier ensemble/blending/HPO/calibration/threshold/
submission queda future-locked.

# 6. Borrador de aceptación (docs/.../phase9a_acceptance.md)

Redacta el borrador de aceptación para firma del director, usando el template del
runbook §12, incluyendo: decisión diagnóstica; estado del audit; reproducción ROC-AUC
(±1e-9); veredictos por candidato (carry/observe/drop, sin winner); hallazgos de slice
(incl. Age_missing=1); warnings; resumen del backlog; estado de submission (none);
main log (unchanged); locks Phase 10/11; y los campos de hash/firma en blanco para el
director. NO firmes por el director. NO hagas commit.

# 7. Al terminar

Reporta: PASS/BLOCKER del review; valores recomputados vs Codex; discrepancias;
archivos creados (backlog + acceptance draft); git status; y la frase literal:
"Phase 9A strategic review complete. No final winner selected, no submission
 authorized. Backlog is phase-gated. Acceptance is drafted for project-director
 signature. Phase 10 and Phase 11 remain locked."

================================= END PROMPT =================================
```

**Operator reminder:** this prompt runs only after Codex execution + independent recomputation. It produces the prioritized backlog and the acceptance draft; the project director signs acceptance and authorizes any selective commit. No winner, no submission, no future-phase opening occurs here.
