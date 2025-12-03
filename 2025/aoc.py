import os
import time

DATA_FOLDER = r"data/"

BASE_DIR = os.path.dirname(__file__)


def read(day: int, mid_name: str = "input", split_lines=False, remove_blanks=True, single_line=False, as_int=False, fp=None):
    """Generic function to simplify loading"""

    if fp is None:
        file_path = os.path.join(BASE_DIR, f"{DATA_FOLDER}{day}_{mid_name}.txt")
    else:
        if os.path.isfile(fp):
            file_path = fp
        else:
            raise FileNotFoundError(f"File not found {fp}")


    with open(file_path, "r", encoding="utf-8") as f:
        if remove_blanks:
            document_cleansed = [line for line in f.read().split("\n") if line != ""]
        else:
            document_cleansed = [line for line in f.read().split("\n")]

    if not split_lines:
        data_file = document_cleansed
        if as_int:
            data_file = [int(x) for x in document_cleansed]
    else:
        data_file = [[*line] for line in document_cleansed]
        if as_int:
            data_file = [[int(x) for x in line] for line in document_cleansed]

    if single_line:
        data_file = data_file[0]

    return data_file


def time_solution(func):
    def inner(*args, **kwargs):
        start = time.time() * 1000
        out = func(*args, **kwargs)
        end = time.time() * 1000
        time_ms = int(end - start)

        if time_ms > 1000:
            print(f"Timing for '{os.path.basename(func.__code__.co_filename)}, {func.__name__}': {time_ms / 1000}s")
        else:
            print(f"Timing for '{os.path.basename(func.__code__.co_filename)}, {func.__name__}': {time_ms}ms")
        return out

    return inner


if __name__ == "__main__":
    x = read(1)
    print(x)
