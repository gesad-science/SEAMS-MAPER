from guardrails.guardrail_exception import GuardrailContractError
from guardrails.utils import contains_valid_json, extract_first_json

def input_plan_llm_guardrails(input: str) -> str:
    if input is None or not isinstance(input, str):
        raise GuardrailContractError("PLAN LLM input must be a string")

    return input

def output_plan_llm_guardrails(output: str) -> str:
    if output is None or not isinstance(output, str):
        raise GuardrailContractError("PLAN LLM output must be a string")

    parsed = extract_first_json(output)

    if not parsed:
        return {
            "action": [],
            "reason": "Invalid or missing plan output"
        }

    actions = parsed.get("action", [])
    if not isinstance(actions, list):
        actions = []


    plan = {
        "action": actions,
        "reason": str(parsed.get("reason", "Reason not provided"))
    }

    if "target" in parsed:
        plan["target"] = parsed["target"]

    return f"{plan}".replace("'",'"')

