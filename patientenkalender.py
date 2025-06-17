import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from streamlit import session_state as state
from streamlit_calendar import calendar



if "patient_data" not in st.session_state:
    st.session_state.patient_data = pd.DataFrame(columns=["Name", "Date", "Time", "Description"])

def show_patient_calendar():
    st.title("🗓️ Patientenkalender")

    # 🔍 Suchfeld
    suchbegriff = st.text_input("🔎 Suche nach Patient oder Beschreibung")

    # Daten laden & filtern
    df = st.session_state.patient_data
    if suchbegriff:
        df = df[df.apply(lambda row: suchbegriff.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    # 📅 Kalender vorbereiten
    events = []
    for _, row in df.iterrows():
        start_datetime = datetime.strptime(f"{row['Date']} {row['Time']}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + pd.Timedelta(minutes=30)  # Termin dauert z. B. 30 Minuten
        events.append({
            "title": f"{row['Name']} - {row['Description']}",
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
        })

    # 📆 Kalender anzeigen
    calendar_options = {
        "initialView": "timeGridWeek",  # Oder "dayGridMonth", "timeGridDay"
        "editable": False,
        "selectable": False,
    }
    calendar(events=events, options=calendar_options)

    st.markdown("---")

    # ➕ Formular für neuen Termin
    with st.form("Neuen Termin hinzufügen"):
        name = st.text_input("Name des Patienten")
        datum = st.date_input("Datum", value=date.today())
        uhrzeit = st.time_input("Uhrzeit", value=datetime.now().time())
        beschreibung = st.text_input("Beschreibung")
        submitted = st.form_submit_button("🆕 Termin hinzufügen")

        if submitted:
            if name and beschreibung:
                new_entry = {
                    "Name": name,
                    "Date": datum.strftime("%Y-%m-%d"),
                    "Time": uhrzeit.strftime("%H:%M"),
                    "Description": beschreibung
                }
                st.session_state.patient_data = pd.concat([
                    st.session_state.patient_data,
                    pd.DataFrame([new_entry])
                ], ignore_index=True)
                st.success("✅ Termin erfolgreich hinzugefügt!")
            else:
                st.error("❌ Bitte alle Felder ausfüllen.")


