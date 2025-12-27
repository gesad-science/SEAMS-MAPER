from reasoning import ask_reasoning
from kb import KnowledgeBase
import logging
import sys
import json
from system_config import CONVERSATION_ATTEMPTS, REASONING, JUDGE_MODE

from util.dict_utils import parse_json

from guardrails.analyze_judge_guardrails import input_analyze_judge_guardrails, output_analyze_judge_guardrails
from guardrails.analyze_llm_guardrails import input_analyze_llm_guardrails, output_analyze_llm_guardrails

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class Analyzer:
    def __init__(self, knowledge:KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.last_update
        self.adaptation_options = self.knowledge.adaptation_options
        self.llm_settings = self.knowledge.llm_settings['analyze']
        self.judge_settings = self.knowledge.llm_settings['analyze_judge']

    def analyze(self):
        for option_name, option_criteria in sorted(self.adaptation_options.items(), key=lambda x: x[1]['priority']):
            if self.evaluate_option(option_criteria):
                return option_name
            
        if REASONING:
            analysis_result = self.model_analyze()
            return analysis_result
        
        return "call_human"
    
    def evaluate_option(self, criteria: dict) -> bool:
        for metric, bounds in criteria.items():
            if metric == 'priority' or metric=='margin_':
                continue
            current_value = self.last_update.get(metric)
            try:
                if isinstance(bounds, list) and len(bounds) == 2:
                    lower_bound = bounds[0] 
                    upper_bound = bounds[1] 
                    if criteria['margin_']:
                        if not (lower_bound <= current_value <= upper_bound):
                            return False
                    else:
                        if not (lower_bound < current_value < upper_bound):
                            return False
                else:
                    expected_value = bounds 
                    if current_value != expected_value:
                        return False
            except Exception as e:
                raise ValueError(f"Error evaluating metric '{metric}': {e}")
        return True
    
    def model_analyze(self) -> str:

        additional_context = ''
        attempts = 0

        while attempts <= CONVERSATION_ATTEMPTS:

            prompt = f"PROMPT:{self.llm_settings['prompt']} CONTEXT:{self.llm_settings['context']} ADDITIONAL_CONTEXT:{additional_context}"

            ### INPUT LLM GUARDRAIL ###
            prompt = input_analyze_llm_guardrails(prompt)

            analysis_result = ask_reasoning(prompt, self.llm_settings['temperature'], self.llm_settings['max_tokens'])

            ### OUTPUT LLM GUARDRAIL ###
            analysis_result = output_analyze_llm_guardrails(analysis_result)

            if not JUDGE_MODE:
                logging.info(f"Analyzer Result: {analysis_result}")
                return analysis_result
            
            judge_prompt = f"PROMPT:{self.judge_settings['prompt']} CONTEXT:{self.judge_settings['context']} ANALYZER_RESULT:{analysis_result}"

            ### INPUT JUDGE GUARDRAIL ###
            judge_prompt = input_analyze_judge_guardrails(judge_prompt)

            judge_result = ask_reasoning(judge_prompt, self.judge_settings['temperature'], self.judge_settings['max_tokens'])

            ### OUTPUT JUDGE GUARDRAIL ###
            judge_result = output_analyze_judge_guardrails(judge_result)

            logging.info(f"Judge Result: {judge_result}")
            try:
                logging.info(f"TRYING TO LOAD JSON: {judge_result}")
                judge_json = json.loads(judge_result)
                judge_result = str(judge_json['verdict'])
            except Exception as e:
                attempts += 1
                logging.error(f"Error parsing judge result JSON: {e}")
                continue
            if 'true' in judge_result.lower():
                return analysis_result
            
            additional_context += f"\nPrevious Analysis was rejected because: {judge_result}\nPlease provide a revised analysis.\n"
            attempts += 1

        return "call_human"
    