from token import OP

from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
from typing import Annotated, Optional
import os

class Config(BaseModel):
    width: int = Field(ge=2, le=50)
    height: int = Field(ge=2, le=50) 
    entry:tuple[Cord, Cord]
    exit: tuple[Cord, Cord]
    o_file: str 
    is_perfect: bool 
    seed:Optional[int] = Field(default = None , ge = 0)

    def show_config(self):
        for value in self.model_dump().values():
            print(value)

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_entry(self) -> tuple[Cord,Cord]:
        return self.entry

    def get_exit(self) -> tuple[Cord, Cord]:
        return self.exit

    def get_o_file(self) -> str:
        return self.o_file

    def get_is_perfect(self) -> bool:
        return self.is_perfect

    def get_seed(self) -> Optional[int]:
        return self.seed
    


def get_variable(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        return "Missing"
    return value

load_dotenv()
Cord = Annotated[int, Field(ge = 0, le = \
    max(int(get_variable("WIDTH")) - 1, int(get_variable("HEIGHT")) -1 ))] 


def create_conf() -> Config:
    entry = get_variable("ENTRY").split(",")
    exit = get_variable("EXIT").split(",")
    seed = get_variable("SEED")

    if entry == exit:
        raise ValueError("The exit can't be at the same place as the entree !")

    if seed != "Missing":
        return Config(
            width = int(get_variable("WIDTH")),
            height = int(get_variable("HEIGHT")),
            entry = (int(entry[0]), int(entry[1])),
            exit = (int(exit[0]), int(exit[1])),
            o_file = get_variable("OUTPUT_FILE"),
            is_perfect= get_variable("PERFECT").lower() == "true",
            seed = int(get_variable("SEED"))
        )
    else : 
        return Config(
                    width = int(get_variable("WIDTH")),
                    height = int(get_variable("HEIGHT")),
                    entry = (int(entry[0]), int(entry[1])),
                    exit = (int(exit[0]), int(exit[1])),
                    o_file = get_variable("OUTPUT_FILE"),
                    is_perfect= get_variable("PERFECT").lower() == "true"
                )