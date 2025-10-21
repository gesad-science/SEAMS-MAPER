from configurations import CONSTRAINTS, ADAPTATION_GOALS, ADAPTATION_OPTIONS, PLAN_OPTIONS, LLM_SETTINGS
from util.parse_dict import substitute_values


class KnowledgeBase:
    def __init__(self):
        self.historical_base = []
        self.system_information = {}
        self.constraints = {}
        self.last_update = {}
        self.llm_settings = {}
        self.adaptation_goals = {}
        self.adaptation_options = {}
        self.plan_options = {}
        
    def get_kb_metrics(self):
        return f"Knowledge(Adaptation_goals={self.adaptation_goals}, History={str(self.historical_base[-5:])}, Constraints={self.parse_constraints()}), Last_update={str(self.last_update)})"
    
    def set_sistem_information(self, info: dict):
        for key, value in info.items():
            self.system_information[key] = value
        self.consume_config()
        return

    def pass_goal(self):
        for key, value in ADAPTATION_GOALS.items():
            self.adaptation_goals[key] = value
            self.system_information[key] = value
        return

    def consume_config(self):
        self.pass_goal()
        self.constraints = substitute_values(CONSTRAINTS, self.system_information)
        self.adaptation_options = substitute_values(ADAPTATION_OPTIONS, self.system_information)
        self.plan_options = substitute_values(PLAN_OPTIONS, self.system_information)
        self.llm_settings = substitute_values(LLM_SETTINGS, self.system_information)
        return
    
    def update_historical_base(self, metrics: dict):
        self.historical_base.append(metrics)
        self.last_update = metrics

        context = {'context': self.get_kb_metrics()}
        self.llm_settings = substitute_values(self.llm_settings, context)
        
        return
    
    def parse_constraints(self):
        return str(self.constraints).replace(':', '=')