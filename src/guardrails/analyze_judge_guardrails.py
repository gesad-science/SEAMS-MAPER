from guardrails.guardrail_exception import GuardrailContractError
from guardrails.utils import contains_valid_json, extract_first_json

def input_analyze_judge_guardrails(input: str) -> str:
    if input is None or not isinstance(input, str):
        raise GuardrailContractError("ANALYZE JUDGE input must be a string")

    return input


import json

def output_analyze_judge_guardrails(output: str) -> str:
    if output is None or not isinstance(output, str):
        raise GuardrailContractError("ANALYZE JUDGE output must be a string")

    parsed = extract_first_json(output)

    if not parsed:
        new = {
            "verdict": False,
            "comments": "Judge output invalid or unparsable"
        }
        return json.dumps(new)

    new = {
        "verdict": bool(parsed.get("verdict", False)),
        "comments": str(parsed.get("comments", "No comments provided"))
    }

    return json.dumps(new)

