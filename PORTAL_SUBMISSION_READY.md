# PolicyGuard — existing contribution correction

## Where
GenLayer Portal → My Contributions / submitted contributions → PolicyGuard → Edit / Needs Action / Resubmit.

**Edit the existing contribution; do not create a duplicate.**

## Title
PolicyGuard — Semantic Policy Change Oracle

## Repository
https://github.com/cacx097/genlayer-policy-guard

## GenLayer Explorer contract evidence (fixed deployment)
https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2

## Current contract address
`0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2`

## Reviewer-response text (copy and paste)

Thank you for the review. I addressed the baseline lifecycle issue by making `capture_baseline()` a one-time initialization. The revised contract checks `baseline_ready` before fetching content or changing state and rejects any subsequent capture call with `baseline is immutable after initial capture`. No public reset method exists, so an arbitrary caller cannot replace the baseline or clear the saved assessment by invoking `capture_baseline()` again. A focused regression test covers first-time capture, repeat-call rejection, and preservation of both the baseline and prior assessment.

The corrected source has been published at https://github.com/cacx097/genlayer-policy-guard. I deployed the updated contract at 0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2. Hosted Studio verification succeeded: first `capture_baseline()` returned SUCCESS, `get_baseline_profile()` returned nonempty data, `is_baseline_ready()` returned true, `check_for_material_change()` returned SUCCESS, and `get_last_assessment()` returned nonempty data. The second-call rejection was confirmed in local regression tests rather than through a separate deliberately failing Studio transaction.

Updated Explorer contract evidence: https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2

## Verification status
- Source-level fix and local regression test — PASS
- GenVM lint / validation — PASS
- New Studio deployment and normal end-to-end functionality — SUCCESS
- Repeat-capture rejection on updated Studio instance — not directly executed
- Old pre-fix contract `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6` — historical only
- Portal resubmission — still pending user action

## Important
After updating the description and the required Explorer evidence, use the Portal's existing correction/resubmission action. Do not spend an additional contribution slot or repeat successful transactions.
