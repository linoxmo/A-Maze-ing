from pymlx import Mlx
from dotenv import load_dotenv
from parsing import get_variable
import os
from typing import Any
import random as rd
from parsing import create_conf
from time import sleep
from a_maze_ing import the_maze


colors: list[int] = [0xFFFFFF, 0x808080, 0x00FF00, 0xFF0000, 0x800000, 0xFF69B4, 0xFF7F50, 0x0000FF, \
0x00FFFF, 0x000080, 0x40E0D0, 0x808000, 0x00FF00, 0x008000, 0x50C878, 0xFFFF00, 0xFFA500, 0x800080]


def prep() -> str:
    """Read the maze data from the configured output file.
    Args: none.
    Returns: the content of the output file as a string."""

    load_dotenv()
    fichier = get_variable("OUTPUT_FILE")
    with open(fichier, "r") as file:
        if os.path.getsize(fichier) == 0:
            raise Exception("Erreur: Le fichier est vide")
        lab = file.read()
        return (lab)

def cell_walls(hex_char: str) -> dict[str,bool]:
    """Decode a hexadecimal character to determine the cell walls.
    Args: hex_char is the hexadecimal representation of a maze cell.
    Returns: the presence or absence of the N, W, S and E walls."""

    v = int(hex_char, 16)
    return {
        'N': bool(v & 0b0001),
        'E': bool(v & 0b0010),
        'S': bool(v & 0b0100),
        'W': bool(v & 0b1000),
    }

def draw_line(img, x0, y0, x1, y1, color) -> None:
    """Draw a line between two points on an image.
    Args: img is the image to draw on, x0 and y0 are the starting coordinates, x1 and y1 are the ending coordinates, color is the line color.
    Returns: none."""

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

def look_for_empty_line(tab: list[str]) -> int:
    """Find the first empty line in a list of strings.
    Args: tab is the list of strings to search.
    Returns: the index of the first empty line (or the list length if none is found)."""

    compt = 0
    for k in tab:
        if k == "":
            return compt
        compt +=1
    return compt

def parse_color(value: str, default: int) -> int:
    """Convertit une chaîne "0xRRGGBB" ou "#RRGGBB" en entier, ou renvoie default."""
    if not value:
        return default
    value = value.strip().lstrip("#")
    if value.lower().startswith("0x"):
        value = value[2:]
    try:
        return int(value, 16)
    except ValueError:
        return default


def rd_colors() -> list[int]:
    cp_colors: list[int] = list(colors)
    set_colors: list[int] = []
    for _ in range(5):
        i:int = rd.randint(0,len(cp_colors) - 1)
        set_colors.append(cp_colors.pop(i))
    return set_colors


