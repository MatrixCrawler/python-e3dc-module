from e3dc._rscp_dto import RSCPDTO
from e3dc._rscp_encrypt_decrypt import RSCPEncryptDecrypt
from e3dc._rscp_utils import RSCPUtils
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType


def test_encrypt_decrypt_works():
    encryptor = RSCPEncryptDecrypt("my_key")
    enc_result = encryptor.encrypt("TestData")
    result = encryptor.decrypt(enc_result).decode("latin_1")
    assert result == "TestData"


def test_encrypted_frame_can_be_decrypted():
    encryptor = RSCPEncryptDecrypt("my_key")
    rscp_utils = RSCPUtils()
    encoded_data = rscp_utils.encode_data(RSCPDTO(RSCPTag.RSCP_REQ_AUTHENTICATION, RSCPType.Container,
                                                  [RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_USER, RSCPType.CString,
                                                           'username'),
                                                   RSCPDTO(RSCPTag.RSCP_AUTHENTICATION_PASSWORD, RSCPType.CString,
                                                           'password')]))
    framed_data = rscp_utils.encode_frame(encoded_data)
    encrypted_data = encryptor.encrypt(framed_data)
    decrypted_data = encryptor.decrypt(encrypted_data)
    redecoded_data = rscp_utils.decode_data(decrypted_data)
    assert redecoded_data.tag == RSCPTag.RSCP_REQ_AUTHENTICATION
    assert redecoded_data.type == RSCPType.Container
    assert len(redecoded_data.data) == 2
    assert redecoded_data.data[0].tag == RSCPTag.RSCP_AUTHENTICATION_USER
    assert redecoded_data.data[0].type == RSCPType.CString
    assert redecoded_data.data[0].data == 'username'
    assert redecoded_data.data[1].tag == RSCPTag.RSCP_AUTHENTICATION_PASSWORD
    assert redecoded_data.data[1].type == RSCPType.CString
    assert redecoded_data.data[1].data == 'password'
