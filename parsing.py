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
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        perfect = data.get("is_perfect")
        if not isinstance(perfect, str):
            raise ValueError("PERFECT must be 'True' or 'False'")
        if perfect.lower() not in ("true", "false"):
            raise ValueError("PERFECT must be 'True' or 'False'")
        data["is_perfect"] = perfect.lower() == "true"
        return data

    @model_validator(mode = "after")
    def check_coordinates(self) -> "Config":
        """ Function to xxx

        Args:
            None

        Returns:
            xxx
        """
        for name, (x, y) in (("entry", self.entry), ("exit", self.exit)):
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} {(x, y)} is outside the maze")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")
        return self


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
