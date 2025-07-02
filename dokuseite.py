import streamlit as st
import matplotlib.pyplot as plt
from Patientenseite_pietschi.backend_patientenseite import TherapySession, Patient, add_therapy_session, get_numeric_tendency, delete_therapy_session

import os
from datetime import datetime
#from streamlit import experimental_rerun 
from patientenkalender import show_patient_calendar

import json

# 1. Speichere alle TherapySessions in einer JSON-Datei
def save_therapy_sessions_to_file(filename="therapy_sessions.json"):
    with open(filename, "w") as f:
        json.dump([s.to_dict() for s in st.session_state.therapy_sessions], f, indent=4)

def load_therapy_sessions_from_file(filename="therapy_sessions.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return [TherapySession.from_dict(d) for d in data]
    else:
        return []

if "therapy_sessions" not in st.session_state:
    st.session_state.therapy_sessions = []

  
def show_therapy_page(mein_patient=None):
    
    if 'therapy_sessions' not in st.session_state:
        st.session_state.therapy_sessions = load_therapy_sessions_from_file()

    """Zeigt die Therapiedokumentation für den ausgewählten Patienten an."""
    if mein_patient is None:
        mein_patient = Patient(
            Name="Mustermann",
            Vorname="Max",
            Geburtsdatum="01.01.1980",
            Straße="Musterstraße",
            Hausnummer="1",
            Postleitzahl="12345",
            Stadt="Musterstadt",
            Versicherung="AOK",
            Arzt="Dr. med. Beispiel"
        )
        st.info("Es wird ein Testpatient angezeigt.")

    
    
    st.title(f"Therapiedokumentation für {mein_patient.Vorname} {mein_patient.Name}")

    # Spaltenlayout
    left_col, right_col = st.columns([1, 3], gap="large")

    # def local_css(file_name):
    #     with open(file_name) as f:
    #         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # local_css("layout.css")
    # Linke Spalte: Patientendaten
    with left_col:
        st.markdown("### 👤 Patientendaten")
        patient_info_html = "<div style='line-height:1.3;'>"
        for key, value in mein_patient.__dict__.items():
            patient_info_html += f"<div><strong>{key}:</strong> {value}</div>"
        patient_info_html += "</div>"
        st.markdown(patient_info_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📈 Tendenz")

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
        st.header("📁 Therapiedokumentation")
        st.write("")

        st.markdown("### 📝 Anamnese")

        # Hole aktuelle Anamnese aus session_state oder leere Zeichenkette
        anamnese_key = f"anamnese_{mein_patient.ID}"
        if anamnese_key not in st.session_state:
            st.session_state[anamnese_key] = getattr(mein_patient, "Anamnese", "")

        anamnese_text = st.text_area(
            "Speichern mit Strg+Enter",
            value=st.session_state[anamnese_key],
            height=150,
            key=f"anamnese_input_{mein_patient.ID}",
            help="Diese Anamneseinformation wird für diesen Patienten gespeichert."
        )

    # Speichere die Anamnese direkt, wenn sich etwas geändert hat
        if anamnese_text != st.session_state[anamnese_key]:
            st.session_state[anamnese_key] = anamnese_text
            mein_patient.Anamnese = anamnese_text  # Optional: speichere es auch im Patientenobjekt
            st.success("✅ Anamnese gespeichert.")
            st.rerun()  # Optional: um Erfolgsmeldung sofort zu zeigen


        st.button(
            "Therapie-Sitzung hinzufügen",
            key="add_session",
            on_click=add_therapy_session,
            args=(mein_patient,)
        )

        for idx, session in enumerate(st.session_state.therapy_sessions):

                # Sicherstellen, dass es wirklich eine TherapySession ist
            if not isinstance(session, TherapySession):
                st.error(f"Fehler: Ungültiger Sitzungs-Typ in session_state gefunden! Typ: {type(session)}")
                continue
            displayed_date = getattr(session, 'displayed_date', session.date)
            expander_label = f"Therapie-Sitzung {displayed_date}"

            with st.expander(expander_label):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.text_input("Datum:", value=session.displayed_date, disabled=True)

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
                        
                        submitted_save = st.form_submit_button("💾 Speichern", use_container_width=True)
                        
                        submitted_delete = st.form_submit_button("🗑️ Löschen", use_container_width=True)
                            
                        if submitted_delete:
                            delete_therapy_session(idx)  # Diese Funktion kommt aus dem Import!
                            st.success("Sitzung gelöscht.")
                            st.rerun()

                        if submitted_save:
                            session.tendency = tendency_option
                            session.documentation = documentation
                            st.markdown('<div class="success-message">✅ Änderungen gespeichert!</div>', unsafe_allow_html=True)
                            st.rerun()

                

                with col2:
                    pass  # Optional: weitere Aktionen
    
    if st.button("⬅️ Zurück zur Patientenliste", key="btn_back_to_list"):
        st.session_state.pop('selected_patient', None)
        st.session_state.mode = "patientenliste"  # ODER wie auch immer dein Modus heißt
        st.rerun()
        
                    
if __name__ == "__main__":
    show_therapy_page()


    

