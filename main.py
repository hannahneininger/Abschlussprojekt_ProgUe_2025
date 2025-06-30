import streamlit as st
from patientenkalender import show_patient_calendar
from patientseite import searchbar  


# Hauptmenü für T-Doc

st.title("T-Doc: Hauptmenü")
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'mode' not in st.session_state:
    st.session_state.mode = None

def set_mode(mode):
    st.session_state.mode = mode
    st.session_state.stage = 1

# Auswahl Buttons
col1, col2 = st.columns(2)
with col1:
    st.button('Patienten', on_click=set_mode, args=['patient'], key='patient_btn', use_container_width=True)
with col2:
    st.button('Kalender', on_click=set_mode, args=['kalender'], key='kalender_btn', use_container_width=True)

# Optional: Button-Text größer machen mit CSS
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
    }
    .stButton button:hover {
        background: #42a5f5;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def go_back():
    st.session_state.button_clicked = None

# Anzeige je nach Auswahl
if st.session_state.mode == 'patient' and st.session_state.stage == 1:
    searchbar()
elif st.session_state.mode == 'kalender' and st.session_state.stage == 1:
    show_patient_calendar()
    st.button("Zurück zum Hauptmenü", on_click=go_back)



