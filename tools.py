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
    non_opt = " n" if allow_empty else ""
    defaults = default.strftime("%Y-%m-%d") if default else "None"

    print(message)
    print(f"  {COLOR_BRIGHT_CYAN}(Options: ? YYYY-MM-DD d+<DAYS> d-<DAYS> t{non_opt}){COLOR_RESET}")
    print(f"  {COLOR_BRIGHT_BLACK}(You may cancel by entering ctrl-x){COLOR_RESET}")
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
    lines = default.splitlines() if default else []
    current_line = len(lines)
    larr = current_char_set[2] # left arrow character
    
    while True:
        cls()
        hl()
        center(message, color=COLOR_BRIGHT_CYAN)
        hl()
        num_len = len(str(len(lines)))
        for i, line in enumerate(lines):
            # create line num based in the width of the length of length of lines
            ln = f"{i + 1:>{num_len}} "
            lend = "\n" if i < len(lines) - 1 else ""
            if i == current_line:
                print(f"{ln}{COLOR_BRIGHT_GREEN}{larr} {line}{COLOR_RESET}", end=lend)
            else:
                print(f"{ln}  {line}", end=lend)
        if current_line >= len(lines):
            print(f"{COLOR_BRIGHT_GREEN} {larr}{COLOR_RESET}")
        else:
            print("")
        hl()
        print(f"{COLOR_BRIGHT_CYAN} Options: // /del /done /<LIN> /? /edit <NEW_LINE>{COLOR_RESET}")
        hl()
        cmd = input(": ").strip()
        if cmd == "/done":
            return "\n".join(lines)

        elif cmd == "/?":
            cls()
            hl()
            print(f"{COLOR_BRIGHT_CYAN}Options:{COLOR_RESET}")
            hl()
            print(f"  //          move to the end of the text.")
            print(f"  /del        delete the current line.")
            print(f"  /done       finish editing and return the text.")
            print(f"  /<LIN>      go to line number <LIN> (e.g., /3 for line 3).")
            print(f"  /?          show this help message.")
            print(f"  /edit       edit the current line.")
            print(f"  <NEW_LINE>  add a new line at the current position.")
            hl()
            input("Press Enter to continue...")

        elif cmd == "/del":
            if current_line < len(lines):
                del lines[current_line]
                if current_line >= len(lines):
                    current_line = max(0, len(lines) - 1)

        elif cmd == "/edit":
            if current_line < len(lines):
                new_line = edit_string("Change line %i:" % (current_line + 1), default=lines[current_line])
                lines[current_line] = new_line

        elif cmd.startswith("/"):
            lins = cmd[1:]
            if lins == "/":
                lins = "%i" % (len(lines) + 1)
            if lins.isnumeric():
                line_num = int(lins) - 1
                if 0 <= line_num <= len(lines):
                    current_line = line_num
                else:
                    print(f"{COLOR_RED}Line number out of range.{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}Invalid command.{COLOR_RESET}")
        
        else:
            new_line = cmd
            if current_line < len(lines):
                lines.insert(current_line, new_line)
            else:
                lines.append(new_line)
            current_line += 1