from parsing import create_conf,Config, Cord
import random as rd


class MazeGenerator():
    def __init__(self) -> None:
        new_conf: Config = create_conf()
        self._width: int = new_conf.get_width() * 2
        self._height: int = new_conf.get_height() * 2 
        self._entry: tuple[Cord, Cord] = new_conf.get_entry()
        self._exit: tuple [Cord, Cord] = new_conf.get_exit()
        self._isperfect: bool = new_conf.get_is_perfect()
        self._seed: int | None = new_conf.get_seed()
        self.maze : list[list[int]]
        self.sol : str = ""
        self.path: str = ""

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_entry(self) -> tuple[Cord, Cord]:
        return self._entry

    def get_exit(self) -> tuple[Cord, Cord]:
        return self._exit

    def get_isperfect(self) -> bool:
        return self._isperfect

    def get_seed(self) -> int | None:
        return self._seed

    def init_maze(self) -> list[list[int]]:
        self.maze: list[list[int]] =  [[ 1 for _ in range(self.get_width())] for _ in range (self.get_height())]

        return self.maze
    
    def dfs(self, x , y) -> None:
        w: int = self.get_width()
        h: int = self.get_height()
        self.maze[y][x] = 0
        directions: list[tuple[int,int]] = [(0, -2), (0, 2), (-2, 0), (2, 0)]

        rd.shuffle(directions)
        for dx, dy in directions :
            nx: int = x + dx 
            ny = y +dy
            if 0 <= nx < w and 0 <= ny < h:
                if self.maze[ny][nx] == 1:
                    #print(f"de ({x},{y}) vers ({nx},{ny}), mur creusé à ligne={y+dy//2} col={x+dx//2}")
                    self.maze[y + dy // 2 ][x + dx // 2] = 0 
                    self.dfs(nx,ny)

    def build_pattern(self) -> list[str]:
        digit_4: list[str] = ["101", "101", "111", "001", "001"]
        digit_2: list[str] = ["111", "001", "111", "100", "111"]

        return [d4 + "0" + d2 for d4, d2 in zip(digit_4, digit_2)]

    def blocked_cells(self) -> set[tuple[int, int]]:
        pattern: list[str] = self.build_pattern()
        p_h: int = len(pattern) 
        p_w: int = len(pattern[0])
        n_rows: float = (self._height + 1) // 2   
        n_cols: float = (self._width + 1) // 2  
        start_row: float = (n_rows - p_h) // 2
        start_col: float = (n_cols - p_w) // 2 
        blocked: set  = set()

        if n_rows < p_h or n_cols < p_w:
            print("Labyrinthe trop petit pour le motif 42, motif ignoré")
            return set()
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == '1':
                    blocked.add((int(start_row + r), int(start_col + c)))
        return blocked

    def apply_pattern_blocks(self) -> None:
        for (r, c) in self.blocked_cells():
            row: int = r * 2 
            col: int = c * 2  
            self.maze[row][col] = 2   
              
    def create_maze(self, x , y) -> list[list[int]]:
        seed: int | None = self.get_seed()
        if not type(seed) == "None":
            rd.seed(seed)
        self.init_maze()
        maze.apply_pattern_blocks()
        self.dfs(x, y)
        return self.maze

    def is_wall(self, i, j) -> bool:
        if i < 0 or i >= self._height or j < 0 or j >= self._width:
            return True
        return self.maze[i][j] == 1

    def convert_maze(self) -> None:
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

        
if __name__ == '__main__':
    maze = MazeGenerator()
    grille = maze.create_maze(0,0)
    print(grille[1][1], grille[1][0], grille[0][1])
    for ligne in grille:
        texte = "".join(["#" if c == 1 else ("P" if c == "P" else " ") for c in ligne])
        print(texte)
    maze.convert_maze()
    print(maze.sol)