"""UTF-8 rendering."""

from __future__ import annotations

import random

from perfect_maze import build_maze, printable_maze
from tests.fixtures import MazeFixture


def test_render_matches_fixture(fixture: MazeFixture) -> None:
    maze = build_maze(fixture.width, fixture.height, open_walls=fixture.open_walls)
    assert printable_maze(maze) == fixture.pmaze


def test_single_cell() -> None:
    assert printable_maze(build_maze(1, 1)) == "┌─┐\n└─┘"


def test_dimensions() -> None:
    for width, height in [(1, 1), (3, 5), (10, 2)]:
        rendered = printable_maze(
            build_maze(width, height, randrange=random.Random(1).randrange)
        )
        lines = rendered.split("\n")
        assert len(lines) == height + 1
        assert all(len(line) == 2 * width + 1 for line in lines)


def test_outer_border_is_closed() -> None:
    lines = printable_maze(
        build_maze(8, 6, randrange=random.Random(5).randrange)
    ).split("\n")
    assert lines[0][0] == "┌" and lines[0][-1] == "┐"
    assert lines[-1][0] == "└" and lines[-1][-1] == "┘"
    for line in lines[1:-1]:
        assert line[0] in "│├" and line[-1] in "│┤"
    assert set(lines[0][1:-1]) <= {"─", "┬"}
    assert set(lines[-1][1:-1]) <= {"─", "┴"}


def test_corridors() -> None:
    # 3x1 with both walls open: a horizontal corridor.
    maze = build_maze(3, 1, open_walls=((0, 0, 1), (1, 0, 1)))
    assert printable_maze(maze) == "┌─────┐\n└─────┘"
    # 1x3 with both walls open: a vertical corridor.
    maze = build_maze(1, 3, open_walls=((0, 0, 2), (0, 1, 2)))
    assert printable_maze(maze) == "┌─┐\n│ │\n│ │\n└─┘"
