"""Render a maze as a UTF-8 string using box-drawing characters."""

from __future__ import annotations

from perfect_maze.maze import Cell, Direction, Maze

__all__ = ["printable_maze"]

# Corner glyph indexed by a 4-bit mask of the segments leaving the corner:
# bit 0 = east, bit 1 = south, bit 2 = west, bit 3 = north.
_CORNERS = " ╶╷┌╴─┐┬╵└│├┘┴┤┼"
_EAST, _SOUTH, _WEST, _NORTH = 1, 2, 4, 8


def _built(cell: Cell | None, direction: Direction) -> int:
    """1 if ``cell`` exists and its wall in ``direction`` is built, else 0."""
    return int(cell is not None and cell.wall(direction).is_built)


def printable_maze(maze: Maze) -> str:
    """Return a UTF-8 box-drawing representation of ``maze``.

    Each cell is two characters wide and one line tall; the drawing is
    ``2 * width + 1`` columns by ``height + 1`` lines. Every corner glyph is
    chosen from the walls that meet at that corner, so junctions render as
    ``├``, ``┼``, ``╵``... rather than bare crosses.

    Args:
        maze: The maze to render.
    """
    lines: list[str] = []
    bottom: list[str] = []
    for row in maze.cells:
        line: list[str] = []
        for cell in row:
            n, e, s, w = (
                _built(cell, Direction.NORTH),
                _built(cell, Direction.EAST),
                _built(cell, Direction.SOUTH),
                _built(cell, Direction.WEST),
            )
            north = cell.north_cell
            east = cell.east_cell
            south = cell.south_cell
            west = cell.west_cell

            north_west = (
                _EAST * n
                + _SOUTH * w
                + _WEST * _built(west, Direction.NORTH)
                + _NORTH * _built(north, Direction.WEST)
            )
            line.append(_CORNERS[north_west])
            line.append("─" if n else " ")

            if east is None:
                north_east = (
                    _EAST * _built(east, Direction.NORTH)
                    + _SOUTH * e
                    + _WEST * n
                    + _NORTH * _built(north, Direction.EAST)
                )
                line.append(_CORNERS[north_east])

            if south is None:
                south_west = (
                    _EAST * s
                    + _SOUTH * _built(south, Direction.WEST)
                    + _WEST * _built(west, Direction.SOUTH)
                    + _NORTH * w
                )
                bottom.append(_CORNERS[south_west])
                bottom.append("─" if s else " ")
                if east is None:
                    south_east = (
                        _EAST * _built(east, Direction.SOUTH)
                        + _SOUTH * _built(south, Direction.EAST)
                        + _WEST * s
                        + _NORTH * e
                    )
                    bottom.append(_CORNERS[south_east])
        lines.append("".join(line))
    lines.append("".join(bottom))
    return "\n".join(lines)
