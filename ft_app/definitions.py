import pathlib
import os

PROJECT_ROOT_PATH = pathlib.Path(os.path.abspath(__file__)).parent.parent
INPUT_PATH = pathlib.Path.joinpath(PROJECT_ROOT_PATH, "input")

if __name__ == "__main__":
    print("PROJECT_ROOT_PATH:", PROJECT_ROOT_PATH)
    print("INPUT_PATH:", INPUT_PATH)