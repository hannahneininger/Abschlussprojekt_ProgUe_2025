# %%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


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

    # ➕ Neue Methode: Konvertiert Objekt zu Dictionary für JSON-Speicherung
    def to_dict(self):
        return {
            "date": self.date,
            "displayed_date": self.displayed_date,
            "tendency": self.tendency,
            "patient": self.patient,
            "timestamp": self.timestamp,
            "documentation": self.documentation
        }

    # ➕ Neue Methode: Erstellt ein TherapySession-Objekt aus einem Dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(
            date=data.get("date"),
            displayed_date=data.get("displayed_date"),
            tendency=data.get("tendency"),
            patient=data.get("patient"),
            timestamp=data.get("timestamp"),
            documentation=data.get("documentation", "")  # Standardwert leerer String
        )


PATIENTEN_JSON = "patienten.json"
    

class Patient:
    """Represents a patient with various attributes."""
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', -1)
        self.Name = kwargs.get('Name', '')
        self.Vorname = kwargs.get('Vorname', '')
        self.Geburtsdatum = kwargs.get('Geburtsdatum', '')
        self.Straße = kwargs.get('Straße', '')
        self.Hausnummer = kwargs.get('Hausnummer', '')
        self.Postleitzahl = kwargs.get('Postleitzahl', '')
        self.Stadt = kwargs.get('Stadt', '')
        self.Versicherung = kwargs.get('Versicherung', '')
        self.Zusatzversicherung = kwargs.get('Zusatzversicherung', False)
        self.Arzt = kwargs.get('Arzt', '')
        self.email = kwargs.get('email', '')
        self.Telefon = kwargs.get('Telefon', 0)
        self.Anamnese = kwargs.get('Anamnese', '')
        self.sessions = []  # Leere Liste für spätere Sitzungen

    def __repr__(self):
        return (f"Patient(Name={self.Name}, Vorname={self.Vorname}, "
                f"Geburtsdatum={self.Geburtsdatum}, Arzt={self.Arzt})")

    def to_dict(self):
        data = {
            "ID": self.ID,
            "Vorname": self.Vorname,
            "Name": self.Name,
            "Geburtsdatum": self.Geburtsdatum,
            "Straße": self.Straße,
            "Hausnummer": self.Hausnummer,
            "Postleitzahl": self.Postleitzahl,
            "Stadt": self.Stadt,
            "Versicherung": self.Versicherung,
            "Zusatzversicherung": self.Zusatzversicherung,
            "Arzt": self.Arzt,
            "email": self.email,
            "Telefon": self.Telefon,
            "Anamnese": self.Anamnese,
            "sessions": [session.to_dict() for session in self.sessions]  # Sessions werden hier mitgespeichert
        }
        return data

    @classmethod
    def from_dict(cls, data):
        normalized = {
            'ID': data.get('ID', data.get('id', data.get('Id', -1))),
            'Name': data.get('Name', data.get('name', '')),
            'Vorname': data.get('Vorname', data.get('vorname', '')),
            'Geburtsdatum': data.get('Geburtsdatum', data.get('geburtsdatum', '')),
            'Straße': data.get('Straße', data.get('strasse', data.get('straße', ''))),
            'Hausnummer': data.get('Hausnummer', data.get('hausnummer', '')),
            'Postleitzahl': data.get('Postleitzahl', data.get('plz', data.get('postleitzahl', ''))),
            'Stadt': data.get('Stadt', data.get('stadt', '')),
            'Versicherung': data.get('Versicherung', data.get('versicherung', '')),
            'Zusatzversicherung': data.get('Zusatzversicherung', data.get('zusatzversicherung', '')),
            'Arzt': data.get('Arzt', data.get('arzt', '')),
            'email': data.get('email', data.get('e-mail', data.get('mail', ''))),
            'Telefon': data.get('Telefon', data.get('telefon', '')),
            'Anamnese': data.get('Anamnese', data.get('anamnese', ''))
        }

        patient = cls(**normalized)

        # Falls Sitzungen im Dict sind, lade sie als TherapySession-Objekte
        sessions_data = data.get("sessions", [])
        patient.sessions = [TherapySession.from_dict(sess) for sess in sessions_data]

        return patient

def create_tendency_dropdown():
    tendency_options = ["Steigend", "Fallend", "Stagnierend"]
    tendency = st.selectbox("Tendenz auswählen", tendency_options)
    return tendency

def get_numeric_tendency(tendency):
    tendency_map = {"Steigend": 1, "Stagnierend": 0, "Fallend": -1}
    return tendency_map.get(tendency, None)

def add_therapy_session(patient):
    """Add a new therapy session with today's date or versioned duplicate if one exists."""
    
    today = datetime.now().strftime("%Y-%m-%d")

    # Count how many sessions already exist for today
    existing_sessions = [s for s in st.session_state.therapy_sessions if s.date.startswith(today)]
    next_version = len(existing_sessions) + 1

    # Use versioned label
    displayed_date = f"{today} ({next_version})" if next_version > 1 else today

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    new_session = TherapySession(
        date=today,
        displayed_date=displayed_date,
        tendency="",
        patient=patient.Name,
        timestamp=timestamp,
        documentation=""
    )
    patient.sessions.append(new_session)
    st.session_state.therapy_sessions.append(new_session)
    st.success(f"✅ Neue Therapiesitzung hinzugefügt: {displayed_date}")
    

def delete_therapy_session(index):
    """Löscht die Therapiesitzung am gegebenen Index."""
    st.session_state.therapy_sessions.pop(index)
    st.rerun()

    




