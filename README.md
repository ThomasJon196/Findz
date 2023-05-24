### FindZ - Web3D-Project

- [Vision](#vision)
- [Description](#description)
- [Setup \& Deployment](#setup--deployment)
  - [Cloudflare Tunnel](#cloudflare-tunnel)
  - [Flask](#flask)
  - [Angular](#angular)
  - [Docker Compose](#docker-compose)
- [TODO (delete when finished)](#todo-delete-when-finished)
- [Notes](#notes)
- [MVP](#mvp)
- [Optional](#optional)
- [Criteria](#criteria)


## Vision

Spotlight yourself so your friends find you easily. Dont lose your friend in a crowd.


## Description


Augumented-Reality marker, which displays your friends current position through the camera, lets you add locations of intereset and join groups for restricted visibility.





## Setup & Deployment

### Cloudflare Tunnel

To make the app accessible over the internet Cloudflares `Tunnel` option is used.
Setting up a local cloudflare-daemon `cloudflared` is required.

Follow the instructions on [Cloudflare Dashboard](https://one.dash.cloudflare.com/3675dc4a228ca040243803bc358815e7/access/tunnels)


The tunnels IP address has to be added inside the google oauth console for the google login to work properly.


### Flask

```bash
# Install venv
python3 -m venv venv

# Select `venv` as environment & python interpreter
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Run flask server
python app.py
```

### Angular


```bash
# Install angular cli (ng)
npm install -g @angular/cli

# Set baseHref to static folder in angular.json
"build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "baseHref": "/static/",
          }
}

# Install node packages
npm install

# Build project
ng build --configuration production --build-optimizer

# Move files move created files from dist/ into static/ & index.html into templates/

```

### Docker Compose

Deploy method requires only a Docker & Docker-compose installation. Cloudflare tunnel & token is required for this to work. `.env` file.

1. Pull repository

```bash
cd Scripts/

# Build frontend scripts
bash build_frontend.sh

# Build docker image
bash build_docker_image.sh

# Deploy containers
bash compose_docker_containers.sh
```

---

## TODO (delete when finished)

__OPEN__

- Clear project structure. (src/, )
- Create prod/dev deployments with seperate domains. (e.g. findz.dev., findz.)
- Add project setup docs
- Add angular build via docker-container. (Remove any dependencies from system. Such that only docker is required.)
- Reduce Flask image size. (Currently 1 GB)
- Integrate user sessions. Currently everyone sees everyone. (Privacy problem.)
  - Flask SocketIO rooms
  - flask.session
  - update logged in userlist
- Add logging. (Replace print statements)
- Integrate error handling. (e.g. user already exists/friend already exist. (Extra)
- Secure code against sql injections
- Asynchronous update of locations via periodic tasks.
- Persist database (docker volumes)
- custom pictures
- Tobi: Insert resources/links for webXR development

__DONE__
- Fix `static` endpoints. (Added automatic rerouting)
- Write a local/global deployment script 
- Configure deployment via docker-containers to remove OS-dependency. (cloudflared & flaskserver)
- WebXR GPS Koordinaten einlesen [Tobi]
- Authentifizierung + Freundesliste (Backend mit Typescript) [Thomas]
- Authentifizierung + Freundesliste usw. (FrontEnd Mobile first development) [Wiete]
- Erster prototyp eines 3D Markers 
- Platzierung des Markers auf den GPS Koordinaten


## Notes

- Codesandbox.io -> reactive development of 3D objects...


## MVP

- Get current position of a user based on app interaction. (Optimaly raising a hand. first simple button click.)
    - GPS, ...?

- Create a groups.
    - Settings who wants to be seen/ Who wants to transmit


## Optional

- Create symbol above head/ circle on the ground. (e.g. when distance is small enough) 

## Criteria
