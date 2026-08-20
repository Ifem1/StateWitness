# Standalone Intelligent Contract submission

**Primitive:** StateWitness — consensus-certified semantic state transitions.

StateWitness lets a builder define a bounded natural-language state machine and require independent GenLayer leader/validator agreement before evidence-backed transitions mutate state. Consensus is load-bearing because semantic rules such as material completion are not deterministic string checks; removing GenLayer removes the independent adjudication guarantee.

The contract is `contracts/state_witness.py`. Deterministic code owns bounds, versions, access control, parsing, equivalence anchors, receipts, and state mutation. Nondeterministic execution performs only semantic adjudication. Invalid, malformed, stale, paused, or disagreeing attempts fail closed.

Evidence currently available: Direct Mode 7/7 passed; AST lint 2/2 passed. No Studionet deployment is claimed because no authenticated deployment/runtime evidence was available after the contract fix. The repository contains one deployable contract and no frontend.
