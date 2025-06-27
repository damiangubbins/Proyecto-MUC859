import os
import typing

RED = "\u001b[31m"
GRN = "\u001b[32m"
YLW = "\u001b[33m"
BLU = "\u001b[34m"
CLR = "\u001b[0m"

type Color = typing.Literal[
    "\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[34m", "\u001b[0m"
]

clear = lambda: print("\u001b[H\u001b[J", end="")
clear_line = lambda: print("\u001b[2K", end="")

logging_space = os.get_terminal_size().lines - 18


def fprint(x: int, c: Color, *args, **kwargs):
    print(f"\u001b[{x};{4}f", end="")
    print(c, *args, **kwargs, sep="", end=f"{CLR}", flush=True)


def top_print(*args, **kwargs):
    """Print at the top of the console, scrolling existing content down"""
    print(f"\u001b[{16};{4}f", end="")
    print("\u001b[1L", end="")
    print(f"\u001b[{16};{4}f", end="")
    print(*args, **kwargs)
    print(f"\u001b[7B", end="")
    print("\u001b[2K", end="")
