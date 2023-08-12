from src import explore_directory

from rich import print, print_json

class Main:
    def __init__(self, dir_info) -> None:
        pass

if __name__ == "__main__":
    print_json(data=explore_directory("./TestDir/"))
