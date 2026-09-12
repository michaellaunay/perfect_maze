# perfect_maze

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

- [Usage](usage.md) — installation, command line and library examples.
- [API reference](api.md) — generated from the docstrings.
- [Changelog](changelog.md)

## How it works

The grid starts with every wall built. Walls are then picked at random and
removed whenever they separate two cells that are not yet connected, using a
union-find structure to track connectivity. The loop stops after
`width * height - 1` walls have been removed, which is exactly the number of
edges of a spanning tree, so the result is guaranteed to be perfect.

## License

GNU Affero General Public License v3.0 or later.
