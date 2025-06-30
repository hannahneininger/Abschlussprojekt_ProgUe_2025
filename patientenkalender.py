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
