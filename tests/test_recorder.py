"""Recording of random draws into a replayable fixture file."""

from __future__ import annotations

import random
from pathlib import Path

from perfect_maze import build_maze, printable_maze, record_maze_construction


def test_record_file_is_replayable(tmp_path: Path) -> None:
    path = tmp_path / "maze.py"
    maze = record_maze_construction(5, 4, path, randrange=random.Random(11).randrange)

    namespace: dict[str, object] = {}
    exec(path.read_text(encoding="utf-8"), namespace)

    assert namespace["width"] == 5
    assert namespace["height"] == 4
    assert namespace["open_walls"] == tuple(
        tuple(int(v) for v in w) for w in maze.open_walls
    )
    assert namespace["pmaze"] == printable_maze(maze)

    draws = iter(namespace["randrange"])
    replayed = build_maze(5, 4, randrange=lambda _a, _b: next(draws))
    assert printable_maze(replayed) == namespace["pmaze"]


def test_record_overwrites_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "maze.py"
    path.write_text("garbage", encoding="utf-8")
    record_maze_construction(2, 2, str(path), randrange=random.Random(0).randrange)
    assert path.read_text(encoding="utf-8").startswith("width = 2\n")
