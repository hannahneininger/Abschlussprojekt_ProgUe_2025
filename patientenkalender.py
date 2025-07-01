import pandas as pd
from datetime import datetime, timedelta, date
from streamlit import session_state as state
from streamlit_calendar import calendar
import streamlit as st
from Patientenseite_pietschi.backend_patientenseite import TherapySession, Patient

def show_patient_calendar():
    """Zeigt den interaktiven Kalender für Therapiesitzungen an."""
    
    # Initialize session_state if needed
    if "therapy_sessions" not in st.session_state:
        st.session_state.therapy_sessions = []

    st.title("🗓️ Patientenkalender")

    # ➕ Formular für neuen Termin
    with st.form("Neuen Termin hinzufügen"):
        ausgewaehlter_patient = None  # <- Wichtig: Definiere die Variable hier!
        
        if not st.session_state.patientenliste:
            st.warning("Keine Patienten vorhanden. Bitte fügen Sie zuerst einen Patienten hinzu.")
            name = st.text_input("Name des Patienten")
        else:
            # Liste von Anzeigetexten generieren
            patienten_auswahl = [
                f"{p.Vorname} {p.Name} (ID: {p.ID})" for p in st.session_state.patientenliste
            ]
            ausgewaehlter_patient = st.selectbox(
                "Wähle einen Patienten",
                options=patienten_auswahl,
                index=None,
                placeholder="Patient auswählen..."
            )

            if ausgewaehlter_patient:
                # Extrahiere ID
                patient_id = int(ausgewaehlter_patient.split("ID: ")[1].strip(")"))
                selected_patient = next((p for p in st.session_state.patientenliste if p.ID == patient_id), None)

                if selected_patient:
                    name = f"{selected_patient.Vorname} {selected_patient.Name}"
                else:
                    name = ""
                    st.error("❌ Patient konnte nicht gefunden werden.")
            else:
                name = ""
            
        
        datum = st.date_input("Datum", value=date.today())
        uhrzeit = st.time_input("Uhrzeit", value=datetime.now().time())
        beschreibung = st.text_input("Kurzdoku")

        submitted = st.form_submit_button("🆕 Termin hinzufügen")

        if submitted:
            if name and beschreibung:
        # Validierung der Uhrzeit
                if not (7 <= uhrzeit.hour < 18):
                    st.error("⚠️ Bitte wähle eine Uhrzeit zwischen 07:00 und 18:00 Uhr.")
                else:
                # Extrahiere Datum als String
                    date_str = datum.strftime("%Y-%m-%d")

                    # Generiere displayed_date mit Versionierung
                    existing_sessions = [s for s in st.session_state.therapy_sessions if s.date == date_str]
                    next_version = len(existing_sessions) + 1
                    displayed_date = f"{date_str} ({next_version})"

                    # Dummy-Patient for calendar-added session
                    dummy_patient = Patient(
                        ID="dummy",
                        Name=name,
                        Vorname="",
                        Geburtsdatum="",
                        Straße="",
                        Hausnummer=0,
                        Postleitzahl=0,
                        Stadt="",
                        Versicherung="",
                        Zusatzversicherung=False,
                        Arzt="",
                        email="",
                        Telefon=0
                    )

                    new_session = TherapySession(
                        date=date_str,
                        displayed_date=displayed_date,
                        tendency="",
                        patient=dummy_patient.Name,
                        timestamp=datetime.now().strftime("%Y%m%d%H%M%S%f"),
                        documentation=beschreibung
                    )
                    st.session_state.therapy_sessions.append(new_session)
                    st.success("✅ Termin erfolgreich hinzugefügt!")
            else:
                st.warning("Bitte gib alle erforderlichen Daten ein.")
    
    # 🔍 Suchfeld
    suchbegriff = st.text_input("🔎 Suche nach Patient oder Beschreibung")

    # 📁 Daten laden
    sessions_data = [
        {
            "Name": session.patient,
            "Date": session.date,
            "Time": "10:00",  # Placeholder time
            "Description": session.documentation or "Keine Beschreibung"
        }
        for session in st.session_state.therapy_sessions
    ]
    df = pd.DataFrame(sessions_data)

    # 🔍 Filtern nach Suchbegriff
    if suchbegriff:
        df = df[df.apply(lambda row: suchbegriff.lower() in str(row).lower(), axis=1)]

    # 📅 Kalender vorbereiten
    events = []
    for _, row in df.iterrows():
        start_datetime = datetime.strptime(f"{row['Date']} {row['Time']}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=30)
        events.append({
            "title": f"{row['Name']} - {row['Description']}",
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
        })

    # 📆 Kalender anzeigen
    calendar_options = {
        "initialView": "timeGridWeek",
        "editable": False,
        "selectable": True,
        "businessHours": {
            "daysOfWeek": [ 1, 2, 3, 4, 5],  # Alle Wochentage (0 = Sonntag)
            "startTime": "07:00",  # Früheste Uhrzeit
            "endTime": "18:00",    # Späteste Uhrzeit
        },
        "minTime": "07:00:00",
        "maxTime": "18:00:00",
        "slotMinTime": "07:00:00",
        "slotMaxTime": "18:00:00"
    }
    selected_event = calendar(events=events, options=calendar_options)

    

    # 📎 Optional: Zeige ausgewähltes Ereignis an
    if selected_event and "eventClick" in selected_event:
        # Wenn ein Event angeklickt wurde
        event_data = selected_event["eventClick"]["event"]
        st.info("Ausgewähltes Ereignis:")
        st.json(event_data)

    elif selected_event and "dateClick" in selected_event:
        # Optional: Wenn der Benutzer auf ein Datum geklickt hat
        date_data = selected_event["dateClick"]
        st.info("Datum ausgewählt:")
        st.json(date_data)

    else:
        st.write("Kein Ereignis ausgewählt.")