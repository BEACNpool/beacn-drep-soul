# Changelog

## 1.4.0 — 2026-07-09
- Restored the hard treasury dossier gate: missing evidence now yields `NEEDS_MORE_INFO`, not a
  penalty-driven directional `NO`.
- Adopted a balanced four-dimension treasury contract: ecosystem benefit, delivery confidence,
  cost efficiency, and downside protection.
- Directional `NO` now requires affirmative independently verified waste/harm evidence; absence of
  evidence is never treated as evidence against a proposal.
- Language-model analysis is advisory-only and cannot change the binding vote.

## 2026-07-04 (second entry)
- `treasury_spending_doctrine.json` → v1.3.0: `dossier_approval.mode = "agentic"` (owner
  directive: fully agentic end-to-end, human checks randomly via the website).
  - **What changed:** a machine-drafted diligence dossier no longer waits for a human
    `--approve`. It is auto-approved when it passes deterministic gates (7/7 sections
    grounded, anchor sha256 matches the drafting receipt, financial+risk extraction rows
    present) AND an independent model verification pass that re-checks every dossier FACT
    against the anchor text (≥90% supported, zero material discrepancies). Approval status
    is `approved_agentic`, with the full per-fact verification attestation published in the
    dossier receipt.
  - **Human role:** random spot-checks of the published dossiers/receipts/attestations on
    the public site. A confirmed fabricated or contradicted fact reverts the dossier and is
    a doctrine incident.
  - **Fail-safe:** verification failure keeps `dossier_complete: no` (soft-gate penalty and
    the wider ±0.12 threshold stay). Kill switch: `BEACN_DOSSIER_AUTOAPPROVE_DISABLED=1`.

## 2026-07-04
- `treasury_spending_doctrine.json` → v1.2.0 (owner directive: full system audit remediation).
  - **True flow basis:** the sustainability regime ratio is now enacted withdrawals vs TRUE
    treasury inflow (ada_pots treasury delta + enacted withdrawals = tau share + donations)
    over 36 epochs. The old fee-only inflow basis understated inflow ~500x and pinned every
    treasury action at "unsustainable" (ratio ~1776); the honest ratio at adoption is ~2.28 —
    still unsustainable under the unchanged thresholds (≤1.0 sustainable, >2.0 hard-no), so no
    vote direction changes, but the published claim is now correct and falsifiable.
  - **Profile rules (new):** deterministic treasury sub-profiles from the on-chain title
    (reimbursement / maintenance / event / general). Reimbursements are exempt from the
    `no_milestones` penalty — demanding milestone-gated disbursement from a one-time deposit
    reimbursement was a category error (seen live on the Ikigai action). The engine records
    the detected profile in the public facts.
- `values_hierarchy.md`: reconciled with the v1.1.0 soft gate (the "prefer NEEDS_MORE_INFO"
  default contradicted live doctrine), required rationales to attribute outstanding evidence
  honestly (proposer's homework vs BEACN's own), and codified that confidence measures
  verified evidence coverage, capped at 0.90 — never penalty size (the engine had published
  "confidence 1.0" on thin-evidence NO votes).

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
## 2026-07-10
- `treasury_spending_doctrine.json` → v1.5.0: added a project-neutral counterfactual infrastructure model.
  - Established service, builder workflow dependency, functional substitutability, and non-funding disruption risk are explicit verified benefit inputs.
  - Intrinsic merit is published separately from NCL/portfolio executability.
  - Founder preference and personal use have zero direct score weight.
