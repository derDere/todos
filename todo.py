from datetime import datetime
from typing import Optional

from consts import *
from tools import *


class AsLiteral(str):
  pass


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
    
    def toggle(self) -> None:
        """Toggle the state of the task."""
        self.state = not self.state

    def to_dict(self) -> dict:
        """Convert ToDo object to a dictionary for YAML serialization."""
        task_dict = {}
        task_dict["state"] = self.state
        task_dict["created"] = self.created_at
        if self.planned_at is not None:
            task_dict["planned"] = self.planned_at
        if self.description:
            task_dict["details"] = AsLiteral(self.description)
        return task_dict
    
    @staticmethod
    def From_dict(title: str, task_dict: dict) -> 'ToDo':
        """Create a ToDo object from a dictionary."""
        task = ToDo(
            title=title,
            description=task_dict.get("details", ""),
            planned_at=task_dict.get("planned")
        )
        task.state = task_dict["state"]
        task.created_at = task_dict["created"]
        return task

    def print_min(self, prefix:str = "", suffix:str = "", padw:int=0, width:int = HL_SIZE, color:str=None, index:int|None = None, max_index:int|None = None):
        check = style(0)
        state = f"[{check}]" if self.state else "[ ]"
        index_str = ""
        if index is not None and max_index is not None:
            index_str = f"{index:>{len(str(max_index))}}: "
        line = f"{index_str}{state} {self.title}"
        if len(line) > width - len(prefix) - len(suffix):
            line = line[:width - len(prefix) - len(suffix) - 3] + "..."
        if len(line) < padw:
            line = line.ljust(padw)
        line = f"{prefix}{line}{suffix}"
        center(line, width, color=color)
    
    def selectable_fields(self) -> list[str]:
        return ["title", "planned", "created", "description"]
    
    def print_full(self, selection:str=""):
        larr = style(2)
        larr = larr + larr + larr + " "
        rarr = style(3)
        rarr = " " + rarr + rarr + rarr
        hl()
        check = style(0)
        state = f"[{check}]" if self.state else "[ ]"
        line = f"{state} {self.title}"
        title_color = COLOR_BRIGHT_MAGENTA
        if selection == "title":
            title_color = COLOR_BRIGHT_GREEN
            line = f"{larr}{line}{rarr}"
        center(line, color=title_color)
        hl()
        if self.planned_at or len(selection) > 0:
            if not self.planned_at:
                planned_str = " - Deadline: `None`"
            else:
                planned_str = self.planned_at.strftime(" - Deadline: `%Y-%m-%d`")
            if selection == "planned":
                planned_str = colorize(f"{planned_str}{rarr}", COLOR_BRIGHT_GREEN)
            print(planned_str)
        created_str = self.created_at.strftime(" - Created: `%Y-%m-%d`")
        if selection == "created":
            created_str = colorize(f"{created_str}{rarr}", COLOR_BRIGHT_GREEN)
        print(created_str)
        if self.description or len(selection) > 0:
            hl()
            description_color = COLOR_BRIGHT_CYAN
            if selection == "description":
                description_color = COLOR_BRIGHT_GREEN
            center("Description:", color=description_color)
            lines = self.description.splitlines()
            if len(lines) <= 0 and len(selection) > 0:
                lines = [colorize("EMPTY", COLOR_BRIGHT_BLACK)]
            midIndex = (len(lines) // 2) - 1
            if midIndex < 0:
                midIndex = 0
            for i, line in enumerate(lines):
                if selection == "description":
                    if i == midIndex:
                        line = f"{larr}{line}"
                    else:
                        line = f"    {line}"
                    line = colorize(line, COLOR_BRIGHT_GREEN)
                else:
                    line = f"    {line}"
                print(line)
        hl()