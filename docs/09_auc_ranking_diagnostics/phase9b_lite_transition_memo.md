# Phase 9B-Lite Transition Memo

## Purpose
Document the intentional skip of a full Phase 9B and define the narrow handoff from Phase 9A into Phase 10 planning.

## Objective
Phase 9B-Lite exists to preserve the Phase 9A evidence trail while avoiding a longer diagnostic cycle that is not needed right now.
The project already has enough OOF-based evidence to move toward a complete Phase 10 planning package.

## Why a full Phase 9B is not necessary now
Phase 9A already answered the main ranking and robustness questions at the technical level.
It established the main carry candidate, the secondary candidate, and the drop-candidates without requiring new training or new selection logic.
Given the time constraint, a larger Phase 9B would add documentation cost without materially changing the next planning decision.

## Evidence inherited from Phase 9A
- M1 Logistic Regression is the main carry candidate with warnings.
- CatBoost remains a secondary observe candidate with warnings.
- XGBoost and LightGBM remain dropped for now.
- No final winner was selected.
- No submission was authorized.
- Phase 10 and Phase 11 remain locked.

## Decisions
- M1 advances as the primary candidate for Phase 10 planning.
- CatBoost remains a secondary observe candidate.
- XGBoost and LightGBM remain dropped for now.

## Risks to monitor in Phase 10
- `Age_missing=1`
- `Position=QB`
- CatBoost robust-slice instability
- M1 stability under future validation

## Explicit Non-Actions
- no notebook
- no new metrics
- no model training
- no HPO
- no ensemble
- no calibration
- no threshold tuning
- no submission
- no leaderboard
- no Phase 10 execution
- no Phase 11

## Recommended Next Step
Create a full Phase 10 planning package.
