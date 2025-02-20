from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
import os

""" Simple flask application to create to-do tasks with due dates and mark as completed/delete/edit them"""

app = Flask(__name__)
app.secret_key = 'my_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

@app.route('/')
def home():
    filter = request.args.get('filter', None)

    if filter == 'completed':
        tasks = Task.query.filter_by(completed=True).all()
    elif filter == 'incomplete':
        tasks = Task.query.filter_by(completed=False).all()
    elif filter == 'date':
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    else:
        tasks = Task.query.all()

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('task')
    new_task = Task(title=title)

    db.session.add(new_task)
    db.session.commit()

    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True

    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
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

        return redirect('/')

    return render_template('edit_task.html', task=task)

@app.route('/clear', methods=['POST'])
def clear_tasks():
    db.session.query(Task).delete()
    db.session.commit()
    return redirect('/')
    
if __name__  == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)