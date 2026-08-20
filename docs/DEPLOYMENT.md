# Deployment evidence

## Canonical deployment

- Network: hosted Studionet (`https://studio.genlayer.com/api`)
- Deployment source commit: `703cc50`
- Contract address: `0x5eF8600D96f92fEFe6406ee7bCB9826D0B955fFd`
- Explorer: https://explorer-studio.genlayer.com/address/0x5eF8600D96f92fEFe6406ee7bCB9826D0B955fFd
- Deployment transaction: `0x86f8f2856ae9089dbb2667d8a8b252a2fc605c4c9c407393bab6bb9469665271`
- Lifecycle: `ACCEPTED`
- Consensus: `MAJORITY_AGREE`; validators agreed before quorum cancellation of idle validators.
- Deployer: `0xf8531058E0a3df4aE1d58C11529bCDECB9aA4487`

## Live runtime evidence

Using machine `str:final2`:

- Creation: `0x76cc491e56cb83d3b6f05459af04d71c095607d41fee501b4bc088deda4fb67c`; accepted.
- Safe transition: `0xeab1e3353e27487ca2c29bdd2c8e99303c42309656e6242c789fd69471606f1a`; `MAJORITY_AGREE`, receipt `str:final2:1`, `decision=VALID`, `applied=true`, state version 1.
- Negative transition: `0xfe3a43b40b4291bee3f2a2f48afb7c2c837eace25cdab0de25c2bdd1c2b0ebba`; `MAJORITY_AGREE`, receipt `str:final2:2`, `decision=INVALID`, `applied=false`; state remained version 1.
- Pause lifecycle: `0xe719b72089d609c96dbf87acb7055bcff550e4c96d0ce80c732e8c252dd49f00`; accepted pause. Resume: `0xd664718ae15a2babada2bd264551f7d5736106e465b2cd82de8e4e473af6b172`; accepted resume. Final view showed `active=true`, `state_version=1`, `attempt_nonce=2`.

The earlier deployment at `0xa04ac435888a48a4F9a99084326a3dDF3c862C95` is historical only. The canonical deployment is the corrected source above.

Verified locally: Direct Mode 7/7 passed, the integration suite collected 3 tests and skipped 3 without live configuration, and GenVM AST lint 2/2 checks passed with `genvm-linter 0.10.0`. Full SDK validation was attempted but the linter setup step did not complete in this environment.
