import httpx
import pytest


@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
async def async_client():
    # Setup for async HTTP client testing
    async with httpx.AsyncClient() as client:
        yield client