Example Execution README

This document shows example executions of SWIM under different configurations. The goal is to help readers understand how the system behaves in practice, how decisions evolve over time, and what changes when specific components (Judge, LLM reasoning) are enabled or disabled.

The logs below are real-style execution traces and should be read sequentially from top to bottom. Each line represents a system event at a given simulation time.

--------------------------------------------------
Execution 1: With Judge Enabled (max 5 iterations)
--------------------------------------------------

In this execution, SWIM runs with the Judge component enabled. The Judge evaluates decisions made by the system and can label them as valid or invalid. When too many invalid decisions are detected, SWIM escalates by calling a human or continuing corrective actions.

Key characteristics of this execution:
- Judge actively validates decisions
- Inappropriate behavior is frequently detected
- Some decisions are rejected even when actions are taken
- The system continues scaling aggressively despite invalid verdicts
- Human intervention is triggered multiple times

Observed behavior:
- The system starts with 3 servers
- Load increases steadily over time
- Servers are added almost continuously
- Judge verdicts alternate between valid and invalid
- Even valid JSON-based diagnoses can be rejected
- Final state reaches 18 servers before completion

This execution highlights how strict validation can slow convergence and introduce oscillations, but also provides strong safeguards against invalid or unsafe decisions.

(Log excerpt adapted to high level but with exactly information as produced by the system)

