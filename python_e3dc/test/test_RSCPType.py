from python_e3dc._rscp_type import RSCPType


def test_rscptype_value_is_returned():
    result = RSCPType['Nil'].value
    assert result == 0x00


def test_rscptype_name_is_returned():
    result = RSCPType(0x00).name
    assert result == 'Nil'


def test_rscptype_mapping_is_returned():
    result = RSCPType(0x00).mapping
    assert result is None
