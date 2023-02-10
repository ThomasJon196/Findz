from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit
import ssl

from flask import url_for, redirect
from authlib.integrations.flask_client import OAuth
import os

context = ssl.SSLContext()
context.load_cert_chain('cert.pem', 'key.pem')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.secret_key = os.urandom(12)
oauth = OAuth(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = '194463054446-o83f7f4i51vhh795lbov71bo0hvqu1p8.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token    )
    print(" Google User ", user)
    return redirect('/groups')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('answer', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)  #, host='0.0.0.0') #, ssl_context=context)
