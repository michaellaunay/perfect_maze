"""Maze model and perfect-maze generation.

The maze is a rectangular grid of :class:`Cell` objects. Adjacent cells
share a single :class:`Wall` instance, so opening a wall from either side
opens it for both.

Generation follows a randomised Kruskal-like algorithm: starting from a
grid where every wall is built, walls are picked at random and removed
whenever they separate two cells that are not yet connected. Connectivity
is tracked with a union-find structure. The process stops once
``width * height - 1`` walls have been removed, which is exactly the
number of edges of a spanning tree.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterator, Sequence
from enum import IntEnum
from typing import Self

__all__ = [
    "Cell",
    "Direction",
    "Maze",
    "MazeFormatError",
    "OpenWall",
    "RandRange",
    "Wall",
    "build_maze",
]

type RandRange = Callable[[int, int], int]
"""Signature of :func:`random.randrange` restricted to ``(start, stop)``."""

type OpenWall = tuple[int, int, int]
"""An opened wall: ``(x, y, direction)`` where ``direction`` is a
:class:`Direction` value."""


class MazeFormatError(ValueError):
    """Stored passages do not describe a valid perfect maze."""


class Direction(IntEnum):
    """The four directions a cell can be left through.

    Values are contiguous from 0 so that ``randrange(0, len(Direction))``
    draws a direction uniformly.
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def opposite(self) -> Direction:
        """The direction pointing back to the origin cell."""
        return Direction((self.value + 2) % 4)


class Wall:
    """A border between two cells, or between a cell and the outside.

    Args:
        first_cell: The cell on one side of the wall.
        second_cell: The cell on the other side, or ``None`` for an
            outer wall.
        is_built: ``True`` while the wall blocks passage.
    """

    __slots__ = ("first_cell", "is_built", "second_cell")

    def __init__(
        self,
        first_cell: Cell,
        second_cell: Cell | None,
        is_built: bool = True,
    ) -> None:
        self.first_cell = first_cell
        self.second_cell = second_cell
        self.is_built = is_built

    @property
    def is_outer(self) -> bool:
        """``True`` when the wall lies on the maze boundary."""
        return self.second_cell is None

    def __iter__(self) -> Iterator[Cell | None]:
        """Yield the two cells separated by this wall."""
        yield self.first_cell
        yield self.second_cell

    def __repr__(self) -> str:
        state = "built" if self.is_built else "open"
        return f"Wall({self.first_cell!r}, {self.second_cell!r}, {state})"


