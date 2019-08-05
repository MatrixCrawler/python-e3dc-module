import struct
import sys

import libscrc
import pytest

from python_e3dc._rscp_lib import RSCPLib
from python_e3dc.rscp import RSCP, RSCPFrameError


def test_decode_data_returns_correct_value():
    rscp = RSCP()
    hex_ = "e3dc" + \
           "1010" + \
           int.to_bytes(1564732130, length=8, byteorder=sys.byteorder).hex() + \
           int.to_bytes(94967295, length=4, byteorder=sys.byteorder).hex() + \
           int.to_bytes(11, length=2, byteorder=sys.byteorder).hex() + \
           "01000001" + "07" + struct.pack("<H", 4).hex() + struct.pack("<I", 98562).hex()
    checksum = libscrc.crc32(bytes.fromhex(hex_))
    complete_hex = hex_ + int.to_bytes(checksum, length=4, byteorder=sys.byteorder).hex()
    result, size = rscp.decode_data(bytes.fromhex(complete_hex))
    rscp_lib = RSCPLib()
    assert result[0] == rscp_lib.get_data_tag_name(0x01000001)
    assert result[1] == rscp_lib.get_data_type_name(0x07)
    assert result[2] == 98562


def test_decode_data_raises_checksum_exception():
    rscp = RSCP()
    hex_ = "e3dc" + \
           "1010" + \
           int.to_bytes(1564732130, length=8, byteorder=sys.byteorder).hex() + \
           int.to_bytes(94967295, length=4, byteorder=sys.byteorder).hex() + \
           int.to_bytes(256, length=2, byteorder=sys.byteorder).hex() + \
           bytearray(256).hex()
    checksum = 156
    complete_hex = hex_ + int.to_bytes(checksum, length=4, byteorder=sys.byteorder).hex()
    with pytest.raises(RSCPFrameError):
        rscp.decode_data(bytes.fromhex(complete_hex))


def test_decode_frame_raises_no_exception():
    rscp = RSCP()
    hex_ = "e3dc" + \
           "1010" + \
           int.to_bytes(1564732130, length=8, byteorder=sys.byteorder).hex() + \
           int.to_bytes(94967295, length=4, byteorder=sys.byteorder).hex() + \
           int.to_bytes(256, length=2, byteorder=sys.byteorder).hex() + \
           bytearray(256).hex()
    checksum = libscrc.crc32(bytes.fromhex(hex_))
    complete_hex = hex_ + int.to_bytes(checksum, length=4, byteorder=sys.byteorder).hex()
    data, timestamp = rscp._decode_frame(bytes.fromhex(complete_hex))
    assert timestamp == 1564827097.295

def test_encode_frame_returns_correct_frame():
    rscp = RSCP()


    # print(complete_hex)
    # key = bytes("This is a key".ljust(32, "\xff"), encoding="latin_1")
    # print(key.hex())
    # print(len(key))
    # init_vector = bytes(RSCP.BLOCKSIZE * '\xff', encoding="latin_1")
    # print(init_vector.hex())
    # print(len(init_vector))
    # cbc = RijndaelCbc(key=key, iv=init_vector, padding=ZeroPadding(RSCP.BLOCKSIZE), block_size=RSCP.BLOCKSIZE)
    # encres = cbc.encrypt(
    #     rscp.pad_data(bytes.fromhex(complete_hex), RSCP.BLOCKSIZE))
    # print(encres.hex())
    # decres = cbc.decrypt(
    #     rscp.pad_data(encres, RSCP.BLOCKSIZE))
    # print(decres.hex())


if __name__ == '__main__':
    test_decode_frame_raises_no_exception()