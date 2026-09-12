"""Perfect maze generator.

A *perfect* maze is a maze in which every cell is reachable from every
other cell by exactly one path: it has no isolated cell and no loop.
Structurally it is a spanning tree of the grid graph.

Typical use::

    >>> from perfect_maze import build_maze, printable_maze
    >>> maze = build_maze(6, 4)
    >>> print(printable_maze(maze))  # doctest: +SKIP
    ┌─────┬─────┐
    │ ╷ ╷ └───╴ │
    ├─┴─┤ ╶─┐ ┌─┤
    ├─╴ └─╴ └─┘ │
    └───────────┘
"""

from perfect_maze._version import __version__
from perfect_maze.maze import (
    Cell,
    Direction,
    Maze,
    OpenWall,
    RandRange,
    Wall,
    build_maze,
)
from perfect_maze.recorder import record_maze_construction
from perfect_maze.render import printable_maze

__all__ = [
    "Cell",
    "Direction",
    "Maze",
    "OpenWall",
    "RandRange",
    "Wall",
    "__version__",
    "build_maze",
    "printable_maze",
    "record_maze_construction",
]
