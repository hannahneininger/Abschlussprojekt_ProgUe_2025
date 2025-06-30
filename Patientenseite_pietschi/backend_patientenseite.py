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
    """Add a new therapy session with today's date or versioned duplicate if one exists."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Count how many sessions already exist for today
    existing_sessions = [s for s in st.session_state.therapy_sessions if s.date.startswith(today)]

    next_version = len(existing_sessions) + 1

    # Use versioned date if more than one session exists
    if next_version > 1:
        displayed_date = f"{today} ({next_version})"
    else:
        displayed_date = today

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    new_session = TherapySession(
    date=today,
    displayed_date=displayed_date,  # <-- Add this line
    tendency="",
    patient=patient.Name,
    timestamp=timestamp,
    documentation=""
)

    st.session_state.therapy_sessions.append(new_session)
    st.success(f"✅ Neue Therapiesitzung hinzugefügt: {displayed_date}")

def delete_therapy_session(index):
    """Löscht die Therapiesitzung am gegebenen Index."""
    st.session_state.therapy_sessions.pop(index)
    st.rerun()
    
# %%
#create an empty list of dates which can later on be filled with the dates of therapy sessions
def create_empty_dates_list():
    return []

class TherapySession:
    def __init__(self, date, displayed_date, tendency, patient, timestamp=None, documentation=""):
        self.date = date
        self.displayed_date = displayed_date
        self.tendency = tendency
        self.patient = patient
        self.timestamp = timestamp or datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.documentation = documentation

    def __repr__(self):
        return f"TherapySession(date={self.date}, tendency={self.tendency}, patient={self.patient})"
    
# create a class Patient wich has the Attributes: Name = str, Vorname= str, Geburtsdatum= str, Straße= str, Hausnummer= int, PLZ= int, Stadt= str, Versicherung= str, Zusatzversicherung= True/False, Arzt= str, email= str, Telefon= int
class Patient:
    def __init__(self, Name, Vorname, Geburtsdatum, Straße, Hausnummer, Postleitzahl, Stadt, Versicherung, Zusatzversicherung, Arzt, email, Telefon):
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


    def _repr_(self):
        return (f"Patient(Name={self.Name}, Vorname={self.Vorname}, Geburtsdatum={self.Geburtsdatum}, "
                f"Versicherung={self.Versicherung}, Zusatzversicherung={self.Zusatzversicherung}, "
                f"Arzt={self.Arzt}, email={self.email}, Telefon={self.Telefon})")
