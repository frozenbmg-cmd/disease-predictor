import streamlit as st

st.set_page_config(
    page_title="About",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CONTENT ----------------
st.title("ℹ️ About Project")

st.markdown("""
# AI Disease Prediction System

This project is an advanced AI-based healthcare assistant
developed using:

- Python
- Streamlit
- NLP-based Symptom Extraction
- Weighted Hybrid Prediction System

---

## Features

- Real-time disease prediction
- Smart symptom analysis
- Chatbot-style interaction
- Prediction history
- Emergency detection
- Confidence scoring
- Professional dashboard

---

## Developed By

- Bharath M Gowda
- Mohammed Kasim G
""")
