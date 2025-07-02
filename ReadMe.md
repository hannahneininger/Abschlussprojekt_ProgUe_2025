### Therapiedokumentations Datei
In diesem Abschlussprojekt soll ein Prototyp für ein Therapiedokumentationsprogramm erstellt werden.
Der Fokus dieses Programms soll dabei auf dem Therapieverlauf liegen. Funktionen, welche mehr der Therapieplanung und -organisation dienen, sollen im Rahmen des Projektes zuvernachlässigen sein.
Die Überlegung ist, mehrere 'States' zu erschaffen, auf welche über ein einfaches, aber ansprechendes Interface zugegriffen werden kann.

## States
In diesem Abschitt sollen die Vorläufigen Ideen der Haupt-States beschrieben werden. Sie sollen später miteinander verknüpft werden und Informationen untereinander kommunizieren.
- States (in dem Kontext): interaktive Seiten

# State 1- "Hauptmenü"
Die erste Seite, die sich durch das Ausführen der App öffnet, ist das Hauptmenü. Diese Seite soll als "Gateway" dienen, um auf die zwei weiteren Haupt-States zu gelangen. Mittig angerichtet sollen sich zwei Button befinden. Einer soll ein Patienten-Symbol tragen und auf die "Patientenseite"-State zugreifen. Der Zweite, welcher mit einem Kalender-Symbol gekennzeichnet sein soll, fürht zu der "Kalender"-State.

# State 2- "Patientenseite"
Geöffnet wird diese State, sobald auf das Patientensymbol gedrückt wird. Sie dient auch als Callback-Station, damit von dort aus weitere Aspekte geöffnet werden können, ohne dass das komplette Programm neugeladen werden muss. Hier gibt es wieder drei Optionen:

Option 1: Suchfeld

Option 2: Patient anlegen
    Diese soll zum einen "hard fact"-Abfrage besitzen mit den Patienten-Daten (über eine Patienten-Klasse):
    - ID 
    - Name  
    - Vorname    
    - Geburtsdatum   
    - Straße   
    - Hausnummer   
    - Postleitzahl   
    - Stadt   
    - Versicherung    
    - Zusatzversicherung   
    - Arzt   
    - email   
    - Telefon   
    - Anamnese    
    Das Programm soll dem Patienten dann eine ID zuordnen.
    Die Daten sollen in einer JSON Datei gespeichert werden

Option 3:
    Es wird eine Liste aller Patienten angezeigt, die erstellt wurden.
    Dort sollen zwei Interaktionen möglich sein. Entweder "Löschen" oder "Auswählen" 
    Wenn man auf "Auswählen" klickt wird dann die Dokumentationsseite des jeweiligen Patienten geöffnet.
    
# Dokumentationsseite   
Das "Auswählen" eines Patienten aus der Patientenliste soll auf die Patienten-Seite führen.
Diese Seite wird die Hauptseite des Projekts. Sie soll links eine Spalte haben, in der die Patientendaten sowie die Anamnese dargestellt werden. Zusätzlich soll ein Textfeld mit der Anamnese bestehen.
Darunter- ebenfalls auf der linken Seite- soll eine Graphik generiert werden, welche die Tendenz des Patienten über den Behandlungsverlauf angibt. Diese wiederum zieht ihren Input aus der Verlaufsdoku/ Behandlungsdoku, welche den Hauptteil der Seite darstellt.

Die Doku soll als Expander dargestellt werden und über einen Button "Therapie hinzufügen" erscheinen. Sind mehrere Therapiesitzungen an einem Tag geplant, erscheint ein weiterer Balken mit einem Zusatz (z.B (2) ):
    geschlossener Expander:   "T1- dd/mm/yyyy"

    offener Expander:   TX- dd/mm/yyyy (nicht zwangsweise bearbeitungsfähig, weil generiert durch Erstellungsdatum)
                        Tendenz als Dropdown:   - besser        value= +1
                                                - unverändert   value= +/- 0
                                                - schlechter    value= -1 
                        beschreibbares Feld für Therapiedoku

# Patientenkalender
Der Kalender selbst ist im Rahmen des Projektes ein "Nice-To-Have"-Aspekt, dessen Bedeutung lediglich der Übersichtlichkeit dienen soll. Wie bereits erwähnt steht die Therapieplanung, bei welcher der Kalender deutlich ausreizendere Funktionen erfüllen sollte, keine Rolle. Daher lassen sich über den Kalender Termine erstellen, welche dann in der Dokuseite erscheinen un die erstellten Termine der Dokuseite wiederum erscheinen im Kalender. Da wir auf eine Work-Life-Balance der Nutzer achten, ist der Kalender nur für die Arbeitszeiten des fiktiven Therapieanbieters zugänglich.