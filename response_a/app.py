from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from models import db, Task
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
socketio = SocketIO(app)

# Ensure the database exists
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    socketio.emit('task_update', task.to_dict())
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.completed = 'completed' in request.form
    db.session.commit()
    socketio.emit('task_update', task.to_dict())
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_delete', {'id': task_id})
    return redirect(url_for('index'))

@socketio.on('connect')
def test_connect():
    emit('response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True)