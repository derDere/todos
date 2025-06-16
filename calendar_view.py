from datetime import datetime
import re


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
    LARR = style(3) # Left Arrow
    return TL, TR, BL, BR, LC, RC, TC, BC, HL, VL, MC, DHL, LARR


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
    show_list:bool = False

    def __init__(self, todos:ToDoList, current_date:datetime = None):
        self.todos = todos
        if current_date is None:
            self.current_date = datetime.now()
        else:
            self.current_date = current_date
        self.show_list = False
    
    def display(self):
        #Calculations
        year = self.current_date.year
        month_name = self.current_date.strftime("%B")
        view_width = 5 + 8 + (7 * CAL_CELL_WIDTH) # 5 for CalWeekCol, 8 for the borders, 7 for each day, and CAL_CELL_WIDTH for cell width
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        first_day_of_month = self.current_date.replace(day=1)
        first_weekday = first_day_of_month.weekday()
        view_start_monday = first_day_of_month - timedelta(days=first_weekday)
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        view_end_sunday = last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday()))
        TL, TR, BL, BR, LC, RC, TC, BC, HL, VL, MC, DHL, LARR = _get_chars()

        days = [] # list of tuple of (datetime, task count, task done, in month)
        current_day = view_start_monday
        while current_day <= view_end_sunday:
            day_tasks = self.todos.get_tasks_for_date(current_day)
            task_count = len(day_tasks)
            task_done = sum(1 for task in day_tasks if task.state)
            in_month = current_day.month == self.current_date.month
            days.append((current_day, task_count, task_done, in_month))
            current_day += timedelta(days=1)

        # Printing the calendar view
        cls()
        hl(view_width)
        center(f"{month_name} - {year}", width=view_width, color=COLOR_BRIGHT_MAGENTA)
        print(line([4] + [CAL_CELL_WIDTH] * 7, TL, HL, TC, TR))
        print(cells([(4, "CW", COLOR_BRIGHT_YELLOW)] + [(CAL_CELL_WIDTH, day, COLOR_BRIGHT_CYAN) for day in week_days], TextAlign.CENTER, VL, " ", VL, VL))
        print(line([4] + [CAL_CELL_WIDTH] * 7, LC, DHL, MC, RC))
        today = datetime.now().date()
        for i in range(0, len(days), 7):
            wdays = days[i:i + 7]
            week_of_year = "%02i" % wdays[0][0].isocalendar()[1]
            tasks = [(4, "", None)]
            dates = [(4, week_of_year, COLOR_YELLOW)]
            for day, task_count, task_done, in_month in wdays:
                if not in_month or task_count <= 0:
                    tcontent = ""
                else:
                    tcontent = f"{task_done}/{task_count}"
                tcolor = COLOR_BRIGHT_GREEN if task_done == task_count else COLOR_BRIGHT_YELLOW
                tasks.append((CAL_CELL_WIDTH, tcontent, tcolor))
                dcolor = COLOR_WHITE if in_month else COLOR_BRIGHT_BLACK
                if in_month and day.date() == today:
                    dcolor = COLOR_BRIGHT_YELLOW
                dcontent = day.strftime("%d")
                if day.date() == self.current_date.date():
                    dcontent += " " + LARR
                dates.append((CAL_CELL_WIDTH, dcontent, dcolor))
            if i > 0:
                print(line([4] + ([CAL_CELL_WIDTH] * 7), LC, HL, MC, RC))
            print(cells(tasks, TextAlign.RIGHT, VL, " ", VL, VL))
            print(cells(dates, TextAlign.LEFT, VL, " ", VL, VL))
        print(line([4] + ([CAL_CELL_WIDTH] * 7), BL, HL, BC, BR))
        self._print_options(view_width)
        hl(view_width)
    
    def _print_options(self, view_width):
        center("Options: b y+-N m+-N d+-N t p n YYYY-MM-DD l ?", width=view_width, color=COLOR_BRIGHT_CYAN)
    
    def _print_help(self):
        cls()
        hl()
        center("Calendar View Help", color=COLOR_BRIGHT_MAGENTA)
        hl()
        print("   q")
        print("   b")
        print("  ^X           Back to the main menu")
        print("")
        print("  y+-N         Change the year by N years (e.g., y+1 for next year, y-1 for previous year)")
        print("")
        print("  m+-N         Change the month by N months (e.g., m+1 for next month, m-1 for previous month)")
        print("")
        print("  d+-N         Change the day by N days (e.g., d+1 for next day, d-1 for previous day)")
        print("")
        print("  t            Go to today's date")
        print("")
        print("  p            Previous month")
        print("")
        print("  n            Next month")
        print("")
        print("  YYYY-MM-DD   Go to a specific date (e.g., 2023-10-01)")
        print("")
        print("  l            List all tasks for the selected date")
        print("")
        print("  ?            Show this help message")
        hl()
        input(" Press Enter to continue...")
    
    def _move_by_span(self, cmd):
        if not re.match(TIME_JUMP_PATTERN, cmd):
            return False
        unit = cmd[0]
        mult = 1 if cmd[1] == "+" else -1
        vals = cmd[2:]
        val = int(vals)
        if unit == "y":
            self.current_date = self.current_date.replace(year=self.current_date.year + (mult * val))
        elif unit == "m":
            new_month = self.current_date.month + (mult * val)
            if new_month < 1:
                new_month += 12
                self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=new_month)
            elif new_month > 12:
                new_month -= 12
                self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=new_month)
            else:
                self.current_date = self.current_date.replace(month=new_month)
        elif unit == "d":
            self.current_date += timedelta(days=mult * val)

    def _handle_input(self):
        cmd = input(": ").strip().lower()
        cmds = cmd[0]
        if cmd == "b" or cmd == "q" or cmd == CTRL_X_INPUT:
            return False
        
        elif cmds == "y" or cmds == "m" or cmds == "d": 
            self._move_by_span(cmd)
        
        elif cmd == "t":
            self.current_date = datetime.now()
        
        elif cmd == "p":
            self._move_by_span("m-1")
        
        elif cmd == "n":
            self._move_by_span("m+1")
        
        elif cmd == "l":
            self.show_list = True
            return False

        elif cmd == "?":
            self._print_help()

        elif re.match(ISO_DATE_PATTERN, cmd):
            try:
                self.current_date = datetime.strptime(cmd, "%Y-%m-%d")
            except ValueError:
                pass

        return True

    def run(self):
        while True:
            self.display()
            if not self._handle_input():
                break