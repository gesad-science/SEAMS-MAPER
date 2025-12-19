# MAPER Configuration Guide

This document provides a complete and detailed explanation of how MAPER can be configured and customized through the file:

> `src/user_config.py`

This configuration file defines how the system reasons, adapts, reacts to uncertainty, and interacts with its environment. It is the central mechanism through which users encode domain knowledge, business rules, adaptation logic, and LLM behavior.

The configuration is declarative: users describe constraints, goals, states, plans, scenarios, and reasoning prompts, and MAPER operationalizes them at runtime.

---

## General Structure

The user_config.py file is organized into the following conceptual sections:

- Constraints: define what is allowed or forbidden
- Adaptation Goals: define what the system tries to achieve
- Adaptation Options: define how system states are diagnosed
- Plan Options: define what actions are executed in response to states
- LLM Settings: define how the reasoning component behaves

Each section contributes to a different phase of the MAPER control loop.

---

## Constraints

The variable CONSTRAINTS defines hard boundaries over system variables and execution conditions for actions. Constraints are enforced during planning and execution, preventing unsafe or invalid adaptations.

Constraints can be expressed in two main forms:

1. Variable bounds (ranges or exact values)
2. Action preconditions based on system state

### Variable Constraints

A variable constraint restricts the allowable range of values for a given variable.

Example:

> `'dimmer': [0.0, 1.0]`

This means the variable dimmer can never assume values lower than 0.0 or higher than 1.0. Any plan that would violate this constraint is considered invalid.

Another example:

> `'servers': [1, 10]`

This restricts the number of servers to be between 1 and 10.

---

### Action Constraints

Action constraints define logical conditions that must be satisfied before an action can be executed.

Example:

```
'add_server': {
    'active_servers': 'servers'
}
```

This constraint means that the action add_server can only be executed if the number of active servers is equal to the total number of servers. If there are inactive servers available, adding a new one is forbidden.

More complex examples are possible:

```
'remove_server': {
    'active_servers': [2, 'servers']
}
```

This indicates that a server can only be removed if the number of active servers is at least 2.

Action constraints act as safety guards and are checked before execution.

---

## Adaptation Goals

The variable ADAPTATION_GOALS defines target objectives that the system continuously attempts to satisfy through adaptation.

Goals are typically expressed as upper bounds, lower bounds, or exact targets.

Example:

```
ADAPTATION_GOALS = {
    'threshold_response_time': 0.1
}
```

This specifies that the system should keep the response time less than or equal to 0.1.

Multiple goals can be defined simultaneously:

```
ADAPTATION_GOALS = {
    'threshold_response_time': 0.1,
    'energy_consumption': [0.0, 50.0],
    'availability': 0.99
}
```

In this case, the system will attempt to maintain low response time, bounded energy usage, and high availability at the same time, potentially trading off among them.

Goals influence diagnosis, planning, and LLM reasoning.

---

## Adaptation Options

The variable ADAPTATION_OPTIONS defines how the system interprets observed variables and classifies the current situation into a system state.

Each adaptation option represents a diagnosis and is defined by a set of conditions over variables.

Example:

```
'ok': {
    'priority': 1,
    'margin_': True,
    'dimmer': [0.75, 1.0],
    'servers': 1,
    'basic_rt': [0.0, 'threshold_response_time']
}
```

This definition means the system is considered to be in the ok state when:
- The dimmer is between 0.75 and 1.0
- There is exactly one server
- The response time is between 0.0 and the configured response time threshold

The field priority determines the order in which states are evaluated. Lower values indicate higher priority.

The field margin_ controls comparison strictness:
- True means inclusive comparisons (>=, <=)
- False means strict comparisons (>, <)

Another example:

```
'overloaded': {
    'priority': 0,
    'margin_': False,
    'basic_rt': ['threshold_response_time', 10.0],
    'servers': [1, 3]
}
```

This state captures overload situations where response time exceeds acceptable limits.

Adaptation options define the diagnosis space of the system.

---

## Plan Options

The variable PLAN_OPTIONS defines the plans executed when the system enters a specific adaptation state.

Each plan links:
- A triggering state
- A sequence of actions
- A justification for traceability and analysis

Example:

```
'decrease_servers_plan': {
    'entry': 'decrease_servers',
    'action': ['remove_server'],
    'reason': 'System underutilized; a server can be removed to optimize resource usage.'
}
```

This plan is triggered when the system is diagnosed as being in the decrease_servers state. The executor will perform the listed actions in order.

Plans may contain multiple actions:

```
'scale_up_plan': {
    'entry': 'overloaded',
    'action': ['add_server', 'increase_dimmer'],
    'reason': 'High response time detected; scaling resources and capacity.'
}
```

Plans are validated against constraints before execution.

---

## LLM Settings

The variable LLM_SETTINGS configures the LLM-based Reasoner that augments the Analyze and Plan phases of MAPER.

It must define two sections:

- analyze
- plan

Each section contains the following fields:

- model: the LLM model identifier
- temperature: deprecated parameter, kept for compatibility
- max_tokens: maximum size of the generated response
- context: system context automatically injected (constraints, goals, state)
- prompt: the prompt template guiding the model’s reasoning

Example:

```
LLM_SETTINGS = {
    'analyze': {
        'model': 'gpt-4',
        'temperature': 0.0,
        'max_tokens': 500,
        'context': 'context',
        'prompt': 'Analyze the current system state and identify possible causes.'
    },
    'plan': {
        'model': 'gpt-4',
        'temperature': 0.0,
        'max_tokens': 500,
        'context': 'context',
        'prompt': 'Propose a safe and effective adaptation plan.'
    }
}
```

The LLM Reasoner complements predefined rules by handling uncertainty, ambiguity, and unanticipated situations.

---

## Final Notes

The configuration model of MAPER is intentionally expressive. Simple rule-based adaptations and complex reasoning-driven adaptations can coexist in the same system.

By modifying user_config.py, users effectively define the cognitive boundaries and decision-making style of the self-adaptive system.
