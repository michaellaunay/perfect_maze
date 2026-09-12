"""Record the random draws used to build a maze.

The output file is valid Python and matches the layout of the test fixtures
in ``tests/fixtures.py``, which makes it easy to turn an interesting maze
into a regression test.
"""

from __future__ import annotations

import random
from pathlib import Path

from perfect_maze.maze import Maze, RandRange, build_maze
from perfect_maze.render import printable_maze

__all__ = ["record_maze_construction"]


def record_maze_construction(
    width: int,
    height: int,
    path: str | Path,
    *,
    randrange: RandRange = random.randrange,
) -> Maze:
    """Build a maze while recording every random draw into ``path``.

    The file contains, as Python assignments: ``width``, ``height``, the
    full ``randrange`` draw sequence (including rejected draws), the
    resulting ``open_walls`` and the printable maze ``pmaze``.

    Args:
        width: Number of cells per row.
        height: Number of rows.
        path: Destination file, overwritten if it exists.
        randrange: Underlying random source to spy on.

    Returns:
        The generated maze.
    """
    draws: list[int] = []

    def spy(start: int, stop: int) -> int:
        value = randrange(start, stop)
        draws.append(value)
        return value

    maze = build_maze(width, height, randrange=spy)
    content = (
        f"width = {width}\n"
        f"height = {height}\n"
        f"randrange = {draws!r}\n"
        f"open_walls = {tuple(tuple(int(v) for v in w) for w in maze.open_walls)!r}\n"
        f'pmaze = """{printable_maze(maze)}"""\n'
    )
    Path(path).write_text(content, encoding="utf-8")
    return maze
