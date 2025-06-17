import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit import session_state as state
#from streamlit_calendar import calendar



def show_patient_calendar():
    st.title("Patientenkalender")


    # Eingabefelder für neuen Termin
    with st.form("Neuen Termin hinzufügen"):
        name = st.text_input("Name des Patienten") # Liste von Patienten laden mit selectbox
        date = st.date_input("Datum", value=datetime.today())
        time = st.time_input("Uhrzeit", value=datetime.now().time())
        description = st.text_input("Beschreibung")
        submitted = st.form_submit_button("Termin hinzufügen")
        if submitted:
            if name and description:
                new_entry = {
                    'Name': name,
                    'Date': date.strftime("%Y-%m-%d"),
                    'Time': time.strftime("%H:%M"),
                    'Description': description
                }
                state.patient_data = pd.concat([state.patient_data, pd.DataFrame([new_entry])], ignore_index=True)
                st.success("Termin erfolgreich hinzugefügt!")
            else:
                st.error("Bitte füllen Sie alle Felder aus.")
