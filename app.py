from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit
# import ssl
import json

# from flask import url_for, redirect
# from authlib.integrations.flask_client import OAuth

import os
import pathlib
import requests
from flask import session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_KEY', None)

GLOBAL_DOMAIN = 'findz.thomasjonas.de'
LOCAL_DOMAIN = '127.0.0.1'


app = Flask("Findz")  #naming our application


userListe = []
app.secret_key = "GeekyHuman.com"  #it is necessary to set a password when dealing with OAuth 2.0
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri=f"https://{GLOBAL_DOMAIN}/google/auth/"  #and the redirect URI is the point where the user will end up after the authorization
)


# context = ssl.SSLContext()
# context.load_cert_chain('cert.pem', 'key.pem')

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# SocketIO Endpoints


# GOOGLE AUTH FUNCTIONS & ENDPOINTS

app.secret_key = os.urandom(12)
users = json.dumps([
      { "name": "Thomas", "latitude": "50.780757972246015, ", "longitude": "7.1830757675694805", "bild": "tomas.png" },
      { "name": "Wiete", "latitude": "50.799765", "longitude": "7.204590", "bild": "Wiete.png" },
      { "name": "Tobias", "latitude": "50.799985", "longitude": "7.205288", "bild": "Tobias.png" }
    ])


def login_is_required(function):  # a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/google/")  # the page where the user can login
def login():
    authorization_url, state = flow.authorization_url()  # asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@app.route('/google/auth/')  # this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  # defing the results to show on the page
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return redirect("/webXR")  # the final page where the authorized users will end up


@app.route("/logout")  # the logout page and function
def logout():
    session.clear()
    return redirect("/")

#####################
# BASIC ENDPOINTS
#####################

@app.route("/groups")  # the page where only the authorized users can go to
@login_is_required
def protected_area():

    email = session.get("email")
    print(email)

    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"  # the logout button


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webXR')
def webxr():
    email = session.get("email")
    print(email)

    return render_template('webXR.html', user=email)


@socketio.on('update')
def handle_message(message):
    print('received message: ' + message)
    angekommennachicht = json.loads(message)
        
    new_user_flag = True
    for idx, user in enumerate(userListe):
        if user['name'] == angekommennachicht['name']:
            user = angekommennachicht
            new_user_flag = False
        
    if new_user_flag:
        userListe.append(angekommennachicht)
        


    print('Message to send' + str(userListe))
    emit('answer', json.dumps(userListe), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True) #, ssl_context=('cert.pem', 'key.pem'))
  #, host='0.0.0.0') #)





# @app.route('/google/auth/')
# def google_auth():
#     token = oauth.google.authorize_access_token()
#     user = oauth.google.parse_id_token(token)
#     print(" Google User ", user)
#     return redirect('/groups')

# @app.route('/google/')
# def google():

    
#     CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
#     oauth.register(
#         name='google',
#         client_id=GOOGLE_CLIENT_ID,
#         client_secret=GOOGLE_CLIENT_SECRET,
#         server_metadata_url=CONF_URL,
#         client_kwargs={
#             'scope': 'openid email profile'
#         }
#     )

#     # Redirect to google_auth function
#     redirect_uri = url_for('google_auth', _external=True)
#     print(redirect_uri)
#     return oauth.google.authorize_redirect(redirect_uri)
