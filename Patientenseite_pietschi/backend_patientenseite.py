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


PATIENTEN_JSON = "patienten.json"
    

class Patient:
    """Represents a patient with various attributes. mit kwargs damit man flexibel beim Erstellen von Patienten ist."""
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

    def __repr__(self):
        return (f"Patient(Name={self.Name}, Vorname={self.Vorname}, "
                f"Geburtsdatum={self.Geburtsdatum}, Arzt={self.Arzt})")
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        # Normalisiere die Keys: z.B. "id" → "ID"
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
            'Telefon': data.get('Telefon', data.get('telefon', ''))
        }

        return cls(**normalized)
    

    def to_dict(self):
        return {
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
            "Telefon": self.Telefon
        }

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

    st.session_state.therapy_sessions.append(new_session)
    st.success(f"✅ Neue Therapiesitzung hinzugefügt: {displayed_date}")

def delete_therapy_session(index):
    """Löscht die Therapiesitzung am gegebenen Index."""
    st.session_state.therapy_sessions.pop(index)
    st.rerun()

    def __repr__(self):
        return (f"Patient(Name={self.Name}, Vorname={self.Vorname}, Geburtsdatum={self.Geburtsdatum}, "
                f"Versicherung={self.Versicherung}, Zusatzversicherung={self.Zusatzversicherung}, "
        )


    @staticmethod
    def from_dict(data):
        return Patient(**data)


