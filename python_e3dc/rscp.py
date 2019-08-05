import logging
import socket

from python_e3dc._rscp_encrypt_decrypt import RSCPEncryptDecrypt
from python_e3dc._rscp_exceptions import RSCPAuthenticationError, RSCPCommunicationError
from python_e3dc._rscp_utils import RSCPUtils

logger = logging.getLogger(__name__)


class RSCP:
    PORT = 5033

    def __init__(self, username, password, ip, key):
        self.password = password
        self.username = username
        self.encrypt_decrypt = RSCPEncryptDecrypt(key)
        self.ip = ip
        self.socket = None

    def send_request(self, message: tuple):
        self._send(message)
        response = self._receive()
        if response[1] == 'Error':
            raise (RSCPCommunicationError(None, logger))

    def connect(self):
        if self.socket is not None:
            pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.PORT))
        result = self.send_request(('RSCP_REQ_AUTHENTICATION', 'Container',
                                    [('RSCP_AUTHENTICATION_USER', 'CString', self.username),
                                     ('RSCP_AUTHENTICATION_PASSWORD', 'CString', self.password)]))
        if result[1] == 'Error':
            self._disconnect()
            raise RSCPAuthenticationError("Invalid username or password", logger)

    def _disconnect(self):
        self.socket.close()
        self.socket = None

    def _send(self, message):
        rscp_utils = RSCPUtils()
        prepared_data = rscp_utils.encode_frame(rscp_utils.encode_data(message))
        encrypted_data = self.encrypt_decrypt.encrypt(prepared_data)
        self.socket.send(encrypted_data)
