# LOG

## Web Serving: Handling HTTP (Webframework Flask/Spring or nginx for static content)
- Serve angular in Flask: https://avishkabalasuriya980330.medium.com/serve-angular-application-in-python-flask-server-bd37c8a0b431
	

## HTTPS/SSL Certificate

- For communication over https we need a ssl cert: https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server

- Quick fix: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

- TODO


## Web Sockets: Two way communication, Updating user states (sockets.io)

[FlaskSocketIO Docs](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

[Flask-SocketIO and JavaScript Socket.IO](https://medium.com/@abhishekchaudhary_28536/building-apps-using-flask-socketio-and-javascript-socket-io-part-1-ae448768643)

- Problem, client uses unsupported socketio version:
    - Check compatability matrix: https://socket.io/docs/v3/client-installation/



## Authentication

[Frontend vs. Backend Authentication](https://stackoverflow.com/questions/54823611/google-oauth-where-to-sign-in-users-backend-frontend)

- Authentication in backend is safere
- Backend if user-data/email is required without them beeing authenticated. (Group management)