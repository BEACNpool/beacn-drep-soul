# Changelog

## 2026-06-19
- `treasury_spending_doctrine.json` → v1.1.0: added `dossier_gate` with `mode: "soft"`.
  - **Why:** owner directive to empower the autonomous DRep to make on-chain decisions
    from the available repo context (proposal anchor + doctrine + reasoning lean) instead
    of returning NEEDS_MORE_INFO whenever a full diligence dossier is absent. The previous
    hard gate meant every treasury proposal without a hand-built dossier was held, so the
    DRep could not defend the treasury directionally.
  - **Effect:** a treasury action without a complete dossier is now judged directionally
    with a `-0.10` caution penalty (on top of the base treasury penalty and the conservative
    reasoning lean), so it typically resolves to **NO/ABSTAIN on thin asks** rather than a
    blanket hold — voting NO protects the treasury, it does not spend it. Incomplete diligence
    is still recorded as explicit uncertainty on every such rationale.
  - **Fail-safe:** the engine CODE default remains the strict `hard` gate; only this versioned,
    hashed doctrine file loosens it. Revert by setting `dossier_gate.mode` back to `"hard"`
    (or `BEACN_TREASURY_GATE_MODE=hard`).

## 2026-06-15
- `scoring_weights.json` → v1.1.0: reduced `drep_margin_cap` from 0.45 to 0.10.
  - **Why:** at 0.45 the network DRep vote distribution could single-handedly drive a
    directional vote (the non-treasury YES/NO threshold is only ±0.12). That contradicted
    README principle 14 ("do not optimize for popularity, social pressure, or delegation
    size") and `values_hierarchy.md`, which ranks "social consensus momentum" last (5th).
  - **Effect:** the network distribution may now only *inform* a vote (cap 0.10 < the 0.12
    directional threshold), never *determine* it. BEACN's own evidence-based penalties and
    bonuses must carry any directional call. This is a values-compliance fix, not a new value.
  - Engine code unchanged; the cap is read from this versioned, hashed file.

## 2026-03-24
- Initial doctrine established.
- Added reproducibility, uncertainty, and conflict-handling commitments.

## 2026-03-26
- Added action-specific doctrine modules: parameter changes, hard forks, committee updates, info actions, constitutional amendments.
- Added `GOVERNANCE_PHILOSOPHY.md` for human-readable rationale behind doctrine.
- Added `values_hierarchy.md` to make value conflicts explicit.
- Added `scoring_weights.json` as canonical auditable weights surface.
- Added `WHY_DELEGATE.md` for delegator-facing transparency.
- Updated principle 13 in README to point at `scoring_weights.json` (not embedded code).
