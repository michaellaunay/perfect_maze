"""Command-line interface."""

from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

import pytest

from perfect_maze import __version__, build_maze, printable_maze
from perfect_maze.cli import DEFAULT_HEIGHT, DEFAULT_WIDTH, main


def test_default_size(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    lines = capsys.readouterr().out.rstrip("\n").split("\n")
    assert len(lines) == DEFAULT_HEIGHT + 1
    assert all(len(line) == 2 * DEFAULT_WIDTH + 1 for line in lines)


def test_seed_is_reproducible(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["-w", "7", "-H", "5", "--seed", "42"]) == 0
    out = capsys.readouterr().out
    expected = printable_maze(build_maze(7, 5, randrange=random.Random(42).randrange))
    assert out == expected + "\n"


def test_quiet(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--quiet"]) == 0
    assert capsys.readouterr().out == ""


def test_output_records_draws(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "rec.py"
    assert main(["-w", "3", "-H", "2", "-s", "1", "-o", str(path)]) == 0
    printed = capsys.readouterr().out
    namespace: dict[str, object] = {}
    exec(path.read_text(encoding="utf-8"), namespace)
    assert printed == f"{namespace['pmaze']}\n"


def test_output_unwritable(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["-q", "-o", str(tmp_path / "missing" / "rec.py")]) == 1
    assert "cannot write" in capsys.readouterr().err


@pytest.mark.parametrize("args", [["-w", "0"], ["-H", "-2"], ["--width", "abc"]])
def test_invalid_size(args: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == f"perfect-maze {__version__}"


def test_python_dash_m() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "perfect_maze", "-w", "2", "-H", "1", "-s", "0"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == "┌───┐\n└───┘\n"
