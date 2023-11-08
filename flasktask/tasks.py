from flask import Blueprint, render_template, url_for

tasks_bp = Blueprint('tasks', __name__)

tasks = [
    {
        "task_name": "Water plant",
        "done": True,
        "date_posted": "Nov 3 2023"
    },

    {
        "task_name": "Make Python website",
        "done": False,
        "date_posted": "Oct 31 2023"
    }
]

@tasks_bp.route("/")
def tasks_page():
    return render_template("tasks.html", tasks=tasks)
