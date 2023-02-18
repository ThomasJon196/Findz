from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit
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
    add_new_group_members,
    get_grouplist,
    get_group_memberlist
)

GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_KEY', None)
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "GLOBAL (default)")

# TODO: Add logging instead of print statements. (Slow down the server.)
print("Setting up database")
initialize_database()

if DEPLOY_ENV == "LOCAL":
    DOMAIN = '127.0.0.1:5000'
    print("Deploying: " + DEPLOY_ENV + " accessible on: " + DOMAIN)
    users = ["test@mail.com", "test2@mail.com"]
    print("Adding example users: " + str(users) + " for development.")
    add_new_user(users[0])
    add_new_user(users[1])
else:
    DOMAIN = 'findz.thomasjonas.de'
    print("Deploying: " + DEPLOY_ENV + " accessible on: " + DOMAIN)

# Name of the application. Used inside flask for module loading.. and so on. Idk rly.
app = Flask(__name__)

# Ecryption of client-side sessions. Necessary for OAuth 2.0.
app.secret_key = os.urandom(12).hex()

# this is to set our environment to https because OAuth 2.0 only supports https environments
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  

# Google authentication secrets
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
# and which information we get from google.
flow = Flow.from_client_secrets_file(  
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri=f"https://{DOMAIN}/google/auth/"  # and the redirect URI is the point where the user will end up after the authorization
)

# SLL Stuff
# context = ssl.SSLContext()
# context.load_cert_chain('cert.pem', 'key.pem')

# SocketIO functions

userListe = []
socketio = SocketIO(app)


def update_userlist():
    # TODO: Refresh the userlist based on logged in/out users.
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

# Wrapper: checks if the current user is logged in.
def login_is_required(function):  
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()
    return wrapper


# Login route
@app.route("/google/")
def login():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url()  
    session["state"] = state
    return redirect(authorization_url)


# Callback route. Redirected by google after authentication.
@app.route('/google/auth/')  
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

    # Safe session informations
    email = id_info.get("email")

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = email

    print("New user-login: " + session['email'])
    add_new_user(email)

    # Final redirect.
    return redirect("/static/gruppen")  


# Logout by clearing cache and redirect to landing page.
@app.route("/logout")
def logout():
    print("User logged out: " + session['email'])
    session.clear()
    return redirect("/")

#####################
# BASIC ENDPOINTS
#####################


# @login_is_required TODO: Check why this doesnt work?
@app.route("/addFriend", methods=['POST'])
def addFriend():
    friendMail = request.data.decode("utf-8")
    add_new_friend(friends_email=friendMail, user_email=session["email"])
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getFriends", methods=['GET'])
def getFriends():
    friendlist = get_friendlist(session['email'])
    data = jsonify({"friendlist": friendlist})
    return data, 200


@app.route("/deleteFriend", methods=['DELETE'])
def deleteFriend():
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getGroups", methods=['GET'])
def getGroups():
    grouplist = get_grouplist(admin_mail=session["email"])
    data = jsonify({"grouplist": grouplist})
    return data, 200

@app.route("/getGroupMembers", methods=['GET'])
def getGroupMembers():
    payload = request.args.get('groupName')
    print(payload)
    memberlist= get_group_memberlist(admin_mail=session["email"], group_name=payload)
    data = jsonify({"memberlist": memberlist})
    return data, 200
"""
@app.route("/addMembers", methods=['POST'])
def add_Group_Member():
    payload = json.loads(request.data)
    add_new_group_members(admin=session.get('email'),
                          groupname=payload["name"],
                          new_users=payload["members"])
    data = jsonify({"status": "success"})
    return data, 200
"""

@app.route("/createGroup", methods=['POST'])
def createGroup():
    payload = json.loads(request.data)
    print(payload)
    add_new_group(admin=session.get("email"), groupname=payload["name"])
    add_new_group_members(admin=session.get('email'),
                              groupname=payload["name"],
                              new_users=payload["members"])
    data = jsonify({"status": "success"})
    return data, 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webXR')
def webxr():
    email = session.get("email")
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
