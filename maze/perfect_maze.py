#!/usr/bin/python3
# -*- coding: utf-8
# author: Michael Launay
# mail : michaellaunay@ecreall.com
# creation_date : 2015
# update_date : 2021, 2022
# Description : Creates a two dimension perfect maze, and provides function to
#      print it on stdout. Can be used as a stand alone python scrypt.
# Usage :
#      m = build_maze(60,40)
#      print(printable_maze(m))
VERSION = "0.1.3"
SCRIPT_USAGE = """Usage: perfect_maze.py [OPTIONS]

    Buid a perfect maze and print it on stout.

Options:
    --help          This usage.
    --version       Version.
    --quite         Do not print maze on stdout.
    --width=int     The number of vertical cells.
    --length=int    The number of horizontal cells.
    --fout=path     File path to store the printable maze and the random serie
                    used to create it.
"""

import itertools
import random
from typing import List, Tuple, Type, Callable, IO
from enum import Enum

DEFAULT_WIDTH = 6
DEFAULT_LENGTH = 4
DEFAULT_SPY_FILE_OUT = None
DEFAULT_PRINT_MAZE = True

class DIRECTIONS(Enum):
    """ The possible mouvement directions.
    It determines the number of cells for a wall.
    """
    NORTH:int = 0
    EAST:int = 1
    SOUTH:int = 2
    WEST:int = 3
NORTH=DIRECTIONS.NORTH.value
EAST=DIRECTIONS.EAST.value
SOUTH=DIRECTIONS.SOUTH.value
WEST=DIRECTIONS.WEST.value

class Wall:
    """Border wall.
    """

    def __init__(self,
        first_cell:Type["Cell"],
        second_cell:Type["Cell"],
        is_build:bool=True):
        """The maze is made of cells, wall is a hard border beetween two cells.

        Args:
            first_cell (Cell): first side of the wall.
            second_cell (Cell): oposite side of the wall
            is_build (bool, optional): If false, the border between the 2
                cells is open. Defaults to True.
        """
        self.first_cell = first_cell
        self.second_cell = second_cell
        self.is_build = is_build

    def set_cells(first_cell:Type["Cell"], second_cell:Type["Cell"]):
        """Modify the border.

        Args:
            first_cell (Cell): cell at the first side of the wall.
            second_cell (Cell): cell at the oposite side of the wall.
        """

        self.first_cell = first_cell
        self.second_cell = second_cell

    def __iter__(self):
        """yield the cells separated by this wall.
        Yields:
            Cell: next cell
        """
        yield self.first_cell
        yield self.second_cell


class Cell:
    """A cell is a square place which can have 4 walls.
    """

    def __init__(self, n:int=-1):
        """Constructor

        Args:
            n (int, optional): n is the id number of the cell. Defaults to -1.
        """
        self.north_wall = None
        self.east_wall = None
        self.south_wall = None
        self.west_wall = None
        self._north_cell = None
        self._east_cell = None
        self._south_cell = None
        self._west_cell = None
        self.n = n

    @property
    def north_cell(self):
        return self._north_cell

    @north_cell.setter
    def north_cell(self, value:Type["Cell"]):
        self._north_cell = value
        if value:
            if value.south_cell != self: #Stop recursion
                self.north_wall = value.south_wall = Wall(self, value)
                #set cell after setting the wall for data consistence
                value.south_cell = self
        else:
            self.north_wall = Wall(self, None)

    @property
    def east_cell(self):
        return self._east_cell

    @east_cell.setter
    def east_cell(self, value:Type["Cell"]):
        self._east_cell = value
        if value:
            if value.west_cell != self: #Stop recursion
                self.east_wall = value.west_wall = Wall(self, value)
                #set cell after setting the wall for data consistence
                value.west_cell = self
        else:
            self.east_wall = Wall(self, None)

    @property
    def south_cell(self):
        return self._south_cell

    @south_cell.setter
    def south_cell(self, value:Type["Cell"]):
        self._south_cell = value
        if value:
            if value.north_cell != self: #Stop recursion
                self.south_wall = value.north_wall = Wall(self, value)
                #set cell after setting the wall for data consistence
                value.north_cell = self
        else:
            self.south_wall = Wall(self, None)

    @property
    def west_cell(self):
        return self._west_cell

    @west_cell.setter
    def west_cell(self, value:Type["Cell"]):
        self._west_cell = value
        if value:
            if value.east_cell != self: #Stop recursion
                self.west_wall = value.east_wall = Wall(self, value)
                #set cell after setting the wall for data consistence
                value.east_cell = self
        else:
            self.west_wall = Wall(self, None)


