# ToDo Application

![Screenshot](screenshot.png)

A simple command-line ToDo application to manage your tasks efficiently.

## Features
- Add, edit, and toggle tasks.
- Save and load tasks from a file.
- CLI options for ASCII UI, demo tasks, and disabling colors.
- View tasks in a calendar format with navigation options.
- Advanced commands for filtering tasks by date and opening the calendar view.
- Generate demo tasks for testing purposes.
- Advanced commands can now also be passed as CLI arguments, such as `/calendar` or `/YYYY-MM-DD`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/derDere/todos
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Quick Install

To quickly install the ToDo application, run the following command:

### Ubuntu
```bash
curl -s https://raw.githubusercontent.com/derDere/todos/main/install.sh | bash
```

### Windows
```powershell
powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/derDere/todos/main/install.ps1' -OutFile 'install.ps1'; & .\install.ps1}" 
```

This will install the application to `AppData\Local\derDere\todos` and create a `todos` command available system-wide.

## Usage
Run the application with the following options:
- `-h, --help`: Show help message.
- `-a, --ascii`: Use ASCII character set for the UI.
- `-d, --demo`: Add demo tasks to the ToDo list.
- `-nc, --no-colors`: Disable colored output.
- `filename`: Specify the file to load/save the ToDo list (default: `~/todo.yaml`).

### Advanced Commands
- `/calendar`: Open the calendar view.
- `/YYYY-MM-DD`: Filter tasks by a specific date.
- `/default`: Reset to the default view.

### Calendar Navigation
- `t`: Go to today's date.
- `p`: Previous month.
- `n`: Next month.
- `YYYY-MM-DD`: Go to a specific date.

Example:
```bash
python main.py --ascii --demo my-todos.yaml
python main.py /calendar
python main.py /2025-06-16
```

## License
This project is licensed under the [GNU GPLv3 License](LICENSE).
