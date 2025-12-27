import re
from typing import List

TIME_RE = re.compile(r"t=([0-9]+(?:\.[0-9]+)?)")
RT_RE = re.compile(r"RT=([0-9.]+)s")
ARRIVAL_RE = re.compile(r"arrival=([0-9.]+)")
ACTIVE_RE = re.compile(r"Active servers=([0-9]+)")
DIAG_RE = re.compile(r"Diagnosis:\s*(.*)")
VERDICT_RE = re.compile(r'"verdict":\s*(true|false)')

def optimize_logs(lines: List[str]) -> List[str]:
    events = []
    last_time = 0.0

    in_diagnosis_block = False
    in_judge_block = False
    pending_verdict = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        # ---- time extraction ----
        t_match = TIME_RE.search(line)
        if t_match:
            last_time = float(t_match.group(1))
        time = last_time

        if "addServer() complete" in line:
            events.append(f"time = {time:.2f} - server added")
            continue

        if "removeServer() complete" in line:
            events.append(f"time = {time:.2f} - server removed")
            continue

        if "RT=" in line and "Active servers" in line:
            rt = RT_RE.search(line)
            arrival = ARRIVAL_RE.search(line)
            active = ACTIVE_RE.search(line)

            events.append(
                f"time = {time:.2f} - monitoring cycle | "
                f"RT={rt.group(1)}s | "
                f"active_servers={active.group(1)} | "
                f"arrival={arrival.group(1)} req/s"
            )
            continue

        if "Diagnosis:" in line:
            diag = line.split("Diagnosis:")[-1].strip()
            if diag.startswith("{"):
                in_diagnosis_block = True
                continue
            events.append(f"time = {time:.2f} - diagnosis: {diag}")
            continue

        if in_diagnosis_block:
            if "}" in line:
                in_diagnosis_block = False
            continue

        if "Action plan" in line and "add_server" in line:
            events.append(f"time = {time:.2f} - action plan: add_server")
            continue

        if "INAPROPRIATE BEHAVIOR" in line:
            events.append(f"time = {time:.2f} - inappropriate behavior detected")
            continue

        if "Judge Result" in line:
            in_judge_block = True
            pending_verdict = None
            continue

        if in_judge_block:
            verdict = VERDICT_RE.search(line)
            if verdict:
                pending_verdict = verdict.group(1)
            if "}" in line:
                result = "valid" if pending_verdict == "true" else "invalid"
                events.append(
                    f"time = {time:.2f} - judge verdict: {result} decision"
                )
                in_judge_block = False
            continue

        if "All runs completed" in line:
            events.append(f"time = {time:.2f} - execution completed successfully")
            continue

    return events



if __name__ == "__main__":
    with open("results/results1/baseline-5.txt") as f:
        raw_logs = f.readlines()

    for e in optimize_logs(raw_logs):
        print(e)
