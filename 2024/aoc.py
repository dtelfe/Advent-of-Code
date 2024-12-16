import os
import time

DATA_FOLDER = r"data/"
FILE_NAMES = {True: "test", False: "input"}

dirname = os.path.dirname(__file__)


def aoc_read(day: int, is_test: bool = False, split_lines: bool = False, remove_blanks: bool = True):
    """Generic function to simplify loading."""
    mid_name = FILE_NAMES.get(is_test)

    # Make the file name. Example: "data/1_input.txt"
    file_name = f"{DATA_FOLDER}{day}_{mid_name}.txt"
    file_path = os.path.join(dirname, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        document = f.read()

    document = [line for line in document.split("\n")]

    if remove_blanks:
        document = [line for line in document if line != ""]

    if split_lines:
        document = [[*line] for line in document]

    return document


# Decorators
def time_solution(func):
    def inner(*args, **kwargs):
        start = time.time() * 1000
        out = func(*args, **kwargs)
        end = time.time() * 1000
        time_ms = int(end - start)

        if time_ms > 1000:
            print(f"Timing for '{func.__name__}': {time_ms/1000}s")
        else:
            print(f"Timing for '{func.__name__}': {time_ms}ms")
        return out

    return inner


if __name__ == "__main__":
    x = aoc_read(1, False, False)
    print(x)
