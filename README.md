_This activity has been created as part of the 42 curriculum by lagerard, tmagoudi._


# DESCRIPTION


A-Maze-ing is a maze generator.

It configurates the maze based on the parameters in the **.env**.

The parsing is then handled with **Pydantic**, which validates the dimensions,
entry, exit coordinates and other values and conditions before generating the
maze.

The maze is generated using a randomized **Depth-First Search (DFS)**.
We chose this algorithm because it is simple and efficient for exploring the
grid while creating the maze passages.

#### !!!!! Confirmer les choix avec Theo

Once the maze is generated, a **Breadth-First Search (BFS)** is used to find
a path between the entry and the exit.

The project also includes a **42** pattern in the center of the maze. Its cells
are treated as blocked cells during generation and solution.

The code is divided into several modules:
- **parsing.py**: reads and validates the configuration
- **maze.py**: generates the maze and finds the solution path
- **representation.py**: handles the graphical display with MiniLibX
- **a_maze_ing.py**: runs and coordinates the program


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
