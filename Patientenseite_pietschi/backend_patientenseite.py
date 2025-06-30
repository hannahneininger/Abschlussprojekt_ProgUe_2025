# %%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def create_tendency_dropdown():
    tendency_options = ["Steigend", "Fallend", "Stagnierend"]
    tendency = st.selectbox("Tendenz auswählen", tendency_options)
    return tendency

def get_numeric_tendency(tendency):
    tendency_map = {"Steigend": 1, "Stagnierend": 0, "Fallend": -1}
    return tendency_map.get(tendency, None)


#%% 
def add_therapy_session(patient):
    """Add a new therapy session with today's date."""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    if "therapy_sessions" not in st.session_state:
        st.session_state.therapy_sessions = []

    existing_dates = [session.date for session in st.session_state.therapy_sessions]
    if today in existing_dates:
        st.warning("Für heute wurde bereits eine Therapiesitzung erfasst.")
    else:
        new_session = TherapySession(
            date=today,
            tendency="",
            patient=patient.Name,
            timestamp=timestamp
        )
        st.session_state.therapy_sessions.append(new_session)
        st.success(f"Neue Therapiesitzung für {today} hinzugefügt!")
        st.rerun()

# %%
#create an empty list of dates which can later on be filled with the dates of therapy sessions
def create_empty_dates_list():
    return []

class TherapySession:
    def __init__(self, date, tendency, patient, timestamp=None, documentation=""):
        self.date = date
        self.tendency = tendency
        self.patient = patient
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.documentation = documentation  # Unique per session

    def _repr_(self):
        return f"TherapySession(date={self.date}, tendency={self.tendency}, patient={self.patient})"
    
# create a class Patient wich has the Attributes: Name = str, Vorname= str, Geburtsdatum= str, Straße= str, Hausnummer= int, PLZ= int, Stadt= str, Versicherung= str, Zusatzversicherung= True/False, Arzt= str, email= str, Telefon= int
class Patient:

    def __init__(self, ID, Name, Vorname, Geburtsdatum, Straße, Hausnummer, Postleitzahl, Stadt, Versicherung, Zusatzversicherung, Arzt, email, Telefon):
        self.ID = ID

        self.Name = Name
        self.Vorname = Vorname
        self.Geburtsdatum = Geburtsdatum
        self.Straße = Straße
        self.Hausnummer = Hausnummer
        self.Postleitzahl = Postleitzahl
        self.Stadt = Stadt
        self.Versicherung = Versicherung
        self.Zusatzversicherung = Zusatzversicherung
        self.Arzt = Arzt
        self.email = email
        self.Telefon = Telefon


    def __repr__(self):

        return (f"Patient(Name={self.Name}, Vorname={self.Vorname}, Geburtsdatum={self.Geburtsdatum}, "
                f"Versicherung={self.Versicherung}, Zusatzversicherung={self.Zusatzversicherung}, "
                f"Arzt={self.Arzt}, email={self.email}, Telefon={self.Telefon})")
