# PolicyGuard — GenLayer Intelligent Contract

Repository: https://github.com/cacx097/genlayer-policy-guard

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

- `capture_baseline()` — one-time initialization that fetches the source and stores an immutable validator-approved baseline; repeated calls revert before modifying state **once**; subsequent calls revert without changing the baseline or assessment
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

## Review-requested security fix (pending redeployment)

The source code now prevents a second `capture_baseline()` call once `baseline_ready` is true. This protects the baseline and the last assessment from arbitrary re-initialization. Regression testing covers the first successful capture and rejection of a second call without changing existing state.

**Deployment distinction:** the earlier Studio contract `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6` was deployed *before* this security fix and must not be presented as evidence of the fixed code. A new deployment and Explorer contract URL are required before Portal resubmission.

## Verification

Verified locally on Windows with Python 3.12:

- `genvm-lint check contracts/policy_guard.py` — PASS
- GenLayer schema extraction — PASS
- source/structure tests — 7 PASS, including repeat-capture rejection and preserved assessment

Hosted GenLayer Studio runtime was also exercised with the Builder wallet.

Deployed contract address: `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`

Runtime checks:

- contract deployment — accepted
- `capture_baseline()` — accepted
- `get_baseline_profile()` — accepted and returned a non-empty profile
- `check_for_material_change()` — transaction accepted
- `get_last_assessment()` — accepted and returned a non-empty assessment

This confirms the deployed contract completed the full baseline → semantic change check → assessment retrieval flow in Hosted GenLayer Studio.

The `genlayer-test 0.29.2` Direct Mode loader currently hits a Windows `WinError 32` while deleting a temporary stdin file that is still open. The Direct Mode tests remain in `tests/test_direct.py` and are skipped only on Windows so they can run on Linux/CI instead of masking the framework limitation.

## Builder review remediation (pending redeployment)

GenLayer Portal requested that an arbitrary caller must not be able to replace the baseline or erase the last assessment by calling `capture_baseline()` again.

The current source code now makes baseline initialization one-time: once `baseline_ready` is true, `capture_baseline()` raises `gl.vm.UserError("baseline is immutable after initial capture")` before fetching external content or changing stored state. There is deliberately no reset method. `check_for_material_change()` remains callable after the baseline is captured.

A focused regression test checks that the first capture is allowed, the second is rejected, and both the saved profile and the saved assessment remain unchanged. Local structure tests: 7 passed; 3 separate GenLayer Direct Mode tests are skipped on Windows owing to the known runner issue. The GenVM lint and validation checks passed locally.

**The historical Studio deployment address above references the earlier version and has NOT been updated.** A new Studio deployment, baseline capture, second-call rejection, and new Explorer address are required before submitting the fix for review.

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

## Review-requested hardening (2026-10-22)

The revised source prevents a second `capture_baseline()` call after the initial capture, rejecting it before web access or consensus and preserving both the stored baseline and prior assessment. A focused regression test verifies this behavior. The original deployed contract address above refers to the **pre-fix** deployment; this revised source still requires a new Hosted Studio deployment and updated Explorer evidence before the Portal review request can be resubmitted.
