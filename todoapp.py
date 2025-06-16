import time
from datetime import datetime
from typing import Optional
import re


from consts import *
from tools import *
from todo import ToDo
from todolist import ToDoList
from calendar_view import CalendarView


class ToDoApp:

    todo_list: ToDoList
    filename: str
    _selected_task_index: int
    _selected_date: Optional[datetime] = None
    _start_commands: list[str] = []

    def __init__(self, filename: str):
        self.todo_list = ToDoList()
        self.filename = filename
        self._selected_task_index = 0
        self.todo_list.load(filename)
        self._start_commands = []
    
    def _print_edit_help(self):
        cls()
        hl()
        center("EDIT HELP:", HL_SIZE, color=COLOR_CYAN)
        hl()
        print("")
        print("  t    Toggle the state of the task")
        print("")
        print("  n    Select next field")
        print("")
        print("  p    Select previous field")
        print("")
        print("  e    Edit the selected field (not implemented yet)")
        print("")
        print(" ^X")
        print("  q")
        print("  b    Go back to the main menu")
        print("       you may also enter nothing to go back")
        print("")
        print("  ?    Show this help")
        print("")
        hl()
        input("Press Enter to return to the edit menu...")
    
    def _edit_task(self, task: ToDo):
        selectables = task.selectable_fields()
        selection = 0
        while True:
            selected_field = selectables[selection]
            cls()
            task.print_full(selection=selected_field)
            center("Options: t n p e b ?", color=COLOR_BRIGHT_CYAN)
            hl()

            cmd = input(": ").strip().lower()
            if cmd == "n":
                selection = (selection + 1) % len(selectables)
            elif cmd == "p":
                selection = (selection - 1) % len(selectables)
            elif cmd == "t":
                task.toggle()
            elif cmd == "e":
                hl()
                if selected_field == "title":
                    new_title = edit_string("Edit Title:", task.title).strip()
                    task.title = new_title
                    self.todo_list.save(self.filename)
                elif selected_field == "planned":
                    new_deadline = edit_date("Edit Deadline:", task.planned_at, True)
                    task.planned_at = new_deadline
                    self.todo_list.save(self.filename)
                elif selected_field == "created":
                    new_created = edit_date("Edit Creation Date:", task.created_at)
                    task.created_at = new_created
                    self.todo_list.save(self.filename)
                elif selected_field == "description":
                    new_description = edit_multiline("Edit Description:", task.description).strip()
                    task.description = new_description
                    self.todo_list.save(self.filename)
            elif cmd == "b" or cmd == CTRL_X_INPUT or cmd == "q" or cmd == "":
                break
            elif cmd == "?":
                self._print_edit_help()

    def _print_help_min(self, max_w: int = HL_SIZE):
        center("Options: + t d e q ? p n g", max_w, color=COLOR_BRIGHT_CYAN)
        hl(max_w)
    
    def _print_help_full(self):
        cls()
        hl()
        center("HELP:", HL_SIZE, color=COLOR_BRIGHT_MAGENTA)
        hl()
        center("Quick Commands:", HL_SIZE, color=COLOR_BRIGHT_CYAN)
        hl()
        print("")
        print("  +    Add a new task")
        print("       You can add a title right after the + sign, e.g. `+ My new task`")
        print("")
        print("  -    Remove the selected task")
        print("       You can also remove using the tasks name, e.g. `- My new task`")
        print("       Partial matches are allowed, e.g. `- new` will remove all tasks that contain the word 'new'")
        print("")
        print("  d    show details of the selected task")
        print("       You can also view using the tasks name, e.g. `d My new task`")
        print("       partial matches are allowed, e.g. `d new` will show the first task that contains the word 'new'")
        print("")
        print("  e    Edit the selected task")
        print("       You can also edit using the tasks name, e.g. `e My new task`")
        print("       partial matches are allowed, e.g. `e new` will edit the first task that contains the word 'new'")
        print("")
        print("  ?    Show advanced help")
        print("")
        print("  p    select previous task")
        print("       You can also enter the letter p muiltiple times to go back several tasks")
        print("")
        print("  n    select next task")
        print("       You can also enter the letter n muiltiple times to go forward several tasks")
        print("")
        print("  g    Go to task by index")
        print("       You can also use nonnumeric input, e.g. `g Test` will go to the first task that contains the word 'Test'")
        print("")
        print("  t    Toggle task completion")
        print("       You can also toggle using the tasks name, e.g. `t My new task`")
        print("       partial matches are allowed, e.g. `t new` will toggle all tasks that contains the word 'new'")
        print("       You can also combine this with n and p, e.g. `ntp` as long as t is not the first character")
        print("")
        print("  b    go back or exit the application")
        print("")
        print("  q")
        print("  b")
        print(" ^X    Exit the application")
        hl()
        center("Advanced Commands:", HL_SIZE, color=COLOR_BRIGHT_CYAN)
        hl()
        print("  Advanced commands can now also be passed as CLI arguments.")
        print("")
        print("  /             All advanced commands starting with a slash")
        print("")
        print("  /YYYY-MM-DD   Enter an iso-formatted date to filter tasks by date")
        print("")
        print("  /d")
        print("  /def")
        print("  /default      Goes back to the default view (no date filter)")
        print("")
        print("  /c")
        print("  /cal")
        print("  /calendar     Opens the calendar view")
        print("")
        print("  /aon")
        print("  /asciion      Turn ASCII mode on")
        print("  /aoff")
        print("  /asciioff     Turn ASCII mode off")
        print("")
        print("  /con")
        print("  /colorson      Turn colors on")
        print("  /coff")
        print("  /colorsoff     Turn colors off")
        print("")
        print("  /?")
        print("  /h")
        print("  /help         Show this help message")
        hl()
        input("  Press Enter to return to the main menu...")
    
    def _confirm_deletion(self, tasks:list[ToDo]) -> bool:
        if len(tasks) <= 0:
            return False
        if len(tasks) == 1:
            cls()
            hl()
            center("Deleting Task:", color=COLOR_BRIGHT_RED)
            hl()
            tasks[0].print_min(prefix="  ", suffix="", color=COLOR_BRIGHT_YELLOW)
            hl()
            time.sleep(2)
            return True
        cls()
        hl()
        center("Confirm Deletion:", color=COLOR_BRIGHT_RED)
        hl()
        center("Are you sure you want to delete the following tasks?")
        max_w = 0
        for task in tasks:
            if len(task.title) > max_w:
                max_w = len(task.title)
            if max_w > HL_SIZE - 4:
                max_w = HL_SIZE - 4
                break
        max_w += 4  # for prefix and suffix
        for task in tasks:
            task.print_min(prefix="  ", suffix="", padw=max_w, color=COLOR_BRIGHT_YELLOW)
        hl()
        print("Type 'yes' to confirm or anything else to cancel.")
        cmd = input(": ").strip().lower()
        if cmd == "yes":
            return True
        else:
            cls()
            hl()
            center("Deletion cancelled.", color=COLOR_BRIGHT_GREEN)
            hl()
            input("Press Enter to return to the main menu...")
            return False
    
    def next_task(self, all_tasks) -> None:
        self._selected_task_index += 1
        if self._selected_task_index >= len(all_tasks):
            self._selected_task_index = 0
    
    def previous_task(self, all_tasks) -> None:
        self._selected_task_index -= 1
        if self._selected_task_index < 0:
            self._selected_task_index = len(all_tasks) - 1

    def _find_tasks(self, cmd:str, all_tasks:list[ToDo]) -> list[ToDo]:
        if len(cmd) > 1:
            search = cmd[1:].strip()
            found_tasks = self.todo_list.find_task(search, all_tasks)
            if len(found_tasks) > 0:
                tasks = found_tasks
            else:
                tasks = []
        else:
            tasks = [all_tasks[self._selected_task_index]]
        return tasks
    
    def _find_task(self, cmd:str, all_tasks:list[ToDo], allow_none:bool=False) -> ToDo:
        tasks = self._find_tasks(cmd, all_tasks)
        if len(tasks) > 0:
            return tasks[0]
        else:
            if allow_none:
                return None
            return all_tasks[self._selected_task_index]
    
    def _new_task_title(self, cmd:str) -> str:
        new_task_title = cmd[1:].strip() if len(cmd) > 1 else ""
        if len(new_task_title) <= 0:
            new_task_title = "New Task"
        return new_task_title
    
    def _menu_input(self) -> str:
        if len(self._start_commands) > 0:
            cmd = self._start_commands.pop(0)
        else:
            cmd = input(": ").strip() + " "
        cmds = cmd[0].lower()
        cmd = cmd.strip()
        return cmds, cmd
    
    def _menu_calculations(self):
        max_w = 16
        todays_tasks = self.todo_list.get_todays_tasks()
        if self._selected_date is not None:
            todays_tasks = self.todo_list.get_tasks_for_date(self._selected_date)
        todays_len = len(todays_tasks)
        if self._selected_date is None:
            future_tasks = self.todo_list.get_upcoming_tasks()
        else:
            future_tasks = []
        future_len = len(future_tasks)
        all_tasks = [*todays_tasks, *future_tasks]
        larr = style(2)
        rarr = style(3)
        for task in all_tasks:
            if len(task.title) > max_w:
                max_w = len(task.title)
            if max_w > HL_SIZE - 5 - 5:
                max_w = HL_SIZE - 5 - 5
                break
        inner_w = max_w + 4 #  + len("[ ] ")
        inner_w += len(str(len(all_tasks))) + 2 # for index and colon
        max_w = inner_w + 5 + 5 # plus suffix and prefix
        return max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr, all_tasks
    
    def _display_list_part(self, tasks:list[ToDo], max_w:int, inner_w:int, larr:str, rarr:str, offset:int=0, page_size:int=10, max_index:int|None=None):
        from_i = offset
        to_i = from_i + page_size
        if self._selected_task_index > (to_i - 3):
            from_i = self._selected_task_index - page_size + 2
            to_i = self._selected_task_index + 2
        if (from_i - offset) > (len(tasks) - page_size):
            from_i = (len(tasks) - page_size + offset)
            to_i = (len(tasks) + offset)
        if from_i < offset:
            from_i = offset
            to_i = from_i + page_size
        for i, task in enumerate(tasks):
            i += offset
            if i < from_i or i >= to_i:
                continue
            prefix = "     " if i != self._selected_task_index else (" " + larr + larr + larr + " ")
            suffix = "     " if i != self._selected_task_index else (" " + rarr + rarr + rarr + " ")
            color = COLOR_BRIGHT_YELLOW if i == self._selected_task_index else None
            task.print_min(prefix, suffix, inner_w, max_w, color=color, index=i, max_index=max_index)
    
    def _display_menu(self, max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr):
        cls()
        hl(max_w)
        center("TODOS:", max_w, color=COLOR_BOLD + COLOR_BRIGHT_MAGENTA + COLOR_UNDERLINE)
        hl(max_w)
        if todays_len > 0 or self._selected_date is not None:
            if self._selected_date is not None:
                center(f"Date: {self._selected_date.strftime('%Y-%m-%d')}", max_w, color=COLOR_CYAN)
            else:
                center("Today:", max_w, color=COLOR_CYAN)
            if todays_len > 0:
                self._display_list_part(todays_tasks, max_w, inner_w, larr, rarr, max_index=todays_len + future_len - 1)
            elif self._selected_date is not None:
                center("No tasks for this date.", max_w, color=COLOR_BRIGHT_BLACK)
            hl(max_w)
        if future_len > 0:
            center("Upcoming:", max_w, color=COLOR_CYAN)
            self._display_list_part(future_tasks, max_w, inner_w, larr, rarr, offset=todays_len, max_index=todays_len + future_len - 1)
            hl(max_w)
        self._print_help_min(max_w)
    
    def _print_alert(self, msg: str, max_w: int = HL_SIZE, color: str = COLOR_BRIGHT_RED, delay: float = 0.5):
        hl(max_w)
        print(" " + colorize(msg, color))
        time.sleep(delay)

    def _main_menu(self) -> bool:
        max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr, all_tasks = self._menu_calculations()
        
        self._display_menu(max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr)

        cmds, cmd = self._menu_input()

        if cmds == "+":
            new_task_title = self._new_task_title(cmd)
            new_task = ToDo(title=new_task_title)
            self._edit_task(new_task)
            self.todo_list.add_task(new_task)
            self.todo_list.save(self.filename)

        elif cmds == "-":
            tasks = self._find_tasks(cmd, all_tasks)
            if self._confirm_deletion(tasks):
                for task in tasks:
                    self.todo_list.remove_task(task)
                self.todo_list.save(self.filename)

        elif cmds == "d":
            task = self._find_task(cmd, all_tasks)
            cls()
            task.print_full()
            input("Press Enter to return to the main menu...")

        elif cmds == "e":
            task = self._find_task(cmd, all_tasks)
            self._edit_task(task)
            self.todo_list.save(self.filename)

        elif cmds == "g":
            argstr = cmd[1:].strip()
            if argstr.isnumeric():
                aindex = int(argstr)
                if aindex < 0 or aindex >= len(all_tasks):
                    self._print_alert(f"Index out of range! (Max: {len(all_tasks) - 1})", max_w)
                else:
                    self._selected_task_index = aindex
            else:
                task = self._find_task(cmd, all_tasks, allow_none=True)
                if task is not None:
                    self._selected_task_index = all_tasks.index(task)
                else:
                    self._print_alert("Task not found!", max_w)

        elif cmds == "q" or cmd == CTRL_X_INPUT or cmd == "b":
            self._print_alert("Exiting the application...\n", max_w, COLOR_WHITE)
            return False
        
        elif cmds == "?":
            self._print_help_full()
        
        elif cmds == "t" and len(cmd) > 1:
            found_tasks = self._find_tasks(cmd, all_tasks)
            if len(found_tasks) > 0:
                for task in found_tasks:
                    task.toggle()
                self.todo_list.save(self.filename)
        
        elif cmds == "/" and len(cmd) > 1:
            self._adv_menu(cmd, max_w)

        else:
            for c in cmd.lower():
                if c == "p":
                    self.previous_task(all_tasks)
                elif c == "n":
                    self.next_task(all_tasks)
                elif c == "t":
                    all_tasks[self._selected_task_index].toggle()
                    self.todo_list.save(self.filename)

        return True
    
    def _adv_menu(self, cmd, max_w=HL_SIZE):
        acmd = cmd[1:].strip().lower()
        if acmd == "default" or acmd == "def" or acmd == "d":
            self._selected_date = None
            self._selected_task_index = 0
        
        elif acmd == "cal" or acmd == "calendar" or acmd == "c":
            cv = CalendarView(self.todo_list, self._selected_date)
            cv.run()
            if cv.show_list:
                self._selected_date = cv.current_date
                self._selected_task_index = 0
        
        elif acmd == "?" or acmd == "h" or acmd == "help":
            self._print_help_full()
        
        elif acmd == "aon" or acmd == "asciion":
            turn_on_ascii()

        elif acmd == "aoff" or acmd == "asciioff":
            turn_off_ascii()
        
        elif acmd == "con" or acmd == "colorson":
            turn_on_colors()
        
        elif acmd == "coff" or acmd == "colorsoff":
            turn_off_colors()

        elif re.match(ISO_DATE_PATTERN, acmd):
            try:
                self._selected_date = datetime.strptime(acmd, "%Y-%m-%d")
                self._selected_task_index = 0
            except ValueError:
                self._print_alert(f"Invalid date: {acmd}", max_w)

    def run(self, start_commands: list[str] = []):
        self._start_commands = start_commands
        while self._main_menu():
            pass