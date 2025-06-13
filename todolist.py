from datetime import datetime
import os
import yaml


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
        # Prepare data for YAML
        data = {
            "ToDos": {
                "author": os.getlogin(),
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "changed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tasks": {}
            }
        }
        
        # Convert tasks to dictionary format with title as the key
        for task in self.tasks:
            # Use dict(task) and store with title as key
            data["ToDos"]["tasks"][task.title] = dict(task)
        
        # Write to YAML file
        with open(filename, "w+", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
    def load(self, filename: str):
        if os.path.exists(filename):
            self.tasks = []
            with open(filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                
                # Only process tasks from the new YAML format with title keys
                if data and "ToDos" in data and "tasks" in data["ToDos"]:
                    task_dict = data["ToDos"]["tasks"]
                    for title, task_data in task_dict.items():
                        # Use the From_dict method
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
    
    def find_task(self, search:str) -> list[ToDo]:
        search = search.lower().strip()
        found_tasks = []
        for task in self.tasks:
            if search in task.title.lower():
                found_tasks.append(task)
        return found_tasks