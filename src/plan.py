from reasoning import ask_reasoning
from kb import KnowledgeBase
from system_config import CONVERSATION_ATTEMPTS, REASONING, JUDGE_MODE

from util.dict_utils import parse_json

from guardrails.plan_judge_guardrails import input_plan_judge_guardrails, output_plan_judge_guardrails
from guardrails.plan_llm_guardrails import input_plan_llm_guardrails, output_plan_llm_guardrails

import json
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


class Planner:
    def __init__(self, knowledge: KnowledgeBase):
        self.knowledge = knowledge
        self.last_update = self.knowledge.historical_base[-1]
        self.plan_options = self.knowledge.plan_options
        self.llm_settings = self.knowledge.llm_settings['plan']
        self.judge_settings = self.knowledge.llm_settings['plan_judge']


    def plan(self, analysis_result: str) -> dict:

        try:
            analysis_json = json.loads(parse_json(analysis_result))
            recomendation = analysis_json['recomendations']
            additional_information = analysis_json['analysis']
            #logging.info(f"RECOMENDATION: {recomendation}, ADD_INF: {additional_information}")
        except Exception as e:
            #logging.info(f"ERRO NO PARSE: {analysis_result}")
            recomendation = analysis_result
            additional_information = ''

        for plan_name, plan_data in self.plan_options.items():
            if plan_data.get('entry') == recomendation:
                return {plan_name: plan_data}
        
        # Unexpected case: use LLM to generate plan
        if REASONING:
            plan_result = self.model_plan(diagnosis=recomendation+' : '+ additional_information)
            plan_json = json.loads(parse_json(plan_result))
            plan_json['entry'] = recomendation 
            new_plan_name = f"{recomendation}_plan"
            new_plan = {new_plan_name: plan_json}
            self.knowledge.update_plans(new_plan=new_plan)
            return new_plan
        
        return {'danger': {'action':['call_human']}}

    
    def model_plan(self, diagnosis:str) -> str:
        additional_context = ''
        attempts = 0

        while attempts <= CONVERSATION_ATTEMPTS:

            prompt = f"PROMPT:{self.llm_settings['prompt']} CONTEXT:{self.llm_settings['context']} ANALYZER DIAGNOSIS: {diagnosis} ADDITIONAL_CONTEXT:{additional_context}"

            ### INPUT LLM GUARDRAIL ###
            prompt = input_plan_llm_guardrails(prompt)

            plan_result = ask_reasoning(prompt, self.llm_settings['temperature'], self.llm_settings['max_tokens'])

            ### OUTPUT LLM GUARDRAIL ###
            plan_result = output_plan_llm_guardrails(plan_result)

            if not JUDGE_MODE:
                logging.info(f"Plan Result: {plan_result}")
                return plan_result
            

            prompt_judge = f"PROMPT:{self.judge_settings['prompt']} CONTEXT:{self.judge_settings['context']} ANALYZER DIAGNOSIS: {diagnosis} PLANNER_RESULT:{plan_result}"

            ### INPUT JUDGE GUARDRAIL ###
            prompt_judge = input_plan_judge_guardrails(prompt_judge)

            judge_result = ask_reasoning(prompt_judge, self.judge_settings['temperature'], self.judge_settings['max_tokens'])

            ### OUTPUT JUDGE GUARDRAIL ###
            judge_result = output_plan_judge_guardrails(judge_result)

            logging.info(f"Judge Result: {judge_result}")
            try:
                judge_json = json.loads(parse_json(judge_result))
                judge_result = str(judge_json['verdict'])
            except Exception as e:
                logging.error(f"Error parsing judge result JSON: {e}")
                attempts += 1
                continue
            if 'true' in judge_result.lower():
                return plan_result
            
            additional_context += f"\nPrevious Analysis was rejected because: {judge_result}\nPlease provide a revised analysis.\n"
            attempts += 1

        return {'danger': {'action':['call_human']}}

