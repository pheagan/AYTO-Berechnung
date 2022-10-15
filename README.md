# Are You The One - Berechnung
Python Berechnungsskript für die Sendung Are You The One: \
Berechnet auf Basis der bisherigen Informationen die noch möglichen Kombinationen der Paarungen.

![Example1](https://github.com/pheagan/AYTO-Berechnung/blob/main/AYTO_Berechnung/Img/VIP2022_Nacht_7.png?raw=true)

Im Folgenden ein kurzes **How-To** für die eigene Nutzung

### Vorbereitung
Download der aktuellen Release Version: [Release V1.0](https://github.com/pheagan/AYTO-Berechnung/releases/tag/ayto1.0) 
\
\
Skript erstellt mit Python Version 3.7.\
Es werden die Module _**matplotlib**_, _**sys**_, _**math**_, _**time**_, _**itertools**_, _**tkinter**_, _**pandas**_, _**warnings**_ und _**openpyxl**_ verwendet. 
Die meisten davon müssten in der Standard-Installation von Python enthalten sein, insbesondere matplotlib, pandas und openpyxl gegebenenfalls nachinstallieren.
\
\
Neben der Skriptdatei muss zusätzlich die Excel Datei "AYTO_Data.xlsx" im gleichen Ordner liegen. 
Der Name der Datei, die Namen der Tabellenblätter und die Anordnung der Daten auf den Seiten darf nicht verändert werden.

Die Excel Datei besteht aus 3 Seiten:
1. TeilnehmerInnen
	- Eintragen der TeilnehmerInnen in die 2 Tabellenblätter
	- Gruppe, die die Extraperson enthält, muss in Gruppe B eingetragen werden (eine Person aus Gruppe A hat 2 Matches in Gruppe B)
	- Eingabe der Namen für Matchboxes und MatchingNights über Datenüberprüfung in Excel => TeilnehmerInnen zuerst eintragen
2. Matchboxen
	- Eintragen der Matchbox Ergebnisse
	- Mehr Zeilen zum eintragen, um bei Matches die logischen NoMatches mit Zusatzperson einzutragen 
	- Optionale Spalte für Anmerkungen (z.B. "nach Match mit Person B5, kein Doppelmatch mit B*")
	- Liste von oben nach unten befüllen, Zeile muss immer vollständig befüllt sein! (Anmerkung ausgenommen)
3. MatchingNights
	- Eintragen der Paarungen bei den MatchingNights und der Anzahl der korrekten Matches
	- Bei ausgefallenen MatchingNights (z.B. durch Aussteigen einer Person) die letzte MatchingNight 1zu1 kopieren (weglassen führt zu keinem Fehler, die Anzeige der Ausgabe basiert aber auf der Anzahl der Einträge)
	- Liste von oben nach unten befüllen, Zeile muss immer vollständig befüllt sein!

### Ausführen
Das Skript entweder durch Doppelklick im Explorer oder in der Konsole mit Pyhton ausführen. 
Das Skript sollte im Anschluss von alleine Durchlaufen.\
Bisher ist kaum Fehlerüberprüfung bei der Input-Eingabe implementiert. Sollte das Skript ohne Fehlermeldung abbrechen, überprüfen ob alle notwendigen Python Module installiert sind und die Excel Datei auf Fehler überprüfen.
Tritt weiterhin ein Fehler auf, diesen gerne über ein Issue in GitHub rückmelden.\
\
Nach Initialer Berechnung fragt das Skript, ob eine interaktive Tabelle erstellt werden soll (bestätigen durch Input 'y') oder lediglich eine statische.
Die statische Tabelle entspricht dem oben dargestellten Bild.
Dieses kann beliebig exportiert werden.
Eine weitere Anpassung ist nicht möglich. \
\
Bei der dynamischen Tabelle können durch klicken manuell Matches auf noch offene Kombinationen gesetzt werden.
Die restlichen Möglichkeiten werden daraufhin angepasst.\
Manuell gesetzte Matches werden in hellerem Grün gehighlighted und können auch wieder abgewählt werden.
Durch die Randbedingung (Matchboxen, MatchingNights) vorgegebene Matches können nicht abgewählt werden.
Ein Bild-Export aus dieser interaktiven Tabelle ist nicht möglich. \
\
Beispielhafte Darstellung der interaktiven Tabelle zu oben abgebildeter Tabelle mit manuell gewähltem Match aus Franziska und Martin:

![Example](https://github.com/pheagan/AYTO-Berechnung/blob/main/AYTO_Berechnung/Img/Interaktive_Tabelle_Beispiel.PNG?raw=true)
Beispielhafte Bedienung der interaktiven Tabelle im Img Ordner.