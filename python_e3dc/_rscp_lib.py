class RSCPLib:
    data_types_fixed = {
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
        "Double64": "d"
    }
    data_types_variable = {
        "Bitfield": "s",
        "CString": "s",
        "Container": "s",
        "ByteArray": "s",
        "Error": "s"
    }
