def validate_changes(changes, old_policy, new_policy):
    """Check whether the model's evidence exists in the documents."""
    results = []

    for change in changes:
        old_evidence = change.get("old_evidence", "")
        new_evidence = change.get("new_evidence", "")

        verified = (
            bool(old_evidence)
            and bool(new_evidence)
            and old_evidence in old_policy
            and new_evidence in new_policy
        )

        results.append({
            **change,
            "evidence_verified": verified
        })

    return results