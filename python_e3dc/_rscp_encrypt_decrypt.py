import logging
from typing import Union

from py3rijndael import RijndaelCbc, ZeroPadding

logger = logging.getLogger(__name__)


class ParameterError(Exception):
    def __init__(self, message):
        logger.exception(message)


class RSCPEncryptDecrypt:
    KEY_SIZE: int = 32
    BLOCK_SIZE: int = 32

    def __init__(self, key: str):
        if len(key) > self.KEY_SIZE:
            raise ParameterError("Key must be <%d bytes" % self.KEY_SIZE)

        self.key = bytes(key.ljust(self.KEY_SIZE, '\xff'), encoding="latin_1")
        self.init_vector = bytes('\xff' * self.BLOCK_SIZE, encoding="latin_1")
        self.cbc = RijndaelCbc(key=self.key, iv=self.init_vector, padding=ZeroPadding(self.BLOCK_SIZE),
                               block_size=self.BLOCK_SIZE)

    def encrypt(self, plain_data: Union[str, bytes]) -> bytes:
        if isinstance(plain_data, str):
            plain_data = bytes(plain_data, encoding="latin_1")

        encrypted_data = self.cbc.encrypt(plain_data)
        return encrypted_data

    def decrypt(self, encrypted_data) -> bytes:
        decrypt = self.cbc.decrypt(encrypted_data)

        return decrypt
