# State Model

StateWitness deliberately separates **application state**, **governing rules**, and **adjudication history**.

## Machine

A `Machine` is a reusable semantic state machine registered by a builder.

```text
Machine
├── owner
├── specification
├── state_schema
├── current_state
├── state_version
├── spec_version
├── attempt_nonce
└── active
```

### `owner`

The account that registered the machine. It may update the specification and pause/resume the machine.

It cannot directly force a state transition through an admin setter.

### `specification`

Natural-language rules describing which transitions are permitted.

Specifications should use explicit stable rule identifiers whenever possible.

### `state_schema`

Optional explanatory schema for the state payload. StateWitness stores application state as a string so builders can use JSON or another stable representation without forcing one domain-specific storage shape.

### `current_state`

The currently accepted application state.

### `state_version`

Starts at `0` and increments only after an accepted transition.

A caller must provide the expected version when proposing a transition. This provides optimistic concurrency control and replay protection.

### `spec_version`

Starts at `1` and increments whenever the owner changes the governing specification or schema.

Every transition receipt pins this value.

### `attempt_nonce`

Increments after every completed adjudication, including rejected transitions. It is used to produce unique transition receipt IDs.

### `active`

Owner-controlled pause switch. Pausing prevents new adjudications but does not modify state or history.

## TransitionRecord

Every completed adjudication stores a receipt:

```text
TransitionRecord
├── transition_id
├── machine_id
├── proposer
├── from_state
├── proposed_state
├── evidence
├── context
├── expected_state_version
├── spec_version
├── decision
├── violated_rule_ids
├── missing_preconditions
├── material_reason
└── applied
```

Rejected attempts are retained because they are useful for debugging, auditability, and integration testing.

## Transition lifecycle

```text
CALLER
  |
  | propose_transition(machine, expected_version, next_state, evidence)
  v
VERSION CHECK
  |
  v
GENLAYER CONSENSUS
  |
  +--------------------+
  |                    |
VALID                INVALID
  |                    |
  v                    v
RECHECK VERSIONS     RECORD RECEIPT
  |
  v
APPLY NEXT STATE
  |
  v
INCREMENT state_version
  |
  v
RECORD RECEIPT
```

## Why there is no direct state setter

A direct owner-only `set_state()` would undermine the primitive because consumers could no longer distinguish consensus-certified state from administratively forced state.

The owner controls the rules, but the transition path remains consensus-gated.

## Composition

Downstream contracts can read the machine and/or use `can_consume_state(machine_id, state_version, spec_version)` to require an exact state/specification snapshot.

Pinning both versions matters. A consumer may consider state version `5` safe under specification version `2`, but not want to silently trust the same state after the governing rules have changed to version `3`.
