# Transformers AI local demonstration

This repository contains a static dashboard, a deterministic Rust automaton and a Python telemetry demo. The dashboard does not connect a wallet, submit a transaction or verify an on-chain invariant. Preview actions are explicitly labelled and accept whole-number quantities from 1 to 1,000,000. The Python service enforces the same quantity bounds and validates destinations.

## Verify locally

```sh
python -m unittest discover -s tests -p test_morphic_service.py -v
python tests/reality_check_harness.py
cargo build --offline --locked
```

The tests exercise actual telemetry results and rejected inputs. Passing them does not establish wallet, RPC, token, PQC, escrow, security or production readiness. No deployment or minting is performed. Historical whitepapers, architecture descriptions and checked-in audit reports are not execution evidence.
