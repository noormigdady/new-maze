import random


class Cell():

    """
        Cell class that defines the properties of a single cell
        in the maze.
    """

    def __init__(self, i: int, j: int) -> None:

        """
            The Cell initializer that creats the cell pbject with a set of
            properties and initial values are:

            - top    -> top wall of the cell -> initial value is [True]
            - bottom -> bottom wall of the cell -> initial value is [True]
            - right  -> right wall of the cell -> initial value is [True]
            - left   -> left wall of the cell -> initial value is [True]

            [True -> wall is exist, False -> wall is not exist (open)]

            - visited -> A flag to indecate if the cell is visited during the
              maze generation(dfs algo), initial value is [False]

            - visited_path -> A flag to indecate if the cell is visited while
              finding the shortest path between entry and exit cells(bfs algo),
              initial value is [False]

            - is_path -> A flag to indicate if the cell is part of
              the shortest path between entry and exit cells,
              initial value is [False]

            - locked -> A flag to indicate if the cell is one of the 42
            pattern cells, initial value is [False]

            - i -> the x coordinate
            - j -> the y coordinate

            Args -> i and j values [both integers]

            Return -> None
        """

        self.top = True
        self.bottom = True
        self.right = True
        self.left = True
        self.visited = False
        self.visited_path = False
        self.is_path = False
        self.locked = False
        self.i = i
        self.j = j


class MazeGenerator():

    """
        The MazeGenerator class that defines the prpreties of a maze
        and the functions used to generate it: 
        - Next_cell()
        - valid()
        - where_to()
        - move()
        - generator()
    """

    def __init__(self, height: int, width: int) -> None:

        """
            The MazeGenerator initializer that identifies the maze properties:
            1- creates the first stage of the maze -> the grid
                list[list[Cell]]
            2- height
            3- width

            Args -> maze height and width [both integers]

            Return -> None
        """

        self.grid: list[list[Cell]] = []
        self.height: int = height
        self.width: int = width
        for i in range(height):
            row: list[Cell] = []
            for j in range(width):
                row.append(Cell(i, j))
            self.grid.append(row)

    def Next_cell(self, cell: Cell, direction: str) -> Cell:

        """
            Finds the next for a given cell in a given direction

            Args -> cell: [Cell]
                    direction: [str]

            Return -> retuns the next cell [Cell]
        """

        i = cell.i
        j = cell.j
        if direction == "top":
            i = cell.i - 1
        if direction == "bottom":
            i = cell.i + 1
        if direction == "right":
            j = cell.j + 1
        if direction == "left":
            j = cell.j - 1
        return self.grid[i][j]

    def valid(self, cell: Cell, direction: str) -> bool:

        """
            Checks if the cell found to move from a given direction is valid
            (was not visited before) of not

            Args -> cell: [Cell]
                    direction: [str]

            Return -> [bool]: True if valid and False if not valid
        """

        next_cell = self.Next_cell(cell, direction)
        if next_cell.visited or next_cell.locked:
            return False
        return True

    def where_to(self, cell: Cell) -> str | None:

        """
            Finds the possible unbroken wall (direction) to use it in
            moving toworred the next cell

            Args -> The current cell [Cell]

            Return -> if a direction was found, it returns it [str]
                      if no direction found, nothing to return [None]
        """

        directions = ["top", "bottom", "right", "left"]
        if cell.i == 0:
            directions.remove("top")
        if cell.i == self.height - 1:
            directions.remove("bottom")
        if cell.j == 0:
            directions.remove("left")
        if cell.j == self.width - 1:
            directions.remove("right")

        while True:
            direction = random.choice(directions)
            if self.valid(cell, direction):
                return direction
            else:
                directions.remove(direction)
                if len(directions) == 0:
                    return None

    def move(self, cell: Cell, direction: str) -> Cell:

        """
            Moves from the current to the neighbor cell in a given
            direction and breakes the wall shared between them

            Args -> cell: the current cell [Cell]
                    direction: [str]

            Return -> returns the next cell
        """

        next_cell = self.Next_cell(cell, direction)
        if direction == "top":
            cell.top = False
            next_cell.bottom = False
        if direction == "bottom":
            cell.bottom = False
            next_cell.top = False
        if direction == "right":
            cell.right = False
            next_cell.left = False
        if direction == "left":
            cell.left = False
            next_cell.right = False
        next_cell.visited = True
        return next_cell

    def generator(self, entry: tuple[int, int]) -> list[list[Cell]]:

        """
            Generates a maze using the Depth First Search (dfs)
            algorithm

            Args -> The maze entry cell coordinates [tuple[int, int]]

            Return -> returns a maze [list[list[Cell]]]
        """

        i, j = entry
        track: list[Cell] = []
        track.append(self.grid[i][j])
        cell = self.grid[i][j]
        cell.visited = True
        visited_cells = 1
        if self.width < 11 or self.height < 9:
            size = self.height * self.width
        else:
            size = self.height * self.width - 18

        while visited_cells != size:
            direction = self.where_to(cell)
            if direction is None:
                track.pop()
                if len(track) == 0:
                    break
                cell = track[-1]
            else:
                next_cell = self.move(cell, direction)
                visited_cells += 1
                cell = next_cell
                track.append(cell)
        return self.grid
