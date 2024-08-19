"""Set up some common test helper things."""

import json
from pathlib import Path
from typing import Any

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation


@pytest.fixture
def stations() -> list[dict[str, Any]]:
    """Return stations data from the fixture file."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def station() -> list[dict[str, Any]]:
    """Return the station data from the fixture file."""
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def indexes() -> dict[str, Any]:
    """Return indexes data from the fixture file."""
    with open("tests/fixtures/indexes.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_658() -> dict[str, Any]:
    """Return sensor 658 data from the fixture file."""
    with open("tests/fixtures/sensor_658.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_660() -> dict[str, Any]:
    """Return sensor 660 data from the fixture file."""
    with open("tests/fixtures/sensor_660.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_665() -> dict[str, Any]:
    """Return sensor 665 data from the fixture file."""
    with open("tests/fixtures/sensor_665.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_667() -> dict[str, Any]:
    """Return sensor 667 data from the fixture file."""
    with open("tests/fixtures/sensor_667.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_670() -> dict[str, Any]:
    """Return sensor 670 data from the fixture file."""
    with open("tests/fixtures/sensor_670.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_672() -> dict[str, Any]:
    """Return sensor 672 data from the fixture file."""
    with open("tests/fixtures/sensor_672.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sensor_14395() -> dict[str, Any]:
    """Return sensor 14395 data from the fixture file."""
    with open("tests/fixtures/sensor_14395.json", encoding="utf-8") as file:
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
