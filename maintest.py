import streamlit as st
from patientenkalender import show_patient_calendar
from patientseite import searchbar
from patientseite import show_patients_list

# Initialisiere Session State für den Modus und die Stage
if 'mode' not in st.session_state:
    st.session_state.mode = None

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
        st.button('Patienten', on_click=set_mode, args=['patient'], key='btn_patient')
    with col2:
        st.button('Kalender', on_click=set_mode, args=['kalender'], key='btn_kalender')

# Wenn Modus gewählt wurde, zeige entsprechenden Inhalt
else:
    if st.session_state.mode == 'patient':
        searchbar()

    elif st.session_state.mode == 'kalender':
        show_patient_calendar()

    # Zurück-Button
    st.button("Zurück zum Hauptmenü", on_click=go_back)
