from util.normalize import normalize


class Executor:
    def __init__(self, client):
        self.client = client

    def add_server(self):
        return self.client.set_action("add_server")
    
    def remove_server(self):
        return self.client.set_action("remove_server")
    
    def set_dimmer(self, value):
        #if value < 0.0 or value > 1.0:
        #    value = normalize(value)
        return self.client.set_action(f"set_dimmer {value}")
    
    def handle_plan(self, plan:dict):

        choosen_plan = next(iter(plan))
        details = plan[choosen_plan]

        action = details.get("action", [])

        if isinstance(action, str):
            actions = [action]
        else:
            actions = action
    

        for act in actions:
            if "add" in act:
                self.add_server()
            elif "remove" in act:
                self.remove_server()
            elif "dimmer" in act:
                target = plan.get("target")
                self.set_dimmer(target)
            else:
                return "Unknown action"
        
        return "ok"