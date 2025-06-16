from datetime import datetime
import os
import yaml
from yaml.resolver import BaseResolver
import getpass

from consts import *
from todo import *


def represent_literal(dumper, data):
  return dumper.represent_scalar(BaseResolver.DEFAULT_SCALAR_TAG,
      data, style="|")
yaml.add_representer(AsLiteral, represent_literal)


class ToDoList():

    tasks:list[ToDo]
    creation_date:datetime
    created_by:str

    def __init__(self):
        self.tasks = []
        self.creation_date = datetime.now()
        self.created_by = getpass.getuser()
    
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
        data = {
            "ToDos": {
                "created_by": self.created_by,
                "changed_by": getpass.getuser(),
                "created_date": self.creation_date,
                "changed_date": datetime.now(),
                "tasks": {}
            }
        }
        for task in self.tasks:
            data["ToDos"]["tasks"][task.title] = task.to_dict()

        # Convert OrderedDict to a standard dict before dumping to YAML
        with open(filename, "w+", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def load(self, filename: str):
        if os.path.exists(filename):
            self.tasks = []
            with open(filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

                if data and "ToDos" in data and "tasks" in data["ToDos"]:
                    if "created_date" in data["ToDos"]:
                        self.creation_date = data["ToDos"]["created_date"]

                    if "created_by" in data["ToDos"]:
                        self.created_by = data["ToDos"]["created_by"]

                    task_dict = data["ToDos"]["tasks"]
                    for title, task_data in task_dict.items():
                        task = ToDo.From_dict(title, task_data)
                        self.add_task(task)
                else:
                    raise ValueError(f"File {filename} is not in the expected YAML format")
    
    def get_todays_tasks(self):
        today = datetime.now().date()
        return [task for task in self.tasks if task.planned_at and task.planned_at.date() <= today]
    
    def get_upcoming_tasks(self):
        todays_tasks = self.get_todays_tasks()
        return [task for task in self.tasks if task not in todays_tasks]
    
    def get_tasks_for_date(self, date: datetime) -> list[ToDo]:
        return [task for task in self.tasks if task.planned_at and task.planned_at.date() == date.date()]
    
    def find_task(self, search:str, all_tasks:list[ToDo]) -> list[ToDo]:
        search = search.lower().strip()
        found_tasks = []
        for task in all_tasks:
            if search in task.title.lower():
                found_tasks.append(task)
        return found_tasks