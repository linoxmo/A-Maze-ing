_This activity has been created as part of the 42 curriculum by lagerard, tmagoudi._



# DESCRIPTION

A-Maze-ing is a maze generator.

It configurates the maze based on the parameters in the **.env**.

The parsing is then handled with **Pydantic**, which validates the dimensions,
entry, exit coordinates and other values and conditions before generating the
maze.

## Maze generation algorithm

The maze is generated using a randomized **Depth-First Search (DFS)**.
We chose this algorithm because it is simple and efficient for exploring the
grid while creating the maze passages.

Once the maze is generated, a **Breadth-First Search (BFS)** is used to find
a path between the entry and the exit. We chose this algorithm because it is
the simplest way off inding the best path to the exit.

The project also includes a **42** pattern in the center of the maze. Its cells
are treated as blocked cells during generation and solution.

The code is divided into several modules:
- **parsing.py**: reads and validates the configuration
- **maze.py**: generates the maze and finds the solution path
- **representation.py**: handles the graphical display with MiniLibX
- **a_maze_ing.py**: runs and coordinates the program

## What part of code is Reusable

Kind of every part depending of what project you're working on.

##  The roles of each team member and planning

All the code was shared and understood by both members of the group.

- lagerard specialized in the creation of the maze and the parsing of the entries.

- tmagoudi specialized in the solving and the rendering of the maze.

## Wath worked well and what could be improved.

The project is functionnal, without error and a really nice display.

Codes isn't working with to high numbers beccause dfs was recursivly implemented.

To fix this, you should use a iterativ wy of implementing the code.

## Specific tools:

1) Use of Mlx for rendering finals.
2) Use of queue library for code optimisation



# INSTRUCTIONS

Install the dependencies and create the environment:
```bash
make
```

Run the program:
```bash
make run
```

Or:
```bash
python3 a_maze_ing.py .env
```

## Configuration

Example **.env** configuration:
```env
HEIGHT=15
WIDTH=15
ENTRY=1,1
EXIT=12,12
PERFECT=True
OUTPUT_FILE=output.txt
SEED=42
```



# RESSOURCES

Resources used during the project:
- Pears
- Internet searches
- Python documentation
- Pydantic documentation
- MiniLibX documentation
- Resources about DFS and BFS algorithms
- IA to understand better some concepts and debugging
