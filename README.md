*This activity has been created as part of the 42 curriculum by nibrahee, jaldeek*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator. Given a plain-text configuration file, it builds a
rectangular grid maze, writes it to disk using a compact hexadecimal wall encoding, and
displays it visually in the terminal with colors, an entry/exit marker, and an optional
shortest-path overlay.

The generator supports two modes, controlled by the `PERFECT` flag:

- **`PERFECT=True`** — a perfect maze: exactly one path between the entry and the exit,
  no loops at all.
- **`PERFECT=False`** (default) — a Pac-Man-style playable board: every cell is reachable,
  the four corners and the centre are open, there are at least two independent routes
  between entry and exit, and dead-ends are rare (ideally none, aside from the cells
  used to draw the "42" pattern).

Every maze also contains a visible **"42"** pattern made of permanently closed cells,
placed at the centre of the grid.

## Instructions

### Requirements
- Python 3.10+
- No third-party dependencies — everything uses the standard library.

### Running the program

```bash
python3 amazing.py config.txt
```

> **Note:** the project subject requires the entry point to be named `a_maze_ing.py`.
> The current codebase still uses `amazing.py` — rename the file (or add a thin
> `a_maze_ing.py` wrapper that imports and calls `main()`) before submission.

`config.txt` is the only argument, and it can be renamed to anything you like as long as
you pass the new name on the command line. A default `config.txt` is provided at the
root of the repository.

Once the maze is generated and displayed, an interactive menu lets you:

1. Re-generate a new maze.
2. Show/hide the shortest path from entry to exit.
3. Rotate the maze's wall colors.
4. Quit.

### Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and
ignored.

| Key           | Description                                   | Example              |
|---------------|------------------------------------------------|-----------------------|
| `WIDTH`       | Maze width, number of columns                  | `WIDTH=25`             |
| `HEIGHT`      | Maze height, number of rows                    | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates `x,y` (`x` < WIDTH, `y` < HEIGHT) | `ENTRY=0,0`       |
| `EXIT`        | Exit coordinates `x,y`                         | `EXIT=24,14`           |
| `OUTPUT_FILE` | Output filename (must end in `.txt`)           | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `True` for a perfect (single-path) maze, `False` for a playable multi-route board | `PERFECT=False` |
| `SEED`        | *(optional)* integer seed for reproducible generation | `SEED=42`        |

The parser validates that every mandatory key is present, that `ENTRY`/`EXIT` are
inside the maze bounds and different from each other, and that malformed lines produce
a clear error message instead of a crash.

### Output file format

The maze is written to `OUTPUT_FILE` as one hexadecimal digit per cell, one row per
line (`HEIGHT` lines of `WIDTH` characters each), where each digit encodes which walls
are closed (bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West; a set bit means
the wall is closed). After a blank line, three more lines follow: the entry coordinates,
the exit coordinates, and the shortest path from entry to exit as a string of `N`/`E`/`S`/`W`
letters.

## How the code works

### `MazeGenerator` (in `generator.py`)

`MazeGenerator` is the reusable core of the project. It owns two things: a `width` x
`height` grid of `Cell` objects, and the logic to carve a maze into that grid.

Each `Cell` starts with all four walls closed (`top`, `bottom`, `right`, `left` all
`True`) and carries a few bookkeeping flags used during generation and pathfinding
(`visited`, `visited_path`, `is_path`, `locked` for the "42" pattern cells).

```python
generator = MazeGenerator(height, width)      # build an empty, fully-walled grid
maze = generator.generator(entry=(0, 0))       # carve the maze, starting from (0, 0)
```

Internally, `generator()` implements a **randomized depth-first search (DFS)**, also
known as the "recursive backtracker" algorithm:

1. Start at the entry cell, mark it visited, and push it onto a stack (`track`).
2. At each step, look at the current cell's unvisited neighbors (`where_to()` picks
   one at random among the walls that haven't been broken yet and don't lead to an
   already-visited or "locked" cell).
3. If a valid neighbor exists, break the wall between the two cells (`move()`), mark
   the neighbor visited, and push it onto the stack — this is the "descend" step of DFS.
4. If there's no valid neighbor (a dead end), pop the stack and backtrack to the
   previous cell — this is the classic backtracking step.
5. Repeat until every reachable cell has been visited (or the stack is empty).

This produces a **perfect maze** by construction: since DFS only ever visits each cell
once and always removes exactly one wall per newly-visited cell, the result is a
spanning tree of the grid graph — there is exactly one path between any two cells, with
no loops.

