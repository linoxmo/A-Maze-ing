def new_import() -> list:
    """ Function to xxx

    Args:
        None

    Returns:
        xxx
    """
    import sys
    from maze import MazeGenerator as mg
    from maze import output
    from representation import mlx_rendering as mlxr

    tab_import = [sys, mg, mlxr, output]
    return tab_import


def main() -> None:
    """ Function to xxx

    Args:
        None

    Returns:
        xxx
    """
    try:
        tab = new_import()
        sys = tab[0]
        mg =  tab[1]
        mlxr = tab[2]
        output = tab[3]
        if len(sys.argv) != 2:
            print("Error: input should be \' python3 a_maze_ing.py config.txt \'")
            return
        maze = mg()
        grille = maze.create_maze(0,0)
        print(grille[1][1], grille[1][0], grille[0][1])
        for ligne in grille:
            texte = "".join(["#" if c == 1 else ("P" if c == "P" else " ") for c in ligne])
            print(texte)
        maze.convert_maze()
        output(maze)
        mlxr()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
