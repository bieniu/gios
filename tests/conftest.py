"""Set up some common test helper things."""

import json
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

import aiohttp
import pytest
import pytest_asyncio
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation

BASE = "tests/fixtures/"


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[aiohttp.ClientSession]:
    """Return a mock ClientSession."""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def session_mock() -> Generator[aioresponses]:
    """Create a reusable aioresponses mock."""
    with aioresponses() as mock:
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
