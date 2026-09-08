from generator import Cell
from collections import deque
from typing import Deque


def save_directions(path: list[Cell]) -> str:

    """
        Finds the dicrections of the final path
        N -> North
        S -> South
        E -> East
        W -> West

        Args -> A list that has the cells of the path [list[Cell]]

        Return -> The path directions is a string format
    """

    sequence = ""
    while path:
        current = path.pop(0)
        i = current.i
        j = current.j

        if i + 1 == path[0].i:
            sequence += "S"
        elif i - 1 == path[0].i:
            sequence += "N"
        elif j + 1 == path[0].j:
            sequence += "E"
        elif j - 1 == path[0].j:
            sequence += "W"
        if len(path) == 1:
            break
    return sequence


def discover_neighbors(
        maze: list[list[Cell]],
        current: Cell,
        neighbor: Deque[Cell],
        parent: dict[Cell, Cell]
) -> None:

    """
        Finds the possible and reachable neighbors of a single cell in
        the maze, adds the found neighbor to the queue, adds the parent
        of the neighbor to the dictionary and activates the visited_path
        flag for the neighbor; to so it's not visited again

        Args ->
            - Takes the maze [list[list[Cell]]],
            - current cell the searches for neighbors [Cell],
            - neighbor Deque, each found neighbor is add to
              this deque [Deque[Cell]]
            - parent dictionary, a dictiony contains each cell discoverd
              and its parent [dict[Cell, Cell]]

        Return -> None
    """

    i, j = current.i, current.j
    if not current.top and not maze[i - 1][j].visited_path:
        neighbor.append(maze[i - 1][j])
        parent[maze[i - 1][j]] = current
        maze[i - 1][j].visited_path = True

    if not current.right and not maze[i][j + 1].visited_path:
        neighbor.append(maze[i][j + 1])
        parent[maze[i][j + 1]] = current
        maze[i][j + 1].visited_path = True

    if not current.bottom and not maze[i + 1][j].visited_path:
        neighbor.append(maze[i + 1][j])
        parent[maze[i + 1][j]] = current
        maze[i + 1][j].visited_path = True

    if not current.left and not maze[i][j - 1].visited_path:
        neighbor.append(maze[i][j - 1])
        parent[maze[i][j - 1]] = current
        maze[i][j - 1].visited_path = True


def shortest_path(
        maze: list[list[Cell]],
        entry_cell: Cell,
        exit_cell: Cell
        ) -> str:

    """
        Finds the shortest path between the entry and exit points in the maze
        using BFS algorithm (Breadth First Search)

        Args -> Takes the generated maze, entry and exit points as parameters

        Return -> returns returns the directions of the shortest path
    """
    parent: dict[Cell, Cell] = {}
    neighbor: Deque[Cell] = deque([])
    current = entry_cell
    neighbor.append(current)

    while neighbor:
        current = neighbor.popleft()
        if current == exit_cell:
            break
        discover_neighbors(maze, current, neighbor, parent)
        current.visited_path = True

    path: list[Cell] = []
    while current is not entry_cell:
        path.append(current)
        current.is_path = True
        current = parent[current]

    path.reverse()
    path_directions = save_directions(path)
    return path_directions
