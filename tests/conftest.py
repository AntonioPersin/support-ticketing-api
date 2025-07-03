# conftest.py
import pytest
from httpx import AsyncClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from src.main import app

@pytest.fixture(scope="session", autouse=True)
def initialize_cache():
    # Inicijalizira cache jednom po testnoj sesiji
    FastAPICache.init(InMemoryBackend(), prefix="test_cache")

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
