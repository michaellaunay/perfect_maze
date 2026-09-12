# Usage

## Installation

```shell
pip install perfect-maze          # from PyPI, once published
pip install git+https://github.com/michaellaunay/perfect_maze.git
```

Python 3.12 or later is required.

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

### Reproducible generation

Pass any callable with the signature of `random.randrange`:

```python
import random

maze = build_maze(10, 8, randrange=random.Random(42).randrange)
```

[`Maze.open_walls`][perfect_maze.maze.Maze] records every passage opened
during generation, in order. Feeding it back rebuilds the very same maze
without any randomness:

```python
again = build_maze(10, 8, open_walls=maze.open_walls)
assert printable_maze(again) == printable_maze(maze)
```

### Walking the maze

```python
from perfect_maze import Direction

cell = maze[0, 0]  # cell at (x=0, y=0)
for direction, neighbour in cell.neighbours():
    if cell.is_open(direction):
        print(f"can go {direction.name} to cell {neighbour.index}")
```

### Custom cells

Subclass [`Cell`][perfect_maze.maze.Cell] and pass it as `cell_type` to
attach your own data to every cell:

```python
from perfect_maze import Cell, build_maze


class Room(Cell):
    __slots__ = ("visited",)

    def __init__(self, index: int = -1) -> None:
        super().__init__(index)
        self.visited = False


maze = build_maze(5, 5, cell_type=Room)
```

## Development

```shell
git clone https://github.com/michaellaunay/perfect_maze.git
cd perfect_maze
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,docs]"

ruff format . && ruff check .      # formatting and linting
pytest --cov                       # tests with coverage
mkdocs serve                       # documentation with live reload
```
