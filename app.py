import streamlit as st

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

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

h1, h2, h3 {
    color: white;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MAIN PAGE ----------------
st.title("🩺 AI Disease Prediction System")

st.markdown("""
## Welcome to the Next-Generation AI Healthcare Assistant

### Features:
- Intelligent disease prediction
- NLP-based symptom extraction
- Weighted hybrid prediction engine
- Advanced dashboard
- Secure authentication
- Prediction history
- Emergency detection
- Modern healthcare UI

Use the sidebar to navigate through the application.
""")

st.info("Open pages from the left sidebar.")
