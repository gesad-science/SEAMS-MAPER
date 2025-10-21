def substitute_values(data, value_dict):
    if isinstance(data, dict):
        return {key: substitute_values(value, value_dict) for key, value in data.items()}
    
    elif isinstance(data, list):
        return [substitute_values(item, value_dict) for item in data]
    
    elif isinstance(data, str) and data in value_dict:
        return value_dict[data]
    
    else:
        return data
    