from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@socketio.on('message', namespace='/test')
def handle_message(message):
    print('received message: ' + message)
    if message == "connect":
        print("connect success")
    socketio.emit('message', message, namespace='/test')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
