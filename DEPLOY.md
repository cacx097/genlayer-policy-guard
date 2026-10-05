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

## Pass condition
- Deployment reaches successful execution.
- capture_baseline() reaches successful execution.
- get_baseline_profile() returns non-empty text.

Do not submit to Portal before these three conditions are verified.
