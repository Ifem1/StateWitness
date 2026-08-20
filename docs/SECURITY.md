# Security model

StateWitness protects each machine's current state and transition receipts. Callers supply untrusted proposed states and evidence. Owners can change future specifications or pause a machine, but cannot directly set state.

The leader and validators independently interpret bounded, delimited inputs. Results must be structured JSON with an allowed decision, string-only arrays, and a string reason. Malformed output fails closed. Invalid results must agree on the decision, explicit rule IDs, and whether a precondition is missing.

State changes occur only after consensus and deterministic re-checks of state and specification versions. Consumers should pin both versions with `can_consume_state`.

This is not a guarantee against a malicious validator majority, incorrect specifications, or model misunderstanding. Prompt-injection framing reduces but does not eliminate risks from hostile natural language.
