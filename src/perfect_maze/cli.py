"""Command-line interface: ``perfect-maze`` or ``python -m perfect_maze``."""

from __future__ import annotations

import argparse
import random
import sys
from collections.abc import Sequence

from perfect_maze import __version__
from perfect_maze.maze import build_maze
from perfect_maze.recorder import record_maze_construction
from perfect_maze.render import printable_maze

DEFAULT_WIDTH = 6
DEFAULT_HEIGHT = 4


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not an integer: {value!r}") from None
    if number < 1:
        raise argparse.ArgumentTypeError(f"must be >= 1, got {number}")
    return number


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser (exposed for documentation and tests)."""
    parser = argparse.ArgumentParser(
        prog="perfect-maze",
        description="Build a perfect maze and print it on stdout.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-w",
        "--width",
        type=_positive_int,
        default=DEFAULT_WIDTH,
        help=f"number of cells per row (default: {DEFAULT_WIDTH})",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=_positive_int,
        default=DEFAULT_HEIGHT,
        help=f"number of rows (default: {DEFAULT_HEIGHT})",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="seed the random generator for a reproducible maze",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help="record the random draws and the printable maze into PATH",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="do not print the maze on stdout"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns the process exit code."""
    args = build_parser().parse_args(argv)
    randrange = random.Random(args.seed).randrange if args.seed is not None else None
    kwargs = {"randrange": randrange} if randrange else {}

    if args.output:
        try:
            maze = record_maze_construction(
                args.width, args.height, args.output, **kwargs
            )
        except OSError as err:
            print(
                f"perfect-maze: cannot write {err.filename}: {err.strerror}",
                file=sys.stderr,
            )
            return 1
    else:
        maze = build_maze(args.width, args.height, **kwargs)

    if not args.quiet:
        print(printable_maze(maze))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
