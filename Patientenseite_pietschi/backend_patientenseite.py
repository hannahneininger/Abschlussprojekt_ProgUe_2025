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

# %%
def plot_tendency_over_time(tendencies, dates):
    # Map tendencies to numeric values for plotting
    tendency_map = {"Steigend": 1, "Stagnierend": 0, "Fallend": -1}
    numeric_tendencies = [tendency_map.get(t, 0) for t in tendencies]

    # Convert dates to pandas datetime if not already
    df = pd.DataFrame({
        "Datum": pd.to_datetime(dates),
        "Tendenz": numeric_tendencies
    })

    fig, ax = plt.subplots()
    ax.plot(df["Datum"], df["Tendenz"], marker='o')
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Fallend", "Stagnierend", "Steigend"])
    ax.set_xlabel("Datum")
    ax.set_ylabel("Tendenz")
    ax.set_title("Tendenz über die Zeit")
    plt.tight_layout()
    st.pyplot(fig)

plt.show()

#%% 
def add_therapy_session(patient):
    """Add a new therapy session with today's date."""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    existing_dates = [session.date for session in st.session_state.therapy_session]
    if today in existing_dates:
        st.warning("Für heute wurde bereits eine Therapiesitzung erfasst.")
    else:
        new_session = TherapySession(
            date=today,
            tendency="",
            patient=patient.Name,  # ✅ Zugriff über Instanz
            timestamp=timestamp
        )
        st.session_state.therapy_session.append(new_session)
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


PATIENTEN_JSON = "patienten.json"
    
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

    @staticmethod
    def from_dict(data):
        return Patient(**data)

