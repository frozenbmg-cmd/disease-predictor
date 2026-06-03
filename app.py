import streamlit as st
from auth import register, login, save_history, get_history
from symptom_extractor import extract, is_medical_input
from prediction_engine import predict_disease
from datetime import datetime
import time


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Healthcare Assistant",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:#050816;
}

.hero-section{
    padding:30px;
    border-radius:20px;
    background:linear-gradient(135deg,#0f172a,#1e293b);
    text-align:center;
    margin-bottom:25px;
}

.hero-title{
    font-size:48px;
    font-weight:bold;
    color:white;
    margin-bottom:10px;
}

.hero-subtitle{
    color:#cbd5e1;
    font-size:18px;
    line-height:1.6;
}

.chat-input-container{
    background:#101b32;
    padding:20px;
    border-radius:18px;
    border:2px solid #1e293b;
    margin-top:10px;
}

.ai-response{
    background:#0f172a;
    padding:20px;
    border-radius:15px;
    margin-top:10px;
    border-left:4px solid #00ff99;
}

.prediction-card{
    background:#101b32;
    padding:25px;
    border-radius:18px;
    margin-top:15px;
    border-left:6px solid;
}

.risk-low{
    border-left-color:#00ff99;
}

.risk-moderate{
    border-left-color:#facc15;
}

.risk-high{
    border-left-color:#ff4d4d;
}

.disease-name{
    font-size:32px;
    font-weight:bold;
    margin-bottom:15px;
}

.confidence-badge{
    font-size:24px;
    font-weight:bold;
    margin-bottom:15px;
}

.specialist-label{
    color:#9ca3af;
    font-size:14px;
    margin-top:15px;
}

.health-tip{
    background:#0f172a;
    padding:15px;
    border-radius:10px;
    margin-top:10px;
    border-left:3px solid #00ff99;
    color:#cbd5e1;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================================================
# REGISTER PAGE
# =====================================================
if (
    st.session_state.page == "register"
    and not st.session_state.logged_in
):

    st.title("🩺 AI Health Assistant")
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )
    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if password != confirm:

            st.error(
                "Passwords do not match"
            )

        elif register(username, password):

            st.success(
                "Registration Successful"
            )

            st.session_state.page = "login"

            st.rerun()

        else:

            st.error(
                "Username already exists"
            )

    st.write("---")

    st.write(
        "Already have an account?"
    )

    if st.button("Go to Login"):

        st.session_state.page = "login"

        st.rerun()

# =====================================================
# LOGIN PAGE
# =====================================================
elif (
    st.session_state.page == "login"
    and not st.session_state.logged_in
):

    st.title("🔐 Login")

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button("Login"):

        if login(username, password):

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )

    st.write("---")

    st.write("New user?")

    if st.button("Create Account"):

        st.session_state.page = "register"

        st.rerun()

