from pathlib import Path
from src.policyshift.analyzer import analyze_policies

old = Path("samples/old_policy.txt").read_text()
new = Path("samples/new_policy.txt").read_text()

changes = analyze_policies(old, new)

for change in changes:
    print("\nTopic:", change["topic"])
    print("Before:", change["old_evidence"])
    print("After:", change["new_evidence"])
    print("Impact:", change["customer_impact"])
    print("Action:", change["suggested_action"])
    print("Evidence verified:", change["evidence_verified"])