import socket
import time
import sys
import os
import logging
from config import SERVERS_TO_CRASH
from config import ACTIVE

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
            logging.info(f"Conectado ao SWIM em {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Error in connection: {e} - trying again...")
            time.sleep(5)
            self.connect()
            

    def send_command(self, command):
        try:
            self.sock.sendall((command + "\n").encode())
            data = self.sock.recv(1024).decode().strip()
            return data
        except Exception as e:
            logging.error(f"Error in sending command'{command}': {e}")
            raise

    def get_metric(self, metric):
        return self.send_command(metric)

    def set_action(self, action, value=None):
        cmd = f"{action} {value}" if value is not None else action
        return self.send_command(cmd)

    def close(self):
        self.sock.close()
        logging.info("Connection finished.")

def crash_servers(num_servers):
    swim = SwimClient()
    act_s = int(swim.get_metric("get_active_servers"))
    se = int(swim.get_metric("get_servers"))
    if act_s == se and act_s > 2:
        logging.info(f"Crashing {num_servers} servers...")
        for i in range(num_servers):
            response = swim.set_action("remove_server")
            logging.info(f"Server {i} crash response: {response}")
    else:
        time.sleep(20)
        swim.close()
        crash_servers(num_servers)

if __name__ == "__main__":
    if ACTIVE:
        time.sleep(190)  
        crash_servers(SERVERS_TO_CRASH)