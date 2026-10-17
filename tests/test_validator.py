from src.policyshift.validator import validate_changes


def test_valid_evidence():
    changes = [{
        "topic": "Return Window",
        "old_evidence": "Returns within 14 days.",
        "new_evidence": "Returns within 7 days.",
    }]

    results = validate_changes(
        changes,
        "Returns within 14 days.",
        "Returns within 7 days.",
    )

    assert results[0]["evidence_verified"] is True


def test_fabricated_evidence():
    changes = [{
        "topic": "Return Window",
        "old_evidence": "Returns within 30 days.",
        "new_evidence": "Returns within 7 days.",
    }]

    results = validate_changes(
        changes,
        "Returns within 14 days.",
        "Returns within 7 days.",
    )

    assert results[0]["evidence_verified"] is False


def test_missing_evidence():
    changes = [{
        "topic": "Return Window",
        "old_evidence": "",
        "new_evidence": "Returns within 7 days.",
    }]

    results = validate_changes(
        changes,
        "Returns within 14 days.",
        "Returns within 7 days.",
    )

    assert results[0]["evidence_verified"] is False