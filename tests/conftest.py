"""Set up some common test helper things."""

import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import aiohttp
import pytest
import pytest_asyncio
from aiointercept import aiointercept
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation

BASE = "tests/fixtures/"


@pytest_asyncio.fixture(loop_scope="function")
async def session(session_mock: aiointercept) -> AsyncGenerator[aiohttp.ClientSession]:  # noqa: ARG001
    """Return a mock ClientSession."""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(loop_scope="function")
async def session_mock() -> AsyncGenerator[aiointercept]:
    """Create a reusable aiointercept mock."""
    async with aiointercept(mock_external_urls=True) as mock:
        yield mock


@pytest.fixture
def stations() -> list[dict[str, Any]]:
    """Return stations data from the fixture file."""
    with Path.open(Path(f"{BASE}stations.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def station() -> list[dict[str, Any]]:
    """Return the station data from the fixture file."""
    with Path.open(Path(f"{BASE}station.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def indexes() -> dict[str, Any]:
    """Return indexes data from the fixture file."""
    with Path.open(Path(f"{BASE}indexes.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3759() -> dict[str, Any]:
    """Return sensor 3759 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3759.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3760() -> dict[str, Any]:
    """Return sensor 3760 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3760.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3761() -> dict[str, Any]:
    """Return sensor 3761 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3761.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3762() -> dict[str, Any]:
    """Return sensor 3762 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3762.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3764() -> dict[str, Any]:
    """Return sensor 3764 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3764.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_3765() -> dict[str, Any]:
    """Return sensor 3765 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_3765.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_14688() -> dict[str, Any]:
    """Return sensor 14688 data from the fixture file."""
    with Path.open(Path(f"{BASE}sensor_14688.json"), encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture."""
    return snapshot.use_extension(SnapshotExtension)


class SnapshotExtension(AmberSnapshotExtension):
    """Extension for Syrupy."""

    @classmethod
    def dirname(cls, *, test_location: PyTestLocation) -> str:
        """Return the directory for the snapshot files."""
        test_dir = Path(test_location.filepath).parent
        return str(test_dir.joinpath("snapshots"))
