from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index_socket.html')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('answer', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
