from mazagen.maze import MazeGenerator
from typing import Callable


def new_import() -> list:
    """Import the components required by the main program.
    Args: none.
    Returns: the imported components as a list."""

    import sys
    from mazagen.maze import MazeGenerator as mg
    from mazagen.maze import output
    from mazagen.representation import mlx_rendering as mlxr

    tab_import = [sys, mg, mlxr, output]
    return tab_import


def the_maze(mg: MazeGenerator, output: Callable) -> None:
    """Generate the maze, write its data to the same file and
    display it in the terminal and on a graphical window.
    Args: MazeGenerator as mg, output.
    Returns: none."""

    maze = MazeGenerator()
    _ = maze.create_maze(0, 0)
    maze.convert_maze()
    output(maze)


def main() -> None:
    """Generate the maze, write its data to a new file
    and display it in the terminal and on a graphical window.
    Args: none.
    Returns: none."""

    try:
        tab = new_import()
        sys = tab[0]
        mg = tab[1]
        mlxr = tab[2]
        output = tab[3]
        if len(sys.argv) != 2:
            print("Error: input should be \' python3 a_maze_ing.py .env\'")
            return
        the_maze(mg, output)
        mlxr()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
