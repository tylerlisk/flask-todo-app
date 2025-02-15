from flask import Flask, render_template, request, redirect, flash

""" Simple flask application to create to-do tasks with due dates and mark as completed/delete them"""

app = Flask(__name__)
app.secret_key = "secret_key"

tasks = []

@app.route('/')
def home():
    return render_template('index.html', tasks=tasks, enumerate=enumerate)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    due_date = request.form.get('date')
    if task and due_date:
        tasks.append({"task": task, "dueDate": due_date , "completed": False})
        flash('Task added successfully', 'success')
    else:
        flash('Tasks must have a description and a due date.', 'error')
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if task_id < len(tasks):
        tasks.pop(task_id)
        flash('Task deleted successfully', 'success')
    return redirect('/')

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if task_id < len(tasks):
        tasks[task_id]["completed"] = True
        flash('Task marked as completed', 'success')
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_tasks():
    tasks.clear()
    flash('Task list has been cleared', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)