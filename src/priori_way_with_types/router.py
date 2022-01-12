from typing import Awaitable, Union, cast

from fastapi import APIRouter
from httpx import AsyncClient, Client, Response


class GenderizeClient:
    def __init__(self, use_async: bool) -> None:
        self.use_async = use_async
        self.http_client = AsyncClient() if use_async else Client()

    def _get_common(self, resp: Response) -> str:
        resp.raise_for_status()
        return resp.json()["gender"]

    async def _get_async(self, name: str) -> str:
        resp = await cast(AsyncClient, self.http_client).get(
            f"https://api.genderize.io?name={name}"
        )
        return self._get_common(resp)

    def _get_sync(self, name: str) -> str:
        resp = cast(Client, self.http_client).get(
            f"https://api.genderize.io?name={name}"
        )
        return self._get_common(resp)

    def get(self, name: str) -> Union[Awaitable[str], str]:
        return self._get_async(name) if self.use_async else self._get_sync(name)

    def close(self) -> Union[Awaitable[None], None]:
        return (
            cast(AsyncClient, self.http_client).aclose()
            if self.use_async
            else cast(Client, self.http_client).close()
        )


router = APIRouter()


@router.get("/sync")
def sync_main(name: str) -> str:
    client = GenderizeClient(use_async=False)
    gender = cast(str, client.get(name))
    client.close()
    return gender


@router.get("/async")
async def async_main(name: str):
    client = GenderizeClient(use_async=True)
    gender = await cast(Awaitable[str], client.get(name))
    await cast(Awaitable[str], client.close())
    return gender
