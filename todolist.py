from datetime import datetime


from consts import *
from todo import *


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