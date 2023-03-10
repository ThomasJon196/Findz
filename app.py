from flask import Flask
from flask import render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_apscheduler import APScheduler
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
    get_group_memberlist,
    get_all_users,
    get_group_memberlist_and_location,
    update_location,
    get_saved_group_points,
    save_new_point,
    get_all_groupnames,
    user_logged_in,
    user_logged_out,
    loggout_all_users
)


#####################
#       SETUP       #
#####################

GOOGLE_CLIENT_ID = os.getenv("CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("CLIENT_KEY", None)
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "GLOBAL (default)")

# TODO: Add logging instead of print statements. (Slow down the server.)
print("Setting up database")
initialize_database()
loggout_all_users()

def initialize_test_users():
    users = ["test@mail.com", "test2@mail.com"]
    print("Adding example users: " + str(users) + " for development.")
    add_new_user(users[0])
    add_new_user(users[1])
    add_new_user("tmusic196@gmail.com")
    update_location(users[0], longitute=123, latitude=456)
    update_location(users[1], longitute=123, latitude=456)
    add_new_group(users[0], "testmailGroup")
    add_new_group_members(users[0], "testmailGroup", new_users=["tmusic196@gmail.com"])
    # get_group_memberlist_and_location('tmusic196@gmail.com', 'testgroup') # Group has to be created first.


#initialize_test_users()

if DEPLOY_ENV == "LOCAL":
    DOMAIN = "127.0.0.1:5000"
    print("Deploying: " + DEPLOY_ENV + " accessible on: " + DOMAIN)
elif DEPLOY_ENV == "GLOBAL_2":
    DOMAIN = "findz-dev.thomasjonas.de"
    print("Deploying: " + DEPLOY_ENV + " accessible on: " + DOMAIN)
else:
    DOMAIN = "findz.thomasjonas.de"
    print("Deploying: " + DEPLOY_ENV + " accessible on: " + DOMAIN)


# Name of the application. Used inside flask for module loading.. and so on. Idk rly.
app = Flask(__name__)


# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

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
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],  # here we are specifing what do we get after the authorization
    redirect_uri=f"https://{DOMAIN}/google/auth/",  # and the redirect URI is the point where the user will end up after the authorization
)

# SLL Stuff
# context = ssl.SSLContext()
# context.load_cert_chain('cert.pem', 'key.pem')


#####################
# SocketIO functions
#####################

roomList = []
socketio = SocketIO(app)

# TODO: Implement SocketIO rooms for user groups.
# TODO: Client username & room should be taken from database. Mit Tobi testen.


@socketio.on('join')
def on_join(data):
    data = json.loads(data)
    username = data.get('name')
    if username is None:
        destination = '/'
        emit('redirect', destination)
        return
    room = data.get("current_group")
    join_room(room)
    # If a None type error is thrown here, the current user is not logged in.
    print(username + ' has joined the room ' + room)
    send(username + ' has joined the room ' + room, room=room)

# TODO: Implement a active rooms list.

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room ' + room, room=room)


# @scheduler.task('interval', id='do_job_1', seconds=2, misfire_grace_time=300)
# def test_task():
#     print("hello you")


@scheduler.task('interval', id='Notify users', seconds=2, misfire_grace_time=300)
def broadcast_locations():
    print("Boradcasting locations")
    rooms = get_all_groupnames()

    for room in rooms:
        print("Broadcasting locations for group: " + str(room))
        user_location_list = get_group_memberlist_and_location(room)

        user_payload = transform_to_payload(user_location_list)
        print("User payload to send" + str(user_payload))

        saved_points_list = get_saved_group_points(group=room)
        # example_point = [['examplePoint', 'kill me please', 50.78001445359288, 7.182461982104352]]
        saved_points_list = transform_to_point_payload(saved_points_list)

        payload = [user_payload, saved_points_list]
        print("Full payload to send" + str(payload))

        socketio.emit("answer", json.dumps(payload), room=room)


def transform_to_payload(user_location_list):
    """
    Transform user data to json payload expected by the frontend.
    """

    user_list = []

    for record in user_location_list:
        json_payload = {
            "name": record[0],
            "latitude": record[1],
            "longitude": record[2],
            "bild": None
        }
        user_list.append(json_payload)

    return user_list


def transform_to_point_payload(points):

    payload = []
    for point in points:
        point_payload = {
            "title": point[0],
            "text": point[1],
            "longitude": point[2],
            "latitude": point[3]
        }
        payload.append(point_payload)

    return payload


@socketio.on("update")
def handle_message(message):
    """
    Endpoint which receives the current user position and establishes a socketio-connection
    TODO: Create a periodic tasks for broadcasting, instead of sending locations whenever a users sends an update.
    """
    # print('received message: ' + message)
    # Received format: { "name": '{{user}}', "latitude": position.coords.latitude , "longitude": position.coords.longitude, "bild": "images/Wiete.png" }
    print("SocketIO request by: " + str(session.get("email")))

    request_data = json.loads(message)

    email = request_data.get("name")
    latitude = request_data.get("latitude")
    longitute = request_data.get("longitude")
    # picture = request_data.get("bild")

    update_location(email, latitude, longitute)


