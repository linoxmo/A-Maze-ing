# Generator Documentation

## Usage

Create and use the generator with a configuration:

```
from config import Config
from generator import MazeGenerator

config = Config(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    o_file="maze.txt",
    is_perfect=True,
    seed=42
)

generator = MazeGenerator(config)
generator.generate()
```

# Custom Parameters

The main parameters are:
- width, height: maze dimensions.
- entry, exit: entry and exit coordinates.
- is_perfect: whether the maze is perfect.
- seed: optional seed for reproducible generation.

Configuration can also be loaded from .env using create_conf().

# Accessing the Maze and Solution

After generation:

```
maze = generator.maze
solution = generator.solution
```

maze contains the generated structure, while solution contains the path from the entry to the exit.
