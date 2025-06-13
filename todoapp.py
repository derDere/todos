import time


from consts import *
from tools import *
from todo import ToDo
from todolist import ToDoList


class ToDoApp:

    todo_list: ToDoList
    filename: str
    _selected_task_index: int

    def __init__(self, filename: str):
        self.todo_list = ToDoList()
        self.filename = filename
        self._selected_task_index = 0
        self.todo_list.load(filename)
    
    def _edit_task(self, task: ToDo):
        cls()
        task.print_full()
        input("Press Enter to edit the task...")
        # TODO: Implement task editing functionality

    def _print_help_min(self, max_w: int = HL_SIZE):
        center("Options: + t d e q ? p n", max_w, color=COLOR_BRIGHT_CYAN)
        hl(max_w)
    
    def _print_help_full(self):
        cls()
        hl()
        center("HELP:", HL_SIZE, color=COLOR_CYAN)
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
        print("  t    Toggle task completion")
        print("       You can also toggle using the tasks name, e.g. `t My new task`")
        print("       partial matches are allowed, e.g. `t new` will toggle all tasks that contains the word 'new'")
        print("       You can also combine this with n and p, e.g. `ntp` as long as t is not the first character")
        print("")
        print("  b    go back or exit the application")
        print("")
        print("  q")
        print(" ^X    Exit the application")
        hl()
        input("Press Enter to return to the main menu...")
    
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
    
    def next_task(self) -> None:
        self._selected_task_index += 1
        if self._selected_task_index >= len(self.todo_list.tasks):
            self._selected_task_index = 0
    
    def previous_task(self) -> None:
        self._selected_task_index -= 1
        if self._selected_task_index < 0:
            self._selected_task_index = len(self.todo_list.tasks) - 1
    
    def _find_tasks(self, cmd:str, all_tasks:list[ToDo]) -> list[ToDo]:
        if len(cmd) > 1:
            search = cmd[1:].strip()
            found_tasks = self.todo_list.find_task(search)
            if len(found_tasks) > 0:
                tasks = found_tasks
            else:
                tasks = []
        else:
            tasks = [all_tasks[self._selected_task_index]]
        return tasks
    
    def _find_task(self, cmd:str, all_tasks:list[ToDo]) -> ToDo:
        tasks = self._find_tasks(cmd, all_tasks)
        if len(tasks) > 0:
            return tasks[0]
        else:
            return all_tasks[self._selected_task_index]
    
    def _new_task_title(self, cmd:str) -> str:
        new_task_title = cmd[1:].strip() if len(cmd) > 1 else ""
        if len(new_task_title) <= 0:
            new_task_title = "New Task"
        return new_task_title
    
    def _menu_input(self) -> str:
        cmd = input(": ").strip() + " "
        cmds = cmd[0].lower()
        cmd = cmd.strip()
        return cmds, cmd
    
    def _menu_calculations(self):
        max_w = 14
        todays_tasks = self.todo_list.get_todays_tasks()
        todays_len = len(todays_tasks)
        future_tasks = self.todo_list.get_upcoming_tasks()
        future_len = len(future_tasks)
        all_tasks = [*todays_tasks, *future_tasks]
        larr = current_char_set[2]
        rarr = current_char_set[3]
        for task in all_tasks:
            if len(task.title) > max_w:
                max_w = len(task.title)
            if max_w > HL_SIZE - 5 - 5:
                max_w = HL_SIZE - 5 - 5
                break
        inner_w = max_w + 4 #  + len("[ ] ")
        max_w = inner_w + 5 + 5 # plus suffix and prefix
        return max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr, all_tasks
    
    def _display_menu(self, max_w, todays_len, todays_tasks, inner_w, future_len, future_tasks, larr, rarr):
        cls()
        hl(max_w)
        center("TODOS:", max_w, color=COLOR_BOLD + COLOR_BRIGHT_MAGENTA + COLOR_UNDERLINE)
        hl(max_w)
        if todays_len > 0:
            center("Today:", max_w, color=COLOR_CYAN)
            for i, task in enumerate(todays_tasks):
                prefix = "     " if i != self._selected_task_index else (" " + larr + larr + larr + " ")
                suffix = "     " if i != self._selected_task_index else (" " + rarr + rarr + rarr + " ")
                color = COLOR_BRIGHT_YELLOW if i == self._selected_task_index else None
                task.print_min(prefix, suffix, inner_w, max_w, color=color)
            hl(max_w)
        if future_len > 0:
            center("Upcoming:", max_w, color=COLOR_CYAN)
            for i, task in enumerate(future_tasks):
                i += todays_len
                prefix = "     " if i != self._selected_task_index else (" " + larr + larr + larr + " ")
                suffix = "     " if i != self._selected_task_index else (" " + rarr + rarr + rarr + " ")
                color = COLOR_BRIGHT_YELLOW if i == self._selected_task_index else None
                task.print_min(prefix, suffix, inner_w, max_w, color=color)
            hl(max_w)
        self._print_help_min(max_w)

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

        elif cmds == "q" or cmd == CTRL_X_INPUT:
            hl(max_w)
            print(" Exiting the application...\n")
            time.sleep(0.5)
            return False
        
        elif cmds == "?":
            self._print_help_full()
        
        elif cmds == "t" and len(cmd) > 1:
            search = cmd[1:].strip()
            found_tasks = self.todo_list.find_task(search)
            if len(found_tasks) > 0:
                for task in found_tasks:
                    task.toggle()
                    self.todo_list.save(self.filename)
        
        else:
            for c in cmd.lower():
                if c == "p":
                    self.previous_task()
                elif c == "n":
                    self.next_task()
                elif c == "t":
                    all_tasks[self._selected_task_index].toggle()
                    self.todo_list.save(self.filename)

        return True

    def run(self):
        while self._main_menu():
            pass