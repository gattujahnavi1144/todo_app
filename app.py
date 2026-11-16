"""Flask application for managing a simple, in-memory to-do list."""

from datetime import date

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
PRIORITIES = ("High", "Medium", "Low")
CATEGORIES = ("Work", "Personal", "Health")


@app.route("/", methods=["GET", "POST"])
def index():
    """Display tasks and process task additions or deletions.

    Returns:
        A redirect after a successful action, or the rendered task page and
        its HTTP status code.
    """
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            task = {
                key: request.form.get(key, "").strip()
                for key in ("task", "priority", "category", "due_date")
            }
            if not task["task"]:
                error = "Enter a task name."
            elif len(task["task"]) > 200:
                error = "Task names must be 200 characters or fewer."
            elif task["priority"] not in PRIORITIES:
                error = "Choose a priority: High, Medium, or Low."
            elif task["category"] not in CATEGORIES:
                error = "Choose a category: Work, Personal, or Health."
            else:
                try:
                    task["due_date"] = date.fromisoformat(task["due_date"]).isoformat()
                except ValueError:
                    error = "Choose a valid due date."

            if error is None:
                tasks.append(task)
                # ISO-formatted dates sort chronologically as strings.
                tasks.sort(key=lambda item: item["due_date"])
                return redirect(url_for("index"))
        elif action == "delete":
            task_index = request.form.get("task_index", type=int)
            if task_index is not None and 0 <= task_index < len(tasks):
                tasks.pop(task_index)
                return redirect(url_for("index"))
            error = "Task not found. Refresh the page and try again."
        else:
            error = "Invalid task action."

    return render_template(
        "index.html",
        tasks=tasks,
        error=error,
        priorities=PRIORITIES,
        categories=CATEGORIES,
        form_values=request.form if request.form.get("action") == "add" else {},
    ), 400 if error else 200


def count_tasks_by_priority(tasks, priority): 
    count = 0 
    for task in tasks: 
        if task['priority'] == priority: 
            count += 1 
    return count 
    
if __name__ == "__main__":
    app.run(debug=True)
