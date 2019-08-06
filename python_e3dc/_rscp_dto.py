from typing import NamedTuple, Optional, Union

from python_e3dc.rscp_tag import RSCPTag
from python_e3dc.rscp_type import RSCPType


class RSCPDTO(NamedTuple):
    tag: RSCPTag
    type: RSCPType
    data: Union[list, float, None]
    size: Optional[int]
