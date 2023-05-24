### FindZ - Web3D-Project

- [Vision](#vision)
- [Description](#description)
- [Setup \& Deployment](#setup--deployment)
  - [Cloudflare Tunnel](#cloudflare-tunnel)
  - [Flask](#flask)
  - [Angular](#angular)
  - [Docker Compose](#docker-compose)
- [Lessons learned](#lessons-learned)


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


## Lessons learned


- New Technologies
  - `Flask`: Python Web-Framework (Server-Side)
  - `Angular`: Typescript Web-Framework (Client-Side)
  - `A-Frame`: 3D & WebXR Scence visualization

- Security
  - `SQL injections` [^3]
  - `Secrets in git` [^4]


- Save development time:

  - `Logging libraries`.  [^1]
  - `API-endpoints` documented [^2]. Information flow between independently developed components should be documented.

[^1]: Logging statements clearly defined for easier debugigng. Use 
[^2]: Information flow between independently developed components should be documented.(Small type can cost several hours..)
[^3]: Prevent sql injections by not allowing strings to be passed on as queries.
[^4]: Dont commit secrets into version control


