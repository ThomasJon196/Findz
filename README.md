# FindZ - Web3D-Project
---
## Vision

#### Spotlight yourself so your friends find you easily. Dont lose your friend in a crowd. ...(gerne eigene Beschreibung einfuegen)

Augumented-Reality marker, which displays your friends current position through the camera and locates your friends with higher precision.

---

## Description

...


## Setup

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

--- 

Collect insights inside [Project-Wiki](https://github.com/ThomasJon196/Findz/wiki)

---

## TODO (delete when finished)
- WebXR GPS Koordinaten einlesen [Tobi]
- Authentifizierung + Freundesliste (Backend mit Typescript) [Thomas]
- Authentifizierung + Freundesliste usw. (FrontEnd Mobile first development) [Wiete]
- Erster prototyp eines 3D Markers 
- Platzierung des Markers auf den GPS Koordinaten



- Add main/dev branches + push rules


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
