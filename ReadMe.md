### Therapiedokumentations Datei
In diesem Abschlussprojekt soll ein Prototyp für ein Therapiedokumentationsprogramm erstellt werden.
Die Überlegung ist, mehrere 'States' zu erschaffen, auf welche über ein optisch ansprechendes Interface zugegriffen werden kann.

## States
In diesem Abschitt sollen die Vorläufigen Ideen der Haupt-States beschrieben werden.

# State 1- "Hauptmenü"
Dies ist die erste Seite, wenn man das Programm öffnet. Diese Seite soll als Gateway dienen, um auf die zwei weiteren Haupt-States zu gelangen. Mittig angerichtet sollen sich zwei Button befinden. Einer soll ein Patienten-Symbol tragen und auf die "Patientenmenü"-State zugreifen. Der Zweite, welcher mit einem Kalender-Symbol gekennzeichnet sein soll, fürht zu der "Kalender"-State.

# State 2- "Patientenmenü"
Geöffnet wird diese State, sobald auf das Patientensymbol gedrückt wird. Sie dient auch als Callback-Station, damit von dort aus weitere Aspekte geöffnet werden können, ohne dass das komplette Programm neugeladen werden muss. Hier gibt es wieder zwei Optionen:
Option 1: Suchfeld
    Idee 1: Dorpdownmenü mit Liste der Patienen
    Idee 2: Beschreibbares Feld + Dropdown
Option 2: Patient anlegen
    # State 2.1
    Hier soll eine neue Seite geöffnet werden. Diese soll zum einen "hard fact"-Abfrage besitzen mit den Patienten-Daten:
    - Name, Vorname
    - Adresse
    - E-mail
    - Handynummer
    - Versicherung
    - Zusatzversicherung
    - Arzt
    Das Programm soll dem Patienten dann eine ID zuordnen.
    
    Des Weitern soll ein Textfeld erscheinen mit der Überschrift Anamnese. Entwerder als einzelnes Textfeld oder mehrere mit den Überschriften:
    - Hauptdiagnose und ICF
    - Ziel
    - Hx
    - Nebendiagnosen/ Risiken
    - psychosoziales
    - Funktionsuntersuchung

# State 2.2   
Das Aussuchen eines Patienten UND das speichern eines neuen Patienten, soll auf die Patienten-Seite führen.
Diese Seite wird die Hauptseite des Projekts. Sie soll links eine Spalte haben mit den Patienten-Daten und einer "Abgespeckteren Ansicht" der Anamnese (evtl Hauptdiagnose und Ziel).
Terminliste mit hinzufügeoption. Am besten, die Liste mit dem Kalender irgendwie verlinken. Und so, dass die TX direkt das Datum zuführt. Darunter soll eine Graphik generiert werden, welche die Tendenz des Patienten über den Behandlungsverlauf angibt. Diese wiederum zieht ihren Input aus der Verlaufsdoku/ Behandlungsdoku, welche den Hauptteil der Seite darstellt.

Die Doku wäre als Dropdown Balken denkbar:
    geschlossener Balken:   "T1- dd/mm/yyyy"
                            "Tendenz: -----"

    offener Balken: TX- dd/mm/yyyy (nicht zwangsweise bearbeitungsfähig, weil generiert von woanders?)
                    Tendenz als Dropdown:   - besser        value= +1
                                            - unverändert   value= +/- 0
                                            - schlechter    value= -1 
                    beschreibbares Feld für Therapiedoku

Die Seite zeigt also eine Dokuübersicht mit den Balken.