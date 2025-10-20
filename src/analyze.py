from reasoning import ask_reasoning
from kb import KnowledgeBase

class Analyzer:
    def __init__(self, knowledge:KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.history[len(self.knowledge.history)-1]

    def analyze(self):
        rt = self.last_update.get('basic_rt')
        rt_threshold = self.knowledge.policies.get('rt_threshold')
        dimmer = self.last_update.get('dimmer')
        active_servers = self.last_update.get('active_servers')

        if rt < rt_threshold:
            if active_servers == 1:
                if dimmer == 1:
                    analisys = "ok"
                    self.knowledge.set_diagnosis(analisys)
                    return analisys 
                analisys = "low_dimmer"
                self.knowledge.set_diagnosis(analisys)
                return analisys
            analisys = "too_many_servers"
            self.knowledge.set_diagnosis(analisys)
            return analisys 

        if active_servers == 1:
            analisys = "too_few_servers"
            self.knowledge.set_diagnosis(analisys)
            return analisys
        if dimmer > 0.75:
            analisys = "too_high_dimmer"
            self.knowledge.set_diagnosis(analisys)
            return analisys  
        
        analisys = self.call_agent()
        self.knowledge.set_diagnosis(analisys)
        return analisys

    def call_agent(self):
        prompt = f"""
        You are the ANALYZE component of a MAPE-K self-adaptive system.
        Your role is to **interpret** the current system state based on monitoring data and knowledge base thresholds.
        You **cannot** take or suggest direct adaptation actions (such as adding/removing servers or changing dimmer levels) — 
        those are responsibilities of the PLAN and EXECUTE components.

        Context:
        - Knowledge Base: {self.knowledge.get_kb_metrics()}
        - Last Update From Environment: {self.last_update}
        - ANSWER BRIEFLY based SOLELY on the provided data and knowledge base policies.

        Task:
        1. Explain in natural language what the current system condition indicates.
        2. Identify potential causes for this state using only the provided data.
        3. If relevant, mention what type of adaptation *might* be needed conceptually (but do not propose or execute any specific action).

        Provide a concise but insightful analysis of the system’s current situation.
        """

        response = ask_reasoning(prompt)
        return response