class Maze:
    """
        A maze consists of cells and walls.
    """
    def __init__(self,
        cells:List[List[Cell]],
        width:int,
        length:int,
        open_walls:Tuple[Tuple[int, int, int]]= None):
        """Initialize a maze with the list of cells

        Args:
            cells (List[List[Cell]]): A Cells table as a list of cells lines
            width (int): size of the maze lines
            length (int): number of cell lines
            open_walls (Tuple[Tuple[int, int, int]], optional): List of cells
                described by X and Y coordinates and wall position (DIRECTIONS).
                If given the maze is built from this list, otherwise it's
                randomized. Defaults to None.
        """
        self.cells = cells
        self.width = width
        self.length = length
        self.open_walls = open_walls
    def update_open_walls(new_wall:Tuple[int,int,int] = None):
        """walk the maze cells and update the open wall list or just update the
        given cell by new_wall.

        Args:
            new_wall (Tuple[int,int,int]): X,Y of the cell, direction of the wall.
        """
        raise NotImplementedError("For future version !")

def build_maze(width:int,
        length:int,
        randrange:Callable[[int,int],int] = random.randrange,
        open_walls:Tuple[Tuple[int, int, int]] = None,
        cell_type:Type[Cell] = Cell) -> Maze:
    """Create an return a width*length perfect maze.

    Args:
        width (int): Maze width
        randrange (Callable[[int,int],int], optional): A randrange monky patch provided
            for testing.
        open_walls (Tuple[Tuple[int,int,int]], optional): If provided build the maze from
            this list of  (X,Y cell, open wall direction)for building a maze 
            from open wall list.
        cell_type (Cell base class, optional) is the cell base class used to instantiate
         cells of the maze.
         By override cell_type you can provide your class derived from Cell.
    """
    cells = [[cell_type(x+y*width) for x in range(0, width)] for y in range(0, length)]
    if open_walls:
        chain = itertools.chain(*open_walls) #open walls are used for monkey patching of random list
        def monky_randrange(*l,**d):
            return next(chain)
        randrange = monky_randrange
    new_open_walls = []
    for y, row in enumerate(cells):
        for x, cell in enumerate(row):
            north_cell = None
            east_cell = None
            west_cell = None
            south_cell = None
            if x > 0:
                west_cell = cells[y][x-1]
            if x < width - 1:
                east_cell = cells[y][x+1]
            if y > 0:
                north_cell = cells[y-1][x]
            if y < length - 1:
                south_cell = cells[y+1][x]
            cell.north_cell = north_cell
            cell.east_cell = east_cell
            cell.south_cell = south_cell
            cell.west_cell = west_cell
    #now create the perfect maze
    erased_walls = 0
    nb_cells = width*length
    groups = {k:[k] for k in range(0, width*length)} # We group together 
    # connected cells at the end we must have only one group, and at this
    # time there will be a path between each cell.
    # At the begenning, we build a gride made up of 4-walled cells.
    # Next we randomize the erasing of the walls and connect cells.
    while erased_walls < nb_cells -1:
        x = randrange(0, width)
        y = randrange(0, length)
        direction = randrange(0, len(DIRECTIONS)) #For future we will manage more than 4 directions
        cell = cells[y][x]
        wall = None
        other_cell = None
        if direction == NORTH:
            wall = cell.north_wall
            other_cell = cell.north_cell
        elif direction == EAST:
            wall = cell.east_wall
            other_cell = cell.east_cell
        elif direction == SOUTH:
            wall = cell.south_wall
            other_cell = cell.south_cell
        elif direction == WEST:
            wall = cell.west_wall
            other_cell = cell.west_cell
        else:
            raise NameError("Unknown direction.")
        #other_cell is none if cell is at the maze border
        if other_cell and other_cell.n not in groups[cell.n]:
            wall.is_build = False
            erased_walls += 1
            if other_cell.n < cell.n:
                groups[other_cell.n] += groups[cell.n]
                for n in groups[cell.n]:
                    groups[n] = groups[other_cell.n]
            else:
                groups[cell.n] += groups[other_cell.n]
                for n in groups[other_cell.n]:
                    groups[n] = groups[cell.n]
            new_open_walls.append((x,y,direction))
    return Maze(cells, width, length, tuple(new_open_walls))

