"""Run actual local service regressions; no production score is inferred."""
import sys
import unittest
from pathlib import Path

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern="test_morphic_service.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("Scope: local telemetry demo only. Chain, wallet, RPC and cryptographic readiness remain unverified.")
    sys.exit(0 if result.testsRun > 0 and result.wasSuccessful() else 1)
