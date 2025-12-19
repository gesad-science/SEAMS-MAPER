# Crash and Failure Injection Guide

This document provides a complete and detailed explanation of how MAPER supports crash, fault, and failure injection through scenario configuration.

Failure injection is a first-class concept in MAPER and is used to evaluate how the self-adaptive system behaves under unexpected, disruptive, or adversarial runtime conditions. These mechanisms are essential for testing resilience, robustness, and the effectiveness of LLM-assisted adaptation under uncertainty.

All crash and failure configurations are defined in:

src/unexpected_simulator/scenario.py

This file allows users to declaratively describe when and how unexpected events occur during system execution.

---

## Purpose of Failure Injection

Failure and crash injection serve multiple goals in MAPER:

- Stress-testing adaptation logic under abnormal conditions
- Evaluating the ability of the system to recover from disruptions
- Forcing unanticipated states that were not considered at design time
- Triggering the LLM Reasoner in high-uncertainty situations
- Comparing adaptation quality with and without reasoning support

Rather than hard-coding failures into the system, MAPER separates them into explicit, configurable scenarios.

---

## Scenarios

The variable SCENARIOS defines a collection of unexpected behaviors that are injected into the system during execution.

Each scenario represents a named fault pattern that is triggered at a specific moment and executes one or more commands that affect the managed application.

Basic structure:

SCENARIOS = {
    'scenario_name': {
        'time': <trigger_time>,
        'commands': [<command_1>, <command_2>, ...]
    }
}

---

## Scenario Definition

Each entry in SCENARIOS consists of:

- A scenario name (key)
- A trigger time
- A sequence of commands

### Scenario Name

The key of each entry is the scenario identifier. This name is used only for organization and traceability.

Example:

'crashes'

Other examples could include:

'network_partition'
'power_spike'
'memory_leak'
'cascading_failures'

---

### Trigger Time

The field time specifies when the scenario is activated. This can represent:
- A simulation time
- A logical execution step
- A monitoring iteration

The exact interpretation depends on the managed application and simulator configuration.

Example:

'time': 190

This means the scenario will be triggered when the system reaches time (or step) 190.

---

### Commands

The field commands defines a list of actions that will be executed when the scenario is triggered.

Example:

'commands': ['remove_server', 'remove_server']

This simulates two consecutive server failures at the same moment, modeling a crash of multiple resources.

Commands must be:
- Supported by the executor
- Valid actions in the managed application
- Compatible with defined constraints

---

## Complete Example

SCENARIOS = {
    'crashes': {
        'time': 190,
        'commands': ['remove_server', 'remove_server']
    }
}

This scenario models a sudden crash where two servers are removed simultaneously at time 190, forcing the system into a degraded or overloaded state.

---

## Extended Examples

### Single Failure Event

SCENARIOS = {
    'single_crash': {
        'time': 50,
        'commands': ['remove_server']
    }
}

This represents a simple fault where one server crashes at time 50.

---

### Cascading Failures

SCENARIOS = {
    'cascading_crash': {
        'time': 120,
        'commands': ['remove_server', 'remove_server', 'remove_server']
    }
}

This models a cascading failure where multiple servers fail in rapid succession, stressing the system’s recovery mechanisms.

---

### Resource Exhaustion

SCENARIOS = {
    'resource_exhaustion': {
        'time': 200,
        'commands': ['increase_dimmer', 'increase_dimmer']
    }
}

This scenario simulates a sudden increase in workload or resource pressure rather than a direct crash.

---

### Mixed Disruptions

SCENARIOS = {
    'mixed_failure': {
        'time': 300,
        'commands': ['remove_server', 'increase_dimmer', 'remove_server']
    }
}

This combines infrastructure failure with workload variation, creating a complex and highly uncertain situation for the adaptation loop.

---

## Design Considerations

- Scenarios are intentionally external to the adaptation logic
- They are not adaptations, but disturbances
- They should be used to challenge, not guide, the system
- Well-designed scenarios help reveal blind spots in rules and reasoning

By combining predefined adaptation rules with disruptive scenarios, MAPER enables systematic evaluation of resilience under realistic and extreme conditions.

---

## Final Notes

Failure injection scenarios are a powerful mechanism for exploring the limits of self-adaptive systems. In MAPER, they are especially important for activating the LLM Reasoner, which is designed to operate precisely when predefined knowledge becomes insufficient.

Careful scenario design leads to more meaningful experiments and more credible results.
