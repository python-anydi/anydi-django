from collections.abc import AsyncIterator

import pytest

from anydi_django import container


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def start_container() -> AsyncIterator[None]:
    await container.astart()
    yield
    await container.aclose()
