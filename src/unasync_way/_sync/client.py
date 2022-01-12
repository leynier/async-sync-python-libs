from httpx import Response

from ..utils import SyncClient


class SyncGenderizeClient:
    def __init__(self) -> None:
        self.http_client = SyncClient()

    def _get_common(self, resp: Response) -> str:
        resp.raise_for_status()
        return resp.json()["gender"]

    def _get_async(self, name: str) -> str:
        resp = self.http_client.get(f"https://api.genderize.io?name={name}")
        return self._get_common(resp)

    def get(self, name: str) -> str:
        return self._get_async(name)

    def close(self) -> None:
        return self.http_client.aclose()
