from parsing import create_conf,Config
import random as rd


class MazeGenerator():
    def __init__(self) -> None:
        new_conf = create_conf()
        self._width = new_conf.get_width() * 2
        self._height = new_conf.get_height() * 2 
        self._entry = new_conf.get_entry()
        self._exit = new_conf.get_exit()
        self._isperfect = new_conf.get_is_perfect()
        self._seed = new_conf.get_seed()
        self.maze : list[list[int]]
        self.sol : str = ""
        self.path: str = ""

    def init_maze(self) -> list[list[int]]:
        self.maze =  [[ 1 for _ in range(self._width)] for _ in range (self._height)]
        return self.maze
    
    def dfs(self, x , y) -> None:
        self.maze[y][x] = 0
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        rd.shuffle(directions)
        for dx, dy in directions :
            nx, ny = x + dx, y +dy
            if 0 <= nx < self._width and 0 <= ny < self._height:
                if self.maze[ny][nx] == 1:
                    #print(f"de ({x},{y}) vers ({nx},{ny}), mur creusé à ligne={y+dy//2} col={x+dx//2}")
                    self.maze[y + dy // 2 ][x + dx // 2] = 0 
                    self.dfs(nx,ny)

    def build_pattern(self) -> list[str]:
        digit_4 = ["101", "101", "111", "001", "001"]
        digit_2 = ["111", "001", "111", "100", "111"]
        return [d4 + "0" + d2 for d4, d2 in zip(digit_4, digit_2)]

    def blocked_cells(self):
        pattern = self.build_pattern()
        p_h, p_w = len(pattern), len(pattern[0])
        n_rows = (self._height + 1) // 2   # nb de cellules réelles en hauteur
        n_cols = (self._width + 1) // 2    # nb de cellules réelles en largeur

        if n_rows < p_h or n_cols < p_w:
            print("Labyrinthe trop petit pour le motif 42, motif ignoré")
            return set()

        start_row = (n_rows - p_h) // 2
        start_col = (n_cols - p_w) // 2

        blocked = set()
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == '1':
                    blocked.add((start_row + r, start_col + c))
        return blocked

    def apply_pattern_blocks(self):
        for (r, c) in self.blocked_cells():
            row, col = r * 2, c * 2   # conversion coordonnées compactes -> espace DFS
            self.maze[row][col] = 2   # 2 = "bloqué", jamais creusé
    """
    def bfs(self) -> None :
        self._entry[][] = 0
        pass
    """

    def create_maze(self, x , y) -> list[list[int]]:
        rd.seed(42)
        self.init_maze()
        self.dfs(x, y)
        return self.maze

    def is_wall(self, i, j) -> bool:
        if i < 0 or i >= self._height or j < 0 or j >= self._width:
            return True
        return self.maze[i][j] == 1

    def convert_maze(self):
        hex_digits = "0123456789ABCDEF"
        self.sol = ""
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
    maze.apply_pattern_blocks()
    grille = maze.create_maze(0,0)
    print(grille[1][1], grille[1][0], grille[0][1])
    for ligne in grille:
        texte = "".join(["#" if c == 1 else ("P" if c == "P" else " ") for c in ligne])
        print(texte)
    maze.convert_maze()
    for k in maze.build_pattern():
        print(k)
