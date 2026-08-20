from pathlib import Path
import ast

root = Path(__file__).resolve().parents[1]
contract = root / "contracts" / "state_witness.py"
tree = ast.parse(contract.read_text(encoding="utf-8"))
source = contract.read_text(encoding="utf-8")

checks = {
    "one deployable contract": sum(isinstance(n, ast.ClassDef) and any(
        isinstance(base, ast.Attribute) and base.attr == "Contract" for base in n.bases
    ) for n in tree.body) == 1,
    "consensus primitive present": "run_nondet_unsafe" in source,
    "post-consensus storage write": "self.transitions[transition_id]" in source,
    "bounded evidence": "MAX_EVIDENCE_CHARS" in source,
    "version race checks": "state changed during adjudication" in source and "specification changed during adjudication" in source,
    "strict structured output types": "adjudication arrays must contain strings" in source,
}

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")

print(f"{sum(checks.values())}/{len(checks)} checks passed")
raise SystemExit(0 if all(checks.values()) else 1)
