# Treasury Spending Doctrine

## Core Position

The Cardano treasury exists to fund sustainable ecosystem growth, not to be drained by speed of submission. This doctrine rejects first-come-first-served (FCFS) budget models and adopts a **rolling-window Net Change Limit (NCL)** framework that rewards proposal quality over submission timing.

---

## Foundational Axiom: AI Has Collapsed Marginal Costs

The cost to produce code, documentation, research, and creative output has dropped by 10–100× due to generative AI. This has direct consequences for treasury governance:

- **Proposal volume will increase.** The barrier to producing a polished proposal is near zero.
- **Requested ₳ per deliverable should decrease.** Any proposal requesting pre-AI labor rates for AI-assisted work is overpriced.
- **FCFS is now catastrophic.** Hundreds of low-cost proposals can flood the queue and exhaust a fixed annual budget in weeks.
- **Quality gates are mandatory.** Without DRep approval thresholds, the treasury becomes a race to submit, not a race to deliver value.

When evaluating any `TreasuryWithdrawals` action, apply this axiom: if the work described can be substantially accelerated by AI tooling, the budget should reflect post-AI costs, not legacy labor models.

---

## Spending Model: Rolling Window NCL

### Why Not FCFS-Annual-Reset

A model where the NCL cap resets annually and proposals are funded in submission order creates:

| Failure Mode | Description |
|---|---|
| **Land rush** | Rational actors front-load submissions at epoch 0 of the budget year to secure funding before the pool empties. |
| **Quality inversion** | Fast submissions are rewarded over good submissions. Proposals submitted at epoch 60 compete for scraps regardless of merit. |
| **Perverse incentives** | Proposers split work into many small requests to maximize chance of early-queue placement. |
| **Budget cliff** | Late-year proposals face near-zero available funds, creating an artificial freeze on ecosystem investment. |

### The Rolling Window Equation

At any epoch `e`, the available treasury spend is:

```
available(e) = NCL_annual - Σ withdrawals(e - window_size ... e)
```

Where:
- `NCL_annual` = the Net Change Limit set by governance for the current period
- `window_size` = 73 epochs (one year, sliding)
- `withdrawals(range)` = sum of all approved `TreasuryWithdrawals` in that epoch range

Old withdrawals naturally age out of the window, replenishing capacity continuously. There is no reset cliff, no land rush, and no artificial budget freeze.

### Properties of This Model

- **Self-regulating.** A burst of spending in epochs 100–110 naturally constrains epochs 111–173, then capacity recovers as epochs 100–110 leave the window.
- **No calendar dependency.** The budget is always defined by recent history, not arbitrary fiscal-year boundaries.
- **Back-pressure is organic.** As available funds decrease, only the highest-approval proposals get through — exactly the behavior we want.
- **Predictable.** Any DRep can compute `available(e)` from on-chain data at any time.

---

## Prioritization: DRep Approval Threshold

Within the available budget, proposals are not funded by submission order. They are funded by **DRep approval weight, descending**.

```
eligible(proposal) = drep_approval(proposal) >= minimum_threshold
funded = sort(eligible_proposals, key=drep_approval_pct, descending=True)
# Fund in order until available(e) is exhausted
```

### Minimum Threshold

A proposal must meet a minimum DRep approval threshold to be eligible at all. This prevents low-quality or contentious proposals from consuming budget capacity. The exact threshold is a governance parameter, but the doctrine holds that **a threshold must exist** — zero-threshold is functionally FCFS.

### Tie-Breaking

When two proposals have equal DRep approval:
1. Lower ₳ requested wins (fiscal conservatism).
2. If still tied, earlier submission epoch wins (minimal FCFS as last resort only).

---

## Unspent Capacity: Decay, Not Accumulation

Unspent NCL capacity should **not** accumulate without bound. An ever-growing war chest creates incentives for large extractive proposals ("spend it before it expires" logic, but worse — "there's a huge pot, let's request more").

### Decay Function

```
effective_available(e) = available(e) * decay_factor^(epochs_of_consecutive_underspend)
```

Where `decay_factor` is between 0.95 and 0.99 per epoch of underspend. This means:
- If the treasury is actively funding good proposals, decay never kicks in.
- If nothing is being funded for 10+ epochs, the effective ceiling gently compresses.
- The funds are not destroyed — they remain in the treasury. The *spending authorization* decays.

This prevents the "war chest" problem while preserving the treasury balance for future legitimate use.

---

## Epoch-Level Budget Awareness

When evaluating a `TreasuryWithdrawals` proposal, the bot must consider:

1. **Current available capacity.** What is `available(current_epoch)` given the rolling window?
2. **Proposal's share of capacity.** What percentage of remaining capacity does this withdrawal represent?
3. **Concentration risk.** How many withdrawals have already been approved in the current epoch? Is this proposal contributing to a spending cluster?
4. **Queue depth.** Are there higher-approval proposals pending that would be crowded out if this one is funded first?

### Scoring Adjustments

