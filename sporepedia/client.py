from .api import APIClient


class Client():
    def __init__(self):
        self._api_client = APIClient()
