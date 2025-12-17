import socket
import time
import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)

class SwimClient:
    def __init__(self, host="custom_swim", port=4242):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10.0)
            self.sock.connect((self.host, self.port))
            logging.info(f"Connected to SWIM in {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Erro ao conectar: {e} - tentando novamente em 5 segundos...")
            time.sleep(5)
            self.connect()
            

    def send_command(self, command):
        try:
            self.sock.sendall((command + "\n").encode())
            data = self.sock.recv(1024).decode().strip()
            return data
        except Exception as e:
            logging.error(f"Erro ao enviar comando '{command}': {e}")
            raise

    def get_metric(self, metric):
        return self.send_command(metric)

    def set_action(self, action, value=None):
        cmd = f"{action} {value}" if value is not None else action
        return self.send_command(cmd)

    def close(self):
        self.sock.close()
        logging.info("Conexão encerrada.")


def auto_adaptation_loop():
    logging.info("Iniciando loop de adaptação automática...")
    client = SwimClient()

    try:
        while True:
            try:
                basic_rt = float(client.get_metric("get_basic_rt"))
                servers = int(client.get_metric("get_active_servers"))
                dimmer = float(client.get_metric("get_dimmer"))
                arrival = float(client.get_metric("get_arrival_rate"))
                total_servers = int(client.get_metric("get_servers"))

                logging.info(f"RT={basic_rt:.2f}s | Servidores ativos={servers} | Dimmer={dimmer:.2f} | arrival={arrival:.2f} req/s | Servidores totais={total_servers}")

                if basic_rt > 2.0 and total_servers > servers:
                    logging.info("Tempo alto → Aguardando servidor ativar...")
                elif basic_rt > 2.0:
                    if total_servers < 3:
                        logging.info("Tempo alto → adicionando servidor")
                        result = client.set_action("add_server")
                        logging.info(f"Resultado: {result}")

                elif basic_rt < 0.5 and servers > 1:
                    logging.info("Tempo baixo → removendo servidor")
                    result = client.set_action("remove_server")
                    logging.info(f"Resultado: {result}")

                elif basic_rt > 1.5 and dimmer > 0.5:
                    new_dimmer = max(0.3, dimmer - 0.1)
                    logging.info(f"Reduzindo dimmer para {new_dimmer:.1f}")
                    result = client.set_action("set_dimmer", new_dimmer)
                    logging.info(f"Resultado: {result}")

                elif basic_rt < 0.8 and dimmer < 1.0:
                    new_dimmer = min(1.0, dimmer + 0.1)
                    logging.info(f"Aumentando dimmer para {new_dimmer:.1f}")
                    result = client.set_action("set_dimmer", new_dimmer)
                    logging.info(f"Resultado: {result}")

                time.sleep(10)

            except Exception as e:
                logging.error(f"Erro no loop de adaptação: {e}")
                logging.info("Tentando reconectar em 5 segundos...")
                time.sleep(5)
                try:
                    client.close()
                except:
                    pass
                client = SwimClient()

    except KeyboardInterrupt:
        logging.info("Encerrando manager manualmente.")
    finally:
        client.close()


if __name__ == "__main__":
    auto_adaptation_loop()