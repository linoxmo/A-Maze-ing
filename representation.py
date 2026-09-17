from pymlx import Mlx, Color
from dotenv import load_dotenv
from parsing import get_variable

class Maze():
    def __init__(self, maze: str, entry: str, exit: str, path: str) -> None:
        self._maze = maze
        self._entry = entry
        self._exit = exit
        self._path = path

def prep() -> str:
    load_dotenv()
    fichier = get_variable("OUTPUT_FILE")
    with open(fichier, "r") as file:
        lab = file.read()
        return (lab)

def cell_walls(hex_char):
    v = int(hex_char, 16)
    return {
        'N': bool(v & 0b0001),
        'E': bool(v & 0b0010),
        'S': bool(v & 0b0100),
        'W': bool(v & 0b1000),
    }

def draw_line(img, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        img.pixel_put(x0, y0, color)   
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

TILE = 32
OFFSET_X = 50
OFFSET_Y = 100
def draw_maze(img, grid, draw_line):
    WALL_COLOR = 0xFFFFFF
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            w = cell_walls(ch)
            px, py = x * TILE + OFFSET_X, y * TILE + OFFSET_Y
            if w['N']: draw_line(img, px, py, px + TILE, py, WALL_COLOR)
            if w['S']: draw_line(img, px, py + TILE, px + TILE, py + TILE, WALL_COLOR)
            if w['W']: draw_line(img, px, py, px, py + TILE, WALL_COLOR)
            if w['E']: draw_line(img, px + TILE, py, px + TILE, py + TILE, WALL_COLOR)

def draw_path(img, start, path, draw_line):
    MOVES = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    PATH_COLOR = 0xFF0000
    x, y = start
    for move in path:
        dx, dy = MOVES[move]
        cx1, cy1 = (x * TILE + TILE // 2) + OFFSET_X , (y * TILE + TILE // 2) + OFFSET_Y
        x, y = x + dx, y + dy
        cx2, cy2 = (x* TILE + TILE // 2) + OFFSET_X, (y * TILE + TILE // 2) + OFFSET_Y
        draw_line(img, cx1, cy1, cx2, cy2, PATH_COLOR)



def fill_cell(img, x, y, color, margin=2):
    px, py = x * TILE + OFFSET_X, y * TILE + OFFSET_Y
    for dy in range(margin, TILE - margin):
        for dx in range(margin, TILE - margin):
            img.pixel_put(px + dx, py + dy, color)

def show_lab() :
   
    
    ENTRY_COLOR = 0x00FF00   # vert
    EXIT_COLOR = 0xFF0000    # rouge
    try:
        labyrinth = prep()
        tab_labyrinth = labyrinth.split("\n")
        grid = tab_labyrinth[0:15:1]
        draw_maze(img, grid, draw_line)
        start = tuple(int(d) for d in tab_labyrinth[16].split(","))
        x,y = start
        fill_cell(img, x, y, ENTRY_COLOR, margin=2)
        end = tuple(int(d) for d in tab_labyrinth[17].split(","))
        x,y = end
        fill_cell(img, x, y, EXIT_COLOR, margin=2)
        path = tab_labyrinth[18]
        draw_path(img,start,path,draw_line)
        win.on_mouse(on_mouse_click)
        win.put_image(img)


    except Exception as e:
        import traceback
        traceback.print_exc()

CLOSE_BTN = {"x": 900, "y": 10, "w": 80, "h": 30}
CLOSE_COLOR = 0xFF0000

def draw_close_button(img):
    for dy in range(CLOSE_BTN["h"]):
        for dx in range(CLOSE_BTN["w"]):
            img.pixel_put(CLOSE_BTN["x"] + dx, CLOSE_BTN["y"] + dy, CLOSE_COLOR)
        win.string_put(CLOSE_BTN["x"] + 15, CLOSE_BTN["y"] + 20, 0x00FF00, "Fermer")

def is_in_button(x, y, btn):
    return btn["x"] <= x <= btn["x"] + btn["w"] and btn["y"] <= y <= btn["y"] + btn["h"]

def on_mouse_click(button, x, y):
    if is_in_button(x, y, CLOSE_BTN):
        mlx.loop_end()
    
if __name__ == '__main__':
    mlx = Mlx()
    WIDTH = 1000
    HEIGHT = 1000   
    win = mlx.new_window(WIDTH, HEIGHT, "Labyrinthe")
    img = mlx.new_image(WIDTH, HEIGHT)
    
    show_lab()
    win.on_close(mlx.loop_end)
    mlx.loop()