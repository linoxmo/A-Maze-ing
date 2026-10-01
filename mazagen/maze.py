from mazagen.parsing import create_conf,Config
import random as rd
from collections import deque as dq


class MazeGenerator():
    """Generate a maze and find its solution from the configured parameters.
    Args: none.
    Returns: none."""

    def __init__(self) -> None:
        """Initialize the maze generator with the configuration parameters.
        Args: none.
        Returns: none."""

        new_conf: Config = create_conf()
        self._width: int = new_conf.width * 2
        self._height: int = new_conf.height * 2
        entry: tuple[ int, int]= new_conf.entry
        exit: tuple[int, int] = new_conf.exit
        self._entry: tuple[int, int] = (entry[0] * 2, entry[1] * 2)
        self._exit: tuple[int, int] = (exit[0] * 2, exit[1] * 2)
        self._isperfect: bool = new_conf.is_perfect
        self._seed: int | None = new_conf.seed
        self.o_file: str = new_conf.o_file
        self._directions: list[tuple[int,int]] = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        self.maze : list[list[int]]
        self.sol : str = ""
        self.path: str = ""

    def get_directions(self) -> list[tuple[int,int]]:
        """Return a copy of the possible movement directions.
        Args: none.
        Returns: the possible next movement directions as a list."""

        return list(self._directions)

    def init_maze(self) -> list[list[int]]:
        """Initialize the maze as a grid entirely filled with walls (1).
        Args: none.
        Returns: the initialized maze grid."""

        self.maze: list[list[int]] = [[ 1 for _ in range(self._width)] for _ in range (self._height)]
        return self.maze

    def dfs(self, x , y) -> None:
        """Carve maze passages recursively from the given coordinates using DFS.
        Args: x and y are the starting coordinates in the internal maze grid.
        Returns: none."""

        w: int = self._width
        h: int = self._height
        self.maze[y][x] = 0
        directions = self.get_directions()
        rd.shuffle(directions)
        for dx, dy in directions :
            nx: int = x + dx
            ny: int = y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if self.maze[ny][nx] == 1:
                    self.maze[y + dy // 2 ][x + dx // 2] = 0
                    self.dfs(nx,ny)

    def build_pattern(self) -> list[str]:
        """Build the binary pattern representing the number 42.
        Args: none.
        Returns: the 42 pattern as a list of strings that would be stack one over the other to display the pattern."""

        digit_4: list[str] = ["100", "100", "111", "001", "001"]
        digit_2: list[str] = ["111", "001", "111", "100", "111"]
        return [d4 + "0" + d2 for d4, d2 in zip(digit_4, digit_2)]

    def blocked_cells(self) -> set[tuple[int, int]]:
        """Determine the cells to block to form 42 pattern in the center of the maze.
        Args: none.
        Returns: the coordinates of the cells to block."""

        pattern: list[str] = self.build_pattern()
        p_h: int = len(pattern)
        p_w: int = len(pattern[0])
        n_rows: float = (self._height + 1) // 2
        n_cols: float = (self._width + 1) // 2
        start_row: float = (n_rows - p_h) // 2
        start_col: float = (n_cols - p_w) // 2
        blocked: set = set()
        if n_rows < p_h or n_cols < p_w:
            return set()
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == '1':
                    blocked.add((int(start_row + r), int(start_col + c)))
        return blocked

    def apply_pattern_blocks(self) -> None:
        """Mark the maze cells occupied by the 42 pattern as blocked (2).
        Args: none.
        Returns: none."""

        for (r, c) in self.blocked_cells():
            row: int = r * 2
            col: int = c * 2
            self.maze[row][col] = 2

    def create_maze(self, x , y) -> list[list[int]]:
        """Generate the maze and find the path between its configured entry and exit.
        Args: x and y are the starting coordinates for maze generation.
        Returns: the generated maze grid."""

        seed: int | None = self._seed
        if seed is not None:
            rd.seed(seed)
        self.init_maze()
        self.apply_pattern_blocks()
        en_x, en_y = self._entry
        ex_x, ex_y = self._exit
        if self.maze[en_y][en_x] == 2 or self.maze[ex_y][ex_x] == 2:
            raise Exception("Entry can't be on the 42")
        self.dfs(x, y)
        if not self._isperfect:
            self.remove_dead_ends()
        en_x, en_y = self._entry
        self.bfs(en_x, en_y)
        return self.maze

    def is_wall(self, i, j) -> bool:
        """Check whether the given position represents a wall.
        Args: i and j are the row and column coordinates to check.
        Returns: true if the position is a wall or outside the maze, otherwise false."""

        if i < 0 or i >= self._height or j < 0 or j >= self._width:
            return True
        return self.maze[i][j] == 1

    def convert_maze(self) -> None:
        """Convert the maze walls into their hexadecimal representation.
        Args: none.
        Returns: none."""

        hex_digits: str = "0123456789ABCDEF"
        self.sol: str = ""
        for i in range(0, self._height, 2):
            for j in range(0, self._width, 2):
                value = 0
                if self.is_wall(i - 1, j):
                    value |= 1
                if self.is_wall(i, j + 1):
                    value |= 2
                if self.is_wall(i + 1, j):
                    value |= 4
                if self.is_wall(i, j - 1):
                    value |= 8
                self.sol += hex_digits[value]
            self.sol += "\n"

    def add_directions(self, vector: tuple[int,int]) -> str:
        """Convert a movement vector into its cardinal direction (N, W, S, E).
        Args: a vector.
        Returns: the corresponding cardinal direction as a string."""

        directions = self.get_directions()
        if vector == directions[0]:
            return("N")
        elif vector == directions[1]:
            return("S")
        elif vector == directions[2]:
            return("W")
        elif vector == directions[3]:
            return("E")
        else:
             return("None")

    def bfs(self, start_x , start_y) -> None:
        """Find a path from the given starting coordinates to the maze exit using BFS.
        Args: start_x and start_y are the starting coordinates in the internal maze grid.
        Returns: none."""

        exit_x, exit_y = self._exit
        directions = self.get_directions()
        queue = dq()
        visited = {(start_x, start_y)}

        queue.append((start_x, start_y, ""))
        while queue:
            x, y, path = queue.popleft()
            if x == exit_x and y == exit_y:
                self.path = path
                return
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                mid_x, mid_y = x + dx // 2, y + dy // 2
                if 0 <= nx < self._width and 0 <= ny < self._height:
                    if (nx,ny) not in visited and self.maze[ny][nx] == 0 and self.maze[mid_y][mid_x] == 0:
                        visited.add((nx,ny))
                        letter: str = self.add_directions((dx, dy))
                        queue.append((nx, ny, path + letter ))
        return None

    def remove_dead_ends(self) -> None:
        """ Function that the find the dead ends and open than randomly
            Args:
                self
            Returns:
                None
            """
        for y in range(0, self._height, 2):
            for x in range(0, self._width, 2):
                if self.maze[y][x] == 2:
                    continue

                open_count = 0
                closable = []
                for dx, dy in self.get_directions():
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < self._width and 0 <= ny < self._height):
                        continue
                    mx, my = x + dx // 2, y + dy // 2
                    if self.maze[my][mx] == 0:
                        open_count += 1
                    elif self.maze[ny][nx] == 0:
                        closable.append((mx, my))

                if open_count == 1 and closable:
                    mx, my = rd.choice(closable)
                    self.maze[my][mx] = 0

def output(maze: MazeGenerator) -> None:
    """Write the maze entry, exit and solution path to the configured output file.
    Args: maze is the MazeGenerator containing the data to write.
    Returns: none."""

    fichier: str = maze.o_file
    entry: tuple[int, int] = maze._entry
    exit: tuple[int, int] = maze._exit
    with open(fichier, "w") as f:
        f.write(maze.sol)
        f.write("\n")
        f.write(f"{entry[0] // 2}, {entry[1] // 2}")
        f.write("\n")
        f.write(f"{exit[0] // 2}, {exit[1] // 2} ")
        f.write("\n")
        f.write(maze.path)
