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

![MAPER Architecture](docs/maper-architecture.pdf)

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

Users can modify:
- Prompts used by the LLM Reasoner
- Auto-adaptation logic
- Domain-specific business rules

All of these can be customized in the file:

user_config.py

This is the main entry point for tailoring MAPER’s reasoning behavior to your application domain.

---

### Environment Configuration (SWIM)

The simulated or target environment can be configured via:

swim.ini

This file allows users to adjust environmental parameters, constraints, and execution conditions used by the adaptation loop.

---

### Custom Scenarios

Users can define and experiment with custom adaptation scenarios by editing or creating scenarios in:

Trace.ipynb

This notebook is intended for scenario design, experimentation, and trace analysis.

---

### Crash and Failure Injection

Failure scenarios and crash configurations can be defined by adding files to the directory:

src/unexpected_simulator

These configurations are used to simulate faults, disruptions, and unexpected runtime conditions that challenge the adaptive system.

---

## Demo Video

A demonstration video explaining the architecture, execution flow, and adaptation results is available below:

[MAPER Demo Video](docs/MAPER USE GUIDE VIDEO.mp4)

---

## Summary

MAPER extends MAPE-K with LLM-based reasoning to bridge the gap between design-time assumptions and runtime uncertainty. It empowers self-adaptive systems to reason, adapt, and evolve in complex and unpredictable environments—without relying solely on pre-programmed knowledge.

Welcome to adaptive software that can truly think on its feet.