# =====================================================
# MAIN APPLICATION
# =====================================================
elif st.session_state.logged_in:

    st.markdown("""
    <div class='hero-section'>
    <div class='hero-title'>🩺 AI Healthcare Assistant</div>
    <div class='hero-subtitle'>
    Analyze symptoms, predict possible diseases,<br>
    receive doctor recommendations and health insights.
    </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])

    with col1:
        st.success(
            f"Welcome {st.session_state.username}"
        )

    with col2:

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.page = "login"

            st.rerun()

    st.write("---")

    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:

        st.markdown("""
        ### 💬 Describe Your Symptoms
        """)

        symptoms = st.text_area(
            "",
            placeholder="Describe your symptoms naturally...\n\nExample:\nI have had fever, headache and body pain for 2 days.",
            height=150
        )

        if st.button("🔍 Analyze Symptoms", use_container_width=True):

            if not is_medical_input(symptoms):

                st.error(
                    "Please enter valid medical symptoms."
                )

            else:

                with st.spinner("🤖 AI is analyzing symptoms..."):
                    time.sleep(1.5)

                features = extract(symptoms)
                detected_symptoms = [k for k, v in features.items() if v]

                st.markdown("""
                <div class='ai-response'>

                🤖 <b>AI Assistant</b>

                I analyzed your symptoms and detected:

                """ + "".join([f"<br>• {symptom.title()}" for symptom in detected_symptoms]) + """

                <br><br>Checking against medical knowledge base...

                </div>
                """, unsafe_allow_html=True)

                # Emergency Alert
                if (
                    features.get("chest pain")
                    and features.get("breathlessness")
                ):

                    st.markdown("""
                    <div style="
                    background:#3d1f1f;
                    padding:20px;
                    border-radius:15px;
                    border-left:6px solid #ff4d4d;
                    margin-top:15px;
                    ">

                    <div style="color:#ff4d4d;font-size:20px;font-weight:bold;">
                    🚨 CRITICAL HEALTH ALERT
                    </div>

                    <div style="color:#cbd5e1;margin-top:10px;">
                    <b>Detected combination:</b>
                    <br>• Chest Pain
                    <br>• Breathlessness
                    </div>

                    <div style="color:#cbd5e1;margin-top:10px;">
                    <b>Potential Concern:</b>
                    <br>• Severe Respiratory Condition
                    <br>• Cardiac Issue
                    </div>

                    <div style="color:#ff4d4d;margin-top:10px;font-weight:bold;">
                    ⚠️ Action Required: Consult a doctor immediately.
                    </div>

                    </div>
                    """, unsafe_allow_html=True)

                predictions = predict_disease(
                    features
                )

                st.markdown("---")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Symptoms Found",
                    len(detected_symptoms)
                )

                col2.metric(
                    "Diseases Checked",
                    25
                )

                col3.metric(
                    "Top Match",
                    predictions[0]["disease"]
                )

                col4.metric(
                    "Confidence",
                    f"{predictions[0]['confidence']}%"
                )

                st.markdown("---")

                health_tips = {
                    "Flu": "Stay hydrated and get adequate rest. Avoid contact with others.",
                    "Dengue": "Drink fluids and monitor platelet levels regularly.",
                    "Asthma": "Avoid dust, smoke and allergens. Use prescribed inhalers.",
                    "Food Poisoning": "Consume oral rehydration solutions and bland food.",
                    "Pneumonia": "Get adequate rest and stay hydrated. Take antibiotics if prescribed.",
                    "Migraine": "Avoid bright lights and get proper rest in a quiet room.",
                    "Vertigo": "Avoid sudden movements and stay hydrated.",
                    "Gastritis": "Avoid spicy food, caffeine and acidic drinks.",
                    "IBS": "Maintain a balanced diet with adequate fiber.",
                    "Allergy": "Identify and avoid allergens. Use antihistamines if needed.",
                    "Eczema": "Keep skin moisturized and avoid irritants.",
                    "Fungal Infection": "Keep affected area dry and clean.",
                    "Diabetes": "Monitor blood sugar levels regularly and exercise.",
                    "Hypertension": "Reduce salt intake and exercise regularly.",
                    "Bronchitis": "Stay hydrated and avoid smoke and pollution."
                }

                for i, pred in enumerate(predictions):

                    colors = ["#00ff99", "#facc15", "#ff4d4d"]
                    risk_levels = ["Low", "Moderate", "High"]
                    risk_class = ["risk-low", "risk-moderate", "risk-high"][i]

                    st.markdown(f"""
                    <div class='prediction-card {risk_class}'>

                    <div style="display:flex;justify-content:space-between;align-items:start;">

                    <div class='disease-name' style="color:{colors[i]};">
                    {i+1}. {pred['disease']}
                    </div>

                    <div style="background:{colors[i]};color:black;padding:8px 16px;border-radius:20px;font-weight:bold;">
                    {risk_levels[i]} Risk
                    </div>

                    </div>

                    <div class='confidence-badge' style="color:{colors[i]};">
                    Confidence: {pred['confidence']}%
                    </div>

                    <div style="color:#9ca3af;font-size:16px;">
                    <b>👨‍⚕️ Recommended Specialist:</b><br>
                    {pred['doctor']}
                    </div>

                    <div style="color:#cbd5e1;margin-top:15px;">
                    <b>📋 Recommendation:</b><br>
                    Schedule a consultation with {pred['doctor'].lower()} for proper evaluation.
                    </div>

                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class='health-tip'>
                    💡 <b>Health Tip:</b> {health_tips.get(pred['disease'], 'Maintain healthy habits and consult healthcare professional.')}
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("")

                save_history(
                    st.session_state.username,
                    {
                        "input": symptoms,
                        "prediction": predictions,
                        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
                    }
                )

    with right_col:

        st.markdown("""
        ### 📊 Quick Stats
        """)

        st.metric("Predictions Made", "0", delta=None)

        st.write("")

        st.markdown("""
        ### 📋 Assessment History
        """)

        if st.button("📜 View History", use_container_width=True):

            history = get_history(
                st.session_state.username
            )

            if not history:

                st.info(
                    "No assessment history yet."
                )

            else:

                for item in reversed(history[:5]):

                    timestamp = item.get(
                        "timestamp",
                        "N/A"
                    )

                    st.markdown(f"""
                    <div style="
                    background:#101b32;
                    padding:12px;
                    border-radius:10px;
                    margin-top:8px;
                    ">

                    <div style="color:#00ff99;font-size:12px;font-weight:bold;">
                    {timestamp}
                    </div>

                    <div style="color:#cbd5e1;font-size:12px;margin-top:5px;">
                    {item['input'][:50]}...
                    </div>

                    <div style="color:#facc15;font-size:12px;margin-top:5px;">
                    Top: {item['prediction'][0]['disease']}
                    </div>

                    </div>
                    """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        ### 🚀 Features Coming Soon

        • PDF Reports
        • Hospital Booking
        • AI Chatbot
        • Voice Input
        • Multi-language
        """)

    st.markdown("---")

    st.markdown("""
    <center style="color:#9ca3af;">

    🏥 AI Healthcare Assistant

    Developed using Python, Streamlit and AI-based Weighted Symptom Matching.

    <br>

    Bharath M Gowda (1NH24CS040)

    Mohammed Kasim G (1NH25CS416)

    © 2026

    </center>
    """, unsafe_allow_html=True)
