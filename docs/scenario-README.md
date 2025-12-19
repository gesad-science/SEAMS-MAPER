# Request Scenario Generation Guide

The document: 

Trace.ipynb

describes how our work supports the creation of **request-load scenarios** through a dedicated Jupyter Notebook. These scenarios define how requests arrive over time and are used to stress, evaluate, and challenge the self-adaptive behavior of the system.

The notebook is responsible for generating **time-distributed request patterns**, which are later consumed by the simulator to emulate realistic and adversarial workloads.

The notebook allows users to explicitly design load dynamics such as spikes, bursts, gradual increases, sudden drops, and normalization phases.

---

## Purpose of Request Scenarios

Request scenarios play a central role in MAPER experiments. They are used to:

- Simulate realistic workload behavior
- Create high-load peaks and stress conditions
- Trigger adaptation and reconfiguration
- Evaluate system behavior under non-stationary demand
- Force situations where predefined rules may become insufficient

Unlike random traffic generators, this notebook allows **explicit control over the temporal shape of the workload**.

---

## Core Parameters

The notebook starts by defining global execution parameters.

### Execution Time

TIME defines the total duration of the scenario in seconds.

Example:

TIME = 600

This means the scenario lasts for 600 seconds. 

---

### Request Rate Configuration

The request rate can be defined in two ways:

- Using a default average request rate
- Using a custom request rate

Variables:

TAX_DEF = True
TAX = 90

If TAX_DEF is set to True, the system uses a predefined average request rate.
If TAX_DEF is False, the value in TAX is used as the requests-per-second rate.

The total number of requests is computed automatically:

REQ = int(22.22222 * TIME) + 1   (default mode)
REQ = int(TAX * TIME) + 1        (custom mode)

This ensures consistency between execution time and total load.

---

## Pattern-Based Load Definition

The heart of the notebook is the function that generates request intervals based on a **pattern vector**.

### Pattern Vector

A pattern is a list of integers representing relative load intensity over time.

Example:

[1, 1, 2, 1, 1, 10, 10, 10, 10, 8, 7, 2, 3, 2, 1, 1, 3, 4, 1, 1]

Interpretation:
- Low values represent low request density
- High values represent peaks or bursts
- The sequence encodes the shape of the workload over time

This vector does not represent absolute rates, but relative intensity.

---

## Interval Generation Logic

The function generate_request_intervals performs the following steps:

1. Normalizes the pattern values
2. Repeats the pattern to match the total number of requests
3. Generates base inter-arrival times using an exponential distribution
4. Adjusts each interval based on the pattern intensity
5. Normalizes intervals so their sum equals the total execution time

The result is a list of inter-arrival times whose cumulative sum spans exactly TIME seconds.

This ensures:
- The total duration is preserved
- The request distribution follows the desired shape

---

## Visual Validation

The notebook includes a visualization step that converts inter-arrival times into requests-per-second values and plots them.

This plot allows users to:
- Visually inspect peaks and valleys
- Validate that the intended scenario was correctly generated
- Compare different patterns

The x-axis represents time in seconds.
The y-axis represents requests per second (RPS).

---

## Example Scenarios

### Single Peak Scenario

Pattern:

[1, 1, 1, 8, 10, 10, 8, 1, 1, 1]

This models a sudden traffic spike followed by normalization.

---

### Multiple Bursts

Pattern:

[1, 1, 5, 1, 1, 6, 1, 1, 4, 1, 1]

This creates repeated short bursts separated by calm periods.

---

### Gradual Ramp-Up and Down

Pattern:

[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]

This simulates a smooth increase and decrease in demand.

---

## Scenario Export

Once validated, the scenario is saved to disk as a sequence of inter-arrival times.

Example:

with open('scenario.delta', 'w') as file:
    for interval in intervals:
        file.write(f"{interval}\n")

The generated file contains one value per line, representing the delay until the next request.

This file is later consumed by the simulator to reproduce the exact same request pattern deterministically.

---

## Design Considerations

- Patterns are intentionally simple and interpretable
- Complexity emerges from composition, not randomness
- Scenarios are reproducible
- The same scenario can be reused across experiments

By explicitly designing request-load scenarios, users gain fine-grained control over the experimental conditions under which MAPER is evaluated.

---

## Final Notes

This notebook is a key experimental tool. It bridges abstract adaptation logic and concrete runtime pressure by translating high-level workload ideas into precise, executable request traces.

Well-designed request scenarios are essential for credible evaluation of self-adaptive systems.
