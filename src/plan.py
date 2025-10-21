from reasoning import ask_reasoning
from kb import KnowledgeBase

import json


class Planner:
    def __init__(self, knowledge: KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.historical_base[-1]
        self.plan_options = self.knowledge.plan_options
        self.llm = self.knowledge.llm_settings['plan']

    def plan(self, analysis_result: str) -> dict:
        for plan_name, plan_data in self.plan_options.items():
            if plan_data.get('entry') == analysis_result:
                return {plan_name: plan_data}
            
        # Unexpected case: use LLM to generate plan
        plan_result = ask_reasoning(f"PROMPT:{self.llm['prompt']} CONTEXT:{self.llm['context']}")
        return json.loads({'custom_plan':plan_result})
