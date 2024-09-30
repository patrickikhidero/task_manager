from flask import Flask
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    # Other configurations or extensions can be initialized here
    return app

app = create_app()
socketio = SocketIO(app)