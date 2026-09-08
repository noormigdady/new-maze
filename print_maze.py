from generator import Cell


def print_maze(
        maze: list[list[Cell]],
        height: int,
        width: int,
        entry: tuple[int, int],
        Exit: tuple[int, int],
        show_path: bool,
        colors: dict[str, str]
        ) -> None:
    s, e = Exit
    maze[s][e].top = True
    maze[s][e].left = True
    maze[s][e].bottom = True
    maze[s][e].right = True
    maze[s - 1][e].bottom = True
    maze[s][e - 1].right = True
    """
        Prints the generated maze and path to the terminal screen

        Args -> - maze: [ list[list[Cell]]]
                - maze height: [int]
                - maze width: [int]
                - maze entry cell coordinates: tuple[int, int]
                - maze exit cell coordinates: tuple[int, int]
                - show path flag: bool
                - colors: dict[str, str]

        Return -> None
    """

    maze_color: str = colors["maze_color"]
    color_42: str = colors["color_42"]
    path_color: str = colors["path_color"]
    rows: int = height * 2 + 1
    print(maze_color + "█", end="")
    for j in range(width):
        print(maze_color + "████", end="")
    print()
    for row in range(1, rows - 1):
        i = (row - 1) // 2
        print(maze_color + "█", end="")
        for j in range(width):
            cell: Cell = maze[i][j]
            if cell.locked:
                color = color_42
            else:
                color = maze_color
            if row % 2 == 0:
                if cell.bottom:
                    print(color + "████", end="")
                else:
                    print(color + "   █", end="")
            else:
                if cell.locked:
                    print(color + "████", end="")
                else:
                    if (i, j) == entry:
                        print(color + "🐁 ", end="")
                    elif (i, j) == Exit:
                        print(color + " 🪤", end="")
                    elif cell.is_path and show_path:
                        print(path_color + " * ", end="")
                    else:
                        print(color + "   ", end="")
                    if cell.right:
                        print(color + "█", end="")
                    else:
                        print(" ", end="")
        print()

    print(maze_color + "█", end="")
    for j in range(width):
        print(maze_color + "████", end="")
    print("\033[37m")
