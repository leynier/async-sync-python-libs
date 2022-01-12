from fastapi import APIRouter

from . import AsyncGenderizeClient, SyncGenderizeClient

router = APIRouter()


@router.get("/sync")
def sync_main(name: str) -> str:
    client = SyncGenderizeClient()
    gender = client.get(name)
    client.close()
    return gender


@router.get("/async")
async def async_main(name: str):
    client = AsyncGenderizeClient()
    gender = await client.get(name)
    await client.close()
    return gender
