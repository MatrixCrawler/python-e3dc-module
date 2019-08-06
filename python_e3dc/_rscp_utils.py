import logging
import math
import struct
import time
import zlib

from python_e3dc._rscp_dto import RSCPDTO
from python_e3dc._rscp_exceptions import RSCPFrameError, RSCPDataError
from python_e3dc._rscp_lib import RSCPLib

logger = logging.getLogger(__name__)


class RSCPUtils:
    _FRAME_HEADER_FORMAT = "<HHQIH"
    _FRAME_CRC_FORMAT = "I"
    _DATA_HEADER_FORMAT = "<IBH"
    _MAGIC_CHECK_FORMAT = ">H"

    def __init__(self):
        self.rscp_lib = RSCPLib()

    def encode_frame(self, data: bytes) -> bytes:
        magic_byte = self._endian_swap_uint16(0xe3dc)
        ctrl_byte = self._endian_swap_uint16(0x11)
        current_time = time.time()
        seconds = math.ceil(current_time)
        nanoseconds = round((current_time - int(current_time) * 1000))
        length = len(data)
        frame = struct.pack(self._FRAME_HEADER_FORMAT + str(length) + "s", magic_byte, ctrl_byte, seconds, nanoseconds,
                            length, data)
        checksum = zlib.crc32(frame) % (1 << 32)
        frame += struct.pack(self._FRAME_CRC_FORMAT, checksum)
        return frame

    def encode_data(self, payload: RSCPDTO) -> bytes:
        pack_format = ""
        tag_hex_code = self.rscp_lib.get_hex_code(payload.tag)
        type_hex_code = self.rscp_lib.get_data_type_hex(payload.type)
        data_header_length = struct.calcsize(self._DATA_HEADER_FORMAT)
        if payload.type == "None":
            return struct.pack(self._DATA_HEADER_FORMAT, tag_hex_code, type_hex_code, 0)
        elif payload.type == "Timestamp":
            timestamp = int(payload.data / 1000)
            milliseconds = (payload.data - timestamp * 1000) * 1e6
            high = timestamp >> 32
            low = timestamp & 0xffffffff
            length = struct.calcsize("iii") - data_header_length
            return struct.pack("iii", tag_hex_code, type_hex_code, length, high, low, milliseconds)
        elif payload.type == "Container":
            if isinstance(payload.data, list):
                new_data = b''
                for data_chunk in payload.data:
                    new_data += self.encode_data(RSCPDTO(data_chunk[0], data_chunk[1], data_chunk[2], None))
                payload.data = new_data
                pack_format += str(len(payload.data)) + self.rscp_lib.data_types_variable[payload.type]
        elif payload.type in self.rscp_lib.data_types_fixed:
            pack_format += self.rscp_lib.data_types_fixed[payload.type]
        elif payload.type in self.rscp_lib.data_types_variable:
            pack_format += str(len(payload.data)) + self.rscp_lib.data_types_variable[payload.type]

        data_length = struct.calcsize(pack_format) - data_header_length
        return struct.pack(pack_format, tag_hex_code, type_hex_code, data_length, payload.data)

    def _decode_frame(self, frame_data) -> tuple:
        """

        :param frame_data:
        :return:
        """
        crc = None
        magic, ctrl, seconds, nanoseconds, length = struct.unpack(self._FRAME_HEADER_FORMAT, frame_data[
                                                                                             :struct.calcsize(
                                                                                                 self._FRAME_HEADER_FORMAT)])
        if ctrl & 0x10:
            logger.info("CRC is enabled")
            total_length = struct.calcsize(self._FRAME_HEADER_FORMAT) + length + struct.calcsize(self._FRAME_CRC_FORMAT)
            data, crc = struct.unpack("<" + str(length) + "s" + self._FRAME_CRC_FORMAT,
                                      frame_data[struct.calcsize(self._FRAME_HEADER_FORMAT):total_length])
        else:
            total_length = struct.calcsize(self._FRAME_HEADER_FORMAT) + length
            data = \
                struct.unpack("<" + str(length) + "s",
                              frame_data[struct.calcsize(self._FRAME_HEADER_FORMAT):total_length])[
                    0]
            logger.info("CRC is disabled")

        self._check_crc_validity(crc, frame_data)
        timestamp = seconds + float(nanoseconds) / 1000
        return data, timestamp

    def decode_data(self, data: bytes) -> RSCPDTO:
        magic_byte = struct.unpack(self._MAGIC_CHECK_FORMAT, data[:struct.calcsize(self._MAGIC_CHECK_FORMAT)])[0]
        if magic_byte == 0xe3dc:
            decode_frame_result = self._decode_frame(data)
            return self.decode_data(decode_frame_result[0])

        data_header_size = struct.calcsize(self._DATA_HEADER_FORMAT)
        data_tag, data_type, data_length = struct.unpack(self._DATA_HEADER_FORMAT,
                                                         data[:data_header_size])
        data_tag_name = self.rscp_lib.get_data_tag_name(data_tag)
        data_type_name = self.rscp_lib.get_data_type_name(data_type)

        # Check the data type name to handle the values accordingly
        if data_type_name == "Container":
            container_data = []
            current_byte = data_header_size
            while current_byte < data_header_size + data_length:
                inner_data, used_length = self.decode_data(data[current_byte:])
                current_byte += used_length
                container_data.append(inner_data)
            return RSCPDTO(data_tag_name, data_type_name, container_data, current_byte)
        elif data_type_name == "Timestamp":
            data_format = "<iii"
            high, low, ms = struct.unpack(data_format,
                                          data[data_header_size:data_header_size + struct.calcsize(data_format)])
            timestamp = float(high + low) + (float(ms) * 1e-9)
            return RSCPDTO(data_tag_name, data_type_name, timestamp, data_header_size + struct.calcsize(data_format))
        elif data_type_name == "None":
            return RSCPDTO(data_tag_name, data_type_name, None, data_header_size)
        elif data_type_name in self.rscp_lib.data_types_fixed:
            data_format = "<" + self.rscp_lib.data_types_fixed[data_type_name]
        elif data_type_name in self.rscp_lib.data_types_variable:
            data_format = "<" + str(data_length) + self.rscp_lib.data_types_variable[data_type_name]
        else:
            raise RSCPDataError("Unknown data type", logger)

        value = struct.unpack(data_format, data[data_header_size:data_header_size + struct.calcsize(data_format)])[0]
        return RSCPDTO(data_tag_name, data_type_name, value, data_header_size + struct.calcsize(data_format))

    def _check_crc_validity(self, crc: str, frame_data: bytes):
        if crc is not None:
            frame_data_without_crc = frame_data[:-struct.calcsize("<" + self._FRAME_CRC_FORMAT)]
            calculated_crc = zlib.crc32(frame_data_without_crc) % (1 << 32)
            if calculated_crc != crc:
                raise RSCPFrameError("CRC32 not valid", logger)

    def _endian_swap_uint16(self, val: int) -> tuple:
        return struct.unpack("<H", struct.pack(">H", val))[0]
