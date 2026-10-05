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

The constructor also rejects non-HTTPS sources.

## Verification
Completed:

- genvm-lint: PASS
- contract validation: PASS
- schema extraction: PASS
- source/structure tests: 6 PASS
- hosted GenLayer Studio deployment: accepted
- capture_baseline(): accepted
- get_baseline_profile(): accepted with non-empty output

The Windows Direct Mode runner in genlayer-test 0.29.2 currently hits an upstream temporary-file WinError 32 before contract execution. Direct Mode tests are retained for Linux/CI and are skipped only on Windows.

## Public repository
https://github.com/cacx097/genlayer-policy-guard

## Deployment evidence
CONTRACT_ADDRESS_TODO

## Next milestones
1. Multi-policy registry and per-policy history
2. Scheduled or event-triggered checks
3. Source provenance and evidence snapshots
4. Lightweight frontend/dashboard
5. Webhook/API adapter for agent workflows
