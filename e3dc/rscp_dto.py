from typing import Optional, Union

from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType

"""
This is a data wrapper to send and receive data to the e3dc.
It consists of a tag, the type, the data and the size of the data.
"""


class RSCPDTO:
    def __init__(self, tag: RSCPTag, rscp_type: RSCPType = RSCPType.Nil, data: Union[list, float, str, None] = None,
                 size: Optional[int] = None):
        self.tag = tag
        self.type = rscp_type
        self.data = data
        self.size = size

    def set_data(self, value):
        self.data = value
