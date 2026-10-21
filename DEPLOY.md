# PolicyGuard — verified updated deployment

## Code and deployment
Source: `contracts/policy_guard.py`

Fixed contract: `0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2`

GenLayer Studio Explorer: https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2

Historical pre-fix contract: `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`

## Constructor used
`policy_name`: `GitHub Acceptable Use Policies`

`source_url`: `https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies`

The exact URL is required. One earlier deployment accidentally included a trailing ` 3.`, and `capture_baseline()` failed with `WEBPAGE_LOAD_FAILED` / 404. The corrected new instance succeeded.

## Completed Studio verification
1. Updated contract deployed — SUCCESS.
2. `capture_baseline()` — SUCCESS on first call.
3. `get_baseline_profile()` — nonempty.
4. `is_baseline_ready()` — `true`.
5. `check_for_material_change()` — SUCCESS.
6. `get_last_assessment()` — nonempty.

## Protection of stored state
The revised method contains:

```python
if self.baseline_ready:
    raise gl.vm.UserError("baseline is immutable after initial capture")
```

A focused local test checks rejection of a second capture while preserving baseline and assessment. No second failed transaction was performed on the successful Studio deployment; do not claim otherwise. No further Studio transactions are needed for the ordinary Portal correction unless reviewers specifically demand additional on-chain proof.

## Next step
Update the existing Portal PolicyGuard **Needs Action** contribution (not a new slot), using the fixed contract's Explorer URL and this repository. Do not reference the old deployment as proof of the fix.
