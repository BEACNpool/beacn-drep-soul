#!/usr/bin/env python3
"""Doctrine consistency linter for beacn-drep-soul.

Checks (all fail the run, none mutate anything):
  a. scoring_weights.json and treasury_spending_doctrine.json parse, and every
     value in scoring_weights.weights is a number.
  b. counterfactual_infrastructure_value.benefit_weights sum to 1.00 (+/- 1e-9).
  c. CHANGELOG.md contains an entry naming each JSON's "version" field.
  d. no *.bak* files anywhere in the repo (stray backups in the root are a
     loader-glob risk).
  e. every numeric threshold written in treasury_spending_doctrine.md appears
     somewhere in treasury_spending_doctrine.json.
  f. values_hierarchy.md contains no "soft gate" phrasing (the soft dossier
     gate was retired in doctrine v1.4.0).

Limits of check (e) — it is a best-effort regex, not a parser: it only sees
decimal literals (e.g. 0.95, 3.0) and integer percentages (e.g. 30%) in the md,
compares by absolute numeric value (so a -0.15 penalty and a 0.15 bonus are
indistinguishable), and ignores semver tokens (v1.6.0), prose figures like
"10-100x", bare epoch counts, and years. It catches a drifted or missing
threshold, not a misattributed one.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_json(name: str) -> dict | None:
    try:
        return json.loads((ROOT / name).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - any parse/read failure is a lint failure
        fail(f"{name}: does not load as JSON ({e})")
        return None


def iter_numbers(obj):
    """All numeric leaves in a JSON structure (bools excluded)."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from iter_numbers(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_numbers(v)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield float(obj)


def main() -> int:
    scoring = load_json("scoring_weights.json")
    treasury = load_json("treasury_spending_doctrine.json")

    # (a) weights are numbers
    if scoring is not None:
        weights = scoring.get("weights")
        if not isinstance(weights, dict) or not weights:
            fail("scoring_weights.json: 'weights' must be a non-empty object")
        else:
            for k, v in weights.items():
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    fail(f"scoring_weights.json: weights.{k} is not a number ({v!r})")

    # (b) counterfactual benefit_weights sum to 1.00
    if treasury is not None:
        bw = treasury.get("counterfactual_infrastructure_value", {}).get("benefit_weights", {})
        if not isinstance(bw, dict) or not bw:
            fail("treasury_spending_doctrine.json: counterfactual benefit_weights missing")
        else:
            total = sum(bw.values())
            if abs(total - 1.0) > 1e-9:
                fail(f"treasury_spending_doctrine.json: benefit_weights sum to {total!r}, not 1.00")

    # (c) CHANGELOG mentions each JSON's version
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    for name, data in (("scoring_weights.json", scoring), ("treasury_spending_doctrine.json", treasury)):
        if data is None:
            continue
        version = str(data.get("version", ""))
        if not version:
            fail(f"{name}: missing 'version' field")
        elif not re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.])", changelog):
            fail(f"CHANGELOG.md: no entry mentions {name} version {version}")

    # (d) no backup files in the repo
    for p in sorted(ROOT.rglob("*")):
        if ".git" in p.parts:
            continue
        if p.is_file() and ".bak" in p.name:
            fail(f"backup file present: {p.relative_to(ROOT)} (delete it; git history preserves)")

    # (e) md thresholds present in the JSON (best-effort; see module docstring)
    if treasury is not None:
        md = (ROOT / "treasury_spending_doctrine.md").read_text(encoding="utf-8")
        md = re.sub(r"\bv?\d+\.\d+\.\d+\b", " ", md)  # semver tokens are not thresholds
        json_values = {round(abs(v), 9) for v in iter_numbers(treasury)}
        md_values: set[float] = set()
        md_values.update(float(m) for m in re.findall(r"\b\d+\.\d+\b", md))
        md_values.update(int(m) / 100.0 for m in re.findall(r"\b(\d+)%", md))
        for v in sorted(md_values):
            if round(abs(v), 9) not in json_values:
                fail(
                    f"treasury_spending_doctrine.md names threshold {v} "
                    "which does not appear in treasury_spending_doctrine.json"
                )

    # (f) the soft gate is retired; values_hierarchy must not resurrect it
    vh = (ROOT / "values_hierarchy.md").read_text(encoding="utf-8")
    if re.search(r"soft[\s-]+(dossier[\s-]+)?gate|dossier[\s-]+soft[\s-]+gate", vh, re.IGNORECASE):
        fail("values_hierarchy.md: mentions the retired soft gate (hard gate is doctrine v1.4.0+)")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(f"{len(errors)} doctrine lint failure(s)", file=sys.stderr)
        return 1
    print("doctrine lint OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
