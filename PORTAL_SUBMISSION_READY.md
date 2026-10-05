# GenLayer Portal Submission — Ready to Paste

## Contribution type
Intelligent Contracts

## Title
PolicyGuard — Semantic Policy Change Oracle

## Short description
A GenLayer Intelligent Contract that uses validator-backed semantic consensus to distinguish meaningful policy changes from harmless wording edits.

## Repository
https://github.com/cacx097/genlayer-policy-guard

## Contract address
0x57AF337b9ac18a9dC6890D5B3898097298EC65e6

## Detailed description
PolicyGuard monitors a public HTTPS policy page and stores a validator-approved semantic baseline of the rules that materially affect users, including obligations, prohibitions, permissions, eligibility, fees or economic terms, deadlines, data use, enforcement consequences, and explicit exceptions.

A later check fetches the live policy again and uses GenLayer's nondeterministic execution plus the Equivalence Principle to determine whether the policy changed in substance rather than merely in wording or formatting.

The contract is GenLayer-native: baseline extraction uses non-comparative validation, material-change detection uses comparative validation, and fetched webpage text is explicitly treated as untrusted evidence so embedded instructions are not followed.

## Why GenLayer
A conventional smart contract can detect that bytes changed but cannot reliably decide whether meaning changed. A centralized LLM can make that judgment but introduces a single trusted decision-maker. PolicyGuard uses GenLayer validators to reach consensus on the semantic decision.

## Verification evidence
- genvm-lint: PASS
- GenLayer contract validation: PASS
- ABI/schema extraction: PASS
- source/structure tests: 6 PASS
- hosted GenLayer Studio deployment: Accepted
- capture_baseline(): Accepted
- get_baseline_profile(): Accepted with non-empty returned profile
- check_for_material_change(): Transaction Accepted
- get_last_assessment(): Accepted with non-empty returned assessment
- end-to-end baseline → semantic change check → assessment retrieval: verified
- deployed contract: 0x57AF337b9ac18a9dC6890D5B3898097298EC65e6

## Final runtime status
The deployed PolicyGuard contract completed the full hosted Studio flow: deployment, baseline capture, baseline retrieval, material-change transaction, and final assessment retrieval. The returned baseline and assessment were both non-empty.

## Submission priority
Submit this contribution now under Intelligent Contracts using the title, repository URL, contract address, description, and verification evidence above.