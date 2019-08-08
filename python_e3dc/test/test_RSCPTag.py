from python_e3dc._rscp_tag import RSCPTag


def test_rscptag_value_is_returned():
    result = RSCPTag['SERVER_REGISTER_CONNECTION'].value
    assert result == 0xF800A001

def test_rscptag_name_is_returned():
    result = RSCPTag(0xF800A001).name
    assert result == 'SERVER_REGISTER_CONNECTION'