**Why DFS?** A recursive backtracker is simple to reason about and implement iteratively
(no recursion-depth issues on large grids), and it tends to produce mazes with long,
winding corridors and comparatively few short dead-ends near the start — a good visual
and gameplay baseline to build the two required modes on top of.

### Turning a perfect maze into a playable board (`imperfect.py`)

When `PERFECT=False`, `imperfecter()` walks every cell and, for cells that still have
more than two closed walls, randomly breaks one additional wall that isn't already open,
isn't a boundary wall, and doesn't touch a "42" pattern cell (`remove_wall()`). Since the
DFS step already guarantees full connectivity, each extra wall removed creates a new
cycle in the graph — i.e. an alternative route. Doing this across the grid is what turns
a single-path perfect maze into the required loopy, low-dead-end, Pac-Man-style board.

### Shortest path (`bfs.py`)

Once a maze exists, `shortest_path()` finds the shortest route from entry to exit using
**Breadth-First Search (BFS)**. Starting from the entry cell, it explores all reachable
neighbors level by level (`discover_neighbors()` only follows walls that are actually
open), recording each cell's parent the first time it's discovered. Because BFS always
expands the least-explored cells first, the first time it reaches the exit cell is
guaranteed to be via a shortest path (in terms of number of cells) — this is the classic
reason BFS, rather than DFS, is used for shortest-path queries on unweighted graphs.
Once the exit is found, the path is reconstructed by walking the parent pointers back to
the entry and reversed, then converted into a string of `N`/`E`/`S`/`W` letters.

**DFS vs. BFS in this project, in short:** DFS is used to *build* the maze because it
naturally produces long, connected corridors and is easy to run iteratively; BFS is used
to *solve* it because it's the algorithm that guarantees the shortest path on an
unweighted grid, which DFS does not.

### The "42" pattern (`lock_42.py`)

Before generation starts, a fixed set of cells centered on the grid is marked
`locked = True`. Locked cells are excluded from both the DFS carving step and the
loop-adding step, so they remain fully walled-in for the lifetime of the maze — this is
what makes the "42" visible as a solid block in the middle of the maze. If the grid is
too small to fit the pattern, the program prints a warning and skips it rather than
crashing.

## What's reusable, and how

The reusable, importable core is the `generator.py` module — specifically the
`MazeGenerator` class (and the `Cell` class it depends on). It has no dependency on the
rest of the project (config parsing, terminal rendering, or the hex file writer), so it
can be dropped into another project as-is:

```python
from generator import MazeGenerator

gen = MazeGenerator(height=20, width=20)
maze = gen.generator(entry=(0, 0))          # maze is a list[list[Cell]]

cell = maze[0][0]
print(cell.top, cell.right, cell.bottom, cell.left)   # inspect a cell's walls
```

To also get loops (a playable board) or a shortest-path solution, pair it with
`imperfect.imperfecter()` and `bfs.shortest_path()`, which both operate on the same
`list[list[Cell]]` structure returned by `MazeGenerator.generator()`.

> This module is not yet packaged as an installable `mazegen-*` wheel/sdist as required
> by the subject — that packaging step (with its own `pyproject.toml`/build metadata and
> `LICENSE.md`) is still outstanding.

## Resources

- [Maze generation algorithms overview](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — background on recursive backtracker, Prim's, and Kruskal's algorithms.
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) — shortest-path guarantee on unweighted graphs.
- Python standard library docs for `random`, `collections.deque`, and `typing`.

### AI usage

Claude (Anthropic) was used during development to:
- Debug a systemic width/height axis-mismatch bug spanning `generator.py`,
  `config_parser.py`, `lock_42.py`, `imperfect.py`, `print_maze.py`, and
  `maze_in_hex.py`, verified against `maze_analyzer.py` output at each step rather than
  taken on faith.
- Diagnose a config-file parsing crash on blank/malformed lines and a dead `SEED` branch
  caused by a case-sensitivity bug.
- Help draft this README's algorithm explanations (DFS generation, BFS solving) and
  reusability documentation.

All AI-suggested fixes were tested against the actual codebase and cross-checked with
`maze_analyzer.py` before being accepted — see the project's commit history/PR
discussion for the specific before/after test output at each step.

## Team and project management

*(fill in for your team)*

- **Roles:** —
- **Planning:** —
- **What worked well / what could be improved:** —
- **Tools used:** Git, `maze_analyzer.py` (provided) for validation, Claude for
  debugging assistance.
