from httpx import Response

from ..utils import AsyncClient


class AsyncGenderizeClient:
    def __init__(self) -> None:
        self.http_client = AsyncClient()

    def _get_common(self, resp: Response) -> str:
        resp.raise_for_status()
        return resp.json()["gender"]

    async def _get_async(self, name: str) -> str:
        resp = await self.http_client.get(f"https://api.genderize.io?name={name}")
        return self._get_common(resp)

    async def get(self, name: str) -> str:
        return await self._get_async(name)

    async def close(self) -> None:
        return await self.http_client.aclose()
