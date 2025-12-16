import logging
import sys
import time

from kb import KnowledgeBase
from monitor import Monitor
from execute import Executor
from analyze import Analyzer
from plan import Planner

import traceback


from swim.swim_connection import SwimClient

from unexpected_simulator.execute import CustomScenarioHandler

from util.dict_utils import normalize_diagnosis, normalize_plan

from util.time_utils import verify_loop

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def auto_adaptation_loop():

    client = SwimClient()

    kb = KnowledgeBase()

    monitor = Monitor(client=client, knowledge_base=kb)
    executor = Executor(client=client)
    scenario_handler = CustomScenarioHandler(client=client)

    analyzer = Analyzer(kb)
    planner = Planner(kb)

    logging.info("Starting loop...")

    iteration = 1

    try:
        while True:
            try:
                logging.info(f"KB Metrics: {kb.get_kb_metrics()}")


                monitor.update()
                information = monitor.get_metrics()
                logging.info(f"RT={information['basic_rt']:.2f}s | Active servers={information['active_servers']} | Dimmer={information['dimmer']:.2f} | arrival={information['arrival_rate']:.2f} req/s | Total servers={information['servers']}")

                diagnosis = analyzer.analyze()
                logging.info(f"Diagnosis: {diagnosis}")

                plan = planner.plan(diagnosis)
                logging.info(f"Action plan: {plan}")

                kb.update_metric_reaction(diagonosis=normalize_diagnosis(diagnosis), plan=normalize_plan(plan))

                result = executor.handle_plan(plan)
                logging.info(f"Result: {result}")

                scenario_handler.monitor_scenarios()

                verify_loop(iteration=iteration)
                
                #logging.info(f"RT={information['basic_rt']:.2f}s | Active servers={information['active_servers']} | Dimmer={information['dimmer']:.2f} | arrival={information['arrival_rate']:.2f} req/s | Total servers={information['servers']} | Diagnosis: {diagnosis} | Action plan: {plan} | Result: {result}")

                iteration += 1

            except Exception as e:
                logging.error(f"Error on adaptation loop: {e} {traceback.format_exc()}")
                logging.info("Trying to reconnect in 5 seconds...")
                time.sleep(5)
                client.close()
                client.connect()

    except KeyboardInterrupt:
        logging.info("Loop interrupted by the user")
        client.close()

if __name__ == "__main__":
    auto_adaptation_loop()
