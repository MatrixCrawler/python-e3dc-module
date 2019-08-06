from python_e3dc._rscp_encrypt_decrypt import RSCPEncryptDecrypt


def test_encrypt_decrypt_works():
    encryptor = RSCPEncryptDecrypt("my_key")
    enc_result = encryptor.encrypt("TestData")
    result = encryptor.decrypt(enc_result).decode("latin_1")
    assert result == "TestData"
