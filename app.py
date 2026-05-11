import streamlit as st

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0b1324;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MAIN ----------------
st.title("🩺 AI Disease Prediction System")

if st.session_state.logged_in:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    st.markdown("""
    ## System Features

    - AI-based disease prediction
    - NLP symptom extraction
    - Weighted prediction engine
    - Healthcare dashboard
    - Prediction history
    - Emergency detection

    Open pages from sidebar.
    """)

else:

    st.warning(
        "Please login from sidebar pages."
    )
