#!/usr/bin/python3
# -*- coding: utf-8
# author: Michael Launay
# mail : michaellaunay@ecreall.com
# creation_date : 2015
# update_date : 2021
# Description : Create a maze and print it on stdout.
# Usage :
#      m = build_maze(60,40)
#      print(printable_maze(m))

import random
from typing import List, Type

class Wall:
    """
        Border wall.
    """

    def __init__(self, first_cell:Type["Cell"], second_cell:Type["Cell"], is_build:bool=True):
        """
        The maze is made of cells, wall is a hard border beetween two cells.
        """
        self.first_cell = first_cell
        self.second_cell = second_cell
        self.is_build = is_build

    def set_cells(first_cell, second_cell):
        """
        Modify the border.
        """
        self.first_cell = first_cell
        self.second_cell = second_cell

    def __iter__(self):
        yield self.first_cell
        yield self.second_cell


class Cell:
    """
       A cell is a square place which can have 4 walls.
    """

    def __init__(self, n:int=-1):
        """n is the id number of the cell
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
    def __init__(self, cells:List[List[Cell]], width:int, length:int):
        self.cells = cells
        self.width = width
        self.length = length


def build_maze(width:int, length:int) -> Maze:
    """
        Build a maze.
    """
    cells = [[Cell(x+y*width) for x in range(0, width)] for y in range(0, length)]

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
        x = random.randrange(0, width)
        y = random.randrange(0, length)
        direction = random.randrange(0, 4)
        cell = cells[y][x]
        wall = None
        other_cell = None
        if direction == 0:
            wall = cell.north_wall
            other_cell = cell.north_cell
        elif direction == 1:
            wall = cell.east_wall
            other_cell = cell.east_cell
        elif direction == 3:
            wall = cell.south_wall
            other_cell = cell.south_cell
        else:
            wall = cell.west_wall
            other_cell = cell.west_cell
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

    return Maze(cells, width, length)

def printable_maze(maze:Maze) -> str:
    """
        Return an utf-8 string for representing the maze.
    """
    corners = [' ','╶','╷','┌','╴','─','┐','┬','╵','└','│','├','┘','┴','┤','┼']
    #         [ 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15]
    draw = []
    last_line = []
    for  x, row in enumerate(maze.cells):
        for y, cell in enumerate(row):
            north_cell = cell.north_cell
            north_wall = cell.north_wall.is_build and 1 or 0
            north_cell_east_wall = north_cell and north_cell.east_wall.is_build and 1 or 0
            north_cell_west_wall = north_cell and north_cell.west_wall.is_build and 1 or 0
            east_cell = cell.east_cell
            east_wall = cell.east_wall.is_build and 1 or 0
            east_cell_north_wall = east_cell and east_cell.north_wall.is_build and 1 or 0
            east_cell_south_wall = east_cell and east_cell.south_wall.is_build and 1 or 0
            west_cell = cell.west_cell
            west_wall = cell.west_wall.is_build and 1 or 0
            west_cell_north_wall = west_cell and west_cell.north_wall.is_build and 1 or 0
            west_cell_south_wall = west_cell and west_cell.south_wall.is_build and 1 or 0
            south_cell = cell.south_cell
            south_wall = cell.south_wall.is_build and 1 or 0
            south_cell_east_wall = south_cell and south_cell.east_wall.is_build and 1 or 0 
            south_cell_west_wall = south_cell and south_cell.west_wall.is_build and 1 or 0

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

if __name__ == "__main__":
    m = build_maze(60,40)
    print(printable_maze(m))

