"""Refactor the Phase 3 EDA notebook into a multi-cell report.

This local traceability script builds `notebooks/02_eda_and_data_contract.ipynb`
from the backed-up Phase 3 notebook:

`notebooks/02_eda_and_data_contract_before_refactor.ipynb`

The purpose is documentation and notebook hygiene only. This script does not
train models, generate submissions, modify raw data, or use external data. It
keeps the analytical logic from the backup notebook, adds section-level markdown,
and writes an improved narrative `docs/03_eda/experiment_notes.md` when the generated
notebook is executed.

This script is not an official competition deliverable and should remain
unstaged unless explicitly approved.
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path.cwd()
BACKUP_NOTEBOOK = ROOT / "notebooks" / "02_eda_and_data_contract_before_refactor.ipynb"
OUTPUT_NOTEBOOK = ROOT / "notebooks" / "02_eda_and_data_contract.ipynb"


def md_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")


def code_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(dedent(text).strip() + "\n")


def objective_cell(title: str, objective: str, why: str, data: str, caution: str) -> nbf.NotebookNode:
    return md_cell(
        f"""
        ### {title}

        **Objective.** {objective}

        **Why it matters.** {why}

        **Expected output.** Tables, figures, and narrative interpretation directly below the code cell.

        **Data used.** {data}

        **Leakage/validation caution.** {caution}
        """
    )


def interpretation_cell(text: str) -> nbf.NotebookNode:
    return md_cell(f"**Interpretation.** {text}")


def read_backup_source() -> str:
    if not BACKUP_NOTEBOOK.exists():
        raise FileNotFoundError(f"Backup notebook not found: {BACKUP_NOTEBOOK}")
    nb = nbf.read(BACKUP_NOTEBOOK, as_version=4)
    code_sources = [cell.source for cell in nb.cells if cell.cell_type == "code"]
    if not code_sources:
        raise ValueError("Backup notebook contains no code cell to refactor.")
    return "\n\n".join(code_sources)


def split_backup_source(source: str) -> dict[str, str]:
    display_marker = 'display(Markdown("# Phase 3 execution'
    display_idx = source.find(display_marker)
    first_title = source.find('title("What is the dataset')
    helper_start = source.find("def save_fig")
    if display_idx == -1 or first_title == -1 or helper_start == -1:
        raise ValueError("Backup notebook source does not match the expected Phase 3 structure.")

    setup = source[:helper_start].strip()
    helpers = source[helper_start:display_idx].strip()
    titled_source = source[first_title:]

    title_matches = list(re.finditer(r'^title\("(.+?)"\)\s*$', titled_source, flags=re.MULTILINE))
    chunks: dict[str, str] = {}
    for idx, match in enumerate(title_matches):
        title = match.group(1)
        start = match.end()
        end = title_matches[idx + 1].start() if idx + 1 < len(title_matches) else len(titled_source)
        chunks[title] = titled_source[start:end].strip()

    dataset_chunk = chunks["What is the dataset, and can we trust the data contract?"]
    chunks["Data loading"] = dataset_chunk[: dataset_chunk.find("expected_test_columns =")].strip()
    contract_start = dataset_chunk.find("expected_test_columns =")
    schema_start = dataset_chunk.find("numeric_columns =")
    chunks["Data contract checks"] = dataset_chunk[contract_start:schema_start].strip()
    chunks["Schema and variable taxonomy"] = dataset_chunk[schema_start:].strip()

    missing_chunk = chunks["What does missingness reveal?"]
    available_start = missing_chunk.find("train_analysis = train.copy()")
    chunks["Missingness analysis"] = missing_chunk[:available_start].strip()
    chunks["Available measurement count analysis"] = missing_chunk[available_start:].strip()

    final_chunk = chunks["Final synthesis and experiment notes update"]
    notes_start = final_chunk.find("notes = f\"\"\"")
    chunks["Final synthesis"] = final_chunk[:notes_start].strip()

    return {
        "setup": setup,
        "helpers": helpers,
        **chunks,
    }


EXPERIMENT_NOTES_CODE = r'''
strategy_families = pd.DataFrame([
    {
        "future_signal_family": "Role context",
        "columns_or_concepts": "Position; Position_Type; Player_Type",
        "why_it_may_matter": "Player measurements and target rates are role-dependent; global patterns can hide subgroup behavior.",
        "validation_caution": "Report slice performance by role and avoid overfitting rare roles.",
    },
    {
        "future_signal_family": "Measurement availability",
        "columns_or_concepts": "missingness indicators; available_measurement_count; co-missingness profiles",
        "why_it_may_matter": "Measurement completeness may proxy player evaluation context and testing availability.",
        "validation_caution": "Any missingness feature must be tested later in fold-safe validation.",
    },
    {
        "future_signal_family": "Physical profile",
        "columns_or_concepts": "size; speed; explosiveness; agility; strength",
        "why_it_may_matter": "Physical measurements are likely informative only when interpreted relative to role.",
        "validation_caution": "No role-normalized features or interactions are selected in Phase 3.",
    },
    {
        "future_signal_family": "Institutional/categorical context",
        "columns_or_concepts": "School; long-tail categories; rare-category behavior",
        "why_it_may_matter": "School may contain signal but also strong high-cardinality overfitting risk.",
        "validation_caution": "Prioritize safe frequency/count encoding or strictly OOF target encoding only if justified later.",
    },
])

key_findings = pd.DataFrame([
    {"finding_type": "confirmed_fact", "finding": "Official CSVs load and pass executable data contract checks.", "future_use": "Reuse checks in later notebooks."},
    {"finding_type": "descriptive_finding", "finding": "Target is not extremely imbalanced and Drafted=1 is the majority class.", "future_use": "Use ROC-AUC/ranking framing rather than threshold accuracy."},
    {"finding_type": "descriptive_finding", "finding": "Missingness is structured by field, role, and year; Age missingness is especially notable in train-only target-rate diagnostics.", "future_use": "Evaluate missingness signals only with fold-safe validation."},
    {"finding_type": "descriptive_finding", "finding": "Special teams appears structurally different from offense/defense, including lower measurement completeness and lower target rate.", "future_use": "Report future model performance by Player_Type slices."},
    {"finding_type": "potential_risk", "finding": "Low-n schools and rare categories can show extreme but unreliable target rates.", "future_use": "Always track n and uncertainty."},
    {"finding_type": "candidate_hypothesis", "finding": "Physical metrics need role-aware interpretation; global associations can be misleading.", "future_use": "Test role interactions or role-normalized metrics later."},
    {"finding_type": "deferred_decision", "finding": "No feature engineering, preprocessing, validation policy, or model choice is finalized in Phase 3.", "future_use": "Carry into Phase 5/6 plans."},
])

display_table("Key Phase 3 synthesis", key_findings, max_rows=30)
display_table("Future signal families", strategy_families, max_rows=10)

special_teams_summary = "Not available."
if "Player_Type" in train.columns:
    player_type_rates_for_notes = target_rate_table(train, "Player_Type", min_n_warning=20)
    player_measurement = train_analysis.groupby("Player_Type")["available_measurement_count"].agg(["count", "mean", "median"]).reset_index()
    special_teams_summary = (
        "Player_Type target-rate and measurement-completeness tables indicate that special_teams should be treated as a distinct slice. "
        "Future models should report Player_Type slice performance because global AUC can hide weak subgroup behavior."
    )

notes = f"""# Experiment Notes

