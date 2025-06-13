from datetime import datetime
from typing import Optional
import re
import os
import time


TODO_RE_PATTERN = r"^- \[(X| )\] (.+?)( - Deadline: `(\d{4}-\d{2}-\d{2})`)?( - Created: `(\d{4}-\d{2}-\d{2})`)\\?(?:\n\s*```([\s\S]*?)```)?$"
HL_SIZE = 80
CHAR_SET = "✔─▶◀"
ASCII_CHAR_SET = "X_><"
DEFAULT_FILENAME = "todos.md"

COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_UNDERLINE = "\033[4m"
COLOR_BRIGHT_RED = "\033[91m"
COLOR_BRIGHT_GREEN = "\033[92m"
COLOR_BRIGHT_YELLOW = "\033[93m"
COLOR_BRIGHT_BLUE = "\033[94m"
COLOR_BRIGHT_MAGENTA = "\033[95m"
COLOR_BRIGHT_CYAN = "\033[96m"
COLOR_BRIGHT_WHITE = "\033[97m"
COLOR_BLACK = "\033[30m"
COLOR_BRIGHT_BLACK = "\033[90m"
COLOR_RESET = "\033[0m"

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


class ToDo():

    state:bool
    title:str
    description:str
    created_at:datetime
    planned_at:Optional[datetime]

    def __init__(self, title:str="New Task", description:str="", planned_at: Optional[datetime] = None):
        self.state = False
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.planned_at = planned_at
    
    def __str__(self):
        status = "[X]" if self.state else "[ ]"
        date = self.planned_at.strftime(" - Deadline: `%Y-%m-%d`") if self.planned_at else ""
        cdate = self.created_at.strftime(" - Created: `%Y-%m-%d`")
        desc = ""
        lines = self.description.splitlines()
        if len(lines) > 0:
            desc += "\n        ```"
            for line in self.description.splitlines():
                desc += f"\n        {line}"
            desc += "\n        ```"
        return f"- {status} {self.title}{date}{cdate}{desc}"
    
    @staticmethod
    def From_str(task_str: str):
        match = re.match(TODO_RE_PATTERN, task_str.strip())
        if match:
            state = match.group(1).upper() == "X"
            title = match.group(2)
            planned_at_str = match.group(4)
            planned_at = datetime.strptime(planned_at_str, "%Y-%m-%d") if planned_at_str else None
            created_at_str = match.group(6)
            created_at = datetime.strptime(created_at_str, "%Y-%m-%d")
            description = match.group(7)
            desc = ""
            if description is None:
                description = ""
            else:
                lines = description.splitlines()[:-1]
                for line in lines:
                    if line[:8] == "        ":
                        line = line[8:]
                    else:
                        line = line.strip()
                    desc += f"\n{line}"
            task = ToDo(title=title, description=desc, planned_at=planned_at)
            task.state = state
            task.created_at = created_at
            return task
        raise ValueError("String does not match the expected format for a ToDo task:\n\n" + task_str)

    def print_min(self, prefix:str = "", suffix:str = "", padw:int=0, width:int = HL_SIZE, color:str=None):
        check = current_char_set[0]
        state = f"[{check}]" if self.state else "[ ]"
        line = f"{state} {self.title}"
        if len(line) > width - len(prefix) - len(suffix):
            line = line[:width - len(prefix) - len(suffix) - 3] + "..."
        if len(line) < padw:
            line = line.ljust(padw)
        line = f"{prefix}{line}{suffix}"
        center(line, width, color=color)
    
    def print_full(self):
        hl()
        check = current_char_set[0]
        state = f"[{check}]" if self.state else "[ ]"
        line = f"{state} {self.title}"
        center(line)
        hl()
        if self.planned_at:
            planned_str = self.planned_at.strftime(" - Deadline: `%Y-%m-%d`")
            print(planned_str)
        created_str = self.created_at.strftime(" - Created: `%Y-%m-%d`")
        print(created_str)
        if self.description:
            hl()
            center("Description:")
            lines = self.description.splitlines()
            for line in lines:
                print(f"  {line}")
        hl()


