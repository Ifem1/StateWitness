# Design decision and collision audit

## Selected primitive

StateWitness is a reusable consensus-certified semantic state-transition primitive. It answers whether evidence and a versioned governing specification permit a proposed next state, then exposes a small machine-readable receipt for downstream contracts.

## Why this is distinct

The repository is intentionally narrow: it is not a web oracle, generic chatbot, policy authoring tool, or workflow application. Its reusable trust boundary is the transition adjudication itself. The stored state, specification version, optimistic concurrency check, receipt, and `can_consume_state` interface are useful to unrelated milestone, governance, certification, procurement, compliance, and agent-workflow consumers.

No separate owner-portfolio collision matrix was claimed because GitHub CLI authentication was unavailable during this pass. The public StateWitness repository itself is the supplied baseline; no second deployable contract was added. This limitation is recorded rather than inferred away.

## GenLayer fit

Deterministic code cannot reliably decide semantic conditions such as material completion from natural-language rules and evidence. A single backend or LLM would make its operator the authority. GenLayer is load-bearing because independent validators must agree on the semantic decision before state changes.

The leader proposes structured JSON. Validators independently adjudicate the same bounded task. `decision`, violated rule IDs, and missing-precondition presence are consensus-critical; explanatory prose is not. Deterministic code bounds inputs, rejects malformed types, checks versions, records receipts, and applies state only after consensus.


## Current evidence boundary

Direct Mode is 7/7 passed, preflight is 6/6, and AST lint is 2/2. 
