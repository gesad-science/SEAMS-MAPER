CONSTRAINTS = {
    'dimmer': [0.0, 1.0],
    'servers': [1, 'max_servers'],
    'add_server': {
        'active_servers' : 'servers'
    }
}

ADAPTATION_GOALS = {
    'threshold_response_time': 0.1
}

ADAPTATION_OPTIONS = { ########### SHOULD HAVE A PRIORITY ORDER ############
    'ok': {
        'priority': 1,
        'dimmer' : 1.0,
        'servers': 1,
        'basic_rt': [0.0, 'threshold_response_time']
    },
    'decrease_servers': {
        'priority': 2,
        'dimmer' : [0.0, 1.0],
        'servers': [2, 'max_servers'],
        'basic_rt': [0.0, 'threshold_response_time']
    },
    'increase_dimmer': {
        'priority': 3,
        'dimmer' : [0.0, 0.75],
        'servers': 1,
        'basic_rt': [0.0, 'threshold_response_time']
    },
    'increase_servers': {
        'priority': 4,
        'dimmer' : [0.0, 1.0],  
        'servers': [1, 'max_servers'],
        'basic_rt': ['threshold_response_time', 10.0],
        'activating_server': False
    },
    'decrease_dimmer': {
        'priority': 5,
        'dimmer' : [0.75, 1.0],
        'servers': 1,
        'basic_rt': ['threshold_response_time', 10.0]
    },
}

PLAN_OPTIONS = { ######### SHOULD MATCH ADAPTATION_OPTIONS KEYS ############
    'ok_plan': {
        'entry' : 'ok',
        'action': [],
        'reason': 'System operating within optimal parameters; no adaptation needed.'
    },
    'decrease_servers_plan': {
        'entry' : 'decrease_servers',
        'action': ['remove_server'],
        'reason': 'System underutilized; can remove a server to optimize resources.'
    },
    'increase_dimmer_plan': {
        'entry' : 'increase_dimmer',
        'action': ['increase_dimmer'],
        'target': '+0.25',
        'reason': 'Performance within threshold; dimmer can be maximized.'
    },
    'increase_servers_plan': {
        'entry' : 'increase_servers',
        'action': ['add_server'],
        'reason': 'System overloaded; more servers may be needed to reduce response time.'
    },  
    'decrease_dimmer_plan': {
        'entry' : 'decrease_dimmer',
        'action': ['decrease_dimmer'],
        'target': '-0.25',
        'reason': 'High dimmer may be causing degradation; reduce it.'
    }
}

LLM_SETTINGS = {
    'analyze': {
        'model': 'gpt-4',
        'temperature': 0.2,
        'max_tokens': 500,
        'context' : 'context',
        'prompt': """
        You are the ANALYZE component of a MAPE-K self-adaptive system.
        Your role is to **interpret** the current system state based on monitoring data and knowledge base thresholds.
        You **cannot** take or suggest direct adaptation actions (such as adding/removing servers or changing dimmer levels) — 
        those are responsibilities of the PLAN and EXECUTE components.

        Task:
        1. Explain in natural language what the current system condition indicates.
        2. Identify potential causes for this state using only the provided data.
        3. If relevant, mention what type of adaptation *might* be needed conceptually (but do not propose or execute any specific action).

        Provide a concise but insightful analysis of the system’s current situation.
        """
        
    },
    'plan': {
        'model': 'gpt-4',
        'temperature': 0.3,
        'max_tokens': 700,
        'context' : 'context',
        'prompt': """
        You are the PLAN component in a MAPE-K self-adaptive system.
        You receive analyses from the ANALYZE component and must propose conceptual plans for adaptation.

        Restrictions:
        - You cannot directly execute actions (this is done by the EXECUTE component).
        - You must base your planning only on the given analysis and policies.
        - You must provide the plan in JSON format. RETURN ONLY THE JSON.

        Task:
        1. Interpret the analysis.
        2. Suggest an adaptation plan in JSON format with the following keys:
            - "action": conceptual name (e.g., "add_server", "remove_server", "set_dimmer").
            - "target" (optional): value or goal (e.g., dimmer level).
            - "reason": concise justification.
        """
    }

}
