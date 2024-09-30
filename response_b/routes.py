# routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db, socketio
from database import Task

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        if not title:
            flash('Title is required!')
            return redirect(url_for('index'))
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        socketio.emit('task_added', {'id': new_task.id, 'title': new_task.title}, broadcast=True)
        return jsonify({'result': 'Task added successfully'}), 200

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.completed = 'completed' in request.form
    db.session.commit()
    socketio.emit('task_updated', {'id': task.id, 'title': task.title, 'completed': task.completed}, broadcast=True)
    return jsonify({'result': 'Task updated successfully'}), 200

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_deleted', {'id': task.id}, broadcast=True)
    return jsonify({'result': 'Task deleted successfully'}), 200