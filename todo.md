03.03.2023


# MVP

1. Feature: Gruppen(isolation).
	- [x] Aktuelle Gruppe an Server schicken. (Wiete)
	- [x] Endpunkt erweitern zur Gruppenuebergabe (WebXR)
	- [x] Userlist/Pointlist -> database 
	- [x] Isolate groups from each other. (SocketIO rooms)
    - [x] Only show logged in users inside a group. Login/Logout flag in database with name of group. 
      - loggedIn Flag in database (default False)
      - set False on server restart
  - [x] Endpoint for profile picture

1. Feature: Interaktion
	- [ ] Anstupsen (optional)
	- [x] Punkt platzieren (Button in WebXR einfuegen -> Ruft Endpunkt auf und speichert Location)
	Fuer alle Leute in der Gruppe sichtbar.
  - [x] Zeige Nutzer in der selben Gruppe an.

1. Feature: Frontend UX
	- [x] Choose profile picture
	- [x] User friendly interface.

2. Documentation
   - [x] documentation outline
   - [ ] frontend
   - [ ] backend
   - [ ] webXR
   - [ ] Vision

Bugfixes:
- [x] Remove fixed routes in index.html
- [x] On WebxR- back button: Redirect user to server endpoint so they are logged out.
- [x] Currently loggedIn gorupmembers whoare loggedIn another group are also shown
- [x] Lati/Longi switched when saving/reading point.
- [ ] App langsamer seit AppScheduler: Replace print statements with logging, Disable/Replace clientside logging. Disable 'DEBUG' Flag in production.
- [x] Sonderzeichen in Gruppennamen
- [x] Pink marker at spawn? (Scaled down marker)
- [x] Dont repond to non-logged in users. > Backend redirects to login page.
- [x] Bild flakern (probably download/refresh)
- [ ] Error on first login: **need a full error report from client & serverside** Probably session problems. Maybe the random secret key creates problems. https://stackoverflow.com/questions/61922045/mismatchingstateerror-mismatching-state-csrf-warning-state-not-equal-in-reque
- [x] Bild anzeigen (Vielleicht erstmal fix setzen, Das Flakern kommt vielleicht von der downloadzeit)


# Feedback Sophia

- [ ] User Interface unintuitiv
- [ ] Punkte skalierung: Punkte zu gross
- [x] Anzeige erst ab 50m: User ist aber ab 30 aus der liste entfernt.



# Extras

- [ ] Neues Foto
- [x] SocketIO: Create periodic message. 
- [x] Bild an markierten PuTODOnkt anghaengen
- [x] Optional: Beschreibung von dem Punkt


# Refactoring

- [ ] app.py aufraeumen: [Flask blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/) for tidy folder structure.

# Fazit (Was haben wir aus diesem Projekt gelernt?)

Wie kann man in Zukunft entiwcklungszeit sparen?

- Ausfuehrliche log/print statements essentiell fuer Debugging[^2]
- Einheitliche Schnittstellen definitionen [^1]


[^1]: Kommunikation zwischen unterschiedlichen Komponenten erfordert die Uebergabe einheitlicher Daten. (Hierfuer eignen sich API-Management-Tools). Ansonsten kann ein kleiner typo fuer viel verlorene Entwicklungszeit sorgen.

[^2]: Am besten sofort mit logging bibliotheken arbeiten, anstatt in den stdout zu schreiben, da die programmlaufzeit unter print statements leidet.


__BACKLOG__

__OPEN__

- Clear project structure. (src/, )
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