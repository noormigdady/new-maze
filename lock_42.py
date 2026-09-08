from generator import Cell


def lock_42(grid: list[list[Cell]], height: int, width: int) -> None:

    """
        Finds the 42 pattern cells, so they are not included in
        the breaking walls prosses of the maze generation

        Args -> - grid before being a maze [list[list[Cell]]]
                - maze height and width [both are integers]

        Return -> None
    """

    if width < 11 or height < 9:
        return
    i = height // 2
    j = width // 2
    # grid[i - 1][j - 1].locked = True
    # grid[i - 2][j - 1].locked = True
    grid[i][j - 1].locked = True
    grid[i][j - 2].locked = True
    grid[i][j - 3].locked = True
    grid[i - 1][j - 3].locked = True
    grid[i - 2][j - 3].locked = True
    grid[i + 1][j - 1].locked = True
    grid[i + 2][j - 1].locked = True
    grid[i][j + 1].locked = True
    grid[i][j + 2].locked = True
    grid[i][j + 3].locked = True
    grid[i + 1][j + 1].locked = True
    grid[i + 2][j + 1].locked = True
    grid[i + 2][j + 2].locked = True
    grid[i + 2][j + 3].locked = True
    grid[i - 1][j + 3].locked = True
    grid[i - 2][j + 3].locked = True
    grid[i - 2][j + 2].locked = True
    grid[i - 2][j + 1].locked = True
