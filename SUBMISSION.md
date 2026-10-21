# GenLayer Builder submission draft

## Category
Intelligent Contracts

## Title
PolicyGuard — Semantic Policy Change Oracle

## One-line description
A GenLayer Intelligent Contract that distinguishes meaningful policy changes from harmless wording edits using validator-backed semantic consensus.

## Problem
Public rules change frequently, but a byte-level diff cannot tell whether an edit actually changes what a user may, must, or should do. A centralized LLM can make that judgment, but it introduces a single trusted decision-maker.

## Solution
PolicyGuard records a validator-approved semantic baseline for a public policy URL, then later fetches the live policy and asks GenLayer validators whether the change is material.

A material change is defined as a change to obligations, prohibitions, permissions, eligibility, fees or economic terms, deadlines, data use, enforcement consequences, or explicit exceptions.

## Why GenLayer
PolicyGuard relies on capabilities that are central to GenLayer:

- web access from nondeterministic execution
- LLM-based semantic judgment
- non-comparative validation for baseline extraction
- comparative validation for change detection
- validator consensus instead of a centralized oracle

## Safety and robustness
Fetched policy text is treated as untrusted evidence. The prompts explicitly instruct validators not to follow instructions embedded in the fetched content.

The constructor also rejects non-HTTPS sources. After a successful `capture_baseline()`, any subsequent capture call reverts with `baseline is immutable after initial capture` before web access or consensus. This prevents an arbitrary caller from overwriting the baseline or clearing a prior assessment.

## Verification
Completed:

- genvm-lint: PASS
- contract validation: PASS
- schema extraction: PASS
- source/structure tests: 7 PASS, including a regression test for the immutable baseline
- hosted GenLayer Studio deployment: accepted
- capture_baseline(): accepted
- get_baseline_profile(): accepted with non-empty output
- check_for_material_change(): transaction accepted
- get_last_assessment(): accepted with non-empty output
- end-to-end baseline → change-check → assessment flow: verified in Hosted GenLayer Studio

The Windows Direct Mode runner in genlayer-test 0.29.2 currently hits an upstream temporary-file WinError 32 before contract execution. Direct Mode tests are retained for Linux/CI and are skipped only on Windows.

## Public repository
https://github.com/cacx097/genlayer-policy-guard

## Deployment evidence
0x57AF337b9ac18a9dC6890D5B3898097298EC65e6

## Reviewer-requested correction (pending new deployment)

Reviewer feedback: the original `capture_baseline()` was publicly callable more than once and could overwrite baseline data or clear the latest assessment. The revised contract rejects subsequent calls after successful initialization with `baseline is immutable after initial capture`. No public reset was added. A focused regression test confirms profile and assessment state are preserved.

The old deployment address above documents the **initial v0 instance**, not the patched code. Submit an updated Explorer address only after new Studio deployment and successful verification. Amend the existing `Needs Action` entry; do not duplicate the contribution.

## Next milestones
1. Multi-policy registry and per-policy history
2. Scheduled or event-triggered checks
3. Source provenance and evidence snapshots
4. Lightweight frontend/dashboard
5. Webhook/API adapter for agent workflows

## Hosted Studio runtime evidence
- Contract address: 0x57AF337b9ac18a9dC6890D5B3898097298EC65e6
- Deployment: Accepted
- capture_baseline(): Accepted
- get_baseline_profile(): Accepted with non-empty returned profile
- check_for_material_change(): Transaction Accepted
- get_last_assessment(): Accepted with non-empty returned assessment

## Review requested: baseline immutability

The reviewer requested an immutable baseline lifecycle. The revised `capture_baseline()` rejects a second invocation after successful initialization and preserves the baseline and existing assessment. The existing deployed contract address above is **pre-fix**. A new Hosted Studio deployment and corresponding updated Explorer evidence are required before resubmission. Do not describe the prior deployment as containing this fix.
