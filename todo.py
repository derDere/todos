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
            desc = []
            if description is None:
                description = ""
            else:
                lines = description.splitlines()[:-1]
                for line in lines:
                    if line[:8] == "        ":
                        line = line[8:]
                    else:
                        line = line.strip()
                    if len(line) > 0:
                        desc.append(line)
            desc = "\n".join(desc).strip()
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
    
    def selectable_fields(self) -> list[str]:
        return ["title", "planned", "created", "description"]
    
    def print_full(self, selection:str=""):
        larr = current_char_set[2]
        larr = larr + larr + larr + " "
        rarr = current_char_set[3]
        rarr = " " + rarr + rarr + rarr
        hl()
        check = current_char_set[0]
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
                planned_str = f"{COLOR_BRIGHT_GREEN}{planned_str}{rarr}{COLOR_RESET}"
            print(planned_str)
        created_str = self.created_at.strftime(" - Created: `%Y-%m-%d`")
        if selection == "created":
            created_str = f"{COLOR_BRIGHT_GREEN}{created_str}{rarr}{COLOR_RESET}"
        print(created_str)
        if self.description:
            hl()
            center("Description:", color=COLOR_BRIGHT_CYAN)
            lines = self.description.splitlines()
            midIndex = len(lines) // 2
            for i, line in enumerate(lines):
                if selection == "description":
                    if i == midIndex:
                        line = f"{larr}{line}"
                    else:
                        line = f"    {line}"
                    line = f"{COLOR_BRIGHT_GREEN}{line}{COLOR_RESET}"
                else:
                    line = f"    {line}"
                print(line)
        hl()