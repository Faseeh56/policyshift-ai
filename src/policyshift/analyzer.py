import json
from google import genai
from .validator import validate_changes

MODEL = "gemma-4-26b-a4b-it"


def analyze_policies(old_policy, new_policy):
    if not old_policy.strip() or not new_policy.strip():
        raise ValueError("Both policy documents are required.")

    client = genai.Client()

    prompt = f"""
Compare these two e-commerce policies.

Find meaningful changes only.

Return ONLY a JSON array. Each item must contain:
- topic
- old_evidence
- new_evidence
- customer_impact
- suggested_action

Evidence must be copied EXACTLY from the supplied text.
Do not include unchanged rules.
Do not invent policy details.

OLD POLICY:
<old_policy>
{old_policy}
</old_policy>

NEW POLICY:
<new_policy>
{new_policy}
</new_policy>
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemma returned an empty response.")

    raw = response.text.strip()

    # Handle a JSON response wrapped in Markdown code fences.
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    changes = json.loads(raw)

    if not isinstance(changes, list):
        raise ValueError("Expected a JSON array of changes.")

    return validate_changes(changes, old_policy, new_policy)