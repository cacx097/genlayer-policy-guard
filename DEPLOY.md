# Fast Hosted Studio Deployment

Use the same wallet that already has the GenLayer Builder role.

## File
C:\AI-Workspace\genlayer-policy-guard\contracts\policy_guard.py

## Constructor
- policy_name: GitHub Acceptable Use Policies
- source_url: https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies

## Minimal success path
1. Import/upload policy_guard.py into https://studio.genlayer.com/
2. Open the contract and click the run/deploy control.
3. Enter the constructor values above.
4. Deploy with the Builder wallet.
5. After deployment, call capture_baseline().
6. Call get_baseline_profile().
7. Record the deployed contract address and successful transaction/execution evidence.

## Reviewer-requested one-time baseline verification

For the corrected code at `contracts/policy_guard.py`, deploy a **new contract instance**. Do not assume the earlier Studio deployment includes this change.

1. Deploy with the same public policy name and HTTPS source URL, recording the **new** contract address.
2. Call `capture_baseline()` once using Send Transaction and confirm `Result: SUCCESS`.
3. Confirm `is_baseline_ready()` returns true and `get_baseline_profile()` returns non-empty text.
4. Call `capture_baseline()` a **second time**, only if willing to perform an expected-to-fail Studio test transaction. It must revert with `baseline is immutable after initial capture`. Verify the existing baseline still reads unchanged.
5. For a stronger preservation check, call `check_for_material_change()` and read `get_last_assessment()` before and after a repeat baseline attempt; the assessment should not be cleared.
6. Use the new GenLayer Explorer contract URL and the updated matching repository when editing the existing Portal submission. Do not create a duplicate submission.

The repeated failed transaction in step 4 is a purposeful regression check, not required if Studio cost or signer friction makes it undesirable. Its cost should be reviewed before execution.

## Pass condition
- Deployment reaches successful execution.
- capture_baseline() reaches successful execution.
- get_baseline_profile() returns non-empty text.

Do not submit to Portal before these three conditions are verified.
