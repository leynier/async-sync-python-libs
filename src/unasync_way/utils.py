from httpx import AsyncClient
from httpx import Client as _Client


class SyncClient(_Client):
    def aclose(self):
        return self.close()
