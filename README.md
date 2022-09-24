# Are You The One - Berechnung
Python Berechnungsskript für die Sendung Are You The One: \
Berechnet auf Basis der bisherigen Informationen die noch möglichen Kombinationen der Paarungen.

![Example](https://github.com/pheagan/AYTO-Berechnung/blob/main/AYTO_Berechnung/Img/VIP2022_Nacht_7.png?raw=true)

Im Folgenden ein kurzes **How-To** für die eigene Nutzung

### Vorbereitung
Skript erstellt mit Version 3.7.\
Es werden die Module _**matplotlib**_, _**sys**_, _**math**_, _**time**_, und _**itertools**_ verwendet.

Neben der Skriptdatei müssen zusätzlich Textdateien mit den bekannten Informationen im gleichen Ordner liegen. 
Folgende Textdateien müssen im selben Ordner wie das Skript liegen:
* **1. GruppeA.txt**
	- Liste mit 10 Zeilen mit je einem Eintrag => Gruppe A ist die kleinere Gruppe mit 10 Personen 
	- In jeder Zeile steht ein/e Teilnehmer/in (TN), keine weiteren Einträge oder Trennzeichen
	- Reihenfolge der TN ist egal, Sortierung muss über alle Dateien einheitlich sein, alphabetisch wird empfohlen	
* **2. GruppeB.txt**
	- Liste mit 11 Zeilen mit je einem Eintrag => Gruppe B ist die kleinere Gruppe mit 11 Personen
	- In jeder Zeile steht ein/e TN, keine weiteren Einträge oder Trennzeichen
	- Nachrücker/in muss an Position 11 stehen
	- Reihenfolge der restlichen TN ist egal, Sortierung muss über alle Dateien einheitlich sein, alphabetisch wird empfohlen
* **3. BekannteMatches.txt**
	- In jeder Zeile steht ein Matchpaar, dieses ist getrennt durch ein einzelnes Komma
	- An erster Stelle steht die Person aus Gruppe A, an zweiter Stelle die Person aus Gruppe B
	- Indizes der Personenlisten beginnen bei 0, ein Match von PersonA0 (erste Person aus Gruppe A) und PersonB4 (fünfte Person aus Gruppe B) wäre somit [0,4]
	- Hinweis: Steht ein Match fest und Zusatzkandidat/in ist nicht das zusätzliche Match, muss dieses NoMatch (Kandidat-A mit Zusatzkandidat-B*) zusätzlich in die Liste für NoMatches eingetragen werden
	- Anmerkungen sind am Ende der Zeile nach einem Trennzeichen [%] möglich
* **4. BekannteNoMatches.txt**
	- In jeder Zeile steht ein NoMatch-Paar, dieses ist getrennt durch ein einzelnes Komma
	- An erster Stelle steht die Person aus Gruppe A, an zweiter Stelle die Person aus Gruppe B
	- Indizes der Personenlisten beginnen bei 0, ein NoMatch von PersonA2 (dritte Person aus Gruppe A) und PersonB1 (zweite Person aus Gruppe B) wäre somit [2,1]
	- Anmerkungen sind am Ende der Zeile nach einem Trennzeichen [%] möglich
* **5. MatchingNights.txt**
	- In jeder Zeile steht eine Matchingnight, die Trennung der Matches erfolgt durch ein einzelnes Komma
	- Eintrag 1 in Zeile 1 entspricht dem/r gewählten Partner/in von PersonA-0 in der ersten MatchingNight, etc.
	- Indizes der Personenlisten beginnen bei 0
	- Saß in der ersten Nacht PersonA-0 bei PersonB-5, Person A-1 mit PersonB-2,... beginnt die erste Zeile mit [5,2,...]
	- Anschließend steht in jeder Zeile abgetrennt durch zwei Backslashes [//] die Anzahl der korrekten Matches in der jeweiligen Nacht
	- Anmerkungen sind am Ende der Zeile nach einem Trennzeichen [%] möglich

### Ausführen
Das Skript entweder durch Doppelklick ausführen oder in Konsole das Skript mit Pyhton ausführen. 
Das Skript sollte im Anschluss von alleine Durchlaufen und am Ende eine Übersichtstabelle erstellen.\
Bisher ist kaum Fehlerüberprüfung bei der Input-Eingabe implementiert. Sollte das Skript ohne Fehlermeldung abbrechen, überprüfen ob alle notwendigen Python Module installiert sind und die Textdateien für die Eingabe der Daten auf Fehler überprüfen.
