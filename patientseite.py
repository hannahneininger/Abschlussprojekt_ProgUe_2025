import streamlit as st
def searchbar():
    """
    Creates a search bar for patient names.
    Returns the search term entered by the user.
    """
    st.markdown("### Suche nach Patienten")
    search_term = st.text_input("Geben Sie den Namen des Patienten ein:")
    return search_term.strip() if search_term else None

from Patientenseite_pietschi.backend_patientenseite import Patient

# Liste zum Speichern der Patienten
if 'patientenliste' not in st.session_state:
    st.session_state.patientenliste = []

def zeige_patientenliste():
    st.subheader("Liste aller Patienten")
    if len(st.session_state.patientenliste) == 0:
        st.info("Keine Patienten vorhanden.")
    else:
        for idx, patient in enumerate(st.session_state.patientenliste):
            st.markdown(f"**{idx + 1}. {patient}**")

def neuen_patient_hinzufuegen():
    with st.form("neuer_patient_form"):
        st.subheader("Neuen Patienten hinzufügen")

        col1, col2 = st.columns(2)
        with col1:
            Vorname = st.text_input("Vorname")
            Name = st.text_input("Name")
            Geburtsdatum = st.date_input("Geburtsdatum")
            Straße = st.text_input("Straße")
            Hausnummer = st.text_input("Hausnummer")
            Postleitzahl = st.text_input("Postleitzahl")
            Stadt = st.text_input("Stadt")
        with col2:
            Versicherung = st.text_input("Versicherung")
            #patient_id = st.number_input("Patienten-ID", min_value=1, step=1)
            Zusatzversicherung = st.text_input("Zusatzversicherung")
            Arzt = st.text_input("Behandelnder Arzt")
            email = st.text_input("E-Mail")
            Telefon = st.text_input("Telefonnummer")
        
        submitted = st.form_submit_button("Patient speichern")
        if submitted:
            if not Vorname or not Name:
                st.error("Bitte gib mindestens Vorname und Name ein.")
            else:
                neuer_patient = Patient(
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
