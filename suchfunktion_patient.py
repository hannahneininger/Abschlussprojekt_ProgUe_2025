import streamlit as st
def searchbar():
    """
    Creates a search bar for patient names.
    Returns the search term entered by the user.
    """
    st.markdown("### Suche nach Patienten")
    search_term = st.text_input("Geben Sie den Namen des Patienten ein:")
    return search_term.strip() if search_term else None