class Cell:
    """A square cell with four walls and up to four neighbours.

    Neighbours are assigned through the ``*_cell`` properties. Setting a
    neighbour creates the shared :class:`Wall` and links the neighbour back,
    so the graph stays consistent. Replacing a neighbour detaches the old
    partners at both ends and gives each detached side a built outer wall.
    Setting a neighbour to ``None`` disconnects both sides. New connections
    start with a built wall; assigning the current neighbour again is a no-op
    that preserves wall identity and state (including existing outer walls).
    Self-links raise :class:`ValueError`; non-cell, non-``None`` targets raise
    :class:`TypeError`. Neither error changes the graph.

    Args:
        index: Position of the cell in row-major order. Used as the
            union-find key during generation.
    """

    __slots__ = (
        "_east_cell",
        "_north_cell",
        "_south_cell",
        "_west_cell",
        "east_wall",
        "index",
        "north_wall",
        "south_wall",
        "west_wall",
    )

    def __init__(self, index: int = -1) -> None:
        self.index = index
        self.north_wall: Wall | None = None
        self.east_wall: Wall | None = None
        self.south_wall: Wall | None = None
        self.west_wall: Wall | None = None
        self._north_cell: Cell | None = None
        self._east_cell: Cell | None = None
        self._south_cell: Cell | None = None
        self._west_cell: Cell | None = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.index})"

    # -- generic accessors --------------------------------------------------

    def wall(self, direction: Direction) -> Wall:
        """Return the wall in ``direction``.

        Raises:
            ValueError: If the cell has not been linked in that direction yet.
        """
        wall = (self.north_wall, self.east_wall, self.south_wall, self.west_wall)[
            direction
        ]
        if wall is None:
            raise ValueError(f"{self!r} has no wall towards {direction.name}")
        return wall

    def neighbour(self, direction: Direction) -> Cell | None:
        """Return the neighbouring cell in ``direction``, or ``None``."""
        return (
            self._north_cell,
            self._east_cell,
            self._south_cell,
            self._west_cell,
        )[direction]

    def neighbours(self) -> Iterator[tuple[Direction, Cell]]:
        """Yield ``(direction, cell)`` for every existing neighbour."""
        for direction in Direction:
            cell = self.neighbour(direction)
            if cell is not None:
                yield direction, cell

    def is_open(self, direction: Direction) -> bool:
        """``True`` when one can walk from this cell towards ``direction``."""
        return not self.wall(direction).is_built

    # -- neighbour properties -----------------------------------------------

    def _link(self, direction: Direction, other: Self | None) -> None:
        """Replace one link, detaching the previous partners at both ends.

        New connections and detached boundaries start with built walls.
        Assigning the current neighbour again preserves the existing wall.
        Invalid targets are rejected before any graph state changes.
        """
        if other is not None and not isinstance(other, Cell):
            raise TypeError("neighbour must be a Cell or None")
        if other is self:
            raise ValueError("a cell cannot be linked to itself")

        opposite = direction.opposite
        attr_cell = f"_{direction.name.lower()}_cell"
        attr_wall = f"{direction.name.lower()}_wall"
        back_cell = f"_{opposite.name.lower()}_cell"
        back_wall = f"{opposite.name.lower()}_wall"
        previous = self.neighbour(direction)
        if previous is other and getattr(self, attr_wall) is not None:
            return

        displaced = other.neighbour(opposite) if other is not None else None
        # Allocate replacement walls before changing any endpoint. Avoid the
        # public setters here: recursively linking back can leave stale links.
        wall = Wall(self, other)
        previous_boundary = Wall(previous, None) if previous is not None else None
        displaced_boundary = Wall(displaced, None) if displaced is not None else None

        if previous is not None:
            setattr(previous, back_cell, None)
            setattr(previous, back_wall, previous_boundary)
        if displaced is not None:
            setattr(displaced, attr_cell, None)
            setattr(displaced, attr_wall, displaced_boundary)

        setattr(self, attr_cell, other)
        setattr(self, attr_wall, wall)
        if other is not None:
            setattr(other, back_cell, self)
            setattr(other, back_wall, wall)

    @property
    def north_cell(self) -> Cell | None:
        """Neighbour above this cell."""
        return self._north_cell

    @north_cell.setter
    def north_cell(self, value: Self | None) -> None:
        self._link(Direction.NORTH, value)

    @property
    def east_cell(self) -> Cell | None:
        """Neighbour on the right of this cell."""
        return self._east_cell

    @east_cell.setter
    def east_cell(self, value: Self | None) -> None:
        self._link(Direction.EAST, value)

    @property
    def south_cell(self) -> Cell | None:
        """Neighbour below this cell."""
        return self._south_cell

    @south_cell.setter
    def south_cell(self, value: Self | None) -> None:
        self._link(Direction.SOUTH, value)

    @property
    def west_cell(self) -> Cell | None:
        """Neighbour on the left of this cell."""
        return self._west_cell

    @west_cell.setter
    def west_cell(self, value: Self | None) -> None:
        self._link(Direction.WEST, value)


class Maze:
    """A rectangular maze made of cells and walls.

    Args:
        cells: Rows of cells, ``cells[y][x]``.
        width: Number of cells per row.
        height: Number of rows.
        open_walls: The walls opened during generation, in order. Passing
            this sequence back to :func:`build_maze` rebuilds the same maze.
    """

    __slots__ = ("cells", "height", "open_walls", "width")

    def __init__(
        self,
        cells: Sequence[Sequence[Cell]],
        width: int,
        height: int,
        open_walls: tuple[OpenWall, ...] = (),
    ) -> None:
        self.cells = cells
        self.width = width
        self.height = height
        self.open_walls = open_walls

    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"

    def __str__(self) -> str:
        from perfect_maze.render import printable_maze

        return printable_maze(self)

    def __getitem__(self, xy: tuple[int, int]) -> Cell:
        """Return the cell at ``(x, y)``."""
        x, y = xy
        return self.cells[y][x]

    def __iter__(self) -> Iterator[Cell]:
        """Yield every cell in row-major order."""
        for row in self.cells:
            yield from row

    def __len__(self) -> int:
        return self.width * self.height