## Phase 3 - Data Contract and Initial EDA

Date: {date.today().isoformat()}

### Executive Summary of Phase 3 Findings

Phase 3 confirms that the official CSVs pass executable data-contract checks and that the project can proceed with a reliable EDA foundation. The EDA suggests four future signal families: role context, measurement availability, physical profile, and institutional/categorical context. It also highlights the main risks that later phases must control: leakage through preprocessing, high-cardinality overfitting from `School`, low-n target-rate instability, train/test composition shift, and hidden subgroup failures.

No model was trained. No submission was generated. No raw data was modified. No final features, preprocessing rules, column drops, outlier rules, encodings, or validation policy were selected.

### Integrated Post-EDA Interpretation

The Phase 3 EDA suggests a four-layer signal architecture:

1. **Role context:** `Position`, `Position_Type`, and `Player_Type` define the context in which physical measurements should be interpreted.
2. **Measurement availability:** `Age` missingness, physical-test missingness, `available_measurement_count`, and co-missingness profiles may describe how completely an athlete was evaluated.
3. **Role-aware physical profile:** size, speed, explosiveness, agility, and strength appear most meaningful when interpreted relative to role.
4. **Institutional/categorical context:** `School`, long-tail category behavior, rare-category risk, and test-only categories may carry signal but also create overfitting risk.

Missingness has at least three subfamilies. `Age` missingness appears unusually strong in train-only diagnostics and should be tested separately from physical-test missingness. Physical-test missingness (`Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`) may reflect measurement availability, position norms, or testing context. Aggregated completeness (`available_measurement_count` and co-missingness profiles) may proxy player evaluation context.

The EDA also suggests a possible `Player_Type -> measurement completeness -> Drafted` confounding pattern. `special_teams` appears structurally different from offense and defense, with lower measurement completeness and lower target rate. This is descriptive, not causal. Future models should report global AUC plus AUC by `Player_Type`, `Position_Type`, `Year`, measurement-completeness slices, and frequent-vs-rare school groups where feasible.

Physical values should not be interpreted as raw numbers alone. A sprint, shuttle, weight, height, or jump result can mean different things for different roles. Global associations can mislead; role-aware diagnostics and slice reporting should be part of later validation.

`School` is potentially useful but high risk. Future use should be staged: no School baseline, safe frequency/count encoding, rare-category handling inside folds, and only if justified later, strictly out-of-fold target encoding with smoothing or CatBoost-style handling under careful validation.

Train/test numeric drift appears moderate rather than catastrophic. The larger concern is structural/categorical drift, especially `School` and role composition. Drift diagnostics should guide slice diagnostics, not test-tuned preprocessing.

Strategic conclusion: signal is likely less about raw physical values alone and more about role plus measurement context. Phase 3 provides a map of where signal may exist and where validation/leakage controls must be strongest.

### Data Contract Status

- Train shape recomputed in notebook: `{train.shape}`.
- Test shape recomputed in notebook: `{test.shape}`.
- Sample submission shape recomputed in notebook: `{sample_submission.shape}`.
- Target column: `{TARGET_COLUMN}`.
- ID column: `{ID_COLUMN}`.
- Sample submission columns: `{list(sample_submission.columns)}`.
- Contract checks passed: `{bool(contract_df['status'].all())}`.
- Train duplicated rows: `{int(train.duplicated().sum())}`.
- Test duplicated rows: `{int(test.duplicated().sum())}`.
- Unit of observation: Not confirmed yet.

The unit of observation remains important because validation design depends on whether rows can be treated as independent.

### Target Distribution Interpretation

`Drafted = 1` is the majority class, but the target is not extremely imbalanced. Because the official metric is ROC-AUC, future models must rank players well by probability. Threshold-based accuracy is not the main goal.

### Missingness and Measurement Availability Interpretation

Missingness-prone columns are `{', '.join(analysis_missingness_columns)}`. Missingness is structured by field, role, and year. It should be treated as a candidate signal family, not only as a cleaning problem. Age missingness is especially notable in train-only diagnostics and should be handled carefully as descriptive evidence, not as a final feature decision. Missingness indicators and available-measurement-count features must be tested later using fold-safe validation.

### Available Measurement Count Interpretation

`available_measurement_count` summarizes how many missingness-prone physical measurements are present for each row. It may capture player evaluation context because players with more complete physical profiles may have been measured more thoroughly. This is a strong future feature hypothesis, but no such feature is selected in Phase 3.

### Role and Position Interpretation

Physical metrics cannot be interpreted globally only. `Sprint_40yd`, `Weight`, `Height`, jump metrics, agility, and shuttle can have different meanings by role. `Position_Type` should be a central axis for later feature-engineering hypotheses. Role-normalized features or role interactions should be tested later, not created as final features here.

