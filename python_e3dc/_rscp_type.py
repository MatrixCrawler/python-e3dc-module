from enum import Enum

_data_type_mapping = {
    "Bool": "?",
    "Char8": "b",
    "UChar8": "B",
    "Int16": "h",
    "Uint16": "H",
    "Int32": "i",
    "Uint32": "I",
    "Int64": "q",
    "Uint64": "Q",
    "Float32": "f",
    "Double64": "d",
    "Bitfield": "s",
    "CString": "s",
    "Container": "s",
    "ByteArray": "s",
    "Error": "s",
    "Nil": None,
}


class RSCPType(Enum):
    Nil = 0x00
    Bool = 0x01
    Char8 = 0x02
    UChar8 = 0x03
    Int16 = 0x04
    Uint16 = 0x05
    Int32 = 0x06
    Uint32 = 0x07
    Int64 = 0x08
    Uint64 = 0x09
    Float32 = 0x0A
    Double64 = 0x0B
    Bitfield = 0x0C
    CString = 0x0D
    Container = 0x0E
    Timestamp = 0x0F
    ByteArray = 0x10
    Error = 0xFF

    @property
    def mapping(self):
        return _data_type_mapping[self.name]