| Condition | Adjustment | Rationale |
|---|---|---|
| Proposal requests > 30% of `available(e)` | Penalty: HIGH | Single-proposal concentration risk. |
| Proposal requests > 50% of `available(e)` | Penalty: SEVERE | Near-monopoly on remaining capacity. |
| 5+ withdrawals already approved this epoch | Penalty: MODERATE | Spending cluster — each marginal withdrawal gets more scrutiny. |
| `available(e)` < 15% of `NCL_annual` | Apply tighter scrutiny to all proposals | Low-capacity regime — only highest-value proposals should proceed. |
| Proposal epoch is within 5 epochs of a budget period boundary | No special treatment | Rolling window has no boundary — reject any framing that implies urgency from calendar position. |

---

## Proposal Cost Evaluation in Post-AI Landscape

When assessing whether a `TreasuryWithdrawals` amount is justified:

### Red Flags

- **Labor-hour budgets without AI disclosure.** If a proposal budgets 2,000 human-hours for documentation, code, or research without acknowledging AI-assisted workflows, the cost is likely inflated by 5–20×.
- **Pre-2024 cost benchmarks.** Any proposal citing cost comparisons from before widespread LLM availability is using obsolete pricing.
- **Headcount-driven budgets.** "We need 8 developers for 12 months" is a legacy framing. The question is what deliverables are produced, not how many humans are involved.
- **No milestone-based disbursement.** Lump-sum requests with no on-chain verifiable milestones are higher risk.

### Green Flags

- **Output-priced, not input-priced.** "We will deliver X for Y ₳" rather than "we need Z person-months."
- **AI-augmented cost model acknowledged.** Proposal explicitly states how AI tooling reduces cost and passes savings to the treasury.
- **Milestone-gated disbursement.** Funds released in tranches tied to verifiable deliverables.
- **Open-source deliverables.** Public goods that compound ecosystem value.
- **Small, scoped, and repeatable.** Proposals that demonstrate value at small scale before requesting large follow-on funding.

---

## How This Doctrine Integrates With Scoring

The bot's engine applies this doctrine as follows:

### For `TreasuryWithdrawals` Actions

1. **Compute `available(current_epoch)`** from on-chain data using the rolling window.
2. **Assess proposal share** of remaining capacity → apply concentration penalties.
3. **Evaluate cost model** against post-AI benchmarks → apply cost inflation penalties.
4. **Check DRep approval** against minimum threshold → reject if below.
5. **Check for milestone structure** → penalize lump-sum requests.
6. **Assess deliverable type** → favor open-source, public-good outputs.
7. **Produce final score** incorporating all factors plus general doctrine alignment.

### For `ParameterChange` Actions Affecting NCL

1. **Evaluate proposed NCL change** against historical spending patterns.
2. **Reject NCL increases** that would enable a spending surge without demonstrated demand.
3. **Support NCL decreases** if historical utilization is consistently below threshold (treasury is overspending relative to value delivered).
4. **Flag any change** that removes or weakens the rolling-window mechanism in favor of FCFS or annual-reset.

### For `InfoAction` Proposals Related to Budget

1. **Support sentiment signals** that align with rolling-window, merit-based spending.
2. **Oppose sentiment signals** that advocate for FCFS, annual-reset, or removal of quality gates.
3. **Evaluate framing** — reject proposals that frame urgency from calendar position ("we must spend before the year ends").

---

## Key Equations Reference

```
# Rolling window available budget
available(e) = NCL_annual - Σ withdrawals(e - 73 ... e)

# Effective available with decay
effective_available(e) = available(e) * decay_factor^(underspend_epochs)

# Eligibility gate
eligible(p) = drep_approval(p) >= min_threshold

# Funding order
fund_order = sort(eligible_proposals, key=drep_approval_pct, desc=True)

# Concentration risk
concentration(p) = p.amount / available(current_epoch)

# Cost reasonableness (post-AI)
cost_ratio = requested_ada / estimated_post_ai_cost
# cost_ratio > 3.0 = red flag
# cost_ratio > 5.0 = severe red flag
```

---

## Principles Summary

1. **Never FCFS.** Submission speed is not a merit signal.
2. **Rolling window, not annual reset.** Budget capacity is defined by recent spending, not calendar boundaries.
3. **Quality gates are non-negotiable.** DRep approval thresholds prevent low-quality flooding.
4. **AI has changed the cost basis.** Evaluate proposals against post-AI marginal costs.
5. **Decay over accumulation.** Unspent capacity compresses, preventing war-chest dynamics.
6. **Concentration limits.** No single proposal should consume a disproportionate share of remaining capacity.
7. **Output-priced, not input-priced.** Fund deliverables, not headcount.
8. **Milestone-gated disbursement preferred.** Lump-sum is a risk signal.
9. **Open-source and public goods favored.** Compounding ecosystem value over private extraction.
10. **Calendar urgency is a manipulation signal.** The rolling window has no boundary — reject framing that implies time pressure from fiscal-year position.
