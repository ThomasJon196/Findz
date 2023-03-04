03.03.2023


# TODO

1. Feature: Gruppen(isolation).
	- Aktuelle Gruppe an Server schicken. (Wiete)
	- Endpunkt erweitern zur Gruppenuebergabe (WebXR)
	- Userlist/Pointlist -> database 
    - Only show logged in users inside a group.

2. Feature: Interaktion (Tobi)
	(- Anstupsen)
	- Punkt platzieren (Button in WebXR einfuegen -> Ruft Endpunkt auf und speichert Location)
	Fuer alle Leute in der Gruppe sichtbar.

3. Feature: Frontend UX


Bugfixes:

- [ ] Show only logged in users in webXR. Implement a logout function in WebXR and set a logged in flag in database.
- [x] Dont repond to non-logged in users. > Backend redirects to login page.
- [ ] Bild flakern
- [ ] Error on first login 
- [ ] Bild anzeigen (Vielleicht erstmal fix setzen, Das Flakern kommt vielleicht von der downloadzeit)


# Extras

- [ ] SocketIO: Create periodic message.
- [ ] Bild an markierten Punkt anghaengen
- [ ] Optional: Beschreibung von dem Punkt


# Feedback 

- Kommentare