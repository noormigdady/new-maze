from generator import Cell


def maze_in_hex(maze: list[list[Cell]],
                height: int,
                width: int,
                entry_cell: tuple[int, int],
                exit_cell: tuple[int, int],
                path: str,
                file: str) -> None:

    """
        - Represents the cells of generated maze in hexadecimal
        - Writes to the given output file:
          - Each row cells representation in hex followed by
            a new line
          - The entry and exit cells
          - The shortest path between entry and exit cells

        Args -> - maze: [list[list[Cell]]]
                - maze height: [int]
                - maze width: [int]
                - maze entry cell coordinates: tuple[int, int]
                - maze exit cell coordinates: tuple[int, int]
                - the shortest path directions between entry and exit
                cells in a maze: [str]
                - otput file name: [str]

        Return -> None
    """

    north = 1
    east = 2
    south = 4
    west = 8

    cell: Cell
    with open(file, "w") as f:
        for i in range(height):
            seq: str = ""
            for j in range(width):
                cell_sum: int = 0
                cell = maze[i][j]

                if cell.top:
                    cell_sum += north

                if cell.right:
                    cell_sum += east

                if cell.bottom:
                    cell_sum += south

                if cell.left:
                    cell_sum += west

                seq += f"{hex(cell_sum)[2:]}"
            f.write(seq)
            f.write('\n')
        f.write('\n')
        f.write(f"{entry_cell[0]}, {entry_cell[1]}\n")
        f.write(f"{exit_cell[0]}, {exit_cell[1]}\n")
        f.write(path)
