from typing import Union

from python_e3dc._rscp_dto import RSCPDTO
from python_e3dc.rscp import RSCP
from python_e3dc.rscp_tag import RSCPTag


class E3DC:
    def __init__(self, username, password, ip, key):
        self.rscp = RSCP(username, password, ip, key)

    def send_requests(self, requests: [Union[RSCPDTO, RSCPTag]]) -> [RSCPDTO]:
        dto_list: [RSCPDTO] = []
        if isinstance(requests[0], RSCPTag):
            for tag in requests:
                dto_list.append(RSCPDTO(tag))
        else:
            dto_list = requests
        responses = []
        dto: RSCPDTO
        for dto in dto_list:
            responses.append(self.send_request(dto))
        return responses

    def send_request(self, request: Union[RSCPDTO, RSCPTag]) -> RSCPDTO:
        if isinstance(request, RSCPTag):
            request = RSCPDTO(request)
        response = self.rscp.send_request(request)
        return response


if __name__ == '__main__':
    e3dc = E3DC('usrname', 'password', '127.0.0.1', 'key')
    e3dc.send_requests(
        [RSCPTag.EMS_REQ_BAT_SOC, RSCPTag.EMS_REQ_POWER_PV, RSCPTag.EMS_REQ_POWER_BAT, RSCPTag.EMS_REQ_POWER_GRID,
         RSCPTag.EMS_REQ_POWER_WB_ALL])
