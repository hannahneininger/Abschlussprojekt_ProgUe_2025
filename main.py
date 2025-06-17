import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# Set page config
st.set_page_config(layout="wide")
from Patientenseite_State_2_2.Tendency_dropdown import TherapySession

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

st.session_state.therapy_session = []
st.session_state.therapy_session.append(TherapySession(
    date="2023-10-01",
    tendency="Steigend",
    patient=patient_attributes["Name"]
))

# Generate example tendency plot data
x = np.arange(0, 10, 1)
y = np.random.normal(loc=0.5, scale=0.1, size=10).cumsum()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")

def add_therapy_session():
    """Function to add a new therapy session."""
    # Here you would implement the logic to add a new session
    # For now, we just append a dummy session for demonstration
    new_session = TherapySession(
        date=datetime.now().strftime("%Y-%m-%d"),
        tendency="",
        patient=patient_attributes["Name"]
    )
    st.session_state.therapy_session.append(new_session)
    st.success("Neue Therapiesitzung hinzugefügt!")

# Layout: left colorblocked column, right main area
left_col, right_col = st.columns([1, 3], gap="large")

with left_col:
    st.markdown("### Patient Attributes")
    # Use HTML for compact, styled display
    patient_info_html = "<div style='line-height:1.3;'>"
    for key, value in patient_attributes.items():
        patient_info_html += f"<div><strong>{key}:</strong> {value}</div>"
    patient_info_html += "</div>"
    st.markdown(patient_info_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tendency Plot")
    fig, ax = plt.subplots(figsize=(2.2, 1.2))  # narrower plot
    ax.plot(x, y, marker='o')
    ax.set_title("Tendency Over Time", fontsize=10)
    ax.set_xlabel("Time", fontsize=8)
    ax.set_ylabel("Value", fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=7)
    plt.tight_layout(pad=1.0)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
# End colorblocked background in left_col
# Main content in right_col

with right_col:
    st.header("Therapiedokumentation")
    st.write("Hier könnte ihr Text stehen.")
    st.button("Therapie-Sitzung hinzufügen", key="add_session", on_click=add_therapy_session)
    # use the button to add a new therapy session

    for session in st.session_state.therapy_session:
       
        with st.expander("Therapie-Sitzung " + str(session.date)):
            st.write('''
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            ''')
            st.text_input(f"**Datum:** {session.date}")
            st.text_input(f"**Tendenz:** {session.tendency}")

if __name__ == "__main__":
    st.write("")
    # You can add more functionality here if needed