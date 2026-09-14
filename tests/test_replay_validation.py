"""Strict replay validation, independent of the random generation loop."""

from __future__ import annotations

import copy
import itertools
import json
import random

import pytest

import perfect_maze
from perfect_maze import Cell, Direction, build_maze, printable_maze
from tests.fixtures import MazeFixture


def forbidden_random(_start: int, _stop: int) -> int:
    raise AssertionError("replay must never call randrange")


@pytest.mark.parametrize(
    ("width", "height", "walls"),
    [
        (2, 1, []),
        (2, 1, [(0, 0, 1), (999, 999, 99)]),
        (1, 1, [(999, 999, 99)]),
        (2, 1, [(0, 0), (1,)]),
        (2, 2, [(0, 0, 1), (0, 0, 2)]),
    ],
)
def test_replay_requires_exactly_n_minus_one_records(width, height, walls) -> None:
    with pytest.raises(ValueError, match="exactly") as exc:
        build_maze(width, height, open_walls=walls, randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize(
    "walls", [0, "", "001", b"", bytearray(), memoryview(b""), {}, set(), iter(())]
)
def test_replay_rejects_non_sequences_and_text_even_for_single_cell(walls) -> None:
    with pytest.raises(ValueError, match="sequence") as exc:
        build_maze(1, 1, open_walls=walls, randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize(
    "record",
    [
        (),
        (0, 0),
        (0, 0, 1, 2),
        "001",
        b"\x00\x00\x01",
        bytearray([0, 0, 1]),
        memoryview(b"\x00\x00\x01"),
        {0: 0, 1: 0, 2: 1},
        {0, 1, 2},
        1,
        None,
    ],
)
def test_replay_preserves_record_boundaries(record) -> None:
    with pytest.raises(ValueError, match=r"open_walls\[0\].*triplet") as exc:
        build_maze(2, 1, open_walls=[record], randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize("field", range(3), ids=["x", "y", "direction"])
@pytest.mark.parametrize("value", [True, False, 0.0, 1.0, "0", None])
def test_replay_requires_integers_but_not_booleans(field, value) -> None:
    record = [0, 0, 1]
    record[field] = value
    with pytest.raises(ValueError, match=r"open_walls\[0\].*integers") as exc:
        build_maze(2, 1, open_walls=[record], randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize("record", [(-1, 0, 3), (2, 0, 3), (0, -1, 2), (0, 1, 0)])
def test_replay_rejects_coordinates_outside_grid(record) -> None:
    with pytest.raises(ValueError, match=r"open_walls\[0\].*coordinates") as exc:
        build_maze(2, 1, open_walls=[record], randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize("direction", [-1, 4, 999])
def test_replay_rejects_unknown_directions(direction: int) -> None:
    with pytest.raises(ValueError, match=r"open_walls\[0\].*direction") as exc:
        build_maze(2, 1, open_walls=[(0, 0, direction)])
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize("record", [(0, 0, 0), (1, 0, 1), (0, 1, 2), (0, 0, 3)])
def test_replay_rejects_outer_walls(record) -> None:
    walls = [record, (0, 0, 1), (0, 0, 2)]
    with pytest.raises(ValueError, match=r"open_walls\[0\].*outer wall") as exc:
        build_maze(2, 2, open_walls=walls, randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


@pytest.mark.parametrize("duplicate", [(0, 0, 1), (1, 0, 3)])
def test_replay_rejects_duplicates_from_either_side(duplicate) -> None:
    walls = [(0, 0, 1), duplicate, (0, 0, 2)]
    with pytest.raises(ValueError, match=r"open_walls\[1\].*duplicate") as exc:
        build_maze(2, 2, open_walls=walls, randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


def test_replay_rejects_a_cycle_even_with_the_correct_edge_count() -> None:
    # A square cycle on the left plus one passage: five edges, six cells,
    # and a disconnected bottom-right cell. Counting edges alone is insufficient.
    walls = [(0, 0, 1), (1, 0, 2), (1, 1, 3), (0, 1, 0), (1, 0, 1)]
    with pytest.raises(ValueError, match=r"open_walls\[3\].*cycle") as exc:
        build_maze(3, 2, open_walls=walls, randrange=forbidden_random)
    assert isinstance(exc.value, perfect_maze.MazeFormatError)


def test_invalid_replay_is_validated_before_creating_any_cell() -> None:
    class ForbiddenCell(Cell):
        def __init__(self, index: int = -1) -> None:
            raise AssertionError("invalid replay must not construct cells")

    # The first passage is valid, the second crosses the outer boundary.
    with pytest.raises(ValueError, match=r"open_walls\[1\].*outer wall"):
        build_maze(
            2,
            2,
            open_walls=[(0, 0, 1), (0, 0, 0), (0, 0, 2)],
            randrange=forbidden_random,
            cell_type=ForbiddenCell,
        )


def test_error_is_exported_as_a_value_error() -> None:
    from perfect_maze.maze import MazeFormatError

    assert perfect_maze.MazeFormatError is MazeFormatError
    assert issubclass(MazeFormatError, ValueError)


def test_replay_preserves_fixture_order_and_never_uses_randomness(
    fixture: MazeFixture,
) -> None:
    maze = build_maze(
        fixture.width,
        fixture.height,
        open_walls=fixture.open_walls,
        randrange=forbidden_random,
    )
    assert maze.open_walls == fixture.open_walls
    assert all(isinstance(d, Direction) for _, _, d in maze.open_walls)
    assert printable_maze(maze) == fixture.pmaze


def test_replay_accepts_json_lists_without_modifying_them() -> None:
    walls = json.loads("[[0, 0, 1], [0, 0, 2], [1, 1, 3]]")
    original = copy.deepcopy(walls)
    maze = build_maze(2, 2, open_walls=walls, randrange=forbidden_random)
    assert walls == original
    assert maze.open_walls == ((0, 0, 1), (0, 0, 2), (1, 1, 3))
    walls[0][0] = 999
    assert maze.open_walls[0][0] == 0


def test_replay_preserves_custom_cell_type() -> None:
    class Room(Cell):
        __slots__ = ("visited",)

        def __init__(self, index: int = -1) -> None:
            super().__init__(index)
            self.visited = False

    maze = build_maze(2, 1, open_walls=[(0, 0, Direction.EAST)], cell_type=Room)
    assert all(isinstance(cell, Room) for cell in maze)
    assert [cell.index for cell in maze] == [0, 1]
    assert not any(cell.visited for cell in maze)


def test_replay_accepts_reordered_and_reversed_passages() -> None:
    original = build_maze(5, 4, randrange=random.Random(7).randrange)
    walls = []
    steps = ((0, -1), (1, 0), (0, 1), (-1, 0))
    for x, y, value in reversed(original.open_walls):
        direction = Direction(value)
        dx, dy = steps[direction]
        walls.append((x + dx, y + dy, direction.opposite))
    replayed = build_maze(5, 4, open_walls=walls, randrange=forbidden_random)
    assert replayed.open_walls == tuple(walls)
    assert printable_maze(replayed) == printable_maze(original)


@pytest.mark.parametrize(("width", "height"), [(1, 1), (2, 2), (3, 2), (3, 3)])
def test_replay_accepts_exactly_the_spanning_trees(width: int, height: int) -> None:
    # Enumerate every n-1 edge subset; use an independent traversal as the oracle.
    edges = []
    for y in range(height):
        for x in range(width):
            if x + 1 < width:
                edges.append((x, y, Direction.EAST))
            if y + 1 < height:
                edges.append((x, y, Direction.SOUTH))
    size = width * height
    for walls in itertools.combinations(edges, size - 1):
        adjacent = [set() for _ in range(size)]
        for x, y, direction in walls:
            a = y * width + x
            b = a + (1 if direction is Direction.EAST else width)
            adjacent[a].add(b)
            adjacent[b].add(a)
        seen = {0}
        pending = [0]
        while pending:
            for neighbour in adjacent[pending.pop()] - seen:
                seen.add(neighbour)
                pending.append(neighbour)
        if len(seen) == size:
            maze = build_maze(width, height, open_walls=walls)
            assert maze.open_walls == walls
        else:
            with pytest.raises(ValueError):
                build_maze(width, height, open_walls=walls)
