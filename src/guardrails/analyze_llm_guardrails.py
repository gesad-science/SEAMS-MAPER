from guardrails.guardrail_exception import GuardrailContractError
from guardrails.utils import contains_valid_json, extract_first_json

def input_analyze_llm_guardrails(input: str) -> str:
    if input is None or not isinstance(input, str):
        raise GuardrailContractError("ANALYZE LLM input must be a string")

    return input

import json

def output_analyze_llm_guardrails(output: str) -> str:
    if output is None or not isinstance(output, str):
        raise GuardrailContractError("ANALYZE LLM output must be a string")

    parsed = extract_first_json(output)

    if not parsed:
        new = {
            "recomendations": "none",
            "analysis": "Invalid or missing analysis output"
        }
        return json.dumps(new)

    new = {
        "recomendations": str(parsed.get("recomendations", "none")),
        "analysis": str(parsed.get("analysis", "Analysis not provided"))
    }

    return json.dumps(new)


