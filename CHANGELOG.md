# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-09-12

### Changed (breaking)

- The importable package is now `perfect_maze` (was `maze`); the
  distribution name is `perfect-maze`.
- Python 3.12 or later is required.
- `build_maze(width, length, ...)` is now `build_maze(width, height, *, ...)`:
  `length` is renamed `height` and the options `randrange`, `open_walls` and
  `cell_type` are keyword-only.
- `Maze.length` → `Maze.height`, `Cell.n` → `Cell.index`,
  `Wall.is_build` → `Wall.is_built`, `DIRECTIONS` → `Direction` (an
  `IntEnum`), `spy_maze_construction` → `record_maze_construction`.
- The module-level constants `NORTH`, `EAST`, `SOUTH`, `WEST` are removed;
  use `Direction.NORTH` etc.
- Command line rewritten with `argparse`: options are `--width/-w`,
  `--height/-H`, `--seed/-s`, `--output/-o`, `--quiet/-q`, `--version/-V`.
  A `perfect-maze` console script is installed and `python -m perfect_maze`
  works.

### Added

- `--seed` option for reproducible mazes.
- `Maze[x, y]`, `iter(maze)`, `len(maze)`, `str(maze)`.
- `Cell.wall()`, `Cell.neighbour()`, `Cell.neighbours()`, `Cell.is_open()`,
  `Wall.is_outer`, `Direction.opposite`.
- `build_maze` raises `ValueError` for sizes lower than 1.
- Type hints throughout and a `py.typed` marker.
- Tests covering the structural properties of a perfect maze, replay from
  `open_walls`, custom cell types, the recorder and the CLI.
- GitHub Actions workflow running ruff and pytest.

### Fixed

- `Maze.update_open_walls` was declared without `self` (method removed).
- The CLI documented `--fout` but accepted `--fileout`, misspelt `--quiet`
  as `--quite`, and printed the usage to stdout with `sys.stderr` as a
  positional argument.
- The output file was opened twice and its header line overwritten.

### Performance

- Connectivity is tracked with a union-find structure instead of Python
  lists searched linearly, turning the generation from quadratic to
  near-linear in the number of cells. The random draw sequence is unchanged,
  so recorded mazes still replay identically.

## [0.1.4] - 2022-04-10

- Add Pipfile and Sphinx to generate documentation.

## [0.1.3] - 2022-03-30

- Pylint and Flake8 corrections.

## [0.1.2] - 2022-01-27

- Add `open_walls` parameter to `build_maze` to reload a maze.
- Add argument parsing to use the module as a stand-alone script.

[1.0.0]: https://github.com/michaellaunay/perfect_maze/compare/v0.1.4...v1.0.0
[0.1.4]: https://github.com/michaellaunay/perfect_maze/releases/tag/v0.1.4
[0.1.3]: https://github.com/michaellaunay/perfect_maze/releases/tag/v0.1.3
[0.1.2]: https://github.com/michaellaunay/perfect_maze/releases/tag/v0.1.2
