from pymlx import Mlx
from dotenv import load_dotenv
from parsing import get_variable
import os
from typing import Any

def prep() -> str:
    load_dotenv()
    fichier = get_variable("OUTPUT_FILE")
    with open(fichier, "r") as file:
        if os.path.getsize(fichier) == 0:
            raise Exception("Erreur: Le fichier est vide")
        lab = file.read()
        return (lab)

def cell_walls(hex_char: str) -> dict[str,bool]:
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

class Maze():
    def __init__(self, mlx: Any, win: Any, img: Any, width: int, height: int) -> None:
        self.mlx: Any = mlx
        self.win: Any = win
        self.img: Any = img
        self.width: int = width
        self.height: int = height
        self.maze:  list[str]
        self.entry: tuple[int, ...]
        self.exit:  tuple[int, ...]
        self.path: str
        self.show_path: bool = False
        self.offset_X: int = 50
        self.offset_Y: int = 100
        self.tile: int = 32

        self.close_btn: dict[str,int] = {"x": 900, "y": 10, "w": 80, "h": 30}
        self.toggle_btn: dict[str,int] = {"x": 900, "y": 60, "w": 80, "h": 30}

    def load(self):
        lab = prep()
        tab_lab = lab.split("\n")
        self.maze = tab_lab[0:15:1]
        self.entry = tuple(int(d) for d in tab_lab[16].split(","))
        self.exit = tuple(int(d) for d in tab_lab[17].split(","))
        self.path = tab_lab[18]

    def render(self):
        ENTRY_COLOR = 0x00FF00
        EXIT_COLOR = 0xFF0000
        self.img = self.mlx.new_image(self.width, self.height)
        self.draw_maze()
        self.draw_closed_cells()
        self.fill_cell(self.entry[0], self.entry[1], ENTRY_COLOR)
        self.fill_cell(self.exit[0], self.exit[1], EXIT_COLOR)
        if self.show_path:
            self.draw_path()
        self._draw_button(self.close_btn, 0xFFFFFF)
        self._draw_button(self.toggle_btn, 0x0000FF)

    def _draw_button(self, btn, color):
        for dy in range(btn["h"]):
            for dx in range(btn["w"]):
                self.img.pixel_put(btn["x"] + dx, btn["y"] + dy, color)

    def redraw(self):
        self.win.put_image(self.img)
        self.win.string_put(self.close_btn["x"] + 15, self.close_btn["y"] + 20, 0x00FF00, "Fermer")
        self.win.string_put(self.toggle_btn["x"] + 5, self.toggle_btn["y"] + 20, 0xFFFFFF, "Chemin")

    def on_mouse_click(self, btn, x, y):
        if self._is_in(x, y, self.close_btn):
            self.mlx.loop_end()
        elif self._is_in(x, y, self.toggle_btn):
            self.show_path = not self.show_path
            self.render()

    def draw_maze(self):
        WALL_COLOR = 0xFFFFFF
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                w = cell_walls(ch)
                px, py = x * self.tile + self.offset_X, y * self.tile + self.offset_Y
                if w['N']: draw_line(self.img, px, py, px + self.tile, py, WALL_COLOR)
                if w['S']: draw_line(self.img, px, py + self.tile, px + self.tile, py + self.tile, WALL_COLOR)
                if w['W']: draw_line(self.img, px, py, px, py + self.tile, WALL_COLOR)
                if w['E']: draw_line(self.img, px + self.tile, py, px + self.tile, py + self.tile, WALL_COLOR)

    def draw_closed_cells(self, color=0x808080):
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                w = cell_walls(ch)
                if all(w.values()):
                    self.fill_cell(x, y, color, margin=2)

    def draw_path(self):
        MOVES = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        PATH_COLOR = 0xFF0000
        x, y = self.entry
        for move in self.path:
            dx, dy = MOVES[move]
            cx1, cy1 = (x * self.tile + self.tile // 2) + self.offset_X, (y * self.tile + self.tile // 2) + self.offset_Y
            x, y = x + dx, y + dy
            cx2, cy2 = (x * self.tile + self.tile // 2) + self.offset_X, (y * self.tile + self.tile // 2) + self.offset_Y
            draw_line(self.img, cx1, cy1, cx2, cy2, PATH_COLOR)

    def fill_cell(self, x, y, color, margin=2):
        px, py = x * self.tile + self.offset_X, y * self.tile + self.offset_Y
        for dy in range(margin, self.tile - margin):
            for dx in range(margin, self.tile - margin):
                self.img.pixel_put(px + dx, py + dy, color)

    @staticmethod
    def _is_in(x, y, btn):
        return btn["x"] <= x <= btn["x"] + btn["w"] and btn["y"] <= y <= btn["y"] + btn["h"]

def mlx_rendering() -> None:
    mlx = Mlx()
    WIDTH = 1000
    HEIGHT = 1000
    win = mlx.new_window(WIDTH, HEIGHT, "Labyrinthe")
    img = mlx.new_image(WIDTH, HEIGHT)
    maze = Maze(mlx, win, img, WIDTH, HEIGHT)
    maze.load()
    maze.render()
    win.on_mouse(maze.on_mouse_click)
    mlx.on_loop(maze.redraw)
    win.on_close(mlx.loop_end)
    mlx.loop()
