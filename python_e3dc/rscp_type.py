from enum import Enum


class RSCPType(Enum):
    Nil = (0x00, None)
    Bool = (0x01, "?")
    Char8 = (0x02, "b")
    UChar8 = (0x03, "B")
    Int16 = (0x04, "h")
    Uint16 = (0x05, "H")
    Int32 = (0x06, "i")
    Uint32 = (0x07, "I")
    Int64 = (0x08, "q")
    Uint64 = (0x09, "Q")
    Float32 = (0x0A, "f")
    Double64 = (0x0B, "d")
    Bitfield = (0x0C, "s")
    CString = (0x0D, "s")
    Container = (0x0E, "s")
    Timestamp = (0x0F, "s")
    ByteArray = (0x10, "s")
    Error = (0xFF, None)

    def get(self, code: int):
        for key, (member_code, member_fmt) in self._member_map_:
            if member_code == code:
                return self._member_map_[key]

    def __init__(self, value):
        for key, (member_code, member_format) in self._member_map_:
            if member_code == value:
                return self._member_map_[key]

    def __new__(cls, value):
        for key, (member_code, member_format) in cls._member_map_:
            if member_code == value:
                return cls._member_map_[key]

    # def fmt(self):
    #     return self._fmt
    #
    # @fmt.setter
    # def fmt(self, value):
    #     self._fmt = value