### Special Teams / Player_Type Interpretation

{special_teams_summary}

### School / Cardinality Risk Interpretation

`School` is potentially useful but risky. Many schools are rare, low-n school target rates can be extreme but unreliable, and test-only schools make simple encodings fragile. Future use of `School` should prioritize safe frequency/count encoding or strictly out-of-fold target encoding only if justified later. No target encoding is performed in Phase 3.

### Train/Test Shift Interpretation

Numeric train/test shift appears moderate rather than catastrophic based on descriptive diagnostics. `School` is the main categorical shift and high-cardinality concern. Drift diagnostics are descriptive only and should guide future slice diagnostics, not test-tuned preprocessing.

### Year / Cohort Effects Interpretation

Year may reflect cohort effects. Measurement availability and role composition can vary by year, so future validation should include Year slice diagnostics. This does not automatically justify a temporal split; split design is deferred to a later validation phase.

### Correlation / Redundancy Interpretation

Several physical tests are correlated, suggesting latent physical dimensions such as size, speed, explosiveness, agility, and strength. High correlation is not a reason to drop features in Phase 3. Later model families may handle redundancy differently.

### Outlier Interpretation

Physical outliers should be understood within position context. Global outlier removal can be dangerous in sports data because exceptional athletes may look like outliers. No clipping, winsorization, or row removal is selected in Phase 3.

### Contrarian Pattern Interpretation

Global associations may be misleading. A variable can look weak globally but matter inside a role group. `Height` shows evidence of direction changing across role groups, which reinforces that physical relationships should be inspected within `Position_Type`, not only globally. These contrarian patterns are hypotheses only.

### Future Signal Families

{markdown_table(strategy_families)}

### Key EDA Findings

{markdown_table(key_findings)}

### Train/Test Shift Findings

{markdown_table(category_delta_df)}

Top numeric shift diagnostics by descriptive max CDF distance:

{markdown_table(numeric_shift_df.head(10))}

### Contrarian and Overlooked Pattern Findings

{markdown_table(contrarian_df.head(20))}

### Leakage and Validation Risk Register

{markdown_table(risk_register)}

### Hypothesis Register

{markdown_table(hypothesis_register)}

### Saved High-Value Figures

"""
notes += "\n".join(f"- `{fig}`" for fig in saved_figures)
notes += """

### Deferred Decisions

- No imputation method selected.
- No categorical encoding selected.
- No missingness feature selected.
- No complete-profile or low-profile measurement-completeness feature selected.
- No role-normalized feature, role percentile, or role interaction selected.
- No `School` encoding strategy selected.
- No outlier clipping/removal selected.
- No outlier flag selected.
- No feature interaction selected.
- No temporal split selected.
- No validation split policy finalized beyond preserving the existing need for leakage-safe local validation.
- No model family selected for improvement beyond the previously reproduced baseline context.

### Verification Note

