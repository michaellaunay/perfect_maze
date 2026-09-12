"""Generation: reference fixtures, replay and structural properties."""

from __future__ import annotations

import random
from collections import deque

import pytest

from perfect_maze import Cell, Direction, Maze, build_maze, printable_maze
from tests.fixtures import MazeFixture


def replay(sequence: tuple[int, ...]):
    """A ``randrange`` stub returning ``sequence`` values in order."""
    draws = iter(sequence)

    def randrange(_start: int, _stop: int) -> int:
        return next(draws)

    return randrange


def as_ints(open_walls) -> tuple[tuple[int, int, int], ...]:
    return tuple(tuple(int(v) for v in wall) for wall in open_walls)


# -- reference fixtures -------------------------------------------------------


def test_build_from_random_sequence(fixture: MazeFixture) -> None:
    maze = build_maze(
        fixture.width, fixture.height, randrange=replay(fixture.randrange)
    )
    assert as_ints(maze.open_walls) == fixture.open_walls
    assert printable_maze(maze) == fixture.pmaze


def test_rebuild_from_open_walls(fixture: MazeFixture) -> None:
    maze = build_maze(fixture.width, fixture.height, open_walls=fixture.open_walls)
    assert as_ints(maze.open_walls) == fixture.open_walls
    assert printable_maze(maze) == fixture.pmaze


def test_open_walls_are_directions(fixture: MazeFixture) -> None:
    maze = build_maze(fixture.width, fixture.height, open_walls=fixture.open_walls)
    assert all(isinstance(d, Direction) for _, _, d in maze.open_walls)


# -- structural properties of a perfect maze ----------------------------------


def reachable(maze: Maze, start: Cell) -> set[Cell]:
    seen = {start}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for direction, other in cell.neighbours():
            if cell.is_open(direction) and other not in seen:
                seen.add(other)
                queue.append(other)
    return seen


@pytest.mark.parametrize(
    ("width", "height"), [(1, 1), (1, 7), (7, 1), (2, 2), (5, 3), (20, 15)]
)
@pytest.mark.parametrize("seed", [0, 1, 42])
def test_generated_maze_is_perfect(width: int, height: int, seed: int) -> None:
    maze = build_maze(width, height, randrange=random.Random(seed).randrange)
    n = width * height
    assert len(maze) == n
    # Exactly n - 1 passages: the number of edges of a spanning tree.
    assert len(maze.open_walls) == n - 1
    open_count = sum(cell.is_open(d) for cell in maze for d, _ in cell.neighbours())
    assert open_count == 2 * (n - 1), "each passage is counted once per side"
    # Connected: every cell is reachable from the first one.
    assert len(reachable(maze, maze[0, 0])) == n
    # n vertices, n - 1 edges and connected => a tree, hence no loop.


def test_same_seed_same_maze() -> None:
    a = build_maze(9, 7, randrange=random.Random(7).randrange)
    b = build_maze(9, 7, randrange=random.Random(7).randrange)
    assert a.open_walls == b.open_walls
    assert printable_maze(a) == printable_maze(b)


def test_open_walls_round_trip() -> None:
    original = build_maze(12, 9, randrange=random.Random(3).randrange)
    rebuilt = build_maze(12, 9, open_walls=original.open_walls)
    assert rebuilt.open_walls == original.open_walls
    assert printable_maze(rebuilt) == printable_maze(original)


# -- graph consistency --------------------------------------------------------


def test_neighbours_share_a_single_wall() -> None:
    maze = build_maze(4, 3, randrange=random.Random(0).randrange)
    for cell in maze:
        for direction, other in cell.neighbours():
            assert other.neighbour(direction.opposite) is cell
            assert cell.wall(direction) is other.wall(direction.opposite)


def test_border_walls_are_outer_and_built() -> None:
    maze = build_maze(4, 3, randrange=random.Random(0).randrange)
    for cell in maze:
        for direction in Direction:
            if cell.neighbour(direction) is None:
                wall = cell.wall(direction)
                assert wall.is_outer
                assert wall.is_built
                assert list(wall) == [cell, None]


def test_cell_indexes_are_row_major() -> None:
    maze = build_maze(5, 3, randrange=random.Random(0).randrange)
    assert [cell.index for cell in maze] == list(range(15))
    assert maze[4, 2].index == 14
    assert maze[4, 2] is maze.cells[2][4]


# -- arguments ----------------------------------------------------------------


@pytest.mark.parametrize(("width", "height"), [(0, 3), (3, 0), (-1, 1), (0, 0)])
def test_invalid_size_is_rejected(width: int, height: int) -> None:
    with pytest.raises(ValueError, match="must be >= 1"):
        build_maze(width, height)


def test_custom_cell_type() -> None:
    class Visited(Cell):
        __slots__ = ("visited",)

        def __init__(self, index: int = -1) -> None:
            super().__init__(index)
            self.visited = False

    maze = build_maze(3, 3, randrange=random.Random(0).randrange, cell_type=Visited)
    assert all(isinstance(cell, Visited) for cell in maze)
    assert not any(cell.visited for cell in maze)


def test_positional_options_are_rejected() -> None:
    with pytest.raises(TypeError):
        build_maze(3, 3, random.randrange)  # type: ignore[misc]


def test_maze_dunder_methods() -> None:
    maze = build_maze(2, 2, open_walls=((0, 0, 1), (0, 0, 2), (1, 1, 3)))
    assert repr(maze) == "Maze(2x2)"
    assert str(maze) == printable_maze(maze)
    assert repr(maze[1, 0]) == "Cell(1)"
    assert "open" in repr(maze[0, 0].wall(Direction.EAST))
    assert "built" in repr(maze[0, 0].wall(Direction.NORTH))


def test_wall_access_before_link_fails() -> None:
    with pytest.raises(ValueError, match="no wall towards NORTH"):
        Cell(0).wall(Direction.NORTH)


def test_direction_opposite() -> None:
    assert Direction.NORTH.opposite is Direction.SOUTH
    assert Direction.EAST.opposite is Direction.WEST
    assert Direction.SOUTH.opposite is Direction.NORTH
    assert Direction.WEST.opposite is Direction.EAST
