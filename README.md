# PolicyGuard — GenLayer Intelligent Contract

Repository: https://github.com/cacx097/genlayer-intelligent-builder

PolicyGuard is a GenLayer-native semantic policy change oracle. It captures a validator-approved baseline for a public policy page and later asks GenLayer validators whether the live policy changed in a way that materially affects a user's rights, obligations, restrictions, eligibility, economic terms, deadlines, data use, enforcement consequences, or explicit exceptions.

## Why GenLayer

A byte hash can prove that text changed, but it cannot tell whether the meaning changed. A centralized LLM can make that judgment, but then the result depends on one trusted decision-maker.

PolicyGuard uses GenLayer web access plus the Equivalence Principle so a semantic decision can be validated by the network.

## Contract

`contracts/policy_guard.py`

Constructor:

- `policy_name: str`
- `source_url: str` — HTTPS only

Write methods:

- `capture_baseline()` — fetches the source and stores a validator-approved material-rules profile
- `check_for_material_change()` — fetches the current source and asks validators to agree on whether the change is material

View methods:

- `get_policy_name()`
- `get_source_url()`
- `is_baseline_ready()`
- `get_baseline_profile()`
- `get_last_assessment()`

## Consensus design

Baseline capture uses `prompt_non_comparative`: the leader produces a source-grounded profile and validators judge it against explicit criteria.

Change detection uses `prompt_comparative`: validators independently assess the current policy and must agree on both the verdict and the substance of the changed rule.

Fetched policy text is explicitly treated as untrusted evidence. Prompts instruct validators not to follow instructions embedded inside the fetched page.

## Example uses

- developer/API terms
- protocol or DAO governance rules
- rewards, points, or campaign terms
- marketplace seller rules
- automation and acceptable-use policies
- fee, eligibility, privacy, or enforcement changes

## Verification

Verified locally on Windows with Python 3.12:

- `genvm-lint check contracts/policy_guard.py` — PASS
- GenLayer schema extraction — PASS
- source/structure tests — 6 PASS

Hosted GenLayer Studio runtime was also exercised with the Builder wallet.

Deployed contract address: `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`

Runtime checks:

- contract deployment — accepted
- `capture_baseline()` — accepted
- `get_baseline_profile()` — accepted and returned a non-empty profile

The `genlayer-test 0.29.2` Direct Mode loader currently hits a Windows `WinError 32` while deleting a temporary stdin file that is still open. The Direct Mode tests remain in `tests/test_direct.py` and are skipped only on Windows so they can run on Linux/CI instead of masking the framework limitation.

## Local development

Python 3.12+ is recommended.

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
genvm-lint check contracts/policy_guard.py
python -m pytest -q
```

## Scope

This first release intentionally keeps one policy per deployed contract. That makes the state model small and auditable.

Good milestone extensions include multi-policy registries, policy history, scheduled/event-triggered checks, provenance snapshots, a lightweight dashboard, and webhook/API adapters for agent workflows.
