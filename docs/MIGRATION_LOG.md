# Documentation Migration Log

## Purpose

Record the Phase 4B documentation reorganization so future work can find active project documents by phase without losing traceability.

## Migration date

2026-06-11

## Files moved

| Old path | New path | Reason | Status |
|---|---|---|---|
| `docs/challenge_brief.md` | `docs/00_project_contract/challenge_brief.md` | Active competition contract belongs with project contract docs. | Moved |
| `docs/submission_checklist.md` | `docs/00_project_contract/submission_checklist.md` | Active submission rules belong with project contract docs. | Moved |
| `docs/project_execution_plan_v2_context_efficient.md` | `docs/01_project_planning/project_execution_plan_v2_context_efficient.md` | Active phase plan belongs with project planning docs. | Moved |
| `docs/experiment_notes.md` | `docs/03_eda/experiment_notes.md` | Phase 3 EDA evidence belongs with EDA docs. | Moved |
| `docs/pdf_review_audit.md` | `docs/04_research/pdf_review_audit.md` | Phase 4 PDF audit belongs with research docs. | Moved |
| `docs/pdf_key_findings.md` | `docs/04_research/pdf_key_findings.md` | Phase 4 PDF audit summary belongs with research docs. | Moved |
| `docs/research_notes_validation.md` | `docs/04_research/research_notes_validation.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/research_notes_leakage.md` | `docs/04_research/research_notes_leakage.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/research_notes_feature_engineering.md` | `docs/04_research/research_notes_feature_engineering.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/research_notes_tabular_models.md` | `docs/04_research/research_notes_tabular_models.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/research_notes_hpo.md` | `docs/04_research/research_notes_hpo.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/research_notes_reproducibility.md` | `docs/04_research/research_notes_reproducibility.md` | Phase 4B research note belongs with research docs. | Moved |
| `docs/phase5_methodology_plan.md` | `docs/05_methodology/phase5_methodology_plan.md` | Phase 5 methodology plan belongs with methodology docs. | Moved |

## Files intentionally not moved

| Path | Reason |
|---|---|
| `scripts/audit_pdf_sources.py` | Script remains under `scripts/` as requested. Its output paths were updated to `docs/04_research/`. |
| `docs/project_execution_plan.md` | Not confirmed yet. Git status showed this path as deleted before migration; no file existed to move. |
| `notebooks/02_eda_and_data_contract.ipynb` | Notebook references are not edited in this documentation migration. |
| `notebooks/_official/` | Official notebooks must remain untouched. |
| `data/input/` | Official data must remain untouched. |
| `references/` | PDFs and source materials must remain untouched. |

## References updated

| File | Reference updated | Status |
|---|---|---|
| `docs/01_project_planning/project_execution_plan_v2_context_efficient.md` | Root `docs/*.md` paths updated to phase-organized paths. | Updated |
| `docs/05_methodology/phase5_methodology_plan.md` | Phase 3 and PDF audit paths updated to phase-organized paths. | Updated |
| `scripts/audit_pdf_sources.py` | PDF audit output paths updated from `docs/` root to `docs/04_research/`. | Updated |
| `scripts/phase3_build_notebook.py` | Future Phase 3 experiment-note output path updated to `docs/03_eda/experiment_notes.md`. | Updated |
| `docs/README.md` | New phase-based documentation index created. | Created |
| `docs/MIGRATION_LOG.md` | This migration log created. | Created |

## Remaining manual checks

| Item | Status |
|---|---|
| Check notebooks for old documentation paths without editing them. | Found old `docs/experiment_notes.md` references in Phase 3 notebooks; not edited by policy. |
| Decide whether `docs/project_execution_plan.md` should be restored, archived, or ignored. | Not confirmed yet |
| Decide whether untracked backup notebooks should remain local-only. | Not confirmed yet |
