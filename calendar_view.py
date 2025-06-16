from datetime import datetime


from consts import *
from tools import *
from todo import ToDo
from todolist import ToDoList


def _get_chars():
    TL = style(4) # Top Left
    TR = style(5) # Top Right
    BL = style(6) # Bottom Left
    BR = style(7) # Bottom Right
    LC = style(8) # Left Cross
    RC = style(9) # Right Cross
    TC = style(10) # Top Cross
    BC = style(11) # Bottom Cross
    HL = style(12) # Horizontal Line
    VL = style(13) # Vertical Line
    MC = style(14) # Cross
    DHL = style(15) # Double Horizontal Line
    return TL, TR, BL, BR, LC, RC, TC, BC, HL, VL, MC, DHL


def line(lengths:list[int], LS:str, HL:str, C:str, RS:str):
    line = [LS]
    for i, length in enumerate(lengths):
        if i > 0:
            line.append(C)
        line.append(HL * length)
    line.append(RS)
    return "".join(line)


class TextAlign:
    LEFT = "L"
    CENTER = "C"
    RIGHT = "R"

    def apply(align:str, content:str, length:int, SPC:str) -> str:
        if len(content) >= length:
            return content[:length]
        space = length - len(content)
        if align == TextAlign.CENTER:
            return f"{SPC * (space // 2)}{content}{SPC * (space - (space // 2))}"
        elif align == TextAlign.RIGHT:
            return f"{SPC * space}{content}"
        else:
            return f"{content}{SPC * space}"


def cells(lengths_content_color:list[tuple[int,str,str|None]], align:str, LS:str, SPC:str, C:str, RS:str):
    line = [LS]
    for i, (length, content, color) in enumerate(lengths_content_color):
        if i > 0:
            line.append(C)
        cell = TextAlign.apply(align, content, length, SPC)
        if color is not None:
            cell = colorize(cell, color)
        line.append(cell)
    line.append(RS)
    return "".join(line)


class CalendarView:
    
    todos:ToDoList
    current_date:datetime

    def __init__(self, todos:ToDoList, current_date:datetime = None):
        self.todos = todos
        if current_date is None:
            self.current_date = datetime.now()
        else:
            self.current_date = current_date
    
    def display(self):
        cls()
        year = self.current_date.year
        month_name = self.current_date.strftime("%B")
        view_width = 8 + (7 * 5) # 8 for the borders, 7 for each day, and 5 for cell width
        hl(view_width)
        center(f"{month_name} - {year}", width=view_width, color=COLOR_BRIGHT_MAGENTA)
        TL, TR, BL, BR, LC, RC, TC, BC, HL, VL, MC, DHL = _get_chars()
        print(line([5] * 7, TL, HL, TC, TR))
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        print(cells([(5, day, COLOR_BRIGHT_CYAN) for day in week_days], TextAlign.CENTER, VL, " ", VL, VL))
        print(line([5] * 7, LC, DHL, MC, RC))
    
    def _handle_input(self):
        i = input()
        return i != "b"

    def run(self):
        while True:
            self.display()
            if not self._handle_input():
                break