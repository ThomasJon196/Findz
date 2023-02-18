# LOG

## Web Serving: Handling HTTP (Webframework Flask/Spring or nginx for static content)
- Serve angular in Flask: https://avishkabalasuriya980330.medium.com/serve-angular-application-in-python-flask-server-bd37c8a0b431
	

## HTTPS/SSL Certificate

- For communication over https we need a ssl cert: https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server

- Quick fix [Running flask over https](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

- Exposed via Cloudflare
    - Set Cloudflare Flexibel SSL/TLS
    - Set google console redirect endpoint
    - Set socket endpoints (local/global)


## Web Sockets: Two way communication, Updating user states (sockets.io)

[FlaskSocketIO Docs](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

[Flask-SocketIO and JavaScript Socket.IO](https://medium.com/@abhishekchaudhary_28536/building-apps-using-flask-socketio-and-javascript-socket-io-part-1-ae448768643)

- Problem, client uses unsupported socketio version:
    - Check compatability matrix: https://socket.io/docs/v3/client-installation/

[SocketIO Rooms](https://flask-socketio.readthedocs.io/en/latest/getting_started.html#rooms) for isolating user groups.



## Authentication

[Frontend vs. Backend Authentication](https://stackoverflow.com/questions/54823611/google-oauth-where-to-sign-in-users-backend-frontend)

- Authentication in backend is safere
- Backend if user-data/email is required without them beeing authenticated. (Group management)

> Adjust the redirect-uri inside google-cloud.
> Running localy: localhost:5000/google/auth
> Running globaly: domain/google/auth (findz.thomasjonas.de/google/auth)


[Resource](https://geekyhumans.com/how-to-implement-google-login-in-flask-app/)


## Periodic Tasks

[Flask APScheduler](https://viniciuschiele.github.io/flask-apscheduler/index.html), a lightweight implementation for flask.

For more complex jobs use `Celery`, `cronjob` or `systemd`.



## FAQ

1. GPS coordinates are not received

        Enable GPS transmission in mobile phone

1. Parsing JSON objects in browser

        Transform via [JSON.Stringify()](https://www.w3schools.com/js/js_json_stringify.asp#:~:text=Stringify%20a%20JavaScript%20Object&text=stringify()%20to%20convert%20it,string%20following%20the%20JSON%20notation.)

1. Passing data from Flask to Javascript

        Add variable to `render_template('get_data.html', geocode=geocode)` function. [Source](https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template)

1. Inspect device via browser:

        In chrome: `chrome://inspect/#devices`

1. Get current user who is accessing endpoint

        [Sessions](https://pythonbasics.org/flask-sessions/)

