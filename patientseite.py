import streamlit as st
import datetime
import json
import os
from Patientenseite_pietschi.backend_patientenseite import Patient

PATIENTEN_JSON = os.getenv("PATIENT_JSON_FILE", "patienten.json")

def searchbar():
    """
    Creates a search bar for patient names.
    Returns the search term entered by the user.
    """
    st.markdown("### Suche nach Patienten")
    search_term = st.text_input("Geben Sie den Namen des Patienten ein:")
    return search_term.strip() if search_term else None

def suche_patienten(search_term):
    if not search_term:
        return []
    
    ergebnisse = []
    suchbegriff = search_term.lower()

    for patient in st.session_state.patientenliste:
        if suchbegriff in patient.Vorname.lower() or suchbegriff in patient.Name.lower():
            ergebnisse.append(patient)

    return ergebnisse

def zeige_suchergebnisse(ergebnisse):
    if not ergebnisse:
        st.info("Keine Patienten gefunden.")
        if st.button("Neuen Patienten hinzufügen"):
            st.session_state.suchmodus = False
        return
    
    st.markdown("### Gefundene Patienten")
    for patient in ergebnisse:
        with st.expander(f"{patient.Vorname} {patient.Name} (ID: {patient.ID})"):
            st.write(f"**Geburtsdatum:** {patient.Geburtsdatum}")
            st.write(f"**Adresse:** {patient.Straße} {patient.Hausnummer}, {patient.Postleitzahl} {patient.Stadt}")
            st.write(f"**Versicherung:** {patient.Versicherung}")
            st.write(f"**Arzt:** {patient.Arzt}")
            st.write(f"**Telefon:** {patient.Telefon}")
            st.write(f"**E-Mail:** {patient.email}")

def lade_patienten():
    if os.path.exists(PATIENTEN_JSON):
        with open(PATIENTEN_JSON, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON enthält keine Liste")
                
                valid_data = []
                for p in data:
                    try:
                        valid_data.append(Patient.from_dict(p))
                    except Exception as pe:
                        st.warning(f"Fehler beim Parsen eines Patienten: {pe}")
                
                return valid_data

            except json.JSONDecodeError as je:
                st.error("Die patienten.json ist beschädigt. Fehler beim Lesen der JSON.")
                return []
            except Exception as e:
                st.error(f"Unbekannter Fehler beim Laden der Patientendaten: {e}")
                return []
    return []

# Liste zum Speichern der Patienten
if 'patientenliste' not in st.session_state:
    st.session_state.patientenliste = lade_patienten()

if 'next_patient_id' not in st.session_state:
    st.session_state.next_patient_id = 1

def zeige_patientenliste():
    st.subheader("Liste aller Patienten")
    if len(st.session_state.patientenliste) == 0:
        st.info("Keine Patienten vorhanden.")
        return
    
    for idx, patient in enumerate(st.session_state.patientenliste):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"**{patient.Vorname} {patient.Name}**")

        with col2:
            if st.button(f"Auswählen", key=f"btn_select_{idx}"):
                st.session_state.selected_patient = patient
                st.rerun()

        st.markdown("---")

          
min_date = datetime.date(1900, 1, 1)
max_date = datetime.date.today()

def patient_exists(vorname, name, geburtsdatum):
    """
    Prüft, ob ein Patient mit demselben Namen und Geburtsdatum bereits existiert.
    """
    for p in st.session_state.patientenliste:
        if p.Vorname.lower() == vorname.lower() and \
           p.Name.lower() == name.lower() and \
           p.Geburtsdatum == geburtsdatum.strftime("%Y-%m-%d"):
            return True
    return False

def neuen_patient_hinzufuegen():
    with st.form("neuer_patient_form"):
        st.subheader("Neuen Patienten hinzufügen")
        st.write(f"Nächste verfügbare Patienten-ID: {st.session_state.next_patient_id}")

        col1, col2 = st.columns(2)
        with col1:
            Vorname = st.text_input("Vorname")
            Name = st.text_input("Name")
            Straße = st.text_input("Straße")
            Hausnummer = st.text_input("Hausnummer")
            Postleitzahl = st.text_input("Postleitzahl")
            Stadt = st.text_input("Stadt")
        with col2:
            Geburtsdatum = st.date_input("Geburtsdatum", min_value=min_date, max_value=max_date)
            Versicherung = st.text_input("Versicherung")
            Zusatzversicherung = st.text_input("Zusatzversicherung")
            Arzt = st.text_input("Behandelnder Arzt")
            email = st.text_input("E-Mail")
            Telefon = st.text_input("Telefonnummer")
        
        submitted = st.form_submit_button("Patient speichern")
        if submitted:
            if not Vorname or not Name:
                st.error("Bitte gib mindestens Vorname und Name ein.")
            elif patient_exists(Vorname, Name, Geburtsdatum):
                st.warning("Ein Patient mit diesem Namen und Geburtsdatum existiert bereits.")
            else:
                # Generiere automatische Patienten-ID
                patient_id = st.session_state.next_patient_id
                st.session_state.next_patient_id += 1

                neuer_patient = Patient(
                    ID=patient_id,
                    Vorname=Vorname,
                    Name=Name,
                    Geburtsdatum=Geburtsdatum.strftime("%Y-%m-%d"),
                    Straße=Straße,
                    Hausnummer=Hausnummer,
                    Postleitzahl=Postleitzahl,
                    Stadt=Stadt,
                    Versicherung=Versicherung,
                    Zusatzversicherung=Zusatzversicherung,
                    Arzt=Arzt,
                    email=email,
                    Telefon=Telefon
                )
                st.session_state.patientenliste.append(neuer_patient)
                speichere_patienten(st.session_state.patientenliste)
                st.success(f"Patient {Vorname} {Name} wurde erfolgreich hinzugefügt.")
    return []

# Funktion: Liste speichern
def speichere_patienten(patientenliste):
    try:
        serialized = [p.to_dict() for p in patientenliste]
        with open(PATIENTEN_JSON, "w", encoding="utf-8") as f:
            json.dump(serialized, f, indent=4)
    except Exception as e:
        st.error(f"Fehler beim Speichern der Patientendaten: {e}")


if 'next_patient_id' not in st.session_state:
    if st.session_state.patientenliste:
        st.session_state.next_patient_id = max(p.ID for p in st.session_state.patientenliste) + 1
    else:
        st.session_state.next_patient_id = 1


# Zeige Liste an

#zeige_patientenliste()

