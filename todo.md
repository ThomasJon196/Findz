03.03.2023


# MVP

1. Feature: Gruppen(isolation).
	- [x] Aktuelle Gruppe an Server schicken. (Wiete)
	- [x] Endpunkt erweitern zur Gruppenuebergabe (WebXR)
	- [x] Userlist/Pointlist -> database 
	- [x] Isolate groups from each other
    - [ ] Only show logged in users inside a group. Login/Logout flag in database with name of group. SocketIO rooms

2. Feature: Interaktion (Tobi)
	- [ ] Anstupsen (optional)
	- [ ] Punkt platzieren (Button in WebXR einfuegen -> Ruft Endpunkt auf und speichert Location)
	Fuer alle Leute in der Gruppe sichtbar.

3. Feature: Frontend UX
	- [ ] User friendly interface.

4. Documentation
   - [ ] documentation outline (chatgpt)
   - [ ] frontend
   - [ ] backend
   - [ ] webXR
   - [ ] Vision

Bugfixes:
- [ ] App langsamer seit AppScheduler
- [ ] Sonderzeichen in Gruppennamen
- [ ] Pink marker at spawn? (Scaled down marker)
- [x] Dont repond to non-logged in users. > Backend redirects to login page.
- [ ] Bild flakern (probably download/refresh)
- [ ] Error on first login 
- [ ] Bild anzeigen (Vielleicht erstmal fix setzen, Das Flakern kommt vielleicht von der downloadzeit)


# Extras

- [ ] SocketIO: Create periodic message. 
- [ ] Bild an markierten PuTODOnkt anghaengen
- [x] Optional: Beschreibung von dem Punkt


# Refactoring

- [ ] app.py aufraeumen: [Flask blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/) for tidy folder structure.

# Feedback 

- Kommentare