import json

def substitute_values(data, value_dict):
    if isinstance(data, dict):
        return {key: substitute_values(value, value_dict) for key, value in data.items()}
    
    elif isinstance(data, list):
        return [substitute_values(item, value_dict) for item in data]
    
    elif isinstance(data, str) and data in value_dict:
        return value_dict[data]
    
    else:
        return data
    
def normalize_diagnosis(diagnosis):
    try:
        json_diag = json.loads(diagnosis)
        return json_diag['recomendations']
    except Exception as e:
        return diagnosis

def normalize_plan(plan:dict):
    choosen_plan = next(iter(plan))
    details = plan[choosen_plan]
    if 'reason' in details.keys():
        if len(details['reason'])>70:
            details['reason'] = ''

    return {choosen_plan : details}

def parse_json(s: str) -> str:

    if not s:
        return str(None)

    start_idx = None
    brace_count = 0
    
    for i, char in enumerate(s):
        if char == '{':
            if brace_count == 0:
                start_idx = i 
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx is not None:
                return str(s[start_idx:i+1])
    
    return str(s)  