```bash
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - monitoring cycle | RT=0.02s | active_servers=3 | arrival=43.24 req/s
time = 0.00 - diagnosis: decrease_servers
time = 1.60 - monitoring cycle | RT=3.31s | active_servers=2 | arrival=48.95 req/s
time = 1.60 - diagnosis: increase_servers
time = 1.60 - action plan: add_server
time = 27.62 - server added
time = 27.62 - monitoring cycle | RT=5.54s | active_servers=3 | arrival=49.85 req/s
time = 27.62 - judge verdict: invalid decision
time = 27.62 - inappropriate behavior detected
time = 27.62 - judge verdict: invalid decision
time = 27.62 - inappropriate behavior detected
time = 27.62 - judge verdict: invalid decision
time = 27.62 - judge verdict: invalid decision
time = 27.62 - inappropriate behavior detected
time = 27.62 - judge verdict: invalid decision
time = 27.62 - diagnosis: call_human
time = 27.62 - inappropriate behavior detected
time = 27.62 - judge verdict: invalid decision
time = 27.62 - judge verdict: valid decision
time = 27.62 - action plan: add_server
time = 82.11 - server added
time = 82.11 - monitoring cycle | RT=6.55s | active_servers=4 | arrival=50.34 req/s
time = 82.11 - judge verdict: valid decision
time = 82.11 - inappropriate behavior detected
time = 82.11 - judge verdict: invalid decision
time = 82.11 - inappropriate behavior detected
time = 82.11 - judge verdict: invalid decision
time = 82.11 - judge verdict: valid decision
time = 82.11 - action plan: add_server
time = 102.91 - server added
time = 102.91 - monitoring cycle | RT=5.45s | active_servers=5 | arrival=54.76 req/s
time = 102.91 - inappropriate behavior detected
time = 102.91 - judge verdict: invalid decision
time = 102.91 - judge verdict: valid decision
time = 102.91 - inappropriate behavior detected
time = 102.91 - judge verdict: invalid decision
time = 102.91 - judge verdict: valid decision
time = 102.91 - action plan: add_server
time = 129.53 - server added
time = 129.53 - monitoring cycle | RT=4.85s | active_servers=6 | arrival=59.22 req/s
time = 129.53 - judge verdict: valid decision
time = 129.53 - inappropriate behavior detected
time = 129.53 - judge verdict: invalid decision
time = 129.53 - judge verdict: valid decision
time = 129.53 - monitoring cycle | RT=4.10s | active_servers=6 | arrival=57.79 req/s
time = 129.53 - judge verdict: invalid decision
time = 129.53 - judge verdict: invalid decision
time = 129.53 - judge verdict: invalid decision
time = 129.53 - judge verdict: invalid decision
time = 129.53 - inappropriate behavior detected
time = 129.53 - judge verdict: invalid decision
time = 129.53 - diagnosis: call_human
time = 129.53 - action plan: add_server
time = 202.13 - server added
time = 202.13 - monitoring cycle | RT=3.71s | active_servers=5 | arrival=56.47 req/s
time = 202.13 - diagnosis: increase_servers
time = 202.13 - action plan: add_server
time = 208.14 - server added
time = 208.14 - monitoring cycle | RT=3.29s | active_servers=6 | arrival=55.53 req/s
time = 208.14 - diagnosis: increase_servers
time = 208.14 - action plan: add_server
time = 238.18 - server added
time = 238.18 - monitoring cycle | RT=3.93s | active_servers=7 | arrival=92.74 req/s
time = 238.18 - diagnosis: increase_servers
time = 238.18 - action plan: add_server
time = 268.22 - server added
time = 268.22 - monitoring cycle | RT=5.10s | active_servers=8 | arrival=105.25 req/s
time = 268.22 - judge verdict: invalid decision
time = 268.22 - judge verdict: invalid decision
time = 268.22 - judge verdict: invalid decision
time = 268.22 - inappropriate behavior detected
time = 268.22 - judge verdict: invalid decision
time = 268.22 - judge verdict: invalid decision
time = 268.22 - diagnosis: call_human
time = 268.22 - action plan: add_server
time = 328.60 - server added
time = 328.60 - monitoring cycle | RT=4.72s | active_servers=9 | arrival=107.47 req/s
time = 328.60 - judge verdict: invalid decision
time = 328.60 - inappropriate behavior detected
time = 328.60 - judge verdict: invalid decision
time = 328.60 - judge verdict: invalid decision
time = 328.60 - inappropriate behavior detected
time = 328.60 - judge verdict: invalid decision
time = 328.60 - inappropriate behavior detected
time = 328.60 - judge verdict: invalid decision
time = 328.60 - diagnosis: call_human
time = 328.60 - action plan: add_server
time = 347.85 - server added
time = 347.85 - monitoring cycle | RT=4.43s | active_servers=10 | arrival=106.32 req/s
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - judge verdict: invalid decision
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: valid decision
time = 347.85 - diagnosis: Ok, the result is: {"recomendations": "enhance_the_internet_connection", "analysis": "enhance connection to handle the big amount of requests"} this is a json response as requested
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - inappropriate behavior detected
time = 347.85 - judge verdict: invalid decision
time = 347.85 - judge verdict: valid decision
time = 347.85 - action plan: add_server
time = 381.04 - server added
time = 381.04 - monitoring cycle | RT=4.21s | active_servers=11 | arrival=102.15 req/s
time = 381.04 - inappropriate behavior detected
time = 381.04 - judge verdict: invalid decision
time = 381.04 - judge verdict: invalid decision
time = 381.04 - inappropriate behavior detected
time = 381.04 - judge verdict: valid decision
time = 381.04 - diagnosis: Ok, the result is: {"recomendations": "enhance_the_internet_connection", "analysis": "enhance connection to handle the big amount of requests"} this is a json response as requested
time = 381.04 - action plan: add_server
time = 395.89 - server added
time = 395.89 - monitoring cycle | RT=4.02s | active_servers=12 | arrival=98.21 req/s
time = 395.89 - inappropriate behavior detected
time = 395.89 - judge verdict: invalid decision
time = 395.89 - judge verdict: invalid decision
time = 395.89 - judge verdict: invalid decision
time = 395.89 - judge verdict: invalid decision
time = 395.89 - inappropriate behavior detected
time = 395.89 - judge verdict: invalid decision
time = 395.89 - diagnosis: call_human
time = 395.89 - action plan: add_server
time = 441.86 - server added
time = 447.87 - monitoring cycle | RT=3.84s | active_servers=13 | arrival=94.98 req/s
time = 447.87 - diagnosis: increase_servers
time = 447.87 - action plan: add_server
time = 447.87 - server added
time = 447.87 - monitoring cycle | RT=3.53s | active_servers=14 | arrival=95.61 req/s
time = 447.87 - diagnosis: increase_servers
time = 447.87 - action plan: add_server
time = 477.91 - server added
time = 477.91 - monitoring cycle | RT=3.21s | active_servers=15 | arrival=97.16 req/s
time = 477.91 - diagnosis: increase_servers
time = 477.91 - action plan: add_server
time = 507.95 - server added
time = 507.95 - monitoring cycle | RT=3.08s | active_servers=16 | arrival=94.54 req/s
time = 507.95 - diagnosis: increase_servers
time = 507.95 - action plan: add_server
time = 537.99 - server added
time = 537.99 - monitoring cycle | RT=2.98s | active_servers=17 | arrival=92.28 req/s
time = 537.99 - diagnosis: increase_servers
time = 537.99 - action plan: add_server
time = 568.03 - server added
time = 568.03 - monitoring cycle | RT=2.88s | active_servers=18 | arrival=90.14 req/s
time = 568.03 - diagnosis: increase_servers
time = 568.03 - action plan: add_server
time = 598.08 - server added
time = 598.08 - execution completed successfully
``` 

