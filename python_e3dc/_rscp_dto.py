from typing import Optional, Union

from python_e3dc.rscp_tag import RSCPTag
from python_e3dc.rscp_type import RSCPType


class RSCPDTO:
    def __init__(self, tag: RSCPTag, rscp_type: RSCPType = RSCPType.Nil, data: Union[list, float, str, None] = None,
                 size: Optional[int] = None):
        self.tag = tag
        self.type = rscp_type
        self.data = data
        self.size = size

    def set_data(self, value):
        self.data = value
