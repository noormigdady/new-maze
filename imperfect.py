import random
from generator import Cell


def Next_cell(maze: list[list[Cell]], cell: Cell, wall: str) -> Cell:

    """
        Finds the next for a given cell in a given direction

        Args -> cell: [Cell]
                direction: [str]

        Return -> retuns the next cell [Cell]
    """

    i = cell.i
    j = cell.j
    if wall == "top":
        i = cell.i - 1
    if wall == "bottom":
        i = cell.i + 1
    if wall == "right":
        j = cell.j + 1
    if wall == "left":
        j = cell.j - 1
    return maze[i][j]


def count_walls(cell: Cell) -> int:

    """
        Counts the number of closed walls the given cell has

        Args -> cell: [Cell]

        Return -> returns count
    """
    count = 0
    if cell.top:
        count += 1
    if cell.bottom:
        count += 1
    if cell.right:
        count += 1
    if cell.left:
        count += 1
    return count


def remove_wall(
        maze: list[list[Cell]],
        height: int,
        width: int,
        seed: int | None,
        cell: Cell
        ) -> None:

    """
        For the given cell it breaks a breakable wall.

        The following rules determine whether a wall is breakable wall or not:
        - a wall should exist
         (an already broken wall can't be broken, but a broken heart can❗)
        - a wall cannot be a maze boundary
        - the current cell should be not of the 42 logo cells

        Args -> maze: list[list[Cell]]
                height: int
                width: int
                cell: Cell
        Return -> None
    """

    walls = ["top", "bottom", "right", "left"]
    if cell.locked:
        return
    if count_walls(cell) == 2:
        return
    if cell.i == 0 or not cell.top:
        walls.remove("top")
    if cell.i == height - 1 or not cell.bottom:
        walls.remove("bottom")
    if cell.j == 0 or not cell.left:
        walls.remove("left")
    if cell.j == width - 1 or not cell.right:
        walls.remove("right")

    if len(walls) == 0:
        return
    while True:
        wall = random.choice(walls)
        next_cell = Next_cell(maze, cell, wall)
        if next_cell.locked:
            walls.remove(wall)
            if len(walls) == 0:
                return
        else:
            break
    if wall == "top":
        cell.top = False
        next_cell.bottom = False
    if wall == "right":
        cell.right = False
        next_cell.left = False
    if wall == "bottom":
        cell.bottom = False
        next_cell.top = False
    if wall == "left":
        cell.left = False
        next_cell.right = False


def imperfecter(
        maze: list[list[Cell]],
        height: int,
        width: int,
        seed: int | None
        ) -> None:

    """
        turnes a generated perfect maze into an imperfect one

        Args -> - maze: list[list[Cell]]
                - maze height and width [both are integers]

        Return -> None
    """

    for row in maze:
        for cell in row:
            remove_wall(maze, height, width, seed, cell)