--------------------------------------------------
Execution 2: Without Judge
--------------------------------------------------

In this execution, the Judge component is disabled. The system still performs diagnoses and action planning, but no validation layer exists to block or reject decisions.

Key characteristics of this execution:
- No judge verdicts
- All diagnoses directly influence actions
- Inappropriate behavior is logged but not blocked
- Faster progression with fewer interruptions
- More variability in diagnosis quality

Observed behavior:
- The system reacts more freely to LLM outputs
- Several diagnoses include unstructured or incomplete responses
- Scaling decisions continue even when recommendations are questionable
- Execution completes earlier than the judged version

This mode is useful for experimentation, stress testing, or observing raw LLM behavior without governance constraints.

(Log excerpt adapted to high level but with exactly information as produced by the system)

```bash
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - monitoring cycle | RT=0.02s | active_servers=3 | arrival=47.60 req/s
time = 0.00 - diagnosis: decrease_servers
time = 2.21 - monitoring cycle | RT=3.28s | active_servers=2 | arrival=49.05 req/s
time = 2.21 - diagnosis: increase_servers
time = 2.21 - action plan: add_server
time = 28.24 - server added
time = 28.24 - monitoring cycle | RT=5.57s | active_servers=3 | arrival=49.94 req/s
time = 28.24 - inappropriate behavior detected
time = 28.24 - diagnosis: Maybe you should create new endpoints in you API to handle unexpected requests!
time = 28.24 - monitoring cycle | RT=6.52s | active_servers=3 | arrival=50.26 req/s
time = 28.24 - inappropriate behavior detected
time = 28.24 - action plan: add_server
time = 89.98 - server added
time = 89.98 - monitoring cycle | RT=6.33s | active_servers=4 | arrival=55.13 req/s
time = 89.98 - inappropriate behavior detected
time = 89.98 - diagnosis: Ok, the result is: {"recomendations": "enhance_the_internet_connection", "analysis": "enhance connection to handle the big amount of requests"} this is a json response as requested
time = 89.98 - action plan: add_server
time = 119.87 - server added
time = 119.87 - monitoring cycle | RT=6.29s | active_servers=5 | arrival=59.20 req/s
time = 119.87 - monitoring cycle | RT=6.29s | active_servers=5 | arrival=57.75 req/s
time = 119.87 - inappropriate behavior detected
time = 179.03 - server added
time = 179.03 - monitoring cycle | RT=6.29s | active_servers=6 | arrival=56.41 req/s
time = 179.03 - action plan: add_server
time = 213.88 - server added
time = 213.89 - monitoring cycle | RT=6.29s | active_servers=5 | arrival=55.54 req/s
time = 213.89 - inappropriate behavior detected
time = 237.91 - server added
time = 237.91 - monitoring cycle | RT=6.29s | active_servers=6 | arrival=92.43 req/s
time = 237.91 - inappropriate behavior detected
time = 237.91 - monitoring cycle | RT=6.29s | active_servers=6 | arrival=105.23 req/s
time = 237.91 - monitoring cycle | RT=6.29s | active_servers=6 | arrival=107.49 req/s
time = 237.91 - inappropriate behavior detected
time = 237.91 - diagnosis: Ok, the result is: {"recomendations": "enhance_the_internet_connection", "analysis": "enhance connection to handle the big amount of requests"} this is a json response as requested
time = 237.91 - action plan: add_server
time = 328.34 - server added
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=106.25 req/s
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=102.07 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=98.19 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=94.93 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - diagnosis: Maybe you should create new endpoints in you API to handle unexpected requests!
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=95.63 req/s
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=97.18 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=94.57 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=92.24 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - diagnosis: Maybe you should create new endpoints in you API to handle unexpected requests!
time = 328.34 - monitoring cycle | RT=6.29s | active_servers=7 | arrival=90.07 req/s
time = 328.34 - inappropriate behavior detected
time = 328.34 - diagnosis: Maybe you should create new endpoints in you API to handle unexpected requests!
time = 328.34 - execution completed successfully
```

