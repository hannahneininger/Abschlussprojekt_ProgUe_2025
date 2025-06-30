import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from Patientenseite_pietschi.backend_patientenseite import TherapySession, Patient, add_therapy_session, get_numeric_tendency, delete_therapy_session

# Initialisiere die Therapiesitzungen nur einmal
if "therapy_sessions" not in st.session_state:
    st.session_state.therapy_sessions = []

# Dummy-Patient
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

# Set page config
st.set_page_config(layout="wide")

left_col, right_col = st.columns([1, 3], gap="large")

# Linke Spalte: Patientendaten
with left_col:
    st.markdown("### Patientendaten")
    patient_info_html = "<div style='line-height:1.3;'>"
    for key, value in mein_patient.__dict__.items():
        patient_info_html += f"<div><strong>{key}:</strong> {value}</div>"
    patient_info_html += "</div>"
    st.markdown(patient_info_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tendenz")

    tendency_data = [s for s in st.session_state.therapy_sessions if s.tendency and s.tendency != ""]
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

# Rechte Spalte: Therapiedokumentation
with right_col:
    st.header("Therapiedokumentation")
    st.write("")

    # Button: Neue Therapiesitzung hinzufügen
    st.button(
        "Therapie-Sitzung hinzufügen",
        key="add_session",
        on_click=add_therapy_session,
        args=(mein_patient,)
    )

    # Zeige alle Therapiesitzungen an
    for idx, session in enumerate(st.session_state.therapy_sessions):
        displayed_date = getattr(session, 'displayed_date', session.date)
        expander_label = f"Therapie-Sitzung {displayed_date}"

        with st.expander(expander_label):
            # Layout: Form + Delete button side by side
            col1, col2 = st.columns([4, 1])

            with col1:
                st.text_input("Datum:", value=displayed_date, disabled=True)

                with st.form(key=f"form_{session.timestamp}"):
                    tendency_option = st.selectbox(
                        "Tendenz auswählen",
                        options=["", "Steigend", "Fallend", "Stagnierend"],
                        index=["", "Steigend", "Fallend", "Stagnierend"].index(session.tendency),
                        key=f"selectbox_{session.timestamp}"
                    )

                    documentation = st.text_area(
                        "Dokumentation",
                        value=session.documentation,
                        height=150,
                        key=f"text_area_{session.timestamp}"
                    )

                    # Use columns inside the form to align buttons
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        submitted = st.form_submit_button("Speichern")
                    with btn_col2:
                        if st.form_submit_button("🗑️ Löschen"):
                            delete_therapy_session(idx)
                            st.rerun()

                    if submitted:
                        session.tendency = tendency_option
                        session.documentation = documentation
                        st.success("✅ Änderungen gespeichert!")
                        st.rerun()

            with col2:
                # Optional: Add more actions here or keep empty
                pass

               