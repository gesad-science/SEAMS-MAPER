from util.time_utils import get_system_uptime
from unexpected_simulator.scenario import SCENARIOS 
from swim.swim_connection import SwimClient

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class CustomScenarioHandler:
    def __init__(self, client:SwimClient):
        self.client = client
        self.executed = set()  

    def monitor_scenarios(self):
        uptime = get_system_uptime()

        for name, config in SCENARIOS.items():
            if uptime >= config['time'] and name not in self.executed:
                logging.info(f"Executing customized scenario: {name}")
                for cmd in config['commands']:
                    logging.info(f"Executing command: {cmd}")
                    self.client.set_action(cmd)
                self.executed.add(name)
                logging.info("Customized scenario finished")

