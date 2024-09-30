from flask import request, jsonify, render_template
from app import app, db, socketio
from models import Task

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(title=data['title'], description=data.get('description', ''), completed=False)
    db.session.add(task)
    db.session.commit()

    # Emit the event after the task is created
    socketio.emit('task_updated', {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    }, broadcast=True)

    return jsonify({'message': 'Task created', 'task': {'id': task.id}}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()

    # Emit the event after the task is updated
    socketio.emit('task_updated', {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed
    }, broadcast=True)

    return jsonify({'message': 'Task updated'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    # Emit the event after the task is deleted
    socketio.emit('task_updated', {
        'id': task.id
    }, broadcast=True)

    return jsonify({'message': 'Task deleted'}), 204
