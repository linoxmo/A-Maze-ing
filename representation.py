import mlx
from dotenv import load_dotenv
from parsing import get_variable

class Maze():
    def __init__(self, maze: str, entry: str, exit: str, path: str) -> None:
        self._maze = maze
        self._entry = entry
        self._exit = exit
        self._path = path

load_dotenv()
fichier = get_variable("OUTPUT_FILE")
with open(fichier, "r"):
    


