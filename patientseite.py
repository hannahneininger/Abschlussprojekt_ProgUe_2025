import streamlit as st
import datetime


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



from Patientenseite_pietschi.backend_patientenseite import Patient

# Liste zum Speichern der Patienten
if 'patientenliste' not in st.session_state:
    st.session_state.patientenliste = []

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
            if st.button(f"Auswählen", key=f"btn_selcet_{idx}"):
                st.session_sate.selected_patient = patient
                st.experimental_rerun()

        st.markdown("---")

          
min_date = datetime.date(1900, 1, 1)
max_date = datetime.date.today()

def neuen_patient_hinzufuegen():
    with st.form("neuer_patient_form"):
        st.subheader("Neuen Patienten hinzufügen")

        # zeige nächste verfügbare Patienten-ID
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
            else:
                 # Generiere automatische Patienten-ID
                patient_id = st.session_state.next_patient_id
                st.session_state.next_patient_id += 1  # Erhöhe für nächsten Patienten
               
                neuer_patient = Patient(
                    ID =patient_id,
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
                st.success(f"Patient {Vorname} {Name} wurde hinzugefügt.")
# Zeige Liste an
#zeige_patientenliste()
