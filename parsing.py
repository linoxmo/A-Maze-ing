from pydantic import BaseModel, Field, model_validator
from dotenv import load_dotenv
from typing import Optional
import os


load_dotenv()


class Config(BaseModel):
    """Represent and validate the maze configuration.
    Args: width, height, entry, exit, o_file, is_perfect, optional seed are the maze configuration values.
    Returns: none."""

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
        """Validate and convert the PERFECT configuration value to a boolean.
        Args: data contains the configuration values to validate.
        Returns: the configuration data with PERFECT converted to a boolean. """

        perfect = data.get("is_perfect")
        if not isinstance(perfect, str):
            raise ValueError("PERFECT must be 'True' or 'False'")
        if perfect.lower() not in ("true", "false"):
            raise ValueError("PERFECT must be 'True' or 'False'")
        data["is_perfect"] = perfect.lower() == "true"
        return data

    @model_validator(mode = "after")
    def check_coordinates(self) -> "Config":
        """Validate the entry and exit coordinates of the maze.
        Args: none.
        Returns: the validated configuration. """

        for name, (x, y) in (("entry", self.entry), ("exit", self.exit)):
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} {(x, y)} is outside the maze")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")
        return self


def get_variable(name: str, default: Optional[str] = None) -> str:
    """Get an environment variable by its name.
    Args: name is the variable to get and default is its optional default value.
    Returns: the variable value, its default value or "Missing" if neither exists."""

    value = os.getenv(name, default)
    if value is None:
        return "Missing"
    return value


def create_conf() -> Config:
    """Create the maze configuration based on the environment variables.
    Args: none.
    Returns: the validated maze configuration."""

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
