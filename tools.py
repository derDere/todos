import os


from consts import *


current_char_set = CHAR_SET
no_colors = False


def cls():
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def hl(length:int = HL_SIZE):
    line = current_char_set[1]
    print(f"{line * length}")


def center(text: str, width: int = HL_SIZE, space:str = " ", color:str=None) -> str:
    h = width // 2
    if len(text) < width:
        h -= len(text) // 2
    else:
        h = 0
    if color and not no_colors:
        print(f"{space * h}{color}{text}{COLOR_RESET}")
    else:
        print(f"{space * h}{text}")