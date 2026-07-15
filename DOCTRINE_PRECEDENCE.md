# Doctrine Precedence

When two doctrine sources conflict, the engine follows the highest-ranked source. Rank 1 wins
over everything below it.

```json
{
  "precedence": [
    "scoring_weights.json",
    "treasury_spending_doctrine.json",
    "<action_type>_doctrine.md",
    "values_hierarchy.md",
    "README.md"
  ]
}
```

1. `scoring_weights.json` — canonical numeric weights; the core fails closed without it.
2. `treasury_spending_doctrine.json` — machine-read treasury thresholds, adjustments, and gates.
3. The per-action `*_doctrine.md` module for the action's family.
4. `values_hierarchy.md` — cross-cutting conflict-handling defaults.
5. `README.md` principles — broadest statements, lowest precedence.

A detected conflict is a **doctrine incident**: the engine's behavior follows the ranking above,
and the conflict must be fixed by an explicit doctrine amendment with a changelog entry. Known
unresolved conflicts are tracked in `CHANGELOG.md` under "Known open reconciliations".
