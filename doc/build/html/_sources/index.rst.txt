.. maze documentation master file, created by
   sphinx-quickstart on Sun Apr 10 23:31:59 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to maze's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Perfect maze is a simple python script to create perfect maze which is a maze without dead cells and with all connected cells.
The maze can be printed in utf-8.

Example
-------

python::
   from maze.perfect_maze import *
   m = build_maze(60,40)
   print(printable_maze(m))

Module documentation
--------------------

.. automodule:: perfect_maze
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
