from flask import Blueprint, render_template, url_for, flash, redirect
from .forms import NoteForm, TaskForm
from flask_login import login_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/")
def home():
    return render_template("home.html")

@tasks_bp.route("/create-note", methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    
    if form.validate_on_submit():
        flash("Note created!", 'success')
        return redirect(url_for('tasks.home'))

    return render_template("create_note.html", form=form)
