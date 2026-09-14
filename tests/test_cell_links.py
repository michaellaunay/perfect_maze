"""Neighbour mutations must preserve reciprocal links and shared walls."""

from __future__ import annotations

import random
from collections.abc import Sequence

import pytest

from perfect_maze import Cell, Direction, Wall


def link(cell: Cell, direction: Direction, other: Cell | None) -> None:
    setattr(cell, f"{direction.name.lower()}_cell", other)


def assert_boundary(cell: Cell, direction: Direction) -> None:
    assert cell.neighbour(direction) is None
    wall = cell.wall(direction)
    assert wall.is_outer
    assert wall.first_cell is cell
    assert wall.second_cell is None
    assert wall.is_built


def assert_shared(first: Cell, direction: Direction, second: Cell) -> Wall:
    assert first.neighbour(direction) is second
    assert second.neighbour(direction.opposite) is first
    wall = first.wall(direction)
    assert wall is second.wall(direction.opposite)
    assert not wall.is_outer
    assert set(wall) == {first, second}
    return wall


def snapshot(cells: Sequence[Cell]) -> tuple:
    # Include identities and states of all walls, even uninitialised sides.
    result = []
    for cell in cells:
        for direction in Direction:
            wall = getattr(cell, f"{direction.name.lower()}_wall")
            result.append(
                (
                    cell.neighbour(direction),
                    wall,
                    None if wall is None else tuple(wall),
                    None if wall is None else wall.is_built,
                )
            )
    return tuple(result)


@pytest.mark.parametrize("direction", list(Direction))
def test_none_initialises_an_outer_wall(direction: Direction) -> None:
    cell = Cell(0)
    link(cell, direction, None)
    assert_boundary(cell, direction)


@pytest.mark.parametrize("direction", list(Direction))
@pytest.mark.parametrize("built", [True, False])
def test_assigning_same_neighbour_preserves_wall_and_state(direction, built) -> None:
    a, b = Cell(0), Cell(1)
    link(a, direction, b)
    wall = a.wall(direction)
    wall.is_built = built
    before = snapshot([a, b])
    link(a, direction, b)
    link(b, direction.opposite, a)
    assert snapshot([a, b]) == before
    assert assert_shared(a, direction, b) is wall


@pytest.mark.parametrize("direction", list(Direction))
@pytest.mark.parametrize("built", [True, False])
def test_assigning_none_twice_preserves_boundary_and_state(direction, built) -> None:
    cell = Cell(0)
    link(cell, direction, None)
    cell.wall(direction).is_built = built
    before = snapshot([cell])
    link(cell, direction, None)
    assert snapshot([cell]) == before


@pytest.mark.parametrize("direction", list(Direction))
def test_unlink_detaches_both_cells_and_closes_boundaries(direction: Direction) -> None:
    a, b = Cell(0), Cell(1)
    link(a, direction, b)
    a.wall(direction).is_built = False
    link(a, direction, None)
    assert_boundary(a, direction)
    assert_boundary(b, direction.opposite)
    assert a.wall(direction) is not b.wall(direction.opposite)


@pytest.mark.parametrize("direction", list(Direction))
def test_reconnect_restores_one_shared_wall(direction: Direction) -> None:
    a, b = Cell(0), Cell(1)
    link(a, direction, b)
    old_wall = a.wall(direction)
    old_wall.is_built = False
    link(a, direction, None)
    link(a, direction, b)
    wall = assert_shared(a, direction, b)
    assert wall is not old_wall
    assert wall.is_built
    wall.is_built = False
    assert b.is_open(direction.opposite)


@pytest.mark.parametrize("direction", list(Direction))
def test_replacement_detaches_previous_neighbour(direction: Direction) -> None:
    a, b, c = Cell(0), Cell(1), Cell(2)
    link(a, direction, b)
    link(a, direction, c)
    assert assert_shared(a, direction, c).is_built
    assert_boundary(b, direction.opposite)


