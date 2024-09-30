# app.py

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from models import db, Task

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        title = request.json.get('title')
        description = request.json.get('description')
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        socketio.emit('task_updated', {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'completed': new_task.completed
        })
        return jsonify({'id': new_task.id}), 201

    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def update_delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'PUT':
        task.title = request.json.get('title', task.title)
        task.description = request.json.get('description', task.description)
        task.completed = request.json.get('completed', task.completed)
        db.session.commit()
        socketio.emit('task_updated', {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        })
        return jsonify({'message': 'Task updated'})

    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_updated', {'id': task.id})
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
