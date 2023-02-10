from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit
import ssl
context = ssl.SSLContext()
context.load_cert_chain('cert.pem', 'key.pem')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authenticate', methods=['GET'])
def authenticate():
    # TODO: Write endpoint as POST-method, since user is supposed to enter 
    # credentials and post to server


    # ... your code ...

    return jsonify('Works')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('answer', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)  #, host='0.0.0.0') #, ssl_context=context)
