import logging
import sys
import time

from kb import KnowledgeBase
from monitor import Monitor
from execute import Executor
from analyze import Analyzer
from plan import Planner

from swim.swim_connection import SwimClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def auto_adaptation_loop():

    client = SwimClient()

    kb = KnowledgeBase(client=client)

    monitor = Monitor(client=client, knowledge_base=kb)
    executor = Executor(client=client)

    analyzer = Analyzer(kb)
    planner = Planner(kb)

    logging.info("Iniciando loop de adaptação automática...")

    try:
        while True:
            try:
                monitor.update()
                information = monitor.get_metrics()
                logging.info(f"RT={information['basic_rt']:.2f}s | Servidores ativos={information['active_servers']} | Dimmer={information['dimmer']:.2f} | arrival={information['arrival_rate']:.2f} req/s | Servidores totais={information['servers']}")

                diagnosis = analyzer.analyze()
                logging.info(f"Diagnóstico: {diagnosis}")

                plan = planner.create_plan(diagnosis)
                logging.info(f"Plano de Ação: {plan}")

                executor.handle_plan(plan)

                time.sleep(10)

            except Exception as e:
                logging.error(f"Erro no loop de adaptação: {e}")
                logging.info("Tentando reconectar em 5 segundos...")
                time.sleep(5)
                client.close()
                client.connect()

    except KeyboardInterrupt:
        logging.info("Loop de adaptação automática interrompido pelo usuário.")
        client.close()

if __name__ == "__main__":
    auto_adaptation_loop()
