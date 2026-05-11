import streamlit as st
from symptom_extractor import (
    extract,
    is_medical_input
)
from prediction_engine import predict_disease
from auth import save_history

# ---------------- LOGIN CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.warning("Please login first.")
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

.chat-box {
    background-color: #121a2b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}

.result-card {
    background-color: #101b32;
    padding: 20px;
    border-radius: 18px;
    margin-top: 20px;
    border-left: 5px solid #00ff99;
    box-shadow: 0px 0px 15px rgba(0,255,153,0.2);
}

.small-text {
    color: #aab4d6;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🩺 AI Health Assistant")

st.sidebar.success(
    f"Logged in as: {st.session_state.username}"
)

st.sidebar.markdown("---")

st.sidebar.info("""
### System Features
- NLP Symptom Extraction
- AI Disease Prediction
- Confidence Analysis
- Prediction History
- Emergency Detection
""")

# ---------------- MAIN TITLE ----------------
st.markdown(
    "<div class='main-title'>AI Healthcare Dashboard</div>",
    unsafe_allow_html=True
)

st.markdown("""
<div class='small-text'>
Enter symptoms naturally like talking to a doctor.
</div>
""", unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input(
    "Describe your symptoms..."
)

# ---------------- PROCESS ----------------
if user_input:

    # USER MESSAGE
    with st.chat_message("user"):

        st.write(user_input)

    # AI RESPONSE
    with st.chat_message("assistant"):

        try:

            if not is_medical_input(user_input):

                st.error(
                    "Please enter valid medical symptoms."
                )

            else:

                features = extract(user_input)

                predictions = predict_disease(features)

                st.markdown("""
                ## 🧠 AI Prediction Analysis
                """)

                colors = [
                    "#00ff99",
                    "#facc15",
                    "#ff4d4d"
                ]

                for i, result in enumerate(predictions):

                    disease = result["disease"]
                    confidence = result["confidence"]

                    st.markdown(f"""
                    <div class='result-card'>

                    <h2 style='color:{colors[i]};'>
                    {i+1}. {disease}
                    </h2>

                    <h4>
                    Confidence: {confidence}%
                    </h4>

                    </div>
                    """, unsafe_allow_html=True)

                # ---------------- CONFIDENCE LEVEL ----------------
                top_conf = predictions[0]["confidence"]

                if top_conf >= 80:

                    st.success(
                        "High probability prediction."
                    )

                elif top_conf >= 50:

                    st.warning(
                        "Moderate probability prediction."
                    )

                else:

                    st.info(
                        "Low probability prediction."
                    )

                # ---------------- EMERGENCY DETECTION ----------------
                if (
                    features["chest pain"]
                    and features["breathlessness"]
                ):

                    st.error("""
                    🚨 Emergency Alert

                    Possible severe respiratory or cardiac issue detected.
                    Seek immediate medical attention.
                    """)

                # ---------------- SAVE HISTORY ----------------
                save_history(
                    st.session_state.username,
                    {
                        "input": user_input,
                        "prediction": predictions
                    }
                )

                # ---------------- FINAL DISCLAIMER ----------------
                st.info("""
                This system is an AI-based healthcare assistant
                and not a replacement for professional medical diagnosis.
                """)

        except Exception as e:

            st.error("Prediction Error Occurred")
            st.exception(e)
