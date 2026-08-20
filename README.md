# StateWitness

**Consensus-certified semantic state transitions for GenLayer.**

StateWitness is a standalone reusable Intelligent Contract primitive. It lets builders define a state machine in normal language, then require GenLayer validators to agree that a proposed transition is actually permitted by the machine's rules and evidence **before** persistent state changes.

There is intentionally **no frontend**. The repository is designed for the Intelligent Contracts category: one reusable contract, a clear state model, explicit consensus logic, tests, and examples that other builders can compose.

## Why StateWitness exists

Traditional smart contracts are excellent at deterministic conditions:

```text
balance >= amount
status == "ACTIVE"
```

They cannot directly enforce rules such as:

```text
Move the milestone to APPROVED only when the submitted evidence materially
demonstrates that the agreed deliverable is complete.
```

StateWitness turns that second kind of rule into a reusable contract primitive.

A caller supplies:

1. the governed machine,
2. the expected current state version,
3. a proposed next state,
4. evidence,
5. optional context.

The leader evaluates the transition. Validators independently evaluate the same transition. Consensus is based on stable semantic anchors, not matching prose. Only after consensus does deterministic code apply the new state.

## Core properties

- **Reusable:** the contract is domain-agnostic; the machine owner supplies the specification and state schema.
- **Consensus is load-bearing:** state cannot advance until GenLayer's leader/validator process accepts the semantic transition.
- **Explicit equivalence logic:** validators must agree on `VALID`/`INVALID`; rejected transitions additionally require agreement on violated rule IDs and whether preconditions are missing.
- **Replay/stale-state protection:** every transition pins the expected `state_version`.
- **Specification versioning:** every adjudication records the exact `spec_version` used.
- **Immutable transition audit trail:** accepted and rejected attempts are stored.
- **Safe nondeterminism boundary:** storage-derived data is copied before nondeterministic execution; all writes happen after consensus.
- **Prompt-injection resistance:** specifications, evidence, states, and context are explicitly treated as untrusted data.
- **No hidden admin override:** machine owners may change the governing specification for future attempts, but cannot directly force the current state.

## Contract flow

```text
register machine
      |
      v
current state + governing specification
      |
      v
proposed state + evidence + context
      |
      v
leader independently adjudicates
      |
      v
validators independently adjudicate
      |
      v
custom equivalence check
  |               |
agree VALID    agree INVALID
  |               |
apply state      keep state
  |               |
  +------ record transition ------+
```

## State model

Each `Machine` stores:

| Field | Purpose |
|---|---|
| `owner` | controls specification changes and activation |
| `specification` | natural-language transition rules |
| `state_schema` | optional description/schema for interpreting state |
| `current_state` | canonical current application state |
| `state_version` | increments only after an accepted transition |
| `spec_version` | increments whenever governing rules change |
| `attempt_nonce` | increments for every adjudicated attempt |
| `active` | pause switch |

Each `TransitionRecord` pins the exact from-state, proposed state, evidence, context, state version, spec version, decision, rejection anchors, proposer, and whether the transition was applied.

## Consensus design

StateWitness uses a custom `gl.vm.run_nondet_unsafe` leader/validator pair.

The evaluator returns:

```json
{
  "decision": "VALID",
  "violated_rule_ids": [],
  "missing_preconditions": [],
  "material_reason": "Evidence establishes the required completion condition."
}
```

The validator independently reruns the adjudication.

Equivalence is intentionally asymmetric:

- `decision` must match exactly.
- For `INVALID`, `violated_rule_ids` must match exactly.
- For `INVALID`, both sides must agree on whether missing preconditions exist.
- `material_reason` is **not** consensus-critical because equivalent validators may explain the same conclusion differently.

This avoids a format-only validator while also avoiding brittle word-for-word comparison.

See [`docs/CONSENSUS.md`](docs/CONSENSUS.md) for the full threat model and rationale.

## Public interface

### `create_machine(machine_id, specification, initial_state, state_schema)`

Registers a new governed machine. Machine IDs are globally unique within this StateWitness deployment.

### `update_specification(machine_id, new_specification, new_state_schema)`

Owner-only. Updates rules for future attempts and increments `spec_version`.

### `set_machine_active(machine_id, active)`

Owner-only pause/resume control.

### `propose_transition(machine_id, expected_state_version, proposed_state, evidence, context)`

Runs GenLayer consensus and either applies or rejects the transition. Returns the decision and transition ID.

### `get_machine(machine_id)`

Returns current machine state and versions.

### `get_transition(transition_id)`

Returns the full adjudication receipt.

### `can_consume_state(machine_id, required_state_version, required_spec_version)`

Small composition guard for downstream contracts that want to pin both the state and governing-rule version they rely on.

## Example use cases

StateWitness is deliberately not tied to one product. Builders can use it for:

- milestone workflow transitions,
- governance proposal lifecycle rules,
- certification status changes,
- procurement approval stages,
- autonomous-agent workflow state,
- compliance review states,
- release-readiness gates,
- moderation/escalation workflows.

See [`examples/milestone_workflow.md`](examples/milestone_workflow.md).

## Project structure

```text
contracts/
  state_witness.py
tests/
  direct/
    test_state_witness.py
docs/
  CONSENSUS.md
  STATE_MODEL.md
  SECURITY.md
  INTEGRATION.md
  DEPLOYMENT.md
scripts/
  preflight.py
examples/
  milestone_workflow.md
.github/
  workflows/
    ci.yml
requirements.txt
pyproject.toml
```

## Local development

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Lint:

```bash
genvm-lint check contracts/state_witness.py
```

Run direct-mode tests:

```bash
pytest tests/direct/ -v
```

The tests use GenLayer's direct-mode LLM mocks, so they do not require a running Studio.

For full multi-validator behavior, deploy the contract in GenLayer Studio and exercise the same scenarios with independently configured validators.

## Verification status

The current checkout has no canonical Studionet deployment claim. Direct Mode is verified at 7/7 tests passed, and GenVM AST lint is verified at 2/2 checks passed with `genvm-linter 0.10.0`. Full SDK validation and live deployment require a working GenLayer SDK setup and authenticated network account; see [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the evidence boundary.

Run the independent preflight with `python scripts/preflight.py`. Integration guidance is in [`docs/INTEGRATION.md`](docs/INTEGRATION.md), and the security assumptions are in [`docs/SECURITY.md`](docs/SECURITY.md).

## Design boundary

StateWitness does **not** try to be:

- a frontend application,
- a generic "AI decides X" wrapper,
- a format validator,
- a web oracle,
- a policy authoring tool,
- a workflow UI.

Its one job is narrower and reusable:

> **certify, through GenLayer consensus, whether evidence and governing rules permit a proposed semantic state transition.**

## License

MIT