def printable_maze(maze:Maze) -> str:
    """ Return an utf-8 string for representing the maze.
    Args:
        maze (Maze): The maze to print.
    """
    corners = [' ','╶','╷','┌','╴','─','┐','┬','╵','└','│','├','┘','┴','┤','┼']
    #         [ 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15]
    draw = []
    last_line = []
    for  x, row in enumerate(maze.cells):
        for y, cell in enumerate(row):
            north_cell = cell.north_cell
            north_wall = 1 if cell.north_wall.is_build else 0
            north_cell_east_wall = 1 if north_cell and north_cell.east_wall.is_build else 0
            north_cell_west_wall = 1 if north_cell and north_cell.west_wall.is_build else 0
            east_cell = cell.east_cell
            east_wall = 1 if cell.east_wall.is_build else 0
            east_cell_north_wall = 1 if east_cell and east_cell.north_wall.is_build else 0
            east_cell_south_wall = 1 if east_cell and east_cell.south_wall.is_build else 0
            west_cell = cell.west_cell
            west_wall = 1 if cell.west_wall.is_build else 0
            west_cell_north_wall = 1 if west_cell and west_cell.north_wall.is_build else 0
            west_cell_south_wall = 1 if west_cell and west_cell.south_wall.is_build else 0
            south_cell = cell.south_cell
            south_wall = 1 if cell.south_wall.is_build else 0
            south_cell_east_wall = 1 if south_cell and south_cell.east_wall.is_build else 0
            south_cell_west_wall = 1 if south_cell and south_cell.west_wall.is_build else 0

            north_west_corner = corners[4*west_cell_north_wall + 2*west_wall + 1*north_wall + 8*north_cell_west_wall]
            north_east_corner = corners[8*north_cell_east_wall + 2*east_wall + 4*north_wall + 1*east_cell_north_wall]
            south_east_corner = corners[4*south_wall + 8*east_wall + 2*south_cell_east_wall + 1*east_cell_south_wall]
            south_west_corner = corners[1*south_wall + 8*west_wall + 2*south_cell_west_wall + 4*west_cell_south_wall]

            draw.append(north_west_corner)
            draw.append(north_wall and "─" or " ")

            if not south_cell:
                last_line.append(south_west_corner)
                last_line.append(south_wall and "─" or " ")
            if not east_cell:
                draw.append(north_east_corner)
                if not south_cell:
                    last_line.append(south_east_corner)
        draw.append("\n")
    draw += last_line
    return "".join(draw)

def spy_maze_construction(width:int, length:int, fout:IO) -> Maze:
    """ Build a maze with a spy random function to know random serie,
    Then write the random and the printable maze in fout.
    """
    with open(fout,"w") as fout:
        fout.write(f"width = {width}\nlength = {length}\n")
        fout.write("randrange = [")
        def spy_random(*args, **kargs):
           res = random.randrange(*args, **kargs)
           fout.write(f"{res}, ")
           return res

        maze = build_maze(width,length, spy_random)
        fout.write("]")
        fout.write(f"\nopen_walls={maze.open_walls}")
        p = printable_maze(maze)
        print(p)
        fout.write('\npmaze = """')
        fout.write(p)
        fout.write('"""')
        fout.close()
    return maze

if __name__ == "__main__":
    import errno
    import getopt
    import sys
    import datetime
    def parse():
        """ Parse arguments
        """
        width = DEFAULT_WIDTH
        length = DEFAULT_LENGTH
        fout = DEFAULT_SPY_FILE_OUT
        print_maze = DEFAULT_PRINT_MAZE
        try:
            options, arguments = getopt.gnu_getopt(
                sys.argv[1:], #Arguments
                'vhqw:l:f:',
                ["version", "help", "quite", "width=", "length=", "fileout=",])
        except:
            print(SCRIPT_USAGE)
            sys.exit(1)
        for option, value in options:
            while option.startswith("-"):
                option = option[1:] #remove prefix "-" to allow lazy options
            if option in ("v", "version"):
                print(VERSION)
                sys.exit()
            if option in ("h", "help"):
                print(SCRIPT_USAGE)
                sys.exit()
            if option in ("q", "quite"):
                print_maze = False
            if option in ("w","width"):
                if not value.isdecimal():
                    print(SCRIPT_USAGE, sys.stderr)
                    sys.exit(1)
                width = int(value)
            elif option in ("l","length"):
                if not value.isdecimal():
                    print(SCRIPT_USAGE, sys.stderr)
                    sys.exit(1)
                length = int(value)
            elif option in ("f", "fileout"):
                fout = value
                try: #Check permission to write file
                    with open(fout, "w") as f:
                        now = datetime.datetime.now()
                        f.write(f"#file generated by {sys.argv[0]} the {now}")
                        f.close()
                except IOError as err:
                    print("IO acces error", sys.stderr)
                    exit(1)
        return width, length, fout, print_maze
    width, length, fout, print_maze = parse()
    maze = None
    if fout:
        maze = spy_maze_construction(width, length, fout)
    else:
        maze = build_maze(width, length)
    if print_maze:
        print(printable_maze(maze))
