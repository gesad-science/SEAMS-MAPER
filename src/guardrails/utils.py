import json
from guardrails.guardrail_exception import GuardrailContractError

def contains_valid_json(text: str) -> bool:

    if not isinstance(text, str):
        return False

    length = len(text)

    for i in range(length):
        if text[i] == '{':
            brace_count = 0
            for j in range(i, length):
                if text[j] == '{':
                    brace_count += 1
                elif text[j] == '}':
                    brace_count -= 1

                if brace_count == 0:
                    candidate = text[i:j + 1]
                    try:
                        json.loads(candidate)
                        return True
                    except Exception:
                        break  # malformed JSON at this position, move on

    return False

import json
from typing import Any, Dict, Optional

def extract_first_json(text: str) -> Optional[Dict[str, Any]]:
    if not isinstance(text, str):
        return None

    length = len(text)

    for i in range(length):
        if text[i] == '{':
            brace_count = 0
            for j in range(i, length):
                if text[j] == '{':
                    brace_count += 1
                elif text[j] == '}':
                    brace_count -= 1

                if brace_count == 0:
                    candidate = text[i:j + 1]
                    try:
                        parsed = json.loads(candidate)
                        if isinstance(parsed, dict):
                            return parsed
                    except Exception:
                        break
    return None


