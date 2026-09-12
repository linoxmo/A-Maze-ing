import sys
from parsing import parse

def main() -> None:
    if len(sys.argv) != 2:
            print("Error: input should be \' python3 a_maze_ing.py config.txt \'")
            return
    try:
        with open("config.txt", 'r') as file:
            parse(file)
    except Exception as e:
         print(e)

if __name__ == "__main__":
    data = ["hello"]
    exemple = ("hey", "hou","haha")
    data.extend(exemple)
    print(*data, sep= "\n")