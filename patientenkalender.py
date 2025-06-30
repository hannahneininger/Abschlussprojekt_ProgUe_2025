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
    }
    selected_event = calendar(events=events, options=calendar_options)

    # ➕ Formular für neuen Termin
    with st.form("Neuen Termin hinzufügen"):
        st.markdown("### Neuer Termin")
        name = st.text_input("Name des Patienten")
        datum = st.date_input("Datum", value=date.today())
        uhrzeit = st.time_input("Uhrzeit", value=datetime.now().time())
        beschreibung = st.text_input("Kurzdoku")

        submitted = st.form_submit_button("🆕 Termin hinzufügen")

        if submitted:
            if name and beschreibung:
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
                    date=datum.strftime("%Y-%m-%d"),
                    tendency="",
                    patient=dummy_patient.Name,
                    timestamp=datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    documentation=beschreibung
                )
                st.session_state.therapy_sessions.append(new_session)
                st.success("✅ Termin erfolgreich hinzugefügt!")

    # 📎 Optional: Zeige ausgewähltes Ereignis an
    if selected_event:
        st.info("Ausgewähltes Ereignis:")
        st.json(selected_event)