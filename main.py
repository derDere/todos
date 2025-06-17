from datetime import datetime
import os


from consts import *
from todo import *
from todolist import *
from todoapp import *


def cli_help():
    print("Usage: python main.py [options] [filename]")
    print("Options:")
    print("  -h, --help, ?, -?    Show this help message")
    print("  -a, --ascii              Use ASCII character set for the UI")
    print("  -d, --demo               Add demo tasks to the ToDo list")
    print("  -nc, --no-colors         Disable colored output")
    print("  /<advcmd>                execute an advanced command (e.g., /calendar)")
    print(f"  filename                 The file to load/save the ToDo list (default: ~/{DEFAULT_FILENAME})")
    print("")
    print("  --uninstall              Uninstall the ToDo app")
    print("")
    print("Example:")
    print("  python main.py --ascii --demo my-todos.md")
    print("")


def main(args:list[str]) -> int:
    filename = ""
    add_demo_tasks = False
    start_commands = []
    for arg in args:
        if arg.lower() == "--ascii" or arg.lower() == "-a":
            turn_on_ascii()
        elif arg.lower() == "--demo" or arg.lower() == "-d":
            add_demo_tasks = True
        elif arg.lower() == "--no-colors" or arg.lower() == "-nc":
            turn_off_colors()
        elif arg.lower() == "--help" or arg.lower() == "-h" or arg.lower() == "?" or arg.lower() == "-?":
            cli_help()
            return 0
        elif arg.startswith("/") and arg[1:].count("/") == 0:
            start_commands.append(arg.strip().lower())
        elif os.path.isabs(arg) or os.path.dirname(arg):  # Check if it's a valid file path
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

        for n in range(9, 30):
            demotask = ToDo(f"Demo Task {n}", f"This is a demo task description for task {n}.", datetime.now())
            app.todo_list.add_task(demotask)

        for n in range(30, 60):
            demotask = ToDo(f"Demo Task {n}", f"This is a demo task description for task {n}.", datetime(2026, 10, 15))
            app.todo_list.add_task(demotask)

    app.run(start_commands)
    return 0


if __name__ == "__main__":
    input("TEST...")
    import sys
    sys.exit(main(sys.argv[1:]))