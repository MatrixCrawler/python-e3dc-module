from python_e3dc._rscp_dto import RSCPDTO
from python_e3dc.rscp import RSCP


class E3DC:
    def __init__(self, username, password, ip, key):
        self.rscp = RSCP(username, password, ip, key)

    def send_requests(self, requests: [RSCPDTO]) -> [RSCPDTO]:
        responses = []
        request: RSCPDTO
        for request in requests:
            responses.append(self.send_request(request))
        return responses

    def send_request(self, request: RSCPDTO) -> RSCPDTO:
        response = self.rscp.send_request(request)
        return response