class _UnionFind:
    """Disjoint sets over ``range(size)`` with path compression and union
    by size."""

    __slots__ = ("_parent", "_size")

    def __init__(self, size: int) -> None:
        self._parent = list(range(size))
        self._size = [1] * size

    def find(self, item: int) -> int:
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[item] != root:
            self._parent[item], item = root, self._parent[item]
        return root

    def union(self, a: int, b: int) -> bool:
        """Merge the sets of ``a`` and ``b``; return ``False`` if already
        merged."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        return True


def _grid[C: Cell](width: int, height: int, cell_type: type[C]) -> list[list[C]]:
    """Create a ``width x height`` grid of linked cells with every wall built."""
    cells = [[cell_type(x + y * width) for x in range(width)] for y in range(height)]
    for y, row in enumerate(cells):
        for x, cell in enumerate(row):
            cell.north_cell = cells[y - 1][x] if y > 0 else None
            cell.east_cell = cells[y][x + 1] if x < width - 1 else None
            cell.south_cell = cells[y + 1][x] if y < height - 1 else None
            cell.west_cell = cells[y][x - 1] if x > 0 else None
    return cells


def _validate_open_walls(
    width: int, height: int, open_walls: Sequence[OpenWall]
) -> tuple[OpenWall, ...]:
    """Validate and copy a complete spanning tree before constructing cells."""
    if isinstance(open_walls, (str, bytes, bytearray, memoryview)) or not isinstance(
        open_walls, Sequence
    ):
        raise MazeFormatError("open_walls must be a sequence of triplets")

    size = width * height
    target = size - 1
    if len(open_walls) != target:
        raise MazeFormatError(
            f"open_walls must contain exactly {target} passages for "
            f"{width}x{height}, got {len(open_walls)}"
        )

    groups = _UnionFind(size)
    seen: set[tuple[int, int]] = set()
    validated: list[OpenWall] = []
    for index, record in enumerate(open_walls):
        prefix = f"open_walls[{index}]"
        if (
            isinstance(record, (str, bytes, bytearray, memoryview))
            or not isinstance(record, Sequence)
            or len(record) != 3
        ):
            raise MazeFormatError(f"{prefix} must be an (x, y, direction) triplet")
        if any(
            isinstance(value, bool) or not isinstance(value, int) for value in record
        ):
            raise MazeFormatError(f"{prefix} must contain integers, not booleans")

        x, y, value = record
        if not (0 <= x < width and 0 <= y < height):
            raise MazeFormatError(
                f"{prefix} coordinates ({x}, {y}) are outside {width}x{height}"
            )
        try:
            direction = Direction(value)
        except ValueError:
            raise MazeFormatError(f"{prefix} has invalid direction {value}") from None

        dx, dy = ((0, -1), (1, 0), (0, 1), (-1, 0))[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height):
            raise MazeFormatError(f"{prefix} opens an outer wall")

        first = y * width + x
        second = ny * width + nx
        edge = (min(first, second), max(first, second))
        if edge in seen:
            raise MazeFormatError(f"{prefix} is a duplicate passage")
        if not groups.union(first, second):
            raise MazeFormatError(f"{prefix} creates a cycle")
        seen.add(edge)
        validated.append((int(x), int(y), direction))

    # N-1 distinct, acyclic edges on N vertices necessarily form a connected tree.
    return tuple(validated)


def build_maze(
    width: int,
    height: int,
    *,
    randrange: RandRange = random.randrange,
    open_walls: Sequence[OpenWall] | None = None,
    cell_type: type[Cell] = Cell,
) -> Maze:
    """Create a ``width x height`` perfect maze.

    Args:
        width: Number of cells per row (at least 1).
        height: Number of rows (at least 1).
        randrange: Random source with the signature of
            :func:`random.randrange`. Provide a seeded ``random.Random``
            instance's ``randrange`` for reproducible mazes, or a stub for
            testing.
        open_walls: If given, the maze is rebuilt deterministically from
            this sequence of ``(x, y, direction)`` triplets, typically the
            :attr:`Maze.open_walls` of a previously generated maze.
            Exactly ``width * height - 1`` distinct internal passages must
            form a spanning tree. Coordinates and directions must be integers
            (not booleans), coordinates must be in bounds, and directions
            must be :class:`Direction` values or their integer equivalents.
            No records are skipped; order and orientation are preserved.
            ``randrange`` is then ignored, even for invalid input.
        cell_type: Class used to instantiate cells. Subclass :class:`Cell`
            to attach your own data to the maze.

    Returns:
        The generated maze.

    Raises:
        ValueError: If ``width`` or ``height`` is lower than 1.
        MazeFormatError: If ``open_walls`` is malformed or does not describe
            a perfect maze. Validation completes before any cells are created.
    """
    if width < 1 or height < 1:
        raise ValueError(f"width and height must be >= 1, got {width}x{height}")

    if open_walls is not None:
        passages = _validate_open_walls(width, height, open_walls)
        cells = _grid(width, height, cell_type)
        for x, y, direction in passages:
            cells[y][x].wall(Direction(direction)).is_built = False
        return Maze(cells, width, height, passages)

    cells = _grid(width, height, cell_type)
    groups = _UnionFind(width * height)
    nb_directions = len(Direction)
    target = width * height - 1
    new_open_walls: list[OpenWall] = []

    while len(new_open_walls) < target:
        x = randrange(0, width)
        y = randrange(0, height)
        direction = Direction(randrange(0, nb_directions))
        cell = cells[y][x]
        other = cell.neighbour(direction)
        # ``other`` is None on the maze border: nothing to open there.
        if other is not None and groups.union(cell.index, other.index):
            cell.wall(direction).is_built = False
            new_open_walls.append((x, y, direction))

    return Maze(cells, width, height, tuple(new_open_walls))
