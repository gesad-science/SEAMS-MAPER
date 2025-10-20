from util.normalize import normalize


class Executor:
    def __init__(self, client):
        self.client = client

    def add_server(self):
        return self.client.set_action("add_server")
    
    def remove_server(self):
        return self.client.set_action("remove_server")
    
    def set_dimmer(self, value):
        if value < 0.0 or value > 1.0:
            value = normalize(value)
        return self.client.set_action(f"set_dimmer {value}")
    
    def handle_plan(self, plan:dict):
        action = plan.get("action", [])

        for act in action:
            if act == "add_server":
                self.add_server()
            elif act == "remove_server":
                self.remove_server()
            elif act == "increase_dimmer":
                target = plan.get("target")
                self.set_dimmer(target)
            elif act == "decrease_dimmer":
                target = plan.get("target")
                self.set_dimmer(target)
            else:
                return "Unknown action"
        
        return "ok"