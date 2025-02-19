from flask import Flask, request, redirect, render_template, flash
import sqlite3

""" Simple flask application to create to-do tasks with due dates and mark as completed/delete/edit them"""

app = Flask(__name__)
app.secret_key = "secret_key"

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER NOT NULL DEFAULT 0
            )
            ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = 'SELECT * FROM tasks'
    cursor.execute(sql)
    tasks = cursor.fetchall()

    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    due_date = request.form.get('date') 

    if task:  
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = 'INSERT INTO tasks (title, due_date) VALUES (?, ?)'
        cursor.execute(sql, (task,due_date,)) 
        
        conn.commit()
        conn.close()

        flash('Task added successfully', 'success')
    else:
        flash('Task description cannot be empty.', 'error')

    return redirect('/')

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = 'UPDATE tasks SET completed = 1 WHERE id = ?'
    cursor.execute(sql, (task_id,))
    
    conn.commit()
    conn.close()

    flash('Task marked as completed', 'success')

    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = 'DELETE FROM tasks WHERE id = ?'
    cursor.execute(sql, (task_id,))
    
    conn.commit()
    conn.close()

    flash('Task deleted', 'success')

    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):

    new_title = request.form.get('task_edit')
    new_date = request.form.get('date_edit') 

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = 'UPDATE tasks SET title = ?, due_date = ? WHERE id = ?'
    cursor.execute(sql, (new_title,new_date,task_id,))
    
    conn.commit()
    conn.close()

    flash('Task edited successfully', 'success')

    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tasks')
    
    conn.commit()
    conn.close()

    flash('Task list cleared', 'success')

    return redirect('/')

if __name__ == '__main__':
    app.run()
