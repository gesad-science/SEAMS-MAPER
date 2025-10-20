
class KnowledgeBase:
    def __init__(self, client):
        self.client = client
        self.policies = {}
        self.history = []

    def define_policies(self, policies):
        self.policies = policies

    def get_policies(self):
        return self.policies
    
    def set_policies(self, constraints):
        self.policies = constraints
    
    def get_kb_metrics(self):
        return f"Knowledge(policy={self.policies}, History={str(self.history[-5:])})"
    
    def update_history(self, entry):
        self.history.append(entry)

    def set_reaction(self, reaction: dict):
        self.history[len(self.history)-1]['reaction'] = reaction

    def set_diagnosis(self, diagnosis: dict):
        self.history[len(self.history)-1]['diagnosis'] = diagnosis
    