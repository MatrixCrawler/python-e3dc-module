from typing import NamedTuple, Optional, Union


class RSCPDTO(NamedTuple):
    tag: str
    type: str
    data: Union[list, float, None]
    size: Optional[int]
