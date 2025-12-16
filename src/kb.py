from user_config import CONSTRAINTS, ADAPTATION_GOALS, ADAPTATION_OPTIONS, PLAN_OPTIONS, LLM_SETTINGS
from system_config import JUGDE_SETTINGS
from util.dict_utils import substitute_values
from copy import deepcopy

import logging 
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)



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
        return f"Knowledge(ADAPTATION_GOALS={self.adaptation_goals}, History={str(self.historical_base[-5:])}, Constraints={self.parse_constraints()}), Last_update={str(self.last_update)})"
    
    def set_system_information(self, info: dict = {}):
        self.system_information.update(info)
        self.adaptation_goals.update(ADAPTATION_GOALS)
        self.system_information.update(ADAPTATION_GOALS)
        self.llm_settings = deepcopy(LLM_SETTINGS)
        self.llm_settings.update(JUGDE_SETTINGS)
        self.constraints = substitute_values(CONSTRAINTS, self.system_information)
        self.adaptation_options = substitute_values(ADAPTATION_OPTIONS, self.system_information)
        self.plan_options = substitute_values(PLAN_OPTIONS, self.system_information)
        self.llm_settings = substitute_values(self.llm_settings, self.system_information)
        return
    
    def update_historical_base(self, metrics: dict):
        self.historical_base.append(self.last_update)
        self.last_update = metrics

        context = {'context': self.get_kb_metrics()}
        self.llm_settings = substitute_values(self.llm_settings, context)
        
        return
    
    def parse_constraints(self):
        return str(self.constraints).replace(':', '=')
    
    def update_plans(self, new_plan):
        self.plan_options.update(new_plan)

    def update_metric_reaction(self, diagonosis, plan):
        self.last_update['diagnosis'] = diagonosis
        self.last_update['plan'] = plan