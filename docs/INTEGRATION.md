# Integration

A downstream Intelligent Contract can read `get_machine(machine_id)` and pin the returned `state_version` and `spec_version`. Before consuming the state, call:

```python
allowed = witness.can_consume_state("milestone-1", 3, 2)
```

Require `allowed` before performing downstream work. Use `get_transition("milestone-1:4")` for the immutable adjudication receipt. Pinning both versions prevents a consumer from silently relying on a state under different governing rules.

The committed opt-in suite is under `tests/integration/`. It requires an operator-provided disposable Studionet address/RPC and recorded success/negative transaction hashes through environment variables. Without those values, tests skip rather than claim live evidence.
