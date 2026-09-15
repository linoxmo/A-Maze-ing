import sys
from parsing import create_conf
from typing import Optional
import os
from dotenv import load_dotenv


def get_variable(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        return "Missing"
    return value

def main() -> None:
    if len(sys.argv) != 2:
            print("Error: input should be \' python3 a_maze_ing.py config.txt \'")
            return
    try:
        new_conf = create_conf()
        new_conf.show_config()
    except Exception as e:
        print(e)

if __name__ == "__main__":

    main()
    """
    data = ["hello"]
    exemple = ("hey", "hou","haha")
    data.extend(exemple)
    print(*data, sep= "\n")
    """