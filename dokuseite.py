import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
#from streamlit import experimental_rerun 

# Set page config
st.set_page_config(layout="wide")
from Patientenseite_pietschi.backend_patientenseite import TherapySession,  Patient
from Patientenseite_pietschi.backend_patientenseite import add_therapy_session, get_numeric_tendency


#
mein_patient = Patient(
    Name="Neininger",
    Vorname="Hannobert",
    Geburtsdatum="01.01.1990",
    Straße="Hauptstraße",
    Hausnummer=12,
    Postleitzahl=12345,
    Stadt="Musterstadt",
    Versicherung="Gesetzlich",
    Zusatzversicherung=True,
    Arzt="Dr. Schmidt",
    email="hannobert.neini@example.com",
    Telefon=1234567890
)

## Layout Load CSS
def local_css(layout_css):
    with open(layout_css) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("layout.css")

left_col, right_col = st.columns([1, 3], gap="large")

# linke Seite

if "therapy_session" not in st.session_state:
    st.session_state.therapy_session = []

with left_col:
    st.markdown("### Patientendaten")
    patient_info_html = "<div style='line-height:1.3;'>"
    for key, value in mein_patient.__dict__.items():
        patient_info_html += f"<div><strong>{key}:</strong> {value}</div>"
    patient_info_html += "</div>"
    st.markdown(patient_info_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tendenz")

    tendency_data = [
        s for s in st.session_state.therapy_session if s.tendency and s.tendency != ""
    ]
    if tendency_data:
        times = [s.date for s in tendency_data]
        numeric_tendencies = [get_numeric_tendency(s.tendency) for s in tendency_data]

        fig, ax = plt.subplots(figsize=(2.2, 1.2))
        ax.plot(times, numeric_tendencies, marker='x', linestyle='-', color='blue')
        ax.set_title("Tendenzverlauf", fontsize=8)
        ax.set_xlabel("Zeit", fontsize=6)
        ax.set_ylabel("Wert", fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=5)
        ax.set_ylim(-1.1, 1.1)
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
    else:
        st.write("Keine Tendenzen gespeichert.")

with right_col:
    st.header("Therapiedokumentation")
    st.write("Soll hier noch was stehen?")
    st.button(
        "Therapie-Sitzung hinzufügen", 
        key="add_session", 
        on_click=add_therapy_session, 
        args=(mein_patient,)
    )

    for idx, session in enumerate(st.session_state.therapy_session):
        expander_label = f"Therapie-Sitzung {session.date}"
        with st.expander(expander_label):
            with st.form(key=f"form_{session.timestamp}"):
                st.write('''
                    Dokumentiere die heutige Therapieeinheit. Vergiss nicht das pre- and post-Testing und die Tendenz der Therapie zu notieren.
                ''')

                st.text_input("Datum:", value=session.date, disabled=True)

                tendency_option = st.selectbox(
                    "Tendenz auswählen",
                    options=["Steigend", "Fallend", "Stagnierend"],
                    index=0 if session.tendency == "" else ["Steigend", "Fallend", "Stagnierend"].index(session.tendency),
                    key=f"selectbox_{session.timestamp}"
                )

                documentation = st.text_area(
                    "Therapie-Beschreibung / Notizen",
                    value=session.documentation if hasattr(session, 'documentation') else "",
                    height=150,
                    key=f"text_area_{session.timestamp}",
                    help="Hier können Sie zusätzliche Informationen zur Therapiesitzung eingeben."
                )

                submitted = st.form_submit_button("Speichern")
                if submitted:
                    session.tendency = tendency_option
                    session.documentation = documentation
                    st.success(f"Änderungen gespeichert!")
                    st.rerun()

if __name__ == "__main__":
    pass