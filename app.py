from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit
# import ssl
import json

import os
import pathlib
import requests
from flask import session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from database.sqlite_functions import (
    initialize_database,
    add_new_user,
    add_new_friend,
    get_friendlist,
    add_new_group,
    add_new_group_member,
    get_grouplist
)

GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_KEY', None)
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "unspecified deploy_env")
print(DEPLOY_ENV)

if DEPLOY_ENV == "LOCAL":
    DOMAIN = '127.0.0.1:5000'
else:
    DOMAIN = 'findz.thomasjonas.de'

initialize_database()
add_new_user("test@mail.com")

app = Flask("Findz")  # naming our application
app.secret_key = "secret_session_key"  # it is necessary to set a password when dealing with OAuth 2.0

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # this is to set our environment to https because OAuth 2.0 only supports https environments

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(  # Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri=f"https://{DOMAIN}/google/auth/"  # and the redirect URI is the point where the user will end up after the authorization
)

# SLL Stuff
# context = ssl.SSLContext()
# context.load_cert_chain('cert.pem', 'key.pem')
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

userListe = []

# SocketIO ENDPOINTS


def update_userlist():
    pass

@socketio.on('update')
def handle_message(message):
    # print('received message: ' + message)
    angekommennachicht = json.loads(message)
        
    update_userlist()

    new_user_flag = True
    for idx, user in enumerate(userListe):
        if user['name'] == angekommennachicht['name']:
            user = angekommennachicht
            new_user_flag = False
        
    if new_user_flag:
        userListe.append(angekommennachicht)

    print('Message to send' + str(userListe))
    emit('answer', json.dumps(userListe), broadcast=True)


# GOOGLE AUTH FUNCTIONS & ENDPOINTS

app.secret_key = os.urandom(12)
# users = json.dumps([
#       { "name": "Thomas", "latitude": "50.780757972246015, ", "longitude": "7.1830757675694805", "bild": "tomas.png" },
#       { "name": "Wiete", "latitude": "50.799765", "longitude": "7.204590", "bild": "Wiete.png" },
#       { "name": "Tobias", "latitude": "50.799985", "longitude": "7.205288", "bild": "Tobias.png" }
#     ])


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

    email = id_info.get("email")

    session["google_id"] = id_info.get("sub")  # defing the results to show on the page
    session["name"] = id_info.get("name")
    session["email"] = email

    print(session['email'])
    # print("Current session cookie:" + str(session.sid))

    add_new_user(email)

    return redirect("/static/gruppen")  # the final page where the authorized users will end up


@app.route("/logout")  # the logout page and function
def logout():
    print(session['email'])
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

@login_is_required
@app.route("/addFriend", methods=['POST'])
def addFriend():
    friendMail = request.data.decode("utf-8")
    print(session["email"])
    add_new_friend(friends_email=friendMail, user_email=session["email"])

    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getFriends", methods=['GET'])
def getFriends():
    print("Freundesliste")
    friendlist = get_friendlist(session['email'])
    data = jsonify({"friendlist": friendlist})
    return data, 200

@app.route("/deleteFriend", methods=['DELETE'])
def deleteFriend():
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getGroups", methods=['GET'])
def getGroups():
    print("Aktuelle session: " + str(session["email"]))
    grouplist = get_grouplist(email=session["email"])
    data = jsonify({"goruplist": grouplist})
    return data, 200


@app.route("/addMembers", methods=['POST'])
def add_Group_Member():
    payload = json.loads(request.data)
    print(payload)
    # add_new_group_member(admin=session.get('email'), new_users=payload)
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/createGroup", methods=['POST'])
def createGroup():
    payload = json.loads(request.data)
    print(payload)
    add_new_group(admin=session.get("email"), groupname=payload)
    data = jsonify({"status": "success"})
    return data, 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webXR')
def webxr():
    email = session.get("email")
    print(email)

    return render_template('webXR.html', user=email)


# Reroutes the /static/ pages.
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html')


if __name__ == '__main__':
    if DEPLOY_ENV == "LOCAL":
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
    else:
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0')
