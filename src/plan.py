from reasoning import ask_reasoning
from kb import KnowledgeBase

import json


class Planner:
    def __init__(self, knowledge: KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.history[len(self.knowledge.history)-1]

    def create_plan(self, diagnosis):
        if diagnosis == "ok":
            plan = {"action": "none", "reason": "System stable. No adaptation required."}
            self.knowledge.set_reaction(plan)
            return plan

        if diagnosis == "low_dimmer":
            plan =  {"action": ["increase_dimmer"], "target": self.last_update['dimmer']+0.25, "reason": "Performance within threshold; dimmer can be maximized."}
            self.knowledge.set_reaction(plan)
            return plan

        if diagnosis == "too_many_servers":
            plan =  {"action": ["remove_server"], "reason": "System underutilized; can remove a server to optimize resources."}
            self.knowledge.set_reaction(plan)
            return plan

        if diagnosis == "too_few_servers":
            plan =  {"action": ["add_server"], "reason": "System overloaded; more servers may be needed to reduce response time."}
            self.knowledge.set_reaction(plan)
            return plan

        if diagnosis == "too_high_dimmer":
            plan =  {"action": ["decrease_dimmer"], "target": self.last_update['dimmer']-0.25, "reason": "High dimmer may be causing degradation; reduce it."}
            self.knowledge.set_reaction(plan)
            return plan

        if isinstance(diagnosis, str) and len(diagnosis.split()) > 3:
            plan = self.call_agent_for_plan(diagnosis)
            self.knowledge.set_reaction(plan)
            return plan

        plan =  {"action": "none", "reason": "Unknown system state. No plan generated."}
        return plan

    def call_agent_for_plan(self, analysis_text: str):

        prompt = f"""
        You are the PLAN component in a MAPE-K self-adaptive system.
        You receive analyses from the ANALYZE component and must propose conceptual plans for adaptation.

        Restrictions:
        - You cannot directly execute actions (this is done by the EXECUTE component).
        - You must base your planning only on the given analysis and policies.
        - You must provide the plan in JSON format. RETURN ONLY THE JSON.

        Context:
        - Knowledge Base: {self.knowledge.get_kb_metrics()}
        - Analysis Result: {analysis_text}

        Task:
        1. Interpret the analysis.
        2. Suggest an adaptation plan in JSON format with the following keys:
            - "action": conceptual name (e.g., "add_server", "remove_server", "set_dimmer").
            - "target" (optional): value or goal (e.g., dimmer level).
            - "reason": concise justification.
        """

        response = ask_reasoning(prompt)
        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            return {"action": "none", "reason": "Failed to parse plan from agent response."}

