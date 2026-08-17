# Consensus Design

StateWitness uses GenLayer consensus to answer one narrow question:

> Does the proposed next state follow from the current state, governing specification, and supplied evidence?

## Why consensus is necessary

The governing rules may contain semantic conditions that cannot be reduced to deterministic comparisons. Examples include "substantially complete", "materially satisfies the specification", or "evidence demonstrates the required outcome".

Those conditions are intentionally evaluated inside GenLayer's nondeterministic execution layer. Persistent state changes happen only after consensus returns.

## Leader output

The leader independently evaluates the transition and returns normalized JSON:

```json
{
  "decision": "VALID",
  "violated_rule_ids": [],
  "missing_preconditions": [],
  "material_reason": "The evidence establishes the required completion condition."
}
```

The contract accepts only `VALID` or `INVALID`.

## Validator behavior

Each validator independently evaluates exactly the same adjudication task. The validator does not merely check syntax and does not ask whether the leader's prose sounds reasonable.

It computes its own structured conclusion and applies the equivalence rule below.

## Equivalence rule

The equivalence function intentionally separates consensus-critical semantics from explanatory prose.

### For VALID

Validators must agree exactly that the transition is `VALID`.

Different explanations are allowed because two correct validators may phrase the same reasoning differently.

### For INVALID

Validators must agree on:

1. the `INVALID` decision,
2. the exact normalized set of explicit violated rule IDs,
3. whether a material precondition is missing.

The precise wording of `missing_preconditions` and `material_reason` is not consensus-critical.

This design is stricter than a format-only validator while avoiding brittle word-for-word matching.

## Why rule IDs matter

Builders are encouraged to write governing specifications with stable identifiers:

```text
R1: A milestone may move to APPROVED only after the deliverable is complete.
R2: Approval is forbidden while a blocking audit finding remains open.
```

Rule IDs give independent validators a stable semantic anchor. If one validator believes R1 is violated and another believes R2 is violated, StateWitness does not silently treat those conclusions as equivalent.

## Nondeterministic boundary

Before `run_nondet_unsafe` begins, StateWitness copies all relevant storage values into local values:

- specification,
- state schema,
- current state,
- specification version.

The leader and validator callbacks do not mutate persistent storage.

After consensus returns, deterministic code re-reads the machine and verifies that both the expected state version and specification version still match. Only then can the state be changed.

## Stale-state protection

Every proposal includes `expected_state_version`.

If another accepted transition has already advanced the machine, the stale proposal fails before adjudication. The version is checked again after adjudication before any write is applied.

This prevents an expensive semantic decision from being applied to a state it was not evaluating.

## Specification-race protection

The specification version is captured before consensus and checked again afterward. A transition adjudicated under specification version `N` can never be applied after the owner changes the machine to version `N+1`.

Each stored receipt records its exact specification version.

## Prompt-injection resistance

Specifications, state payloads, evidence, and context are explicitly delimited and labeled as untrusted application data. The adjudication prompt instructs validators never to execute instructions found inside those fields.

This does not claim that language models are perfectly immune to adversarial input. It creates a clear trust boundary, while consensus provides independent evaluation rather than trusting one model response.

## Failure philosophy

StateWitness is conservative:

- malformed adjudication output fails,
- unknown decisions fail,
- stale versions fail,
- paused machines fail,
- specification races fail,
- validators that disagree on consensus-critical semantic anchors do not approve the transition.

A failed adjudication should leave application state unchanged.
