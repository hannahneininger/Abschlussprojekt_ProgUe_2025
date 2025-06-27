import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# Set page config
st.set_page_config(layout="wide")
from Patientenseite_pietschi.backend_patientenseite import TherapySession
from Patientenseite_pietschi.backend_patientenseite import create_tendency_dropdown 

#PatientenDaten
patient_attributes = {
    "Name": "Neininger",
    "Vorname": "Hannobert",
    "Geburtsdatum": "01.01.1990",
    "Straße": "Hauptstraße",
    "Hausnummer": 12,
    "PLZ": 12345,
    "Stadt": "Musterstadt",
    "Versicherung": "Gesetzlich",
    "Zusatzversicherung": True,
    "Arzt": "Dr. Schmidt",
    "Email": "hannobert.neini@example.com"
}

if "therapy_session" not in st.session_state:
    st.session_state.therapy_session = []

# Add an example session if none exists
#if not st.session_state.therapy_session:
#    st.session_state.therapy_session.append(
#        TherapySession(date="2023-10-01", tendency="Steigend", patient=patient_attributes["Name"])
#    )

def add_therapy_session():
    """Add a new therapy session with today's date."""
    today = datetime.now().strftime("%Y-%m-%d")
    # Prevent duplicate dates
    existing_dates = [session.date for session in st.session_state.therapy_session]
    if today in existing_dates:
        st.warning("Für heute wurde bereits eine Therapiesitzung erfasst.")
    else:
        new_session = TherapySession(date=today, tendency="", patient=patient_attributes["Name"])
        st.session_state.therapy_session.append(new_session)
        st.success(f"Neue Therapiesitzung für {today} hinzugefügt!")

def add_therapy_session():
    """Neue Therapiesitzung hinzufügen."""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Prevent duplicate dates? (Optional)
    existing_dates = [session.date for session in st.session_state.therapy_session]
    if today in existing_dates:
        st.warning("Für heute wurde bereits eine Therapiesitzung erfasst.")
    else:
        new_session = TherapySession(
            date=today,
            tendency="",
            patient=patient_attributes["Name"],
            timestamp=timestamp
        )
        st.session_state.therapy_session.append(new_session)
        st.success(f"Neue Therapiesitzung für {today} hinzugefügt!")

def get_numeric_tendency(tendency):
    tendency_map = {"Steigend": 1, "Stagnierend": 0, "Fallend": -1}
    return tendency_map.get(tendency, None)

# Generate example tendency plot data
x = np.arange(0, 10, 1)
y = np.random.normal(loc=0.5, scale=0.1, size=10).cumsum()

# Function to load local CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("layout.css")

# Layout: left colorblocked column, right main area
left_col, right_col = st.columns([1, 3], gap="large")

with left_col:
    st.markdown("### Patientendaten")
    patient_info_html = "<div style='line-height:1.3;'>"
    for key, value in patient_attributes.items():
        patient_info_html += f"<div><strong>{key}:</strong> {value}</div>"
    patient_info_html += "</div>"
    st.markdown(patient_info_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tendenz")

    # Plotting tendency over time
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
# End colorblocked background in left_col

# Main content in right_col
with right_col:
    st.header("Therapiedokumentation")
    st.write("Soll hier noch was stehen?")
    st.button("Therapie-Sitzung hinzufügen", key="add_session", on_click=add_therapy_session)

    for idx, session in enumerate(st.session_state.therapy_session):
        expander_label = f"Therapie-Sitzung {session.date}"
        with st.expander(expander_label):
            with st.form(key=f"form_{session.timestamp}"):
                st.write('''
                    Dokumentiere die heutige Therapieeinheit. Vergiss nicht das pre- and post-Testing und die Tendenz der Therapie zu notieren.
                ''')

                st.text_input("Datum:", value=session.date, disabled=True)

                # Dropdown 
                tendency_option = st.selectbox(
                    "Tendenz auswählen",
                    options=["Steigend", "Fallend", "Stagnierend"],
                    index=0 if session.tendency == "" else ["Steigend", "Fallend", "Stagnierend"].index(session.tendency),
                    key=f"selectbox_{session.timestamp}"
                )

                # dokufeld
                documentation = st.text_area(
                    "Therapie-Beschreibung / Notizen",
                    value=session.documentation if hasattr(session, 'documentation') else "",
                    height=150,
                    key=f"text_area_{session.timestamp}",
                    help="Hier können Sie zusätzliche Informationen zur Therapiesitzung eingeben."
                )

                submitted = st.form_submit_button("Speichern")
                if submitted:
                    # Save tendency and documentation back to session
                    session.tendency = tendency_option
                    session.documentation = documentation  # Make sure your TherapySession class supports this
                    st.success(f"Tendenz für {session.date} gespeichert: {tendency_option}")

if __name__ == "__main__":
    st.write("")

## GANZ DRINGEN AUTOMATISCHE AKTUALISIERUNG BEI SUBMISSION