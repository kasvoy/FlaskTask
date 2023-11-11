from flask import Blueprint, render_template, url_for, flash, redirect
from sqlalchemy.sql import func
from .forms import NoteForm, TaskForm
from flask_login import login_required, current_user
from .models import User, Note, Task, db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/")
def home():

    notes=None
    yet_done_tasks=None
    done_tasks=None

    if current_user.is_authenticated:
        stmt_notes = db.select(Note).where(Note.user_id==current_user.id).order_by(Note.created_on.desc())
        stmt_yet_done_tasks = db.select(Task).where(Task.user_id==current_user.id, Task.is_done==False).order_by(Task.created_on.desc())
        stmt_done_tasks     = db.select(Task).where(Task.user_id==current_user.id, Task.is_done==True).order_by(Task.created_on.desc())
        
        notes = db.session.scalars(stmt_notes).all()
        yet_done_tasks = db.session.scalars(stmt_yet_done_tasks).all()
        done_tasks     = db.session.scalars(stmt_done_tasks).all()


    return render_template("home.html", notes=notes, yet_done_tasks=yet_done_tasks, done_tasks=done_tasks)

       
@tasks_bp.route("/note/new", methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    
    if form.validate_on_submit():
        note = Note(title=form.title.data,
                    content=form.content.data,
                    created_on=func.now(), 
                    user_id=current_user.id)

        print(len(form.content.data))
        db.session.add(note)
        db.session.commit()

        flash("Note created!", 'success')
        return redirect(url_for('tasks.home'))

    return render_template("notes/create_note.html", form=form)


@tasks_bp.route("/task/new", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    
    if form.validate_on_submit():
        task = Task(todo=form.todo.data, 
                    created_on=func.now(),
                    due_by=form.due_by.data, 
                    is_done=False,
                    user_id=current_user.id)
    
    
        db.session.add(task)
        db.session.commit()

        flash("Task created!", 'success')
        return redirect(url_for('tasks.home'))

    return render_template("tasks/create_task.html", form=form)


@tasks_bp.route("/note/<note_id>")
def note_by_id(note_id):
    note = db.session.get(Note, note_id)

    return render_template("notes/note_id.html", note=note)


@tasks_bp.route("/task/<task_id>")
def task_by_id(task_id):
    task = db.session.get(Task, task_id)

    return render_template("tasks/task_id.html", task=task)


@tasks_bp.route("/task/<task_id>/switch_done")
def switch_done(task_id):
    task = db.session.get(Task, task_id)

    updated_task_done_state = not task.is_done
    stmt = db.update(Task).where(Task.id==task_id).values(is_done=updated_task_done_state)

    db.session.execute(stmt)
    db.session.commit()

    print(updated_task_done_state)
    

    return redirect(url_for('tasks.home'))

@tasks_bp.route("/task/<task_id>/delete")
def delete_task(task_id):
    return redirect(url_for('tasks.home'))