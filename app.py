import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="AI Health Assistant",
page_icon="🩺",
layout="wide"
)

# ---------------- SESSION ----------------

if "page" not in st.session_state:
st.session_state.page = "register"

if "logged_in" not in st.session_state:
st.session_state.logged_in = False

st.title("🩺 AI Health Assistant")

st.success("App Loaded Successfully")