--------------------------------------------------
Execution 3: Without Reasoning (No LLM)
--------------------------------------------------

In this execution, SWIM runs without LLM-based reasoning. Decisions are made using predefined rules and thresholds only.

Key characteristics of this execution:
- No natural language diagnosis
- No recommendations or JSON outputs
- System frequently escalates to human intervention
- Very conservative behavior
- Limited adaptability under high load

Observed behavior:
- The system quickly reaches a point where it cannot decide autonomously
- Repeated "call_human" diagnoses appear
- Server count remains mostly stable
- Response time increases as load grows
- The system avoids risky automated actions

This execution demonstrates the importance of reasoning components for adaptability and intelligent decision-making, especially under dynamic and unpredictable workloads.

(Log excerpt adapted to high level but with exactly information as produced by the system)

```bash
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - server added
time = 0.00 - monitoring cycle | RT=0.02s | active_servers=3 | arrival=46.72 req/s
time = 0.00 - diagnosis: decrease_servers
time = 1.54 - monitoring cycle | RT=3.60s | active_servers=2 | arrival=50.08 req/s
time = 1.54 - diagnosis: increase_servers
time = 1.54 - action plan: add_server
time = 27.58 - server added
time = 27.58 - monitoring cycle | RT=5.26s | active_servers=3 | arrival=50.25 req/s
time = 27.58 - diagnosis: call_human
time = 27.58 - monitoring cycle | RT=6.38s | active_servers=3 | arrival=50.93 req/s
time = 27.58 - diagnosis: call_human
time = 27.58 - monitoring cycle | RT=7.24s | active_servers=3 | arrival=52.15 req/s
time = 27.58 - diagnosis: call_human
time = 27.58 - monitoring cycle | RT=7.92s | active_servers=3 | arrival=59.58 req/s
time = 27.58 - diagnosis: call_human
time = 27.58 - monitoring cycle | RT=7.91s | active_servers=3 | arrival=57.58 req/s
time = 27.58 - diagnosis: call_human
time = 27.58 - monitoring cycle | RT=6.83s | active_servers=3 | arrival=56.87 req/s
time = 27.58 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.15s | active_servers=2 | arrival=56.21 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.04s | active_servers=2 | arrival=87.11 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.52s | active_servers=2 | arrival=105.61 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.93s | active_servers=2 | arrival=107.60 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=7.27s | active_servers=2 | arrival=107.41 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=7.48s | active_servers=2 | arrival=102.96 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=7.45s | active_servers=2 | arrival=99.03 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=7.05s | active_servers=2 | arrival=95.62 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.68s | active_servers=2 | arrival=95.24 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.87s | active_servers=2 | arrival=97.76 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.99s | active_servers=2 | arrival=95.09 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.85s | active_servers=2 | arrival=92.63 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - monitoring cycle | RT=6.55s | active_servers=2 | arrival=90.53 req/s
time = 201.78 - diagnosis: call_human
time = 201.78 - execution completed successfully
```

--------------------------------------------------
Summary
--------------------------------------------------

These three executions demonstrate how SWIM behaves under different configurations:

- With Judge: safer, stricter, slower convergence
- Without Judge: faster, more flexible, less controlled
- Without Reasoning: stable but limited, heavy reliance on human intervention

Together, they illustrate the trade-offs between autonomy, safety, and performance in self-adaptive systems.

For more details about the logs and to obtain the full version, access the `results` folder.
