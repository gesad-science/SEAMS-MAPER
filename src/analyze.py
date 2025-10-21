from reasoning import ask_reasoning
from kb import KnowledgeBase

class Analyzer:
    def __init__(self, knowledge:KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.historical_base[-1]
        self.adaptation_options = self.knowledge.adaptation_options
        self.llm_settings = self.knowledge.llm_settings['analyze']

    def analyze(self):
        for option_name, option_criteria in sorted(self.adaptation_options.items(), key=lambda x: x[1]['priority']):
            if self.evaluate_option(option_criteria):
                return option_name

        analysis_result = ask_reasoning(f"PROMPT:{self.llm_settings['prompt']} CONTEXT:{self.llm_settings['context']}")
        return analysis_result
    
    def evaluate_option(self, criteria: dict) -> bool:
        for metric, bounds in criteria.items():
            if metric == 'priority':
                continue

            current_value = self.last_update.get(metric)
            try:
                if isinstance(bounds, list) and len(bounds) == 2:
                    lower_bound = bounds[0] 
                    upper_bound = bounds[1] 
                    if not (lower_bound <= current_value <= upper_bound):
                        return False
                else:
                    expected_value = bounds 
                    if current_value != expected_value:
                        return False
            except Exception as e:
                raise ValueError(f"Error evaluating metric '{metric}': {e}")
        return True

    