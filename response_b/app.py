# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import *

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
socketio = SocketIO(app)

# Import routes after db and socketio are defined to avoid circular imports
from routes import *

if __name__ == '__main__':
    socketio.run(app, debug=True)