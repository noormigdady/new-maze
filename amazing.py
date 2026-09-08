import sys
import random
import os
from generator import MazeGenerator, Cell
from lock_42 import lock_42
from print_maze import print_maze
from config_parser import config_parser
from imperfect import imperfecter
from bfs import shortest_path
from maze_in_hex import maze_in_hex
from typing import Any


def menu() -> None:

    """
        Pints the user interaction menu
        Args -> takes no args
        Return -> None
    """

    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")


def shuffle_colors() -> dict[str, str]:

    """
        Sets the colors of:
        1- maze [a set of colors and the choise is random]
        2- 42 cells [always white]
        3- Path color [always white]

        Args -> Takes no args

        Return -> returns a dictionary that contains the colors selected,
        in the format:
        {
            "maze_color": "color",
            "color_42": "color",
            "path_color": "color"
        }
    """

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
    maze_color = random.choice(COLORS)
    COLORS.remove(maze_color)
    color_42 = WHITE
    path_color = WHITE
    return {"maze_color": maze_color, "color_42": color_42,
            "path_color": path_color}


def produce(config: dict[str, Any]) -> list[list[Cell]]:

    """
        Produces a maze with the values from the configuration file.

        Args -> Takes the configruation dictionary that contains the following
        mandatory values as KEY=VALUE pairs:
            WIDTH=x [int]                   -> Maze width
            HEIGHT=x [int]                  -> Maze height
            ENTRY=(x, y) [tuple(int, int)]  -> maze entry point
            EXIT=(x, y) [tuple(int, int)]   -> maze exit point
            OUTPUT_FILE=file [str]          -> putput file name
            PERFECT=True/False [bool]       -> a flag: True-> generates
                                                        a perfect maze
                                            Flase-> generates an imperfect maze
            SEED=x [int]                    ->

        Return -> Returnes a maze in the structure of:
                    list[list[Cell]]
    """

    try:
        height = config["HEIGHT"]
        width = config["WIDTH"]
        seed = config["SEED"]
        grid = MazeGenerator(height, width)
        lock_42(grid.grid, height, width)
        i, j = config["ENTRY"]
        x, y = config["EXIT"]
        if grid.grid[i][j].locked or grid.grid[x][y].locked:
            raise Exception("ENTRY/EXIT cannot be in 42 logo")
        maze = grid.generator(config["ENTRY"], seed)
        if not config["PERFECT"]:
            imperfecter(maze, height, width, seed)
        path = shortest_path(maze, maze[i][j], maze[x][y])
        maze_in_hex(maze, height, width, (i, j), (x, y),
                    path, config["OUTPUT_FILE"])
        return maze
    except Exception as e:
        message = str(e).split(",")
        print(message[0])
        sys.exit(1)


def main() -> None:

    """
        The main function that runs the whole program

        Args -> No given args

        Return -> None
    """

    show_path = False
    colors = shuffle_colors()
    args = sys.argv
    if len(args) != 2:
        print("Usage: python3 amazing.py config.txt")
        return
    try:
        with open(args[1], "r"):
            pass
    except FileNotFoundError as e:
        print(e)
    try:
        config = config_parser(args[1])
        i, j = config["ENTRY"]
        x, y = config["EXIT"]
        maze = produce(config)
        print_maze(maze, config["HEIGHT"], config["WIDTH"],
                   config["ENTRY"], config["EXIT"], show_path, colors)
        menu()
    except Exception as e:
        print(e)
        sys.exit(1)

    while True:
        try:
            num = int(input("Choice? (1-4):"))
            if num not in [1, 2, 3, 4]:
                continue
            if num == 1:
                os.system("clear")
                maze = produce(config)
                print_maze(maze, config["HEIGHT"], config["WIDTH"],
                           config["ENTRY"], config["EXIT"], show_path, colors)
                menu()
                continue
            if num == 2:
                os.system("clear")
                show_path = not show_path
                print_maze(maze, config["HEIGHT"], config["WIDTH"],
                           config["ENTRY"],  config["EXIT"], show_path, colors)
                menu()
                continue
            if num == 3:
                os.system("clear")
                colors = shuffle_colors()
                print_maze(maze, config["HEIGHT"], config["WIDTH"],
                           config["ENTRY"], config["EXIT"],
                           show_path, colors)
                menu()
                continue
            if num == 4:
                print("Quitting the program !!")
                break
        except Exception as e:
            message = str(e).split(",")
            print(message[0])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting the program !!")
