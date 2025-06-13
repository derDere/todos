from datetime import datetime
from typing import Optional
import re


from consts import *
from tools import *


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
    
    def toggle(self) -> None:
        """Toggle the state of the task."""
        self.state = not self.state
    
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