@pytest.mark.parametrize("direction", list(Direction))
def test_linking_to_occupied_side_detaches_displaced_cell(direction: Direction) -> None:
    a, b, c = Cell(0), Cell(1), Cell(2)
    link(c, direction, b)
    link(a, direction, b)
    assert_shared(a, direction, b)
    assert_boundary(c, direction)


@pytest.mark.parametrize("direction", list(Direction))
def test_replacement_detaches_previous_partners_at_both_ends(direction) -> None:
    a, b, c, d = (Cell(index) for index in range(4))
    link(a, direction, b)
    link(d, direction, c)
    a.wall(direction).is_built = False
    d.wall(direction).is_built = False
    link(a, direction, c)
    assert assert_shared(a, direction, c).is_built
    assert_boundary(b, direction.opposite)
    assert_boundary(d, direction)


@pytest.mark.parametrize("direction", list(Direction))
def test_previous_and_displaced_partner_can_be_the_same_cell(direction) -> None:
    a, b, c = Cell(0), Cell(1), Cell(2)
    link(a, direction, b)
    link(b, direction, c)
    link(a, direction, c)
    assert_shared(a, direction, c)
    assert_boundary(b, direction)
    assert_boundary(b, direction.opposite)


@pytest.mark.parametrize("direction", list(Direction))
def test_other_directions_remain_unchanged(direction: Direction) -> None:
    a, b, c = Cell(0), Cell(1), Cell(2)
    perpendicular = Direction((direction + 1) % len(Direction))
    link(a, perpendicular, b)
    wall = a.wall(perpendicular)
    wall.is_built = False
    link(a, direction, c)
    link(a, direction, None)
    assert assert_shared(a, perpendicular, b) is wall
    assert not wall.is_built


@pytest.mark.parametrize("direction", list(Direction))
def test_self_link_is_rejected_without_mutation(direction: Direction) -> None:
    a, b = Cell(0), Cell(1)
    link(a, direction, b)
    before = snapshot([a, b])
    with pytest.raises(ValueError, match="itself"):
        link(a, direction, a)
    assert snapshot([a, b]) == before


@pytest.mark.parametrize("direction", list(Direction))
@pytest.mark.parametrize("invalid", [False, 0, "cell", object()])
def test_non_cell_is_rejected_without_mutation(direction, invalid) -> None:
    a, b = Cell(0), Cell(1)
    link(a, direction, b)
    before = snapshot([a, b])
    with pytest.raises(TypeError, match="Cell or None"):
        link(a, direction, invalid)
    assert snapshot([a, b]) == before


@pytest.mark.parametrize("direction", list(Direction))
def test_subclass_links_use_the_same_reciprocal_contract(direction) -> None:
    class Room(Cell):
        __slots__ = ()

    a, b, c = Room(0), Room(1), Room(2)
    link(a, direction, b)
    link(a, direction, c)
    assert_shared(a, direction, c)
    assert_boundary(b, direction.opposite)


@pytest.mark.parametrize("seed", [0, 7, 42])
def test_seeded_mutation_sequences_preserve_graph_invariants(seed: int) -> None:
    rng = random.Random(seed)
    cells = [Cell(index) for index in range(9)]
    for _ in range(500):
        a = rng.choice(cells)
        other = rng.choice([None, *(cell for cell in cells if cell is not a)])
        direction = rng.choice(list(Direction))
        link(a, direction, other)
        a.wall(direction).is_built = bool(rng.randrange(2))
        for cell in cells:
            for side in Direction:
                wall = getattr(cell, f"{side.name.lower()}_wall")
                neighbour = cell.neighbour(side)
                if wall is None:
                    assert neighbour is None
                elif neighbour is None:
                    assert wall.first_cell is cell
                    assert wall.second_cell is None
                else:
                    assert_shared(cell, side, neighbour)
