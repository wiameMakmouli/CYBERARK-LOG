import socket
import ssl
import json
import logging

class LogstashSender:
    def __init__(self, config):
        self.config = config['logstash']
        self.logger = logging.getLogger(__name__)
        self.ssl_context = ssl.create_default_context()
        if not self.config['ssl_verify']:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

    def send(self, event):
        try:
            with socket.create_connection(
                (self.config['host'], self.config['port'])
            ) as sock:
                if self.config['use_ssl']:
                    with self.ssl_context.wrap_socket(
                        sock, server_hostname=self.config['host']
                    ) as ssock:
                        ssock.sendall(json.dumps(event).encode('utf-8'))
                else:
                    sock.sendall(json.dumps(event).encode('utf-8'))
            return True
        except Exception as e:
            self.logger.error(f"Failed to send to Logstash: {str(e)}")
            return False