class ToDoList():

    tasks = []

    def __init__(self):
        self.tasks = []
    
    def add_task(self, task: ToDo):
        if not isinstance(task, ToDo):
            raise TypeError("task must be an instance of ToDo")
        self.tasks.append(task)
        return task
    
    def remove_task(self, task: ToDo):
        if not isinstance(task, ToDo):
            raise TypeError("task must be an instance of ToDo")
        if task in self.tasks:
            self.tasks.remove(task)
            return task
        raise ValueError("Task not found in the list.")
    
    def save(self, filename: str):
        with open(filename, "w+", encoding="utf-8") as f:
            # markdown yaml header
            print("---", file=f)
            print("Last updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file=f)
            print(f"Last updated by: {os.getlogin()}", file=f)
            print("Date format: `YYYY-MM-DD`", file=f)
            print("---", file=f)
            print("", file=f)
            # write tasks
            print("# ToDo List:", file=f)
            print("", file=f)
            for task in self.tasks:
                print(task, file=f)

    def load(self, filename: str):
        if os.path.exists(filename):
            self.tasks = []
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.finditer(TODO_RE_PATTERN, content, re.MULTILINE)
                for match in matches:
                    print(match)
                    mstr = match.group(0)
                    task = ToDo.From_str(mstr)
                    self.add_task(task)
    
    def get_todays_tasks(self):
        today = datetime.now().date()
        return [task for task in self.tasks if task.planned_at and task.planned_at.date() <= today]
    
    def get_upcoming_tasks(self):
        todays_tasks = self.get_todays_tasks()
        return [task for task in self.tasks if task not in todays_tasks]
    
    def find_task(self, search:str) -> list[ToDo]:
        search = search.lower().strip()
        found_tasks = []
        for task in self.tasks:
            if search in task.title.lower():
                found_tasks.append(task)
        return found_tasks


class ToDoApp:

    todo_list: ToDoList
    filename: str
    selected_task_index: int

    def __init__(self, filename: str):
        self.todo_list = ToDoList()
        self.filename = filename
        self.selected_task_index = 0
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

    def _main_menu(self) -> bool:
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
        cls()
        hl(max_w)
        center("TODOS:", max_w, color=COLOR_BOLD + COLOR_BRIGHT_MAGENTA + COLOR_UNDERLINE)
        hl(max_w)
        if todays_len > 0:
            center("Today:", max_w, color=COLOR_CYAN)
            for i, task in enumerate(todays_tasks):
                prefix = "     " if i != self.selected_task_index else (" " + larr + larr + larr + " ")
                suffix = "     " if i != self.selected_task_index else (" " + rarr + rarr + rarr + " ")
                color = COLOR_BRIGHT_YELLOW if i == self.selected_task_index else None
                task.print_min(prefix, suffix, inner_w, max_w, color=color)
            hl(max_w)
        if future_len > 0:
            center("Upcoming:", max_w, color=COLOR_CYAN)
            for i, task in enumerate(future_tasks):
                i += todays_len
                prefix = "     " if i != self.selected_task_index else (" " + larr + larr + larr + " ")
                suffix = "     " if i != self.selected_task_index else (" " + rarr + rarr + rarr + " ")
                color = COLOR_BRIGHT_YELLOW if i == self.selected_task_index else None
                task.print_min(prefix, suffix, inner_w, max_w, color=color)
            hl(max_w)
        self._print_help_min(max_w)

        cmd = input(": ").strip() + " "
        cmds = cmd[0].lower()
        cmd = cmd.strip()

        if cmds == "+":
            new_task_title = cmd[1:].strip() if len(cmd) > 1 else ""
            if len(new_task_title) <= 0:
                new_task_title = "New Task"
            new_task = ToDo(title=new_task_title)
            self._edit_task(new_task)
            self.todo_list.add_task(new_task)
            self.todo_list.save(self.filename)

        elif cmds == "-":
            if len(cmd) > 1:
                search = cmd[1:].strip()
                found_tasks = self.todo_list.find_task(search)
                if len(found_tasks) > 0:
                    tasks = found_tasks
            else:
                tasks = [all_tasks[self.selected_task_index]]
            if self._confirm_deletion(tasks):
                for task in tasks:
                    self.todo_list.remove_task(task)
                self.todo_list.save(self.filename)

        elif cmds == "d":
            if len(cmd) > 1:
                search = cmd[1:].strip()
                found_tasks = self.todo_list.find_task(search)
                if len(found_tasks) > 0:
                    task = found_tasks[0]
            else:
                task = all_tasks[self.selected_task_index]
            cls()
            task.print_full()
            input("Press Enter to return to the main menu...")

        elif cmds == "e":
            if len(cmd) > 1:
                search = cmd[1:].strip()
                found_tasks = self.todo_list.find_task(search)
                if len(found_tasks) > 0:
                    task = found_tasks[0]
            else:
                task = all_tasks[self.selected_task_index]
            self._edit_task(task)
            self.todo_list.save(self.filename)

        elif cmds == "q" or cmd == "^X":
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
                    task.state = not task.state
                    self.todo_list.save(self.filename)
        
        else:
            for c in cmd.lower():
                if c == "p":
                    self.selected_task_index -= 1
                    if self.selected_task_index < 0:
                        self.selected_task_index = len(all_tasks) - 1
                elif c == "n":
                    self.selected_task_index += 1
                    if self.selected_task_index >= len(all_tasks):
                        self.selected_task_index = 0
                elif c == "t":
                    task = all_tasks[self.selected_task_index]
                    task.state = not task.state
                    self.todo_list.save(self.filename)

        return True

    def run(self):
        while self._main_menu():
            pass


def cli_help():
    print("Usage: python main.py [options] [filename]")
    print("Options:")
    print("  -h, --help, /?, ?, -?    Show this help message")
    print("  -a, --ascii              Use ASCII character set for the UI")
    print("  -d, --demo               Add demo tasks to the ToDo list")
    print("  -nc, --no-colors         Disable colored output")
    print("  filename                 The file to load/save the ToDo list (default: ~/todos.md)")
    print("")
    print("Example:")
    print("  python main.py --ascii --demo my-todos.md")
    print("")


def main(args:list[str]) -> int:
    filename = ""
    add_demo_tasks = False
    for arg in args:
        if arg.lower() == "--ascii" or arg.lower() == "-a":
            global current_char_set
            current_char_set = ASCII_CHAR_SET
        elif arg.lower() == "--demo" or arg.lower() == "-d":
            add_demo_tasks = True
        elif arg.lower() == "--no-colors" or arg.lower() == "-nc":
            global no_colors
            no_colors = True
        elif arg.lower() == "--help" or arg.lower() == "-h" or arg.lower() == "/?" or arg.lower() == "?" or arg.lower() == "-?":
            cli_help()
            return 0
        elif os.path.exists(arg):
            if len(filename) > 0:
                print("Error: Only one filename can be specified.")
                return 1
            else:
                filename = arg
    if len(filename) <= 0:
        home_dir = os.path.expanduser("~")
        filename = os.path.join(home_dir, DEFAULT_FILENAME)
    app = ToDoApp(filename)

    if add_demo_tasks:
        demotask1 = ToDo("D Task 1", "This is a demo\ntask description.", datetime(2026, 10, 15))
        demotask2 = ToDo("De Task 2", "This is another demo\ntask description.", datetime(2026, 10, 20))
        demotask3 = ToDo("Dem Task 3", "This is yet another\ndemo task description.", datetime(2026, 10, 25))
        demotask4 = ToDo("Demo Task 4", "This is a fourth demo\ntask description.", datetime(2026, 10, 30))
        demotask5 = ToDo("Demo Task 5.", "This is a fifth demo\ntask description.", datetime.now())
        demotask6 = ToDo("Demo Task 6..", "This is a sixth demo\ntask description.", datetime.now())
        demotask7 = ToDo("Demo Task 7...", "This is a seventh demo\ntask description.")
        demotask8 = ToDo("Demo Task 8....", "This is an eighth\ndemo task description.")
        
        app.todo_list.add_task(demotask1)
        app.todo_list.add_task(demotask2)
        app.todo_list.add_task(demotask3)
        app.todo_list.add_task(demotask4)
        app.todo_list.add_task(demotask5)
        app.todo_list.add_task(demotask6)
        app.todo_list.add_task(demotask7)
        app.todo_list.add_task(demotask8)
        
        #app.todo_list.save(filename)

    app.run()
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)