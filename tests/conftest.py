import pytest

from tests.fixtures import MAZES, MazeFixture


@pytest.fixture(params=MAZES, ids=[m.name for m in MAZES])
def fixture(request: pytest.FixtureRequest) -> MazeFixture:
    """Each reference maze in turn."""
    return request.param
