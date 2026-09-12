# perfect_maze

*[Version française](README.fr.md)*

<!-- --8<-- [start:intro] -->
A small, dependency-free Python library and command-line tool that generates
**perfect mazes** and renders them with UTF-8 box-drawing characters.

A perfect maze has no isolated cell and no loop: every cell can be reached
from every other one by exactly one path. Structurally it is a spanning tree
of the grid graph.

```text
┌─────┬─┬─┬─────┬───┬───┐
│ ╷ ╶─┘ │ └─┐ ╷ ╵ ╷ ╵ ┌─┤
│ ├─┬─╴ │ ╶─┘ ├─╴ └─┐ ╵ │
│ │ └─╴ └─╴ ╶─┼─┐ ╷ │ ╶─┤
│ ├───╴ ╶─────┘ │ │ │ ╶─┤
└─┴─────────────┴─┴─┴───┘
```

Requires Python 3.12 or later.

<!-- --8<-- [end:intro] -->

<!-- --8<-- [start:usage] -->
## Installation

```shell
pip install perfect-maze          # from PyPI, once published
pip install git+https://github.com/michaellaunay/perfect_maze.git
```

## Command line

```shell
perfect-maze                       # 6x4 maze on stdout
perfect-maze -w 40 -H 20           # 40 columns by 20 rows
perfect-maze -w 12 -H 5 --seed 42  # reproducible maze
perfect-maze -w 8 -H 8 -o maze.py  # also record the random draws into maze.py
python -m perfect_maze --help      # same tool, without the console script
```

| Option | Description |
| --- | --- |
| `-w`, `--width N` | number of cells per row (default 6) |
| `-H`, `--height N` | number of rows (default 4) |
| `-s`, `--seed N` | seed the random generator |
| `-o`, `--output PATH` | write the draw sequence, `open_walls` and the drawing to `PATH` |
| `-q`, `--quiet` | do not print the maze |
| `-V`, `--version` | print the version |

The file written by `--output` is valid Python. Its layout matches the test
fixtures, so an interesting maze can be pasted straight into
`tests/fixtures.py` as a regression case.

## Library

```python
from perfect_maze import build_maze, printable_maze

maze = build_maze(60, 40)
print(printable_maze(maze))  # or simply print(maze)
```

Reproducible generation and round-tripping:

```python
import random
from perfect_maze import build_maze, printable_maze

maze = build_maze(10, 8, randrange=random.Random(42).randrange)

# open_walls is the list of passages opened during generation, in order.
# Feeding it back rebuilds the very same maze without any randomness.
again = build_maze(10, 8, open_walls=maze.open_walls)
assert printable_maze(again) == printable_maze(maze)
```

Walking the maze:

```python
from perfect_maze import Direction

cell = maze[0, 0]  # cell at (x=0, y=0)
for direction, neighbour in cell.neighbours():
    if cell.is_open(direction):
        print(f"can go {direction.name} to cell {neighbour.index}")
```

Attach your own data to cells by subclassing `Cell` and passing
`cell_type=`:

```python
from perfect_maze import Cell, build_maze


class Room(Cell):
    __slots__ = ("visited",)

    def __init__(self, index: int = -1) -> None:
        super().__init__(index)
        self.visited = False


maze = build_maze(5, 5, cell_type=Room)
```

<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:algorithm] -->
## How it works

The grid starts with every wall built. Walls are then picked at random and
removed whenever they separate two cells that are not yet connected, using a
union-find structure to track connectivity. The loop stops after
`width * height - 1` walls have been removed, which is exactly the number of
edges of a spanning tree.

<!-- --8<-- [end:algorithm] -->

<!-- --8<-- [start:development] -->
## Development

```shell
git clone https://github.com/michaellaunay/perfect_maze.git
cd perfect_maze
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,docs]"

ruff format . && ruff check .      # formatting and linting
pytest --cov                       # tests with coverage
zensical serve                     # documentation with live reload
```

Documentation: <https://michaellaunay.github.io/perfect_maze/>

<!-- --8<-- [end:development] -->

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

GNU Affero General Public License v3.0 or later — see [LICENSE](LICENSE).
