
import streamlit as st
from patientenkalender import show_patient_calendar

from patientenkalender import show_patient_calendar
from patientseite import (
    suche_patienten,
    searchbar,
    zeige_suchergebnisse,
    zeige_patientenliste,
    neuen_patient_hinzufuegen,
    lade_patienten,
    speichere_patienten
)
from dokuseite import show_therapy_page


st.set_page_config(layout="wide")


if 'modus' not in st.session_state:
    st.session_state.modus = None

# Initialisiere Session State für den Modus und die Stage
if 'mode' not in st.session_state:
    st.session_state.mode = None

# Initialisiere selected_patient
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

if 'suchmodus' not in st.session_state:
    st.session_state.suchmodus = True  # Optional: Starte direkt im Suchmodus

if 'patientenliste' not in st.session_state:
    st.session_state.patientenliste = lade_patienten()


# Funktion zum Setzen des Modus
def set_mode(mode):
    st.session_state.mode = mode

# Funktion zum Zurückkehren zum Hauptmenü
def go_back():
    st.session_state.mode = None

# Stylisierte Buttons mit CSS
st.markdown("""
    <style>
    .stButton button {
        font-size: 2em;
        padding: 1em 0.5em;
        background: #6ec6ff;
        color: white;
        border: none;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        transition: background 0.3s;
        width: 100%;
    }
    .stButton button:hover {
        background: #42a5f5;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Titel anzeigen, nur wenn kein Modus aktiv ist
if st.session_state.mode is None:
    st.title("T-Doc: Hauptmenü")

    col1, col2 = st.columns(2)
    with col1:
        st.button('🧑‍⚕️ Patienten', on_click=set_mode, args=['patient'], key='btn_patient')
    with col2:
        st.button('📅 Kalender', on_click=set_mode, args=['kalender'], key='btn_kalender')

# Wenn Modus gewählt wurde, zeige entsprechenden Inhalt
elif st.session_state.mode == 'patient':

    # --- Suchmodus vs. Neuanlage ---
    if st.session_state.suchmodus:
        # Teil 1: Suchleiste + Suchergebnisse
        search_term = searchbar()
        gefundene_patienten = suche_patienten(search_term)

        if search_term is not None:
            if len(gefundene_patienten) > 0:
                zeige_suchergebnisse(gefundene_patienten)
                
            else:
                st.info("Keine Patienten gefunden.")
                
    neuen_patient_hinzufuegen()
    zeige_patientenliste()
    lade_patienten()
    speichere_patienten(patientenliste=st.session_state.patientenliste)
    st.button("⬅️ Zurück zum Hauptmenü", on_click=go_back, key= "back_main_menu_patient")

elif st.session_state.mode == 'kalender':
        show_patient_calendar()
        st.button("⬅️ Zurück zum Hauptmenü", on_click=go_back, key="back_main_menu_calendar")
    

elif st.session_state.mode == "patientenliste":
    # --- Suchmodus vs. Neuanlage ---
    if st.session_state.suchmodus:
        # Teil 1: Suchleiste + Suchergebnisse
        search_term = searchbar()
        gefundene_patienten = suche_patienten(search_term)

        if search_term is not None:
            if len(gefundene_patienten) > 0:
                zeige_suchergebnisse(gefundene_patienten)
                
            else:
                st.info("Keine Patienten gefunden.")
                
    neuen_patient_hinzufuegen()
    zeige_patientenliste()
    lade_patienten()
    speichere_patienten(patientenliste=st.session_state.patientenliste)
    st.button("Zurück zum Hauptmenü", on_click=go_back, key= "back_main_menu_patient")



elif st.session_state.mode == 'therapie_dokumentation':
    patient = st.session_state.selected_patient
    patient = st.session_state.get('selected_patient', None)  
    show_therapy_page(patient)
    