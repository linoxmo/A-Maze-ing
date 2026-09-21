def new_import() -> tuple: 
    import sys
    from parsing import create_conf
    return sys, create_conf

def main() -> None:
    try:
        sys, create_conf = new_import()
    except Exception as e:
        print(e)
        return
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