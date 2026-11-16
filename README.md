# Northstar To-Do App

## What this project does

Northstar To-Do is a small web app for keeping a straightforward list of
upcoming work. From one page, you can enter a task name, choose its priority
and category, and set a due date. The app checks each entry, then displays
valid tasks in a table ordered by due date so the nearest deadlines appear
first. You can remove a task from its row when it is no longer needed.

The app is intended as a simple personal or demonstration project, not a
persistent multi-user task service. Tasks are kept in memory while the Flask
process is running; they are not saved to a database or retained after the
process restarts. Anyone using the same running app sees the same task list.

## Features

- Add a task with four required fields:
  - **Task name:** up to 200 characters.
  - **Priority:** High, Medium, or Low.
  - **Category:** Work, Personal, or Health.
  - **Due date:** selected with a date picker.
- View tasks in a due-date-sorted table and delete individual tasks.
- Receive validation messages for missing or invalid values.
- Use a responsive interface with CSS included in the HTML template.

Tasks are dictionaries with the keys `task`, `priority`, `category`, and
`due_date`, stored in an in-memory Python list. There is no database or
per-user storage: all visitors to the same application process share the list,
and tasks are lost when that process stops or reloads.

## Requirements

- Python 3.9 or newer.
- Python's `venv` module and pip.

The dependencies are listed in [requirements.txt](./requirements.txt):
Flask runs the web application, and pytest is available for testing.

## Setup

Open a terminal in the project folder.

### Linux or macOS

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `.venv` already exists, skip creation and activate it using the appropriate
command above.

### Install dependencies

With the virtual environment active, run:

```bash
python -m pip install -r requirements.txt
```

On Debian or Ubuntu, if virtual environment creation fails because `venv` or
`ensurepip` is unavailable, install the system package and retry:

```bash
sudo apt install python3-venv
```

## Run the app

From the project folder, with the virtual environment active:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
Complete all four fields and select **Add task**. Use **Delete** on a table row
to remove that task.

Press `Ctrl+C` in the terminal to stop the server. Run `deactivate` when you are
finished using the virtual environment.

**Development only:** running [app.py](./app.py) directly enables Flask's debug
mode and automatic reloader. Code changes can reload the process and clear all
tasks. Do not expose the debug server publicly or use it for production.

## Run tests

With the virtual environment active:

```bash
python -m unittest -v test
```

The tests cover required fields, validation, task dictionary keys, due-date
sorting, deletion, and HTML escaping. They use Flask's test client and do not
start a server.

## Project files

- [app.py](./app.py): Flask routes, validation, and in-memory task storage.
- [templates/index.html](./templates/index.html): page template, form, table,
  and inline CSS.
- [requirements.txt](./requirements.txt): Python dependencies.
- [test.py](./test.py): automated regression tests.
