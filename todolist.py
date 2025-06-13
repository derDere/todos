from datetime import datetime
import os
import yaml
import re


from consts import *
from todo import *


# Custom YAML Dumper that formats the output as desired
class CustomDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)
    
    # Override to add line breaks between tasks
    def write_line_break(self, data=None):
        super().write_line_break(data)
        
        # Add extra line breaks for better readability
        if self.column == 0 and self.line > 1:
            # Find current indentation level
            indent_level = 0
            for event in self.events:
                if event.event_type == yaml.MappingStartEvent.yaml_tag:
                    indent_level += 1
                elif event.event_type == yaml.MappingEndEvent.yaml_tag:
                    indent_level -= 1
            
            # Add extra newline when we're at the right indent level
            if indent_level == 2:  # Inside tasks
                super().write_line_break()

# Custom string representer that removes quotes from dates
def date_representer(dumper, data):
    if isinstance(data, str):
        # If this is a date or datetime string
        if re.match(r'^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$', data):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')
        # If this is the "Details" field, use pipe style
        elif len(data) > 20 or '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_str(data)

# Register the custom representer
CustomDumper.add_representer(str, date_representer)


class ToDoList():

    tasks:list[ToDo]
    creation_date:datetime
    created_by:str

    def __init__(self):
        self.tasks = []
        self.creation_date = datetime.now()
        self.created_by = os.getlogin()
    
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
                "changed_by": os.getlogin(),
                "created_date": self.creation_date.strftime("%Y-%m-%d"),
                "changed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tasks": {}
            }
        }
        for task in self.tasks:
            data["ToDos"]["tasks"][task.title] = dict(task)
        
        with open(filename, "w+", encoding="utf-8") as f:
            yaml.dump(data, f, Dumper=CustomDumper, default_flow_style=False, 
                      sort_keys=False, width=70, explicit_start=True, 
                      allow_unicode=True, indent=2)
    
    def load(self, filename: str):
        if os.path.exists(filename):
            self.tasks = []
            with open(filename, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                
                if data and "ToDos" in data and "tasks" in data["ToDos"]:
                    if "created_date" in data["ToDos"]:
                        created_date_str = data["ToDos"]["created_date"]
                        self.creation_date = datetime.strptime(created_date_str, "%Y-%m-%d")
                    
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
    
    def find_task(self, search:str) -> list[ToDo]:
        search = search.lower().strip()
        found_tasks = []
        for task in self.tasks:
            if search in task.title.lower():
                found_tasks.append(task)
        return found_tasks