class Maze():
    """Represent and graphically display a maze.
    Args: none.
    Returns: none."""

    def __init__(self, mlx: Any, win: Any, img: Any, width: int, height: int) -> None:
        """Initialize the maze graphical representation.
        Args: mlx, win, and img are the graphical objects, width and height are the window dimensions.
        Returns: none."""

        self.mlx: Any = mlx
        self.win: Any = win
        self.img: Any = img
        self.width: int = width
        self.height: int = height
        self.maze: list[str]
        self.entry: tuple[int, ...]
        self.exit: tuple[int, ...]
        self.path: str
        self.show_path: bool = False
        self.offset_X: int = 20
        self.offset_Y: int = 20
        config = create_conf()
        size_max: int = max(config.height, config.width)
        self.tile: int = (self.height - 100) // size_max
        set_colors: list[int] = rd_colors()
        self.wall_color: int = set_colors[0]
        self.pattern_color: int = set_colors[1]
        self.entry_color: int = set_colors[2]
        self.exit_color: int = set_colors[3]
        self.path_color: int = set_colors[4]
        self.close_btn: dict[str,int] = {"x": 1100, "y": 100, "w": 150, "h": 30}
        self.toggle_btn: dict[str,int] = {"x": 1100, "y": 200, "w": 150, "h": 30}
        self.newc_btn: dict[str, int] = {"x": 1100, "y": 300, "w": 150, "h": 30}
        self.changes_color: dict[str, int] = {"x": 1100, "y": 400, "w": 150, "h": 30}

    def load(self) -> None:
        """Load the maze, entry, exit and solution path from the output file (after function output).
        Args: none.
        Returns: none."""

        lab = prep()
        tab_lab = lab.split("\n")
        line = look_for_empty_line(tab_lab)
        self.maze = tab_lab[0:line:1]
        self.entry = tuple(int(d) for d in tab_lab[line + 1].split(","))
        self.exit = tuple(int(d) for d in tab_lab[line + 2].split(","))
        self.path = tab_lab[line + 3]

    def render(self) -> None:
        """Render the maze and its graphical elements on the image.
        Args: none.
        Returns: none."""
        self.img = self.mlx.new_image(self.width, self.height)
        self.draw_maze()
        self.draw_pattern_cells()
        self.fill_cell(self.entry[0], self.entry[1], self.entry_color)
        self.fill_cell(self.exit[0], self.exit[1], self.exit_color)
        if self.show_path:
            self.draw_path()
        self._draw_button(self.close_btn, 0x002147)
        self._draw_button(self.toggle_btn, 0x4A0000)
        self._draw_button(self.newc_btn, 0x013220)
        self._draw_button(self.changes_color, 0x301934)

    def draw_pattern_cells(self) -> None:
        """Colore les cellules totalement murées (motif "42")."""
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                w = cell_walls(ch)
                if all(w.values()):
                    self.fill_cell(x, y, self.pattern_color)

    def _draw_button(self, btn, color) -> None:
        """Draw a rectangular button on the image.
        Args: btn contains the button position and dimensions, color is the color of the button.
        Returns: none."""

        for dy in range(btn["h"]):
            for dx in range(btn["w"]):
                self.img.pixel_put(btn["x"] + dx, btn["y"] + dy, color)

    def redraw(self) -> None:
        """Display the current image and buttons and add the buttons' name on it.
        Args: none.
        Returns: none."""

        self.win.put_image(self.img)
        self.win.string_put(self.close_btn["x"] + 10, self.close_btn["y"] + 20, 0xFFFFFF, "Close")
        self.win.string_put(self.toggle_btn["x"] + 10, self.toggle_btn["y"] + 20, 0xFFFFFF, "Path")
        self.win.string_put(self.changes_color["x"] + 10, self.changes_color["y"] + 20, 0xFFFFFF, "Change Color")
        self.win.string_put(self.newc_btn["x"] + 10, self.newc_btn["y"] + 20, 0xFFFFFF, "Regenerate a new Maze")


    def on_mouse_click(self, btn: int, x: int, y: int) -> None:
        """Detect if a mouse click is on the buttons.
        Args:
            btn: The mouse button that was pressed.
            x: The x coordinate of the mouse click.
            y: The y coordinate of the mouse click.
        Returns:
            None.
        """
        if self._is_in(x, y, self.close_btn):
            self.mlx.loop_end()
        elif self._is_in(x, y, self.toggle_btn):
            self.show_path = not self.show_path
            self.render()
        elif self._is_in(x, y, self.changes_color):
            set_colors: list[int] = rd_colors()
            self.wall_color: int = set_colors[0]
            self.pattern_color: int = set_colors[1]
            self.entry_color: int = set_colors[2]
            self.exit_color: int = set_colors[3]
            self.path_color: int = set_colors[4]
            self.render()
        elif self._is_in(x, y, self.newc_btn):
            from maze import MazeGenerator as mg
            from maze import output
            the_maze(mg, output)
            prep()
            self.load()
            self.render()


    @staticmethod
    def _is_in(x, y, btn):
        """Check whether a point (x, y) is inside a button.
        Args: x and y are the point coordinates, btn contains the button position and dimensions.
        Returns: boolean true if the point is inside the button, otherwise false."""

        return btn["x"] <= x <= btn["x"] + btn["w"] and btn["y"] <= y <= btn["y"] + btn["h"]

    def draw_maze(self):
        """Draw the walls of every maze cell on the image.
        Args: none.
        Returns: none."""
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                w = cell_walls(ch)
                px, py = x * self.tile + self.offset_X, y * self.tile + self.offset_Y
                if w['N']: draw_line(self.img, px, py, px + self.tile, py, self.wall_color)
                if w['S']: draw_line(self.img, px, py + self.tile, px + self.tile, py + self.tile, self.wall_color)
                if w['W']: draw_line(self.img, px, py, px, py + self.tile, self.wall_color)
                if w['E']: draw_line(self.img, px + self.tile, py, px + self.tile, py + self.tile, self.wall_color)

    def draw_closed_cells(self, color=0x808080):
        """Fill all maze cells that are closed on all four edges.
        Args: color is the color used to fill the closed cells.
        Returns: none."""

        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                w = cell_walls(ch)
                if all(w.values()):
                    self.fill_cell(x, y, color, margin=2)

    def fill_cell(self, x, y, color, margin=2):
        """Fill one maze cell with a color while preserving a margin around its edges.
        Args: x and y are the cell coordinates, color is the fill color, margin is the space left around its edges (2 by default).
        Returns: none."""

        px, py = x * self.tile + self.offset_X, y * self.tile + self.offset_Y
        for dy in range(margin, self.tile - margin):
            for dx in range(margin, self.tile - margin):
                self.img.pixel_put(px + dx, py + dy, color)

    def draw_path(self):
        """Draw the solution path from the maze entry to the exit.
        Args: none.
        Returns: none."""

        MOVES = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        x, y = self.entry
        for move in self.path:
            dx, dy = MOVES[move]
            cx1, cy1 = (x * self.tile + self.tile // 2) + self.offset_X, (y * self.tile + self.tile // 2) + self.offset_Y
            x, y = x + dx, y + dy
            cx2, cy2 = (x * self.tile + self.tile // 2) + self.offset_X, (y * self.tile + self.tile // 2) + self.offset_Y
            draw_line(self.img, cx1, cy1, cx2, cy2, self.path_color)


def mlx_rendering() -> None:
    """Function that shows a solution"""
    mlx = Mlx()
    WIDTH = 1500
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
