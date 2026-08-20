# Standalone Intelligent Contract submission

**Primitive:** StateWitness — consensus-certified semantic state transitions.

StateWitness lets a builder define a bounded natural-language state machine and require independent GenLayer leader/validator agreement before evidence-backed transitions mutate state. Consensus is load-bearing because semantic rules such as material completion are not deterministic string checks; removing GenLayer removes the independent adjudication guarantee.

The contract is `contracts/state_witness.py`. Deterministic code owns bounds, versions, access control, parsing, equivalence anchors, receipts, and state mutation. Nondeterministic execution performs only semantic adjudication. Invalid, malformed, stale, paused, or disagreeing attempts fail closed.

Canonical Studionet deployment: `0x5eF8600D96f92fEFe6406ee7bCB9826D0B955fFd`; transaction `0x86f8f2856ae9089dbb2667d8a8b252a2fc605c4c9c407393bab6bb9469665271`; Explorer: https://explorer-studio.genlayer.com/address/0x5eF8600D96f92fEFe6406ee7bCB9826D0B955fFd. The deployment was accepted with majority agreement. Live evidence includes an accepted safe transition, a rejected invalid transition, and pause/resume lifecycle receipts; see `docs/DEPLOYMENT.md`. Direct Mode is verified at 7/7 tests passed and AST lint at 2/2. The repository contains one deployable contract and no frontend.
