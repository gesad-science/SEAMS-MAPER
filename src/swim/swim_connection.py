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
            logging.info(f"Connected to swim in {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Error in connection: {e} - Reconnection in 5 seconds...")
            time.sleep(5)
            self.connect()

    def send_command(self, command):
        try:
            self.sock.sendall((command + "\n").encode())
            data = self.sock.recv(1024).decode().strip()
            return data
        except Exception as e:
            logging.error(f"Error in sending command '{command}': {e}")
            raise

    def get_metric(self, metric):
        return self.send_command(metric)

    def set_action(self, action, value=None):
        cmd = f"{action} {value}" if value is not None else action
        return self.send_command(cmd)

    def close(self):
        self.sock.close()
        logging.info("Connection endded.")