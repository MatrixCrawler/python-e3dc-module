import logging
import socket

from python_e3dc._rscp_dto import RSCPDTO
from python_e3dc._rscp_encrypt_decrypt import RSCPEncryptDecrypt
from python_e3dc._rscp_exceptions import RSCPAuthenticationError, RSCPCommunicationError
from python_e3dc._rscp_utils import RSCPUtils
from python_e3dc.rscp_tag import RSCPTag
from python_e3dc.rscp_type import RSCPType

logger = logging.getLogger(__name__)


class RSCP:
    PORT = 5033
    BUFFER_SIZE = 1024 * 32

    def __init__(self, username, password, ip, key):
        self.password = password
        self.username = username
        self.encrypt_decrypt = RSCPEncryptDecrypt(key)
        self.ip = ip
        self.socket = None

    def send_request(self, rscp_dto: RSCPDTO) -> RSCPDTO:
        prepared_data = self.rscp_utils.encode_frame(self.rscp_utils.encode_data(rscp_dto))
        encrypted_data = self.encrypt_decrypt.encrypt(prepared_data)
        self.socket.send(encrypted_data)
        response = self._receive()
        if response[1] == 'Error':
            raise (RSCPCommunicationError(None, logger))
        return response

    def connect(self):
        if self.socket is not None:
            pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.PORT))
        rscp_dto = RSCPDTO(RSCPTag.RSCP_REQ_AUTHENTICATION, RSCPType.Container,
                           [('RSCP_AUTHENTICATION_USER', 'CString', self.username),
                            ('RSCP_AUTHENTICATION_PASSWORD', 'CString', self.password)], None)
        result = self.send_request(rscp_dto)
        if result[1] == 'Error':
            self._disconnect()
            raise RSCPAuthenticationError("Invalid username or password", logger)

    def _disconnect(self):
        self.socket.close()
        self.socket = None

    def _receive(self) -> RSCPDTO:
        data = self.socket.recv(self.BUFFER_SIZE)
        self.rscp_utils = RSCPUtils()

        rscp_dto = self.rscp_utils.decode_data(self.encrypt_decrypt.decrypt(data))
        return rscp_dto
