import streamlit as st

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# Session Variables
if "page" not in st.session_state:
    st.session_state.page = "register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🩺 AI Health Assistant")

st.success("Session Initialized Successfully")

st.write("Current Page:", st.session_state.page)
st.write("Logged In:", st.session_state.logged_in)
