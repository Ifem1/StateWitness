# Example: Milestone Workflow

This example shows how another builder could use StateWitness without modifying the primitive itself.

## 1. Register the governed machine

Machine ID:

```text
grant-42-milestone-2
```

Specification:

```text
R1: The milestone may move from PENDING to APPROVED only when the submitted
    evidence demonstrates that the API described in the milestone specification
    has been deployed and is reachable.

R2: The milestone must remain PENDING if the evidence states that a required
    acceptance test is failing.

R3: APPROVED is terminal for this machine.
```

State schema:

```text
JSON object:
- status: PENDING | APPROVED
- milestone: string
- release: string
```

Initial state:

```json
{
  "status": "PENDING",
  "milestone": "API deployment",
  "release": "v1"
}
```

## 2. Propose a transition

Proposed state:

```json
{
  "status": "APPROVED",
  "milestone": "API deployment",
  "release": "v1"
}
```

Evidence:

```text
Release v1 is deployed. The submitted test report records all required acceptance
checks as passing and identifies the deployed endpoint.
```

The caller pins `expected_state_version = 0`.

## 3. Consensus

The leader and validators independently decide whether the transition satisfies R1-R3.

A valid normalized result could be:

```json
{
  "decision": "VALID",
  "violated_rule_ids": [],
  "missing_preconditions": [],
  "material_reason": "Deployment and required acceptance checks are evidenced."
}
```

After consensus, StateWitness applies the proposed state and increments `state_version` to `1`.

## 4. Rejected transition

Suppose instead the evidence says:

```text
Deployment is live, but acceptance test AT-7 is still failing.
```

An independent adjudication can return:

```json
{
  "decision": "INVALID",
  "violated_rule_ids": ["R2"],
  "missing_preconditions": [],
  "material_reason": "A required acceptance test remains failing."
}
```

The attempt is recorded, but `current_state` and `state_version` stay unchanged.

## Why this is reusable

Nothing in the StateWitness contract knows what a grant, API, milestone, acceptance test, or release is. Those concepts live entirely in the registered specification and state payload.

The same deployed primitive can govern a certification workflow, DAO process, procurement approval, software-release gate, autonomous-agent workflow, or another semantic state machine.
