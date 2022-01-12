from typing import Any

from fastapi import APIRouter
from httpx import AsyncClient, Client


class GenderizeClient:
    def __init__(self, use_async):
        self.use_async = use_async
        self.http_client: Any = AsyncClient() if use_async else Client()

    def _get_common(self, resp):
        resp.raise_for_status()
        return resp.json()["gender"]

    async def _get_async(self, name):
        resp = await self.http_client.get(f"https://api.genderize.io?name={name}")
        return self._get_common(resp)

    def _get_sync(self, name):
        resp = self.http_client.get(f"https://api.genderize.io?name={name}")
        return self._get_common(resp)

    def get(self, name):
        return self._get_async(name) if self.use_async else self._get_sync(name)

    def close(self):
        return self.http_client.aclose() if self.use_async else self.http_client.close()


router = APIRouter()


@router.get("/sync")
def sync_main(name: str):
    client = GenderizeClient(use_async=False)
    gender = client.get(name)
    client.close()
    return gender


@router.get("/async")
async def async_main(name: str):
    client = GenderizeClient(use_async=True)
    gender = await client.get(name)
    await client.close()
    return gender
