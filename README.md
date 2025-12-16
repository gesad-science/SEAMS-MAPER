# MAPER: MAPE-K Extended with LLM Reasoning

## Overview

MAPER is an extension of the classical **MAPE-K architecture** (Monitor, Analyze, Plan, Execute, and Knowledge) designed for **self-adaptive systems** operating under uncertainty.

The core innovation of MAPER is the integration of an **LLM-based Reasoner**. This component augments the traditional control loop by enabling the system to handle **unanticipated situations**, incomplete knowledge, and runtime conditions that were not foreseen at design time.

The LLM Reasoner acts as an experienced human consultant inside the loop. It helps the system:
- Diagnose unforeseen or ambiguous conditions
- Propose new adaptation options beyond predefined rules
- Construct adaptation plans dynamically
- Check the feasibility and coherence of its own suggestions before execution

By combining the structured rigor of MAPE-K with the contextual and inferential power of Large Language Models, MAPER significantly increases software **resilience**, **autonomy**, and **adaptation quality**. Experimental results show that MAPER improves adaptation outcomes under high uncertainty, reducing policy violations while maintaining system goals more effectively.

---

## Architecture

Below is a high-level view of the MAPER architecture, highlighting the integration of the LLM Reasoner into the classical MAPE-K loop.

![MAPER Architecture](docs/maper-architecture.png)

---

## How to Run the Project

### 1. Prerequisites

- Docker
- Docker Compose
- An OpenAI-compatible API key

---

### 2. Environment Configuration

Create a `.env` file at the root of the project with the following content: 

OPENAI_API_KEY=your_api_key_here

This key is required for the LLM Reasoner to operate.

---

### 3. Build and Run

From the project root, execute:

docker-compose up --build

Once this command is executed, the entire MAPER process will start automatically, including the self-adaptive control loop and the LLM-based reasoning component.

---

## Customization and Configuration

MAPER is designed to be highly configurable and extensible.

### Prompt Engineering and Business Rules

MAPER exposes its reasoning behavior through a single configuration file:

src/user_config.py

This file is the main entry point for customizing how the system interprets the environment, reasons about uncertainty, and performs self-adaptation.

Users can modify:
- Prompts used by the LLM Reasoner
- Auto-adaptation logic
- Domain-specific business rules

All of these can be customized in the file above.

##### Constraints

The variable "CONSTRAINTS" defines hard boundaries and execution conditions for system variables and actions. Constraints can specify minimum, maximum, or exact values for variables, as well as logical conditions that must be satisfied for an action to be executed.

For example:

'add_server': {
    'active_servers': 'servers'
}

This indicates that the action 'add_server' can only be executed when the number of active servers is equal to the total number of servers.

Another example:

'dimmer': [0.0, 1.0]

This means that the variable 'dimmer' is constrained to values between 0.0 and 1.0.

##### Goals

The variable "ADAPTATION_GOALS" defines target values for system variables that the adaptation process should achieve or maintain.

For example:

ADAPTATION_GOALS = {
    'threshold_response_time': 0.1
}

This means that the variable 'threshold_response_time' must be less than or equal to 0.1.

##### Adaptations

The variable "ADAPTATION_OPTIONS" defines a pre-configured set of system states (diagnoses) based on observed variables. Each adaptation option describes the conditions under which a specific system state is considered valid.

For example:

'ok': {
    'priority': 1,
    'margin_': True,
    'dimmer': [0.75, 1.0],
    'servers': 1,
    'basic_rt': [0.0, 'threshold_response_time']
}

This definition indicates that the system is in the 'ok' state when:
- The dimmer value is between 0.75 and 1.0
- There is exactly one active server
- The response time is between 0.0 and the configured threshold_response_time

The field 'margin_' specifies whether comparisons are inclusive (>=, <=) or exclusive (>, <).
The field 'priority' determines the order in which adaptation conditions are evaluated.

##### Plans

The variable "PLAN_OPTIONS" defines the execution plans associated with adaptation states. Each plan specifies which actions should be executed when a particular state is entered.

For example:

'decrease_servers_plan': {
    'entry': 'decrease_servers',
    'action': ['remove_server'],
    'reason': 'System underutilized; a server can be removed to optimize resource usage.'
}

In this example, the plan 'decrease_servers_plan' is triggered when the system enters the 'decrease_servers' state. The 'action' field defines the commands executed by the executor component, while the 'reason' field documents the rationale behind the chosen plan.

##### LLMs

The variable "LLM_SETTINGS" configures the LLM-based Reasoner component. It must contain two top-level keys: "analyze" and "plan".

Each of these keys includes the following fields:
- model: the LLM model used by the reasoner
- temperature: currently deprecated; any numeric value is accepted
- max_tokens: the maximum number of tokens expected in the model response
- context: the system context provided to the model; this field is automatically populated with constraints, goals, and relevant system information
- prompt: the prompt template used to guide the model’s reasoning, which may vary depending on the system state and execution phase

---

### Environment Configuration (SWIM)

The simulated or target environment can be configured via:

swim.ini

This file allows users to adjust environmental parameters, constraints, and execution conditions used by the adaptation loop.

All the configuration are done in OMNET (https://doc.omnetpp.org/omnetpp/manual/)

---

### Custom Scenarios

Users can define and experiment with custom adaptation scenarios by editing or creating scenarios in:

Trace.ipynb

This notebook is intended for scenario design, experimentation, and trace analysis.

---

### Crash and Failure Injection

Failure scenarios and crash configurations can be defined in:

src/unexpected_simulator/scenario.py

These configurations are used to simulate faults, disruptions, and unexpected runtime conditions that challenge the adaptive system.

##### Scenarios

The variable "SCENARIOS" allows the definition of unexpected or disruptive behaviors that are injected into the system during execution. These scenarios are used to simulate faults, crashes, or abnormal conditions that challenge the self-adaptive capabilities of MAPER.

Example:

SCENARIOS = {
    'crashes': {
        'time': 190,
        'commands': ['remove_server', 'remove_server']
    }
}

Each key in "SCENARIOS" represents the name of a scenario. Inside each scenario definition:
- The field "time" specifies the simulation time (or execution step) at which the scenario is triggered.
- The field "commands" defines a sequence of actions that will be executed when the scenario is activated.

The commands must be compatible with and supported by the managed application and its executor. By combining multiple commands, users can model complex failure patterns such as cascading crashes, resource exhaustion, or abrupt environmental changes.

---

## Demo Video

A demonstration video explaining the architecture, execution flow, and adaptation results is available below:

[MAPER Demo Video](docs/guide.mp4)

---

## Summary

MAPER extends MAPE-K with LLM-based reasoning to bridge the gap between design-time assumptions and runtime uncertainty. It empowers self-adaptive systems to reason, adapt, and evolve in complex and unpredictable environments—without relying solely on pre-programmed knowledge.

Welcome to adaptive software that can truly think on its feet.

