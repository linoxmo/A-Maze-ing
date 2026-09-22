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
                    print(f"de ({x},{y}) vers ({nx},{ny}), mur creusé à ligne={y+dy//2} col={x+dx//2}")
                    self.maze[y + dy // 2 ][x + dx // 2] = 0 
                    self.dfs(nx,ny)

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

    def  solution (self) -> str:
        return ("path")



if __name__ == '__main__':
    maze = MazeGenerator()
    grille = maze.create_maze(0,0)
    print(grille[1][1], grille[1][0], grille[0][1])
    for ligne in grille:
        texte = "".join(["#" if c == 1 else ("P" if c == "P" else " ") for c in ligne])
        print(texte)
    maze.convert_maze()
    print(maze.sol)
