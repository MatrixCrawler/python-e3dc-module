import struct
import sys
import zlib

import pytest

from python_e3dc._rscp_exceptions import RSCPFrameError
from python_e3dc._rscp_lib import RSCPLib
from python_e3dc._rscp_utils import RSCPUtils
from python_e3dc.rscp_tag import RSCPTag
from python_e3dc.rscp_type import RSCPType


def test_decode_data_returns_correct_value():
    rscp = RSCPUtils()
    hex_ = "e3dc" + \
           "1010" + \
           int.to_bytes(1564732130, length=8, byteorder=sys.byteorder).hex() + \
           int.to_bytes(94967295, length=4, byteorder=sys.byteorder).hex() + \
           int.to_bytes(11, length=2, byteorder=sys.byteorder).hex() + \
           "01000001" + "07" + struct.pack("<H", 4).hex() + struct.pack("<I", 98562).hex()
    checksum = zlib.crc32(bytes.fromhex(hex_))
    complete_hex = hex_ + int.to_bytes(checksum, length=4, byteorder=sys.byteorder).hex()
    rscp_dto = rscp.decode_data(bytes.fromhex(complete_hex))
    rscp_lib = RSCPLib()
    assert rscp_dto.tag == RSCPTag(0x01000001).name
    assert rscp_dto.type == RSCPType(0x07).name
    assert rscp_dto.data == 98562


def test_decode_data_raises_checksum_exception():
    rscp = RSCPUtils()
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
    rscp = RSCPUtils()
    hex_ = "e3dc" + \
           "1010" + \
           int.to_bytes(1564732130, length=8, byteorder=sys.byteorder).hex() + \
           int.to_bytes(94967295, length=4, byteorder=sys.byteorder).hex() + \
           int.to_bytes(256, length=2, byteorder=sys.byteorder).hex() + \
           bytearray(256).hex()
    checksum = zlib.crc32(bytes.fromhex(hex_))
    complete_hex = hex_ + int.to_bytes(checksum, length=4, byteorder=sys.byteorder).hex()
    data, timestamp = rscp._decode_frame(bytes.fromhex(complete_hex))
    assert timestamp == 1564827097.295


def test_encode_frame_returns_correct_frame():
    rscp = RSCPUtils()

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
