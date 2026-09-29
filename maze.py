from parsing import create_conf,Config
import random as rd
from collections import deque as dq


class MazeGenerator():
    def __init__(self) -> None:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
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
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        return list(self._directions)

    def init_maze(self) -> list[list[int]]:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        self.maze: list[list[int]] = [[ 1 for _ in range(self._width)] for _ in range (self._height)]
        return self.maze

    def dfs(self, x , y) -> None:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        w: int = self._width
        h: int = self._height
        self.maze[y][x] = 0
        directions = self.get_directions()
        rd.shuffle(directions)
        for dx, dy in directions :
            nx: int = x + dx
            ny: int = y +dy
            if 0 <= nx < w and 0 <= ny < h:
                if self.maze[ny][nx] == 1:
                    #print(f"de ({x},{y}) vers ({nx},{ny}), mur creusé à ligne={y+dy//2} col={x+dx//2}")
                    self.maze[y + dy // 2 ][x + dx // 2] = 0
                    self.dfs(nx,ny)

    def build_pattern(self) -> list[str]:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        digit_4: list[str] = ["101", "101", "111", "001", "001"]
        digit_2: list[str] = ["111", "001", "111", "100", "111"]
        return [d4 + "0" + d2 for d4, d2 in zip(digit_4, digit_2)]

    def blocked_cells(self) -> set[tuple[int, int]]:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
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
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        for (r, c) in self.blocked_cells():
            row: int = r * 2
            col: int = c * 2
            self.maze[row][col] = 2

    def create_maze(self, x , y) -> list[list[int]]:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        seed: int | None = self._seed
        if seed is not None:
            print(seed)
            rd.seed(seed)
        self.init_maze()
        self.apply_pattern_blocks()
        self.dfs(x, y)
        en_x, en_y = self._entry
        self.bfs(en_x, en_y)
        return self.maze

    def is_wall(self, i, j) -> bool:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        if i < 0 or i >= self._height or j < 0 or j >= self._width:
            return True
        return self.maze[i][j] == 1

    def convert_maze(self) -> None:
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
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
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        directions = self.get_directions()
        print(directions[0])
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
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        exit_x, exit_y = self._exit
        directions = self.get_directions()
        queue = dq()
        visited = {(start_x, start_y)}
        print("start",  start_x, start_y)

        queue.append((start_x, start_y, ""))
        while queue:
            print(queue)
            x, y, path = queue.popleft()
            if x == exit_x and y == exit_y:
                self.path = path
                return
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                mid_x, mid_y = x + dx // 2, y + dy // 2
                #print("nx , ny: ", nx ,ny)
                if 0 <= nx < self._width and 0 <= ny < self._height:
                    if (nx,ny) not in visited and self.maze[ny][nx] == 0 and self.maze[mid_y][mid_x] == 0:
                        visited.add((nx,ny))
                        #print("dx,dy :", dx, dy)
                        letter: str = self.add_directions((dx, dy))
                        queue.append((nx, ny, path + letter ))
        return None


def output(maze: MazeGenerator):
    """ Function to xxx

    Args:
        None

    Returns:
        xxx
    """
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


if __name__ == '__main__':
    """ Function to xxx

    Args:
        None

    Returns:
        xxx
    """
    maze = MazeGenerator()
    grille = maze.create_maze(0,0)
    #for ligne in grille:
    #    texte = "".join(["#" if c == 1 else ("P" if c == "P" else " ") for c in ligne])
    #    print(texte)
    maze.convert_maze()
    #print(maze.sol)
    #print(maze.path)
    output(maze)
