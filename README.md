# PolicyGuard — GenLayer Intelligent Contract

Repository: https://github.com/cacx097/genlayer-policy-guard

PolicyGuard is a GenLayer-native semantic policy change oracle. It stores a validator-approved baseline for a public policy page and later asks GenLayer validators whether a live policy changed in a way that materially affects users' rights, obligations, restrictions, eligibility, costs, deadlines, data use, enforcement, or exceptions.

## Why GenLayer

A byte-level diff cannot tell whether a change in wording changes policy meaning. PolicyGuard combines nondeterministic web access and the Equivalence Principle so semantic judgments can be validated by GenLayer rather than relying on a single centralized model.

## Contract

`contracts/policy_guard.py`

Constructor:
- `policy_name: str`
- `source_url: str` — HTTPS only

Write methods:
- `capture_baseline()` — initializes the baseline **once** using `prompt_non_comparative`. If `baseline_ready` is already true, it raises `baseline is immutable after initial capture` before fetching external content or modifying state.
- `check_for_material_change()` — compares the stored baseline with the current policy via `prompt_comparative` and stores the assessment.

Read methods:
- `get_policy_name()`
- `get_source_url()`
- `is_baseline_ready()`
- `get_baseline_profile()`
- `get_last_assessment()`

Both fetched policy content and baseline text are treated as untrusted evidence. Prompts explicitly reject instructions embedded in source documents.

## Reviewer-requested baseline protection

The initial deployment allowed repeated `capture_baseline()` calls, which could replace the baseline and clear the latest assessment. The revised source prevents repeat capture once initialization succeeds. It deliberately introduces **no public reset function**. `check_for_material_change()` remains callable after baseline initialization.

The local regression test directly executes the isolated capture method with a fake consensus implementation: first capture succeeds; a second capture raises a `UserError`; the stored baseline and existing assessment remain unchanged. The repeat-capture rejection is **locally tested**, not yet demonstrated through a separate intentionally failing Studio transaction.

## Verification

Local Windows / Python 3.12:
- `genvm-lint check contracts/policy_guard.py` — PASS
- GenLayer validation — PASS
- Structure and focused regression tests — **7 PASS**
- GenLayer Direct Mode tests — 3 SKIP on Windows due to a known `genlayer-test 0.29.2` temporary-file `WinError 32` before contract execution; Linux CI completion has not been confirmed

Hosted Studio, updated deployment (reported and checked through the user's Studio session):
- Contract address: `0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2`
- Explorer evidence URL: https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2
- Deployment of the updated source — SUCCESS
- `capture_baseline()` — **Result: SUCCESS**
- `get_baseline_profile()` — returned nonempty data
- `is_baseline_ready()` — returned `true`
- `check_for_material_change()` — **Result: SUCCESS**
- `get_last_assessment()` — returned nonempty output

Demo constructor:
- `policy_name`: `GitHub Acceptable Use Policies`
- `source_url`: https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies

Note: one intervening deployment used a malformed URL with trailing ` 3.` and failed a webpage fetch. A new instance with the corrected URL was deployed and the above runtime flow then succeeded.

Previous, **pre-fix** deployment (historical only): `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`. Do **not** submit that address as evidence of the baseline-protection change.

## Example uses

- API and marketplace usage policies
- Governance rules and protocol terms
- Rewards, points, or campaign policies
- Fees, eligibility, privacy, or enforcement changes

## Local development

Python 3.12+ recommended.

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
genvm-lint check contracts/policy_guard.py
python -m pytest -q
```

## Scope

This release monitors one HTTPS policy per deployed contract. Potential meaningful extensions include multi-policy registries, version history, provenance snapshots, and a lightweight dashboard. The existing Portal contribution requires editing/resubmission with the **updated** contract evidence, not creating a duplicate contribution.
