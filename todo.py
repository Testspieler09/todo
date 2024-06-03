from FileManager import FileManager, DataManager
from ScreenManager import ScreenManager
from os import getcwd

def main() -> None:
    # screen = ScreenManager()
    file = FileManager(f'{getcwd()}\\data.json')
    data = DataManager(file.data)
    print(data.data)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="ToDo",
                            description="A minimalistic terminal-based todo-manager written with curses.",
                            epilog="Have fun using it.")

    args = parser.parse_args()

    main()
