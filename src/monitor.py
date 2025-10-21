from kb import KnowledgeBase

class Monitor:
    def __init__(self, client, knowledge_base : KnowledgeBase):
        self.client = client
        self.knowledge_base = knowledge_base
        self.metrics = {}
        self.constraints = {}
        self.define_constraints()
        self.knowledge_base.set_sistem_information(self.constraints)
        self.update()
        
    def __get_system_metrics__(self):
        self.metrics['active_servers'] = int(self.client.get_metric("get_active_servers"))
        self.metrics['arrival_rate'] = float(self.client.get_metric("get_arrival_rate"))
        self.metrics['basic_rt'] = float(self.client.get_metric("get_basic_rt"))
        self.metrics['basic_throughput'] = float(self.client.get_metric("get_basic_throughput"))
        self.metrics['dimmer'] = float(self.client.get_metric("get_dimmer"))
        self.metrics['opt_rt'] = float(self.client.get_metric("get_opt_rt"))
        self.metrics['opt_throughput'] = float(self.client.get_metric("get_opt_throughput"))
        self.metrics['servers'] = int(self.client.get_metric("get_servers"))
        self.metrics['activating_server'] = (int(self.metrics['servers']) - int(self.metrics['active_servers'])) == 1
        self.__get_server_ult__()

    def __get_server_ult__(self):
        active_servers = int(self.metrics['active_servers'])
        ult = {}
        for i in range(active_servers):
            ult[f'server_{i+1}_ult'] = self.client.get_metric(f"get_utilization server{i+1}")
        self.metrics['server_ult'] = ult

    def get_monitor_metrics(self):
        return f"Monitor(metrics={self.metrics})"
    
    def update(self):
        self.__get_system_metrics__()
        self.knowledge_base.update_historical_base(self.metrics)

    def define_constraints(self):
        self.constraints['max_servers'] = int(self.client.get_metric("get_max_servers"))

    def get_metrics(self):
        return self.metrics