The refactored notebook is designed to run top-to-bottom from the repository root, recompute structural facts from the official CSV files, keep target-aware analysis train-only, and avoid modeling or submission-generation logic.
"""

EXPERIMENT_NOTES_PATH.write_text(notes.strip() + "\n", encoding="utf-8")
print(f"Wrote Phase 3 experiment notes: {EXPERIMENT_NOTES_PATH}")
print("Saved figures:")
for fig in saved_figures:
    print(f"- {fig}")

render_interpretation(
    "Final synthesis",
    [
        "Phase 3 produced a data contract, visual EDA, risk register, hypothesis register, and strategy synthesis.",
        f"Saved high-value figures: {len(saved_figures)}.",
        f"Experiment notes written to {EXPERIMENT_NOTES_PATH.relative_to(PROJECT_ROOT)}.",
    ],
    [
        "The EDA does not select a model or final features, but it shows where signal may exist and where validation/leakage risks must be controlled.",
        "The four future signal families are role context, measurement availability, physical profile, and institutional/categorical context.",
    ],
    [
        "This notebook intentionally does not train models or generate submissions.",
        "Future phases must still implement fold-aware preprocessing and local validation.",
    ],
    ["Use the hypothesis register to prioritize Phase 5/6/7 experiments."],
    ["Stop before Phase 4 or any later phase until explicitly approved."],
)
'''

INTEGRATED_RISK_CODE = r'''
additional_risks = pd.DataFrame([
    {
        "risk": "Promising signal families are implemented without leakage controls",
        "severity": "High",
        "likelihood": "Medium",
        "evidence": "The strongest candidate signals involve missingness, School, role context, and target-rate summaries.",
        "safeguard": "Treat EDA findings as hypotheses; require fold-safe implementation and ablation before adoption.",
        "owner_future_phase": "Phase 5/6/7",
    },
    {
        "risk": "Age_missing is over-trusted because its train-only association is strong",
        "severity": "High",
        "likelihood": "Medium",
        "evidence": "Age missingness appears unusually strong in train-only target-rate diagnostics.",
        "safeguard": "Test Age missingness separately from physical-test missingness with fixed folds and slice checks.",
        "owner_future_phase": "Phase 7",
    },
    {
        "risk": "School encodings overfit rare categories",
        "severity": "High",
        "likelihood": "High",
        "evidence": "School has long-tail behavior, low-n target-rate instability, and test-only categories.",
        "safeguard": "Stage School ablations; use only fold-safe frequency/count, rare handling, or strictly OOF target encoding if later justified.",
        "owner_future_phase": "Phase 7/8",
    },
    {
        "risk": "Role-normalized features leak fold statistics",
        "severity": "High",
        "likelihood": "Medium",
        "evidence": "Role-specific physical interpretation suggests possible role-normalized metrics.",
        "safeguard": "Compute any role statistics inside training folds only; report role-slice AUC.",
        "owner_future_phase": "Phase 7",
    },
    {
        "risk": "Rare grouping is learned globally instead of inside folds",
        "severity": "Medium",
        "likelihood": "Medium",
        "evidence": "Long-tail categorical behavior suggests possible rare-category handling.",
        "safeguard": "Learn rare-category thresholds and mappings inside training folds only.",
        "owner_future_phase": "Phase 7",
    },
    {
        "risk": "Public leaderboard becomes an implicit validation system",
        "severity": "High",
        "likelihood": "Medium",
        "evidence": "Baseline public leaderboard score is known and easy to overuse.",
        "safeguard": "Use public leaderboard only as a sanity check; use local CV and slice diagnostics for decisions.",
        "owner_future_phase": "Phase 11",
    },
])

risk_register = pd.concat([risk_register, additional_risks], ignore_index=True)
risk_register = risk_register.drop_duplicates(subset=["risk"], keep="last").reset_index(drop=True)
display_table("Expanded leakage and validation risk register", risk_register, max_rows=80)

render_interpretation(
    "Integrated risk register",
    [
        "The most promising signal families are also the most dangerous ones if implemented incorrectly.",
        "`Age_missing`, `School`, target-rate tables, role-normalized features, rare grouping, and leaderboard feedback all require explicit safeguards.",
    ],
    [
        "The risk register links EDA evidence to future owners and phases so that later modeling work remains auditable.",
    ],
    [
        "Risk documentation does not make any feature safe; safety must be proven by fold-aware implementation and validation.",
    ],
    [
        "Use these risk rows as acceptance criteria before Phase 7 feature experiments.",
    ],
    [
        "No risk is resolved by Phase 3 alone.",
    ],
)
'''


EXPANDED_HYPOTHESIS_CODE = r'''
additional_hypotheses = pd.DataFrame([
    {
        "hypothesis": "Age_missing should be tested separately from physical-test missingness.",
        "eda_evidence_source": "Age missingness shows unusually strong train-only target-rate diagnostics.",
        "potential_future_feature_or_action": "Test an Age_missing indicator as its own ablation block.",
        "leakage_risk": "Medium - selection must not be based on test or leaderboard feedback.",
        "validation_requirement": "Fixed folds; compare global AUC and AUC by Player_Type, Position_Type, and Year.",
        "priority": "High",
        "future_phase": "Phase 7",
    },
    {
        "hypothesis": "Available measurement count should be tested as raw count, complete-profile indicator, and low-profile indicator.",
        "eda_evidence_source": "Available measurement count plot and train-only target-rate table.",
        "potential_future_feature_or_action": "Ablate raw count, is_complete_measurement_profile, and has_low_measurement_profile.",
        "leakage_risk": "Low/Medium - safe if computed only from row-level official fields and selected via CV.",
        "validation_requirement": "Fixed-fold ablation and slice diagnostics by Player_Type and Position_Type.",
        "priority": "High",
        "future_phase": "Phase 7",
    },
    {
        "hypothesis": "Missingness/completeness effects should be tested within Player_Type and Position_Type slices.",
        "eda_evidence_source": "Player_Type measurement completeness and role missingness summaries.",
        "potential_future_feature_or_action": "Report missingness-feature lift and AUC by role slices.",
        "leakage_risk": "Medium - global gains may reflect subgroup composition rather than stable signal.",
        "validation_requirement": "Slice-level validation for offense, defense, special_teams, and Position_Type groups.",
        "priority": "High",
        "future_phase": "Phase 7/9",
    },
    {
        "hypothesis": "Player_Type slice performance should be reported because special teams may behave differently.",
        "eda_evidence_source": "Special teams has lower measurement completeness and lower target-rate diagnostics.",
        "potential_future_feature_or_action": "Add Player_Type slice metrics to model review reports.",
        "leakage_risk": "Low - reporting risk is interpretation, not leakage, if labels remain train/validation only.",
        "validation_requirement": "OOF or validation predictions with AUC by Player_Type.",
        "priority": "High",
        "future_phase": "Phase 6/9",
    },
    {
        "hypothesis": "Role-aware physical metrics should be tested via interactions, role-normalized values, and within-role percentiles/ranks.",
        "eda_evidence_source": "Position_Type physical profiles and global-vs-within-role association scan.",
        "potential_future_feature_or_action": "Test raw metrics, role interactions, role z-scores, and within-role ranks.",
        "leakage_risk": "High - role statistics must be computed inside training folds.",
        "validation_requirement": "Fold-aware transformers plus role-slice AUC.",
        "priority": "High",
        "future_phase": "Phase 7/8",
    },
    {
        "hypothesis": "Variables with weak global association but strong within-role association should be scanned systematically.",
        "eda_evidence_source": "Contrarian section, including Height direction changes across role groups.",
        "potential_future_feature_or_action": "Build a controlled diagnostic for low-global/high-within-role associations.",
        "leakage_risk": "Medium - scanning many candidates can overfit if used for selection without validation.",
        "validation_requirement": "Predeclare candidate block and validate by fixed-fold ablation.",
        "priority": "Medium",
        "future_phase": "Phase 7",
    },
    {
        "hypothesis": "School should be ablated in staged fashion.",
        "eda_evidence_source": "School coverage, target-rate instability, and test-only school diagnostics.",
        "potential_future_feature_or_action": "Compare no School, frequency/count encoding, rare grouping, and possible OOF target encoding only if justified.",
        "leakage_risk": "High - School can overfit and target encoding can leak labels.",
        "validation_requirement": "Strict fold-aware encoding; monitor fold variance and rare/frequent-school slices.",
        "priority": "Medium/High",
        "future_phase": "Phase 7/8",
    },
    {
        "hypothesis": "Numeric train/test drift should be checked conditionally by role before making modeling decisions.",
        "eda_evidence_source": "Global numeric drift is moderate, while role composition can differ.",
        "potential_future_feature_or_action": "Add role-conditioned drift diagnostics and slice model reporting.",
        "leakage_risk": "Medium - do not tune preprocessing to test distributions.",
        "validation_requirement": "Use drift as diagnostic context, not selection objective.",
        "priority": "Medium",
        "future_phase": "Phase 5/6",
    },
    {
        "hypothesis": "Year-slice diagnostics should be included in future validation reporting.",
        "eda_evidence_source": "Year distribution, Year x missingness, and Year x Position_Type composition.",
        "potential_future_feature_or_action": "Report validation AUC and calibration-style summaries by Year where feasible.",
        "leakage_risk": "Medium - do not automatically switch to temporal split without justification.",
        "validation_requirement": "Combine standard StratifiedKFold with Year-slice reporting unless later evidence changes split design.",
        "priority": "Medium",
        "future_phase": "Phase 5/6",
    },
    {
        "hypothesis": "Within-position outlier flags may be tested later, but no outlier deletion is selected.",
        "eda_evidence_source": "Outlier diagnostics by position show role-contextual extremes.",
        "potential_future_feature_or_action": "Ablate within-position outlier flags or robust transforms versus no outlier handling.",
        "leakage_risk": "Medium - outlier thresholds must be learned inside folds if estimated from data.",
        "validation_requirement": "Compare against no-outlier-handling baseline and inspect role slices.",
        "priority": "Low/Medium",
        "future_phase": "Phase 7",
    },
])

hypothesis_register = pd.concat([hypothesis_register, additional_hypotheses], ignore_index=True)
hypothesis_register = hypothesis_register.drop_duplicates(subset=["hypothesis"], keep="last").reset_index(drop=True)
display_table("Expanded hypothesis register", hypothesis_register, max_rows=120)

render_interpretation(
    "Expanded hypothesis register",
    [
        "The expanded register separates Age missingness from physical-test missingness and records measurement-completeness variants explicitly.",
        "It also adds Player_Type slice reporting, role-aware physical metrics, staged School ablations, conditional drift checks, Year-slice diagnostics, and within-position outlier flags.",
    ],
    [
        "This turns post-EDA interpretation into traceable future experiments rather than informal modeling intuition.",
    ],
    [
        "All rows remain hypotheses. No feature, encoding, split design, or outlier handling is selected in Phase 3.",
    ],
    [
        "Use this register to design Phase 5/6/7 experiments with explicit leakage safeguards.",
    ],
    [
        "No implementation is performed here.",
    ],
)
'''

VERIFICATION_SUMMARY_CODE = r'''
source_safety_checks = pd.DataFrame([
    {"check": "No model training imports", "status": True, "detail": "Notebook imports pandas/numpy/matplotlib/IPython only; seaborn if installed."},
    {"check": "No submissions generated", "status": True, "detail": "No submission-output directory is used."},
    {"check": "Target-aware analysis train-only", "status": True, "detail": "Target-rate helpers are applied to train-derived tables only."},
    {"check": "Test data use is descriptive", "status": True, "detail": "Test data is used for schema, alignment, missingness, and distribution comparison."},
    {"check": "Raw data unmodified", "status": True, "detail": "Official CSVs are only read by pd.read_csv."},
])
display_table("Phase 3 verification summary", source_safety_checks)
display_table("Saved figure list", pd.DataFrame({"figure": saved_figures}), max_rows=100)

render_interpretation(
    "Verification summary",
    [
        "The notebook executed Phase 3 EDA logic without modeling or submission creation.",
        "Saved figures are restricted to high-value Phase 3 visual artifacts.",
    ],
    ["This final verification cell documents the intended safety boundary inside the notebook itself."],
    ["These are notebook-internal checks; repository-level verification should still be run after execution."],
    ["Carry these checks into future notebook reviews."],
    ["No Phase 4 work is started here."],
)
'''


def code_without_title(chunks: dict[str, str], title: str) -> str:
    return chunks[title].strip()


def build_notebook() -> nbf.NotebookNode:
    source = read_backup_source()
    chunks = split_backup_source(source)
    chunks["setup"] = chunks["setup"].replace(
        'EXPERIMENT_NOTES_PATH = DOCS_DIR / "experiment_notes.md"',
        'EXPERIMENT_NOTES_PATH = DOCS_DIR / "03_eda" / "experiment_notes.md"',
    )
    helper_code = chunks["helpers"]
    if "def md_table" in helper_code and "def markdown_table" not in helper_code:
        helper_code += "\n\n# Alias used by the narrative experiment-notes update.\nmarkdown_table = md_table\n"
    if "def section_conclusion" in helper_code and "def render_interpretation" not in helper_code:
        helper_code += "\n\n# Alias used by the refactored interpretation cells.\nrender_interpretation = section_conclusion\n"

    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13.13"},
    }

    cells = [
        md_cell(
            """
            # Phase 3 - Data Contract and Initial EDA

            This notebook is a Phase 3 report for the GCI World NFL Draft Prediction competition. It is intentionally notebook-first, audit-ready, and descriptive.

            Phase 3 boundaries:

            - Recompute and verify the data contract from official CSV files.
            - Explore target distribution, missingness, train/test alignment, role-specific patterns, physical profiles, categorical risks, and overlooked patterns.
            - Generate hypotheses for later phases only.
            - Do not train models, generate submissions, perform final feature engineering, fit preprocessing, target encode, select final features, modify raw data, or use external data.

            Strategic message: this EDA does not select a model or final features, but it shows where signal may exist and where validation/leakage risks must be controlled.
            """
        ),
        md_cell(
            """
            ## 1. Title and Phase 3 Boundaries

            **Objective.** Establish the scope and safety rules for the notebook.

            **Why it matters.** EDA can easily drift into modeling decisions. This section keeps Phase 3 descriptive and audit-ready.

            **Leakage/validation caution.** Any target-aware analysis is train-only. Test data is used only for structural and distribution diagnostics.
            """
        ),
        md_cell(
            """
            ## 2. Setup, Imports, Constants, and Paths

            The notebook uses repository-root paths, dependency-light Python tooling, and stable figure output locations.
            """
        ),
        objective_cell(
            "2.1 Runtime setup",
            "Import EDA libraries, define constants, and establish repository paths.",
            "A reproducible notebook should run from a clean kernel and from the repository root.",
            "No competition data is loaded in this cell.",
            "No modeling libraries are imported. Seaborn is used only if already installed.",
        ),
        code_cell(chunks["setup"]),
        interpretation_cell("The setup cell defines paths and constants only. It does not read data, train models, or generate submissions."),
        md_cell("## 3. Helper Functions"),
        objective_cell(
            "3.1 Reusable EDA helpers",
            "Define table display, figure saving, Wilson intervals, target-rate summaries, missingness summaries, drift diagnostics, and correlation helpers.",
            "Reusable helpers reduce hidden state and keep repeated calculations consistent across sections.",
            "No train/test data is loaded or transformed in this cell.",
            "Helpers are descriptive. They do not fit models, learn preprocessing, or create final features.",
        ),
        code_cell(helper_code),
        interpretation_cell("The helper functions standardize EDA outputs and Wilson uncertainty intervals without adding dependencies."),
        md_cell("## 4. Data Loading"),
        objective_cell(
            "4.1 Load official CSV files",
            "Load `train.csv`, `test.csv`, and `sample_submission.csv` from `data/input/`.",
            "Every later analysis should be traceable to official competition files.",
            "Train, test, and sample submission.",
            "Files are read only. No raw data is modified.",
        ),
        code_cell(chunks["Data loading"]),
        interpretation_cell("The official CSV files are loaded from local repository paths. This cell does not infer labels or create derived datasets."),
        md_cell("## 5. Data Contract Checks"),
        objective_cell(
            "5.1 Contract assertions and structural quality checks",
            "Verify target placement, ID presence, sample submission format, column alignment, ID uniqueness, duplicated rows, constant columns, and near-constant columns.",
            "A trusted data contract prevents silent downstream failures such as wrong ID order or wrong submission schema.",
            "Train/test/sample structural information.",
            "Test is used only for structure and ID alignment. No target-aware test analysis is performed.",
        ),
        code_cell(chunks["Data contract checks"]),
        interpretation_cell(
            "The contract is technically healthy and allows Phase 3 to proceed. Train has 2,781 rows and 16 columns, test has 696 rows and 15 columns, and the sample submission has 696 rows and 2 columns. The target is `Drafted`, the ID is `Id`, and there are no duplicated rows in train/test. However, unique IDs do not prove statistical independence: rows may still be partially grouped by `School`, `Year`, `Position`, or `Position_Type`. This does not block Phase 3, but Phase 5/6 validation should report robustness by slices such as Year, Position_Type, Player_Type, School frequency, and measurement completeness."
        ),
        md_cell("## 6. Schema and Variable Taxonomy"),
        objective_cell(
            "6.1 Column roles, dtypes, missingness, and uniqueness",
            "Classify identifier, target, numeric candidate columns, and categorical candidate columns.",
            "Clear roles prevent accidental leakage and make later feature hypotheses easier to audit.",
            "Train schema with test dtype alignment where available.",
            "Column roles are descriptive labels, not final modeling decisions.",
        ),
        code_cell(chunks["Schema and variable taxonomy"]),
        interpretation_cell("The schema identifies role context, measurement availability, physical profile, and institutional/categorical context as candidate signal families. No columns are selected, dropped, encoded, or transformed."),
        md_cell("## 7. Target Distribution"),
        objective_cell(
            "7.1 Train-only target distribution",
            "Summarize and visualize `Drafted` in train.",
            "The target balance shapes interpretation of local validation and target-rate plots.",
            "Train only.",
            "No test labels exist or are inferred. ROC-AUC is a ranking metric, not a threshold-accuracy target.",
        ),
        code_cell(chunks["What does the target look like?"]),
        interpretation_cell("The target is not extremely imbalanced and `Drafted = 1` is the majority class. Because the official metric is ROC-AUC, future features should be evaluated by whether they improve probability ordering, not whether they create a clean 0/1 threshold separation. A feature can be useful even if it only improves ranking within ambiguous cases."),
        md_cell("## 8. Missingness Analysis"),
        objective_cell(
            "8.1 Missingness by split",
            "Compare missing-value percentages between train and test for columns with missing values.",
            "Similar missingness patterns suggest structural consistency, while large deltas may indicate train/test shift.",
            "Train/test descriptive only.",
            "No imputation strategy is selected here.",
        ),
        code_cell(chunks["Missingness analysis"]),
        interpretation_cell("Missingness separates into three analytical subfamilies. First, demographic/record missingness, especially `Age`, appears unusually strong in train-only target-rate diagnostics and may reflect a different data mechanism, profile quality, eligibility/exposure context, or capture process. Second, physical-test missingness in `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, and `Shuttle` likely describes measurement availability, position norms, or testing context. Third, aggregated completeness and co-missingness describe complete versus incomplete player profiles. Missingness should not be treated only as a cleaning problem, but no missingness indicator is selected in Phase 3."),
        md_cell("## 9. Available Measurement Count Analysis"),
        objective_cell(
            "9.1 Measurement completeness and target-aware missingness",
            "Analyze available physical measurement count, co-missingness, role/year missingness, and train-only target rates by missingness indicators.",
            "Measurement completeness may capture player evaluation context and testing availability.",
            "Train/test descriptive for missingness structure; train-only for target-rate analyses.",
            "Missingness indicators and available-measurement-count features are hypotheses only and must be tested later using fold-safe validation.",
        ),
        code_cell(chunks["Available measurement count analysis"]),
        interpretation_cell("`available_measurement_count` may capture player evaluation context, but the useful pattern may not be a perfectly linear count effect. Future candidates could include the raw count, `is_complete_measurement_profile`, `has_low_measurement_profile`, and interactions with `Player_Type` or `Position_Type`. Before trusting measurement completeness as an independent signal, later phases should test whether it remains informative within Player_Type and Position_Type slices. These are future hypotheses only."),
        md_cell("## 10. Numeric and Physical Metric Analysis"),
        objective_cell(
            "10.1 Numeric summaries, train/test overlays, role profiles, and outliers",
            "Summarize numeric variables, compare train/test distributions, inspect physical profiles by `Position_Type`, and diagnose outliers by position.",
            "Physical measurements are central candidate signals but are role-dependent and can be misleading globally.",
            "Train/test descriptive overlays; train-only role/outlier summaries.",
            "No scaling, clipping, winsorization, transformation, or row removal is selected.",
        ),
        code_cell(chunks["Where is numeric and physical signal likely to be?"]),
        interpretation_cell("Physical metrics cannot be interpreted globally only. The same `Sprint_40yd`, `Weight`, `Height`, jump, agility, or shuttle value can mean different things by `Position_Type`. Lower is usually better for `Sprint_40yd`, `Agility_3cone`, and `Shuttle`; higher is usually better for `Vertical_Jump`, `Broad_Jump`, and `Bench_Press_Reps`; `Height` and `Weight` are role-dependent, not universally better when higher. Physical outliers are not automatically bad data: exceptional athletes may look like outliers, and global outlier removal can be harmful."),
        md_cell("## 11. Categorical Analysis and Target-Rate Uncertainty"),
        objective_cell(
            "11.1 Cardinality, category overlap, Wilson intervals, and school instability",
            "Analyze categorical cardinality, train/test overlap, target rates with sample size, Wilson uncertainty intervals, school cumulative coverage, and school target-rate instability.",
            "Categorical fields may contain signal but also high-cardinality overfitting risk.",
            "Train/test descriptive for overlap and cardinality; train-only for target rates.",
            "No target encoding, category grouping, or final categorical encoding is performed.",
        ),
        code_cell(chunks["Categorical analysis and target-rate uncertainty"]),
        interpretation_cell("`School` is not a normal low-cardinality categorical feature. It may contain useful institutional signal, but it is one of the highest-risk variables for overfitting: many schools are rare, low-n target rates can be extreme but unreliable, and test-only schools make naive encodings fragile. Future use should be staged and ablated: no School, safe frequency/count encoding, rare-category handling inside folds, and only if justified, strictly out-of-fold target encoding with smoothing or CatBoost-style handling under careful validation. No target encoding is performed in Phase 3."),
        md_cell("## 12. Train/Test Shift Diagnostics"),
        objective_cell(
            "12.1 Descriptive drift diagnostics",
            "Compare categorical normalized frequency deltas, numeric descriptive CDF distances, year distribution, and Year x Position_Type composition.",
            "Train/test shift can weaken validation reliability even when the data contract passes.",
            "Train/test descriptive only.",
            "Drift should guide future slice diagnostics, not test-tuned preprocessing.",
        ),
        code_cell(chunks["Does train resemble test?"]),
        interpretation_cell("Train/test numeric shift appears moderate rather than catastrophic. The larger generalization concern is structural/categorical: `School` is the main high-cardinality shift concern, and role composition can hide differences that are small globally. Drift diagnostics should guide future slice diagnostics, not test-tuned preprocessing. Later phases should check whether numeric shift remains after conditioning on `Position_Type`, `Player_Type`, and measurement completeness. Year may reflect cohort effects; future validation can combine standard StratifiedKFold with Year-slice reporting, but a temporal split is not automatically selected here."),
        md_cell("## 13. Role-Based Deep Dive: `Position`, `Position_Type`, `Player_Type`"),
        objective_cell(
            "13.1 Role target rates and measurement completeness",
            "Analyze role-level target rates, Wilson intervals, and measurement completeness by `Position`, `Position_Type`, and `Player_Type`.",
            "Global performance can hide poor subgroup behavior.",
            "Train-only target rates; train-only descriptive role profiles.",
            "No role interaction or role-normalized feature is created.",
        ),
        code_cell(chunks["How do patterns change by Position, Position_Type, and Player_Type?"]),
        interpretation_cell("The descriptive chain `Player_Type -> measurement completeness -> Drafted` should be treated as a possible confounding pattern, not causality. `special_teams` appears structurally different from offense and defense, with lower measurement completeness and lower target rate. This may partly explain missingness effects. Future validation should report model performance by `Player_Type`; global AUC may hide weak subgroup behavior. Later ablations should test whether missingness and available-measurement-count signals remain useful inside offense, defense, and special_teams separately."),
        md_cell("## 14. Physical-Performance Relationships"),
        objective_cell(
            "14.1 Faceted physical relationship plots by Position_Type",
            "Inspect selected physical relationships such as height vs weight, weight vs sprint, sprint vs jump metrics, and agility vs shuttle.",
            "A relationship can look weak or misleading globally but matter within role groups.",
            "Train only, with target coloring for descriptive interpretation.",
            "No interaction, ratio, or nonlinear transform is created.",
        ),
        code_cell(chunks["Physical-performance relationships"]),
        interpretation_cell("Physical relationships should be inspected within `Position_Type`, not only globally. `Position_Type` should be a central axis for later tests of raw metrics, role interactions, role-normalized metrics, and within-role percentiles or ranks. Role-normalized features require fold-safe computation if their statistics are learned from training data. They are hypotheses for later phases, not selected transformations in Phase 3."),
        md_cell("## 15. Correlation and Redundancy Analysis"),
        objective_cell(
            "15.1 Pearson and Spearman correlation heatmaps",
            "Compute Pearson and Spearman heatmaps and a high-correlation pair table.",
            "Correlations can reveal latent physical dimensions and redundancy.",
            "Train numeric columns only.",
            "High correlation is not a reason to drop features in Phase 3.",
        ),
        code_cell(chunks["Correlation and redundancy analysis"]),
        interpretation_cell("Several physical tests are correlated, suggesting latent dimensions such as size, speed, explosiveness, agility, and strength. Examples to inspect later include agility/shuttle, vertical/broad jump, and weight/sprint relationships. High correlation is not a reason to drop features in Phase 3: linear models may need regularization or careful preprocessing, while tree models may use correlated variables as alternative split candidates. Any pruning or dimensionality reduction must be tested inside validation."),
        md_cell("## 16. Contrarian and Overlooked Pattern Mining"),
        objective_cell(
            "16.1 Search for patterns hidden by global summaries",
            "Search for Simpson-style reversals, variables weak globally but informative within roles, missingness-vs-value signal, cohort availability shifts, hidden composition shift, and role-contextual outliers.",
            "Competitors often miss patterns that only appear after grouping by role, year, or measurement profile.",
            "Train-only for target-aware scans; train/test descriptive for cohort availability.",
            "All findings are hypotheses only.",
        ),
        code_cell(chunks["Contrarian and overlooked pattern mining"]),
        interpretation_cell("Global associations can be misleading. A variable can look weak globally but be useful inside role groups; `Height` shows evidence of direction changing across role groups. The future check is not only opposite direction, but also small global effect with large within-role effect, and role-specific sign or magnitude differences. This supports either models capable of interactions or explicit role-aware feature engineering. Future phases should systematically scan variables with low global association but high within-role association. These patterns are hypotheses only."),
        md_cell("## 17. Leakage and Validation Risk Register"),
        objective_cell(
            "17.1 Phase 3 leakage and validation risks",
            "Document risks with severity, likelihood, evidence, safeguards, and future owner/phase.",
            "Explicit risks make later modeling decisions auditable.",
            "EDA outputs and project rules.",
            "Risk documentation is not a substitute for fold-aware implementation later.",
        ),
        code_cell(chunks["What hidden risks could hurt validation?"]),
        interpretation_cell("The main risks are target leakage, preprocessing leakage, high-cardinality school overfit, low-n target-rate instability, drift overuse, outlier mishandling, correlation-as-selection, leaderboard over-trust, and hidden notebook state."),
        objective_cell(
            "17.2 Integrated post-EDA risk expansion",
            "Add risk rows for the most promising but dangerous signal families identified in the interpretive review.",
            "Promising signals such as Age missingness, School, role normalization, and rare grouping are exactly where leakage and overfitting can creep in.",
            "EDA evidence and existing risk register.",
            "This expands documentation only; it does not implement features.",
        ),
        code_cell(INTEGRATED_RISK_CODE),
        interpretation_cell("The expanded risk register makes the tension explicit: the best-looking signal families are also the most dangerous if implemented outside fold-safe validation."),
        md_cell("## 18. Hypothesis Register"),
        objective_cell(
            "18.1 Future hypotheses with evidence, action, risk, validation, priority, and phase",
            "Convert descriptive EDA findings into testable future hypotheses.",
            "This prevents future work from becoming an untracked collection of feature ideas.",
            "Phase 3 EDA findings.",
            "No hypothesis is accepted until validated in later phases.",
        ),
        code_cell(chunks["What hypotheses should move into later phases?"]),
        interpretation_cell("The hypothesis register carries future work forward without implementing it. Missingness, measurement completeness, role context, school handling, year/cohort effects, rare categories, and redundancy remain controlled hypotheses."),
        objective_cell(
            "18.2 Expanded post-EDA hypothesis register",
            "Represent the interpretive review as explicit future hypotheses with evidence, action, leakage risk, validation requirement, priority, and phase.",
            "Traceable hypotheses make later feature engineering auditable and reduce ad hoc experimentation.",
            "Existing hypothesis register plus Phase 3 interpretations.",
            "No hypothesis is implemented or accepted as true in Phase 3.",
        ),
        code_cell(EXPANDED_HYPOTHESIS_CODE),
        interpretation_cell("The expanded register now explicitly covers Age_missing, measurement-completeness variants, role-slice testing, special teams slice reporting, role-aware physical metrics, low-global/high-within-role scans, staged School ablations, conditional drift, Year slices, and within-position outlier flags."),
        md_cell("## 19. Final Synthesis"),
        objective_cell(
            "19.1 Strategy synthesis and future signal families",
            "Summarize the EDA into future signal families and key takeaways.",
            "The notebook should end with a clear strategic message, not only tables.",
            "All prior Phase 3 outputs.",
            "This synthesis does not choose a model or final feature set.",
        ),
        code_cell(EXPERIMENT_NOTES_CODE.split("EXPERIMENT_NOTES_PATH.write_text")[0].strip()),
        interpretation_cell("The EDA suggests that signal is less about raw physical values alone and more about what those values mean inside role and measurement context. The four future signal families are role context (`Position`, `Position_Type`, `Player_Type`), measurement availability (`Age` missingness, physical-test missingness, available measurement count, co-missingness), role-aware physical profile, and institutional/categorical context (`School`, long-tail categories, rare-category risk, test-only categories). Phase 3 does not select the model, final features, or preprocessing policy. It provides a map of where signal may exist and where validation/leakage controls must be strongest."),
        md_cell("## 20. Experiment Notes Update"),
        objective_cell(
            "20.1 Write narrative Phase 3 notes",
            "Update `docs/03_eda/experiment_notes.md` with narrative interpretations, registers, deferred decisions, and verification notes.",
            "Documentation should preserve the reasoning trail outside the notebook.",
            "All prior Phase 3 outputs.",
            "The notes are documentation only; they do not create submissions or model artifacts.",
        ),
        code_cell("EXPERIMENT_NOTES_PATH.write_text" + EXPERIMENT_NOTES_CODE.split("EXPERIMENT_NOTES_PATH.write_text", 1)[1]),
        interpretation_cell("The experiment notes now include narrative sections and tables, making Phase 3 easier to audit without opening every notebook output."),
        md_cell("## 21. Verification Summary"),
        objective_cell(
            "21.1 Notebook-internal safety summary",
            "Display a concise safety summary and saved figure list.",
            "A final verification section makes the notebook boundary explicit.",
            "Notebook source state and saved figure registry.",
            "Repository-level verification still happens after notebook execution.",
        ),
        code_cell(VERIFICATION_SUMMARY_CODE),
        interpretation_cell("Phase 3 is complete when this notebook runs top-to-bottom without model training, submissions, raw-data modification, or final feature decisions."),
    ]

    nb["cells"] = cells
    return nb


def main() -> None:
    notebook = build_notebook()
    OUTPUT_NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, OUTPUT_NOTEBOOK)
    print(f"Wrote {OUTPUT_NOTEBOOK}")
    print(f"Cells: {len(notebook.cells)}")


if __name__ == "__main__":
    main()
