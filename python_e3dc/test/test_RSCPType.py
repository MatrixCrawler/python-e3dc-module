from python_e3dc.rscp_type import RSCPType


def test_rscptype_value_is_returned():
    result = RSCPType['Nil'].value
    assert result == 0x00


def test_rscptype_name_is_returned():
    result = RSCPType(0x00).name
    assert result == 'Nil'
