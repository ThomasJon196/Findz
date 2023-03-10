03.03.2023


# MVP

1. Feature: Gruppen(isolation).
	- [x] Aktuelle Gruppe an Server schicken. (Wiete)
	- [x] Endpunkt erweitern zur Gruppenuebergabe (WebXR)
	- [x] Userlist/Pointlist -> database 
	- [x] Isolate groups from each other. (SocketIO rooms)
    - [ ] Only show logged in users inside a group. Login/Logout flag in database with name of group. 
      - loggedIn Flag in database (default False)
      - set False on server restart
  - [x] Endpoint for profile picture

1. Feature: Interaktion
	- [ ] Anstupsen (optional)
	- [x] Punkt platzieren (Button in WebXR einfuegen -> Ruft Endpunkt auf und speichert Location)
	Fuer alle Leute in der Gruppe sichtbar.

2. Feature: Frontend UX
	- [ ] Choose profile picture
	- [ ] User friendly interface.

3. Documentation
   - [ ] documentation outline (chatgpt)
   - [ ] frontend
   - [ ] backend
   - [ ] webXR
   - [ ] Vision

Bugfixes:
- [x] Lati/Longi switched when saving/reading point.
- [ ] App langsamer seit AppScheduler: Replaced print statements
- [x] Sonderzeichen in Gruppennamen
- [x] Pink marker at spawn? (Scaled down marker)
- [x] Dont repond to non-logged in users. > Backend redirects to login page.
- [x] Bild flakern (probably download/refresh)
- [ ] Error on first login 
- [ ] Bild anzeigen (Vielleicht erstmal fix setzen, Das Flakern kommt vielleicht von der downloadzeit)


# Extras

- [x] SocketIO: Create periodic message. 
- [ ] Bild an markierten PuTODOnkt anghaengen
- [x] Optional: Beschreibung von dem Punkt


# Refactoring

- [ ] app.py aufraeumen: [Flask blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/) for tidy folder structure.

# Fazit (Was haben wir aus diesem Projekt gelernt?)

Wie kann man in Zukunft entiwcklungszeit sparen?

- Ausfuehrliche log/print statements essentiell fuer Debugging[^2]
- Einheitliche Schnittstellen definitionen [^1]


[^1]: Kommunikation zwischen unterschiedlichen Komponenten erfordert die Uebergabe einheitlicher Daten. (Hierfuer eignen sich API-Management-Tools). Ansonsten kann ein kleiner typo fuer viel verlorene Entwicklungszeit sorgen.

[^2]: Am besten sofort mit logging bibliotheken arbeiten, anstatt in den stdout zu schreiben, da die programmlaufzeit unter print statements leidet.