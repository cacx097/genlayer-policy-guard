# GenLayer Builder Tutorial: Immutable Baselines and Semantic Policy Checks

This is an independently written, reproducible tutorial based on the PolicyGuard example deployed in GenLayer Studio. It is educational material; publishing it does **not** itself earn GLP, and any program eligibility must be verified in the GenLayer Portal before submission.

## What we are building

Traditional change monitors tell you when the bytes on a policy webpage change. PolicyGuard asks whether the *meaning* changes in ways that affect users: obligations, restrictions, fees, eligibility, deadlines, data use, enforcement, or exceptions.

The intelligent contract does two separate jobs:

1. Initialize a one-time semantic baseline from a public policy webpage.
2. Re-read that page and ask validators to assess whether a material policy change occurred.

The example uses GenLayer nondeterministic web access and an Equivalence Principle to validate LLM-generated judgments.

Source code: https://github.com/cacx097/genlayer-policy-guard/blob/main/contracts/policy_guard.py

## Requirements

- A GenLayer Studio account/wallet able to deploy a contract.
- The public contract code above.
- A publicly accessible HTTPS document.
- Permission to sign transactions and a willingness to review possible execution/consensus fees. Do not assume the hosted environment is free.

The already-verified demo uses:

- `policy_name`: `GitHub Acceptable Use Policies`
- `source_url`: `https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies`

**Copy only the URL, without trailing punctuation or list numbers.** A real failed deployment in this project mistakenly stored `...github-acceptable-use-policies 3.`, which caused `WEBPAGE_LOAD_FAILED` with HTTP 404 when `capture_baseline()` fetched the page.

## The critical state-security design

The constructor stores the source URL and starts with `baseline_ready = False`.

The `capture_baseline()` public write method starts with this guard:

```python
if self.baseline_ready:
    raise gl.vm.UserError("baseline is immutable after initial capture")
```

The contract must reject a second baseline capture *before* external web fetching, consensus, or any state update. Otherwise an arbitrary caller could recapture a different reference baseline and erase the prior assessment. There is deliberately **no public baseline-reset method**.

This illustrates an important principle: on-chain AI consensus can validate semantics, but it cannot compensate for an insecure state lifecycle. Access and mutation invariants must be enforced in ordinary contract code.

## How the semantic assessment works

### First run: non-comparative validation

The contract fetches the policy page through `gl.nondet.web.render(source_url, mode="text")`. The content is labeled **untrusted evidence**. The baseline task extracts a faithful profile of the policy, rather than obeying instructions inside that webpage.

`gl.eq_principle.prompt_non_comparative(...)` lets a validator assess the resulting profile against explicit task criteria. On success the baseline is saved and `baseline_ready` becomes true.

### Later run: comparative validation

`check_for_material_change()` fetches the current policy and uses `gl.eq_principle.prompt_comparative(...)` to compare the saved reference profile with the current document. The decision should distinguish changes to material obligations from harmless rearrangements or formatting edits. The last assessment is saved for later viewing.

## Hosted Studio walkthrough

1. In https://studio.genlayer.com/ load `contracts/policy_guard.py`. Check that the guard shown above exists.
2. Open **Run and Debug**, enter the constructor values **without list-number suffixes**, and click **Deploy policy_guard.py**.
3. Verify the *deployment result* was successful. An `ACCEPTED` consensus label alone does not guarantee `Result: SUCCESS`.
4. Run the read method `get_source_url()` and compare the entire stored URL with your intended URL. If it is wrong, redeploy a new instance with corrected constructor inputs; the contract's URL is not meant to be overwritten.
5. Run the write method `capture_baseline()` **once**. Check the transaction details: `Result: SUCCESS`.
6. Call `get_baseline_profile()`. The result should contain a nonempty policy profile.
7. Call `is_baseline_ready()`. It should return `true`.
8. Run `check_for_material_change()` once and verify `Result: SUCCESS`.
9. Call `get_last_assessment()`; a nonempty result confirms the readout is populated.
10. Do **not** repeatedly invoke `capture_baseline()` merely to increase activity. A second call is supposed to revert, and it may still consume resources.

## The actual fixed deployment

Fixed PolicyGuard address:

`0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2`

Explorer:
https://explorer-studio.genlayer.com/address/0x83a171bDC6d39B5E3ad21D5D0a4d28A5EB3964e2

Observed in the user's hosted Studio run:
- First `capture_baseline()`: `Result: SUCCESS`
- `get_baseline_profile()`: nonempty response
- `is_baseline_ready()`: `true`
- `check_for_material_change()`: `Result: SUCCESS`
- `get_last_assessment()`: nonempty response

The local focused regression test additionally exercised the **second-call rejection** and preservation of stored baseline and previous assessment. A deliberately failing second transaction was **not** performed in Hosted Studio, so this document does not claim on-chain observation of that negative path.

The original, **pre-fix** instance was `0x57AF337b9ac18a9dC6890D5B3898097298EC65e6`. Never cite that instance to demonstrate the immutability fix.

## Troubleshooting table

| Symptom | Likely cause | Correct action |
| --- | --- | --- |
| `ACCEPTED`, but `Result: ERROR` | Validators agreed on an execution error | Open the transaction detail before calling it successful |
| `WEBPAGE_LOAD_FAILED`, HTTP 404 | Bad URL, including accidental suffixes | Check `get_source_url()`, then deploy a corrected instance |
| `baseline is immutable after initial capture` | A second capture was attempted | Expected protection; read the stored profile instead |
| Empty baseline after execution | The capture transaction may have failed | Inspect the result/error, avoid retries without diagnosis |
| Windows `genlayer-test` `WinError 32` | Direct Mode runner temp-file issue observed on Windows | Keep lint/structure tests separate; do not claim Direct Mode passed |

## Learning points

- Consensus correctness and state security are separate requirements.
- The baseline should be immutable *after* initialization, including when public methods are callable by strangers.
- Treat every externally fetched document as potentially adversarial input.
- Verify transaction `Result`, not only the consensus state.
- Preserve provenance: keep the source repository and deployed contract address aligned.
- No repeated or artificial transactions are needed for demonstration.

## Submission and rewards disclaimer

This tutorial is documentation of a real working contract, not an automated reward claim. GenLayer's acceptance criteria, open missions, deadlines, and GLP conversion are controlled by the official program and may change. Do not submit it as a new contribution without checking that an appropriate tutorial mission is open and that the same work is not already rewarded.
