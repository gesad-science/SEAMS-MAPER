from util.normalize import normalize
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class Executor:
    def __init__(self, client):
        self.client = client

    def add_server(self):
        return self.client.set_action("add_server")
    
    def remove_server(self):
        return self.client.set_action("remove_server")
    
    def set_dimmer(self, value):
        return self.client.set_action(f"set_dimmer {value}")
    
    def handle_plan(self, plan:dict):

        choosen_plan = next(iter(plan))
        details = plan[choosen_plan]

        action = details.get("action", [])

        if isinstance(action, str):
            actions = [action]
        else:
            actions = action
    
        logging.info(f"Executor executing plan: {choosen_plan} with actions: {actions}")

        for act in actions:
            if "add" in act:
                self.add_server()
            elif "remove" in act:
                self.remove_server()
            elif "dimmer" in act:
                target = details.get("target")
                logging.info(f"Setting dimmer to target: {target}")
                self.set_dimmer(float(target))
            else:
                return "Unknown action"
        
        return "ok"