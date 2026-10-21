# GenLayer Builder — PolicyGuard resubmission evidence

## Category
Intelligent Contracts

## Title
PolicyGuard — Semantic Policy Change Oracle

## One-line description
A GenLayer Intelligent Contract that uses validator-backed semantic consensus to distinguish meaningful changes in public policies from harmless wording edits.

## Reviewer request and fix
The original `capture_baseline()` could be called repeatedly by any user, replacing the baseline and clearing the previous assessment. The revised source now checks `baseline_ready` at the start of the method and raises `baseline is immutable after initial capture` if the baseline already exists. This is a one-time initialization design: no public reset or replacement method was added. The change-detection method remains available.

A focused local regression test verifies the initial capture, rejection of the second call, and preservation of both baseline and existing assessment.

## Why GenLayer
PolicyGuard uses nondeterministic public web access, LLM semantic analysis, non-comparative baseline validation, and comparative validation for assessing subsequent policy changes. Fetched policy pages are treated as untrusted evidence.

## Public code and evidence
Repository: https://github.com/cacx097/genlayer-policy-guard

Current (fixed) deployed contract: `0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2`

Current Studio Explorer evidence: https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2

Earlier (pre-fix) contract, retained for history only: `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`

## Verification
- GenVM lint and contract validation — PASS
- Local structure/regression tests — **7 PASS**, Windows Direct Mode **3 SKIP**
- New Studio deployment with the revised code — SUCCESS
- First `capture_baseline()` — SUCCESS
- `get_baseline_profile()` — nonempty
- `is_baseline_ready()` — `true`
- `check_for_material_change()` — SUCCESS
- `get_last_assessment()` — nonempty
- Second `capture_baseline()` expected rejection — locally verified via focused test; no second intentionally failing Studio transaction was performed
- Linux CI pass and independent live Explorer query — not claimed

## Portal action
Edit the existing PolicyGuard contribution marked **Needs Action** and replace the old Explorer evidence with the current contract URL. Update the reviewer response to explain the baseline immutability fix. **Do not create a new submission.** Portal resubmission remains a separate user action and has not been completed by this documentation update.
