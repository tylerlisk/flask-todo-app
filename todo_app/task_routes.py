from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from .models import db, Task

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    filter = request.args.get('filter', None)

    if filter == 'completed':
        tasks = current_user.tasks.filter_by(user_id=current_user.id, completed=True).all()
    elif filter == 'incomplete':
        tasks = current_user.tasks.filter_by(completed=False).all()
    elif filter == 'date':
        tasks = current_user.tasks.order_by(Task.created_at.desc()).all()
    else:
        tasks = current_user.tasks

    return render_template('index.html', tasks=tasks)

@main.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('task')
    new_task = Task(user_id=current_user.id, title=title)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("main.home"))

@main.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for(".home"))

@main.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True

    db.session.commit()
    return redirect(url_for(".home"))

@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)

    if request.method == 'POST':
        new_title = request.form.get('new_title')
        if new_title != task.title:
            task.title = new_title
            db.session.commit()
            flash('Task edited successfully', 'success')
        else:
            flash('Title was not changed', 'info')

        return redirect(url_for(".home"))

    return render_template('edit_task.html', task=task)

@main.route('/clear', methods=['POST'])
@login_required
def clear_tasks():
    db.session.query(Task).delete()
    db.session.commit()
    return redirect(url_for(".home"))