#####################
# GOOGLE AUTH FUNCTIONS & ENDPOINTS
#####################


# EXCLUDED_ENDPOINTS = ["index", "login", "callback", "static", None]


# @app.before_request
# def require_login():
#     # Check if the user is logged in with Google
#     if request.endpoint not in EXCLUDED_ENDPOINTS and session.get('email') is None:
#         print(request.endpoint)
#         print(session.get('email') is None)
#         # If the user is not logged in, redirect to the Google login page
#         return redirect('/')


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
@app.route("/google/auth/")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    # Safe session informations
    email = id_info.get("email")

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = email

    print("New user-login: " + session["email"])
    add_new_user(email)
    user_logged_in(email)

    # Final redirect.
    return redirect("/static/gruppen")


# Logout by clearing cache and redirect to landing page.
@app.route("/logout")
def logout():
    email = session["email"]
    user_logged_out(email)
    print("User logged out: " + email)
    session.clear()
    return redirect("/")


#####################
# BASIC ENDPOINTS
#####################


@app.route("/addFriend", methods=["POST"])
@login_is_required  # TODO: Check why this doesnt work?
def addFriend():
    friendMail = request.data.decode("utf-8")
    add_new_friend(friends_email=friendMail, user_email=session["email"])
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getFriends", methods=["GET"])
def getFriends():
    friendlist = get_friendlist(session["email"])
    data = jsonify({"friendlist": friendlist})
    return data, 200


@app.route("/deleteFriend", methods=["DELETE"])
def deleteFriend():
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/getGroups", methods=["GET"])
def getGroups():
    grouplist = get_grouplist(user=session["email"])
    data = jsonify({"grouplist": grouplist})
    return data, 200


@app.route("/getGroupMembers", methods=["GET"])
def getGroupMembers():
    payload = request.args.get("groupName")
    print(payload)
    memberlist = get_group_memberlist(user=session["email"], group_name=payload)
    data = jsonify({"memberlist": memberlist})
    return data, 200


@app.route("/createGroup", methods=["POST"])
def createGroup():
    payload = json.loads(request.data)
    new_members = payload["members"]
    mail = session.get("email")

    add_new_group(admin=session.get("email"), groupname=payload["name"])

    print("Payload is: " + str(payload["members"]))

    new_members.append(mail)
    add_new_group_members(
        admin=session.get("email"),
        groupname=payload["name"],
        new_users=new_members,
    )
    data = jsonify({"status": "success"})
    return data, 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/webXR")
def webxr():
    groupname = request.args.get("groupname")
    session["current_group"] = groupname

    email = session.get("email")
    print("groupname: " + str(groupname))

    return render_template("webXR.html", user=email, current_group=groupname)


@app.route("/save_point", methods=["POST"])
def save_point_of_interest():
    """
    Saves a location of intereset

    TODO: Points only work if you are currently in a group.
    """
    payload = json.loads(request.data)  

    save_new_point(payload, session.get('email'), session.get('current_group'))
    print('Successfully recevied point of interest: ' + str(payload))

    data = jsonify({"status": "success"})
    return data, 200

@app.route("/updateImage", methods=['POST'])
def updateImage():
    payload = json.loads(request.data)
    imageSource = payload["chosenImageSource"]

    #function to save image

    return 'Image updated successfully', 200


# Reroutes the /static/ pages.
@app.errorhandler(404)
def not_found_error(error):
    return render_template("index.html")


#####################
# BACKGROUND FUNCS  #
#####################


def get_logged_in_users():
    # Retrieve all users from the database
    all_users = get_all_users()

    # Create an empty list to store the logged in users
    logged_in_users = []

    # Iterate over the session keys and check if they correspond to a logged-in user
    for key in session.keys():
        user_id = session.get(key)
        for user in all_users:
            if user.id == user_id:
                logged_in_users.append(user)

    return logged_in_users


if __name__ == "__main__":

    if DEPLOY_ENV == "LOCAL":
        socketio.run(
            app,
            debug=True,
            allow_unsafe_werkzeug=True,
            host="0.0.0.0",
            ssl_context=("cert.pem", "key.pem"),
        )
    else:
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0")


    # import threading
    # # Broadcast locations every x seconds.
    # def broadcast_event():
    #     broadcast_locations()
    #     new_event = threading.Timer(2.0, broadcast_event)
    # def test():
    #     print("Hello you fat fuck")
    #     new_event = threading.Timer(2.0, test)
        
    # print("Starting thread")
    # threading.Timer(interval=2.0, function=test)
