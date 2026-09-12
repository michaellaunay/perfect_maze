Usage
=====

Installation
------------

.. code-block:: shell

   pip install perfect-maze

Python 3.12 or later is required.

Command line
------------

.. code-block:: shell

   perfect-maze                       # 6x4 maze on stdout
   perfect-maze -w 40 -H 20           # 40 columns by 20 rows
   perfect-maze -w 12 -H 5 --seed 42  # reproducible maze
   perfect-maze -w 8 -H 8 -o maze.py  # record the random draws into maze.py
   python -m perfect_maze --help

The file written by ``--output`` is valid Python and has the same layout as
the project's test fixtures.

Library
-------

.. code-block:: python

   from perfect_maze import build_maze, printable_maze

   maze = build_maze(60, 40)
   print(printable_maze(maze))   # or print(maze)

Reproducible generation
~~~~~~~~~~~~~~~~~~~~~~~

Pass any callable with the signature of :func:`random.randrange`:

.. code-block:: python

   import random
   maze = build_maze(10, 8, randrange=random.Random(42).randrange)

:attr:`Maze.open_walls <perfect_maze.Maze.open_walls>` records every passage
opened during generation. Feeding it back rebuilds the very same maze:

.. code-block:: python

   again = build_maze(10, 8, open_walls=maze.open_walls)
   assert printable_maze(again) == printable_maze(maze)

Walking the maze
~~~~~~~~~~~~~~~~

.. code-block:: python

   from perfect_maze import Direction

   cell = maze[0, 0]
   for direction, neighbour in cell.neighbours():
       if cell.is_open(direction):
           print(direction.name, "->", neighbour.index)

Custom cells
~~~~~~~~~~~~

Subclass :class:`~perfect_maze.Cell` and pass it as ``cell_type`` to attach
your own data to every cell:

.. code-block:: python

   from perfect_maze import Cell, build_maze

   class Room(Cell):
       __slots__ = ("visited",)

       def __init__(self, index: int = -1) -> None:
           super().__init__(index)
           self.visited = False

   maze = build_maze(5, 5, cell_type=Room)

Algorithm
---------

The grid starts with every wall built. Walls are picked at random and
removed whenever they separate two cells that are not yet connected; a
union-find structure tracks connectivity. The loop stops once
``width * height - 1`` walls have been removed, the number of edges of a
spanning tree, so the result is guaranteed to be perfect.
