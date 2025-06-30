import streamlit as st
def searchbar():
    """
    Creates a search bar for patient names.
    Returns the search term entered by the user.
    """
    st.markdown("### Suche nach Patienten")
    search_term = st.text_input("Geben Sie den Namen des Patienten ein:")
    return search_term.strip() if search_term else None


def show_patients_list(patients):
    """
    Displays a list of patients with their names and IDs.
    """
    st.markdown("### Patientenliste")
    if not patients:
        st.write("Keine Patienten gefunden.")
        return

    for patient in patients:
        st.write(f"**Name:** {patient['name']} | **ID:** {patient['id']}")
        st.markdown("---")  # Separator for each patient

#def create_patient():
