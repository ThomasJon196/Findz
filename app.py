from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit
import ssl
import json
context = ssl.SSLContext()
context.load_cert_chain('cert.pem', 'key.pem')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = json.dumps([
      { "name": "Thomas", "latitude": "50.780757972246015, ", "longitude": "7.1830757675694805", "bild": "tomas.png" },
      { "name": "Wiete", "latitude": "50.799765", "longitude": "7.204590", "bild": "Wiete.png" },
      { "name": "Tobias", "latitude": "50.799985", "longitude": "7.205288", "bild": "Tobias.png" }
    ])



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webXR')
def webxr():
    return render_template('webXR.html')


@socketio.on('update')
def handle_message(message):
    print('received message: ' + message)
    print('Message to send' + str(users))
    emit('answer', users, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)  #, host='0.0.0.0') #, ssl_context=context)
