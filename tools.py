from datetime import datetime, timedelta
import time
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


def edit_string(message:str, default:str="") -> str:
    print(message)
    print(f"  {COLOR_BRIGHT_BLACK}(You may cancel by entering ctrl-x){COLOR_RESET}")
    print(f"  Current: {COLOR_BRIGHT_GREEN}\"{default}\"{COLOR_RESET}")
    i = input("  New: ")
    if i == CTRL_X_INPUT:
        print(f"{COLOR_BRIGHT_YELLOW}Edit Canceled.{COLOR_RESET}")
        time.sleep(0.5)
        return default
    return i


def edit_date(message:str, default:datetime=None, allow_empty:bool=False) -> datetime:
    print(message)
    non_opt = " n" if allow_empty else ""
    print(f"  {COLOR_BRIGHT_CYAN}(Options: ? YYYY-MM-DD d+<DAYS> d-<DAYS> t{non_opt}){COLOR_RESET}")
    print(f"  {COLOR_BRIGHT_BLACK}(You may cancel by entering ctrl-x){COLOR_RESET}")
    defaults = default.strftime("%Y-%m-%d") if default else "None"
    while True:
        print(f"  Current: {COLOR_BRIGHT_GREEN}{defaults}{COLOR_RESET}")
        i = input("  New: ")
        if i == CTRL_X_INPUT:
            print(f"{COLOR_BRIGHT_YELLOW}Edit Canceled.{COLOR_RESET}")
            time.sleep(0.5)
            return default
        elif i.lower() == "?":
            print("")
            print(f"{COLOR_BRIGHT_CYAN}Options:{COLOR_RESET}")
            print(f"  YYYY-MM-DD: Set a specific date.")
            print(f"  d+<DAYS>: Set a date in the future, e.g., d+7 for 7 days from now.")
            print(f"  d-<DAYS>: Set a date in the past, e.g., d-7 for 7 days ago.")
            print(f"  t: Set to today's date.")
            if allow_empty:
                print(f"  n: Set to None (empty date).")
            print(f"  ctrl-x: Cancel the edit.")
            print("")
        elif i.lower() == "t":
            return datetime.now()
        elif allow_empty and i.lower() == "n":
            return None
        elif i.lower().startswith("d+") or i.lower().startswith("d-"):
            m = 1 if i.lower().startswith("d+") else -1
            ns = i[2:]
            if ns.isnumeric():
                days = int(ns) * m
                new_date = datetime.now() + timedelta(days=days)
                return new_date
            else:
                print(f"{COLOR_RED}Invalid format. Use d+<DAYS> or d-<DAYS> where <DAYS> is a number.{COLOR_RESET}")
        else:
            try:
                new_date = datetime.strptime(i, "%Y-%m-%d")
                return new_date
            except ValueError:
                print(f"{COLOR_RED}Invalid date format. Please use YYYY-MM-DD.{COLOR_RESET}")


def edit_multiline(message:str, default:str="") -> str:
    print(message)
    print(f"  {COLOR_BRIGHT_BLACK}(You may cancel by entering ctrl-x){COLOR_RESET}")
    print("  Current: \"%s\"" % default)
    print("  Enter your text (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line == CTRL_X_INPUT:
            print("Edit Canceled.")
            time.sleep(0.5)
            return default
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines) if lines else default