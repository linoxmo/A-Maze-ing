from termios import VQUIT
from unittest.loader import VALID_MODULE_NAME

from pydantic import BaseModel, Field, model_validator
from dotenv import load_dotenv
from typing import Optional
import os


load_dotenv()


class Config(BaseModel):
    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=50)
    entry:tuple[int, int]
    exit: tuple[int, int]
    o_file: str
    is_perfect: bool
    seed:Optional[int] = Field(default = None , ge = 0)

    @model_validator(mode = "before")
    @classmethod
    def check_perfect(cls, data):
        perfect = data.get("is_perfect")
        if not isinstance(perfect, str):
            raise ValueError("PERFECT must be 'True' or 'False'")
        if perfect.lower() not in ("true", "false"):
            raise ValueError("PERFECT must be 'True' or 'False'")
        data["is_perfect"] = perfect.lower() == "true"
        return data

    @model_validator(mode = "after")
    def check_coordinates(self) -> "Config":
        for name, (x, y) in (("entry", self.entry), ("exit", self.exit)):
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} {(x, y)} is outside the maze")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")
        return self

    def show_config(self) -> None:
        for value in self.model_dump().values():
            print(value)

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_entry(self) -> tuple[int,int]:
        return self.entry

    def get_exit(self) -> tuple[int, int]:
        return self.exit

    def get_o_file(self) -> str:
        return self.o_file

    def get_is_perfect(self) -> bool:
        return self.is_perfect

    def get_seed(self) -> Optional[int]:
        return self.seed


def get_variable(name: str, default: Optional[str] = None) -> str:
    """ Function to get the value of the .env environnment variables

    Args:
        name of the environnement variable

    Returns:
        value of the named environnement variable
    """
    value = os.getenv(name, default)
    if value is None:
        return "Missing"
    return value


def create_conf() -> Config:
    """ Function to iniate a Config with the environnment variables

    Args:
        None

    Returns:
        Config object
    """
    entry = get_variable("ENTRY").split(",")
    exit = get_variable("EXIT").split(",")
    seed = get_variable("SEED")

    if seed != "Missing":
        return Config(
            width = int(get_variable("WIDTH")),
            height = int(get_variable("HEIGHT")),
            entry = (int(entry[0]), int(entry[1])),
            exit = (int(exit[0]), int(exit[1])),
            o_file = get_variable("OUTPUT_FILE"),
            is_perfect=get_variable("PERFECT"),
            seed = int(get_variable("SEED"))
        )
    else :
        return Config(
            width = int(get_variable("WIDTH")),
            height = int(get_variable("HEIGHT")),
            entry = (int(entry[0]), int(entry[1])),
            exit = (int(exit[0]), int(exit[1])),
            o_file = get_variable("OUTPUT_FILE"),
            is_perfect=get_variable("PERFECT")
        )


# python3 a_maze_ing.py .env
