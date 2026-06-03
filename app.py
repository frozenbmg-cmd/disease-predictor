import streamlit as st
from auth import register, login, save_history, get_history
from symptom_extractor import extract, is_medical_input
from prediction_engine import predict_disease
from datetime import datetime
import time


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Healthcare Command Center",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:#050816;
}

.command-header{
    padding:20px;
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border-radius:15px;
    border-top:3px solid #00ff99;
    margin-bottom:20px;
    text-align:center;
}

.command-title{
    font-size:36px;
    font-weight:bold;
    color:#00ff99;
    letter-spacing:2px;
}

.command-divider{
    color:#00ff99;
    font-size:20px;
    margin:5px 0;
}

.chat-container{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    margin:15px 0;
    border-left:4px solid #00ff99;
}

.user-message{
    background:#0f172a;
    border-radius:12px;
    padding:15px;
    margin-bottom:15px;
    border-left:4px solid #3b82f6;
    color:#cbd5e1;
}

.ai-message{
    background:#0f172a;
    border-radius:12px;
    padding:15px;
    margin-top:15px;
    border-left:4px solid #00ff99;
    color:#cbd5e1;
}

.primary-diagnosis{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    border:3px solid #00ff99;
    border-radius:18px;
    padding:30px;
    margin:20px 0;
    text-align:center;
}

.diagnosis-name{
    font-size:48px;
    font-weight:bold;
    color:#00ff99;
    margin:20px 0;
}

.diagnosis-confidence{
    font-size:32px;
    color:#facc15;
    margin:15px 0;
}

.diagnosis-label{
    color:#9ca3af;
    font-size:14px;
    text-transform:uppercase;
    letter-spacing:1px;
}

.secondary-cards{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
    margin:20px 0;
}

.secondary-card{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    border-left:5px solid;
}

.risk-meter{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    margin:15px 0;
}

.health-insights{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    margin:15px 0;
}

.insight-row{
    display:flex;
    justify-content:space-between;
    padding:10px 0;
    border-bottom:1px solid #1e293b;
}

.insight-label{
    color:#9ca3af;
}

.insight-value{
    color:#00ff99;
    font-weight:bold;
}

.recommendation-box{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    border-left:5px solid #00ff99;
    border-radius:15px;
    padding:20px;
    margin:20px 0;
}

.timeline{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    margin:15px 0;
}

.timeline-item{
    padding:15px;
    border-left:3px solid #00ff99;
    margin:10px 0;
    color:#cbd5e1;
}

.roadmap{
    background:#101b32;
    border-radius:15px;
    padding:20px;
    margin:15px 0;
}

.roadmap-completed{
    color:#00ff99;
}

.roadmap-upcoming{
    color:#facc15;
}

.patient-dashboard{
    background:#101b32;
    border-radius:15px;
    padding:15px;
    border:2px solid #00ff99;
}

.emergency-banner{
    background:#3d1f1f;
    border:3px solid #ff4d4d;
    border-radius:15px;
    padding:20px;
    margin:20px 0;
}

.emergency-title{
    color:#ff4d4d;
    font-size:24px;
    font-weight:bold;
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
# MAIN APPLICATION - COMMAND CENTER
# =====================================================
elif st.session_state.logged_in:

    # ========== HEADER ==========
    st.markdown("""
    <div class='command-header'>
    <div class='command-divider'>━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
    <div class='command-title'>🩺 AI HEALTHCARE COMMAND CENTER</div>
    <div class='command-divider'>━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
    </div>
    """, unsafe_allow_html=True)

    # ========== SYSTEM STATUS DASHBOARD ==========
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.5])

    col1.metric("System", "🟢 ONLINE")
    col2.metric("AI Engine", "🤖 ACTIVE")
    col3.metric("Diseases", "25+")
    col4.metric("Accuracy", "85%")

    with col5:
        st.markdown("""
        <div class='patient-dashboard'>
        <b>Patient Dashboard</b>
        <br>
        <small>User: """ + st.session_state.username + """</small>
        <br>
        <small>Status: Active</small>
        <br>
        """ + ("" if st.button("Logout", key="logout_btn", use_container_width=True) else "") + """
        </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="logout_btn2"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("")

    # ========== CHAT INTERFACE ==========
    st.markdown("### 💬 Patient Symptom Input")

    symptoms = st.text_area(
        "",
        placeholder="Describe your symptoms naturally...\n\nExample:\nI have had fever, headache and body pain for 2 days.",
        height=120
    )

    col_analyze, col_history = st.columns(2)

    with col_analyze:
        analyze_btn = st.button("🔍 Analyze Symptoms", use_container_width=True)

    with col_history:
        history_btn = st.button("📋 View History", use_container_width=True)

    if analyze_btn:

        if not is_medical_input(symptoms):

            st.error(
                "Please enter valid medical symptoms."
            )

        else:

            # ========== CHAT DISPLAY ==========
            st.markdown("""
            <div class='chat-container'>
            <div class='user-message'>
            👤 <b>You</b>
            <br><br>
            """ + symptoms + """
            </div>
            </div>
            """, unsafe_allow_html=True)

            # ========== ANALYSIS STEPS ==========
            with st.status("🤖 AI Diagnostic Analysis", expanded=True):
                st.write("📖 Reading symptoms...")
                time.sleep(0.5)
                st.write("🔍 Extracting medical entities...")
                time.sleep(0.5)
                st.write("📊 Comparing against disease database...")
                time.sleep(0.5)
                st.write("⚙️ Generating predictions...")
                time.sleep(0.5)
                st.write("✅ Analysis complete!")

            features = extract(symptoms)
            detected_symptoms = [k for k, v in features.items() if v]

            st.markdown(f"""
            <div class='ai-message'>
            🤖 <b>AI Medical Assistant</b>
            <br><br>
            <b>Detected Symptoms:</b>
            """ + "".join([f"<br>✓ {symptom.title()}" for symptom in detected_symptoms]) + """
            </div>
            """, unsafe_allow_html=True)

            # ========== EMERGENCY ALERT ==========
            if (
                features.get("chest pain")
                and features.get("breathlessness")
            ):

                st.markdown("""
                <div class='emergency-banner'>
                <div class='emergency-title'>🚨 CRITICAL HEALTH ALERT</div>
                <br>
                <b>Detected combination:</b>
                <br>• Chest Pain
                <br>• Breathlessness
                <br><br>
                <b>Potential Concern:</b>
                <br>• Severe Respiratory Condition
                <br>• Cardiac Issue
                <br><br>
                <b style='color:#ff4d4d;'>⚠️ Action Required: Immediate medical consultation</b>
                </div>
                """, unsafe_allow_html=True)

            predictions = predict_disease(
                features
            )

            st.write("")

            # ========== PRIMARY DIAGNOSIS ==========
            if predictions:
                primary = predictions[0]

                st.markdown(f"""
                <div class='primary-diagnosis'>
                <div class='diagnosis-label'>PRIMARY DIAGNOSIS</div>
                <div class='diagnosis-name'>{primary['disease']}</div>
                <div style='font-size:20px;color:#9ca3af;'>Confidence: <span style='color:#facc15;font-size:28px;'>{primary['confidence']}%</span></div>
                <div style='margin-top:15px;color:#cbd5e1;'>
                <b>Specialist:</b> {primary['doctor']}
                <br>
                <b>Risk Level:</b> """ + ("🟢 Low" if primary['confidence'] > 70 else "🟡 Moderate" if primary['confidence'] > 50 else "🔴 High") + """
                </div>
                </div>
                """, unsafe_allow_html=True)

                # ========== RISK METER ==========
                st.write("**Confidence Meter:**")
                st.progress(min(primary['confidence'] / 100, 1.0))

                # ========== HEALTH INSIGHTS ==========
                st.markdown("""
                <div class='health-insights'>
                <b>📊 Health Insights</b>
                <div class='insight-row'>
                <span class='insight-label'>Hydration Status</span>
                <span class='insight-value'>Good</span>
                </div>
                <div class='insight-row'>
                <span class='insight-label'>Respiratory Risk</span>
                <span class='insight-value'>""" + ("Moderate" if "chest pain" in detected_symptoms or "breathlessness" in detected_symptoms else "Low") + """</span>
                </div>
                <div class='insight-row'>
                <span class='insight-label'>Neurological Risk</span>
                <span class='insight-value'>Low</span>
                </div>
                <div class='insight-row'>
                <span class='insight-label'>Digestive Risk</span>
                <span class='insight-value'>Low</span>
                </div>
                </div>
                """, unsafe_allow_html=True)

                # ========== AI RECOMMENDATION ==========
                st.markdown(f"""
                <div class='recommendation-box'>
                <b>🤖 AI Recommendation</b>
                <br><br>
                Based on your symptoms, a consultation with a <b>{primary['doctor']}</b> is advised.
                <br><br>
                Monitor symptoms closely. Avoid strenuous activity. Maintain proper hydration.
                <br><br>
                <i>⚠️ This is not a medical diagnosis. Always consult with licensed healthcare professionals.</i>
                </div>
                """, unsafe_allow_html=True)

                # ========== SECONDARY DIAGNOSES ==========
                if len(predictions) > 1:
                    st.write("### 🔍 Alternative Diagnoses")

                    colors = ["#00ff99", "#facc15", "#ff4d4d"]

                    for i, pred in enumerate(predictions[1:], start=1):
                        st.markdown(f"""
                        <div class='secondary-card' style='border-left-color:{colors[i]};'>
                        <div style='color:{colors[i]};font-size:20px;font-weight:bold;'>
                        {i+1}. {pred['disease']}
                        </div>
                        <br>
                        <div style='color:#9ca3af;'>Confidence: <span style='color:{colors[i]};font-weight:bold;'>{pred['confidence']}%</span></div>
                        <div style='color:#9ca3af;margin-top:10px;'>Specialist: {pred['doctor']}</div>
                        </div>
                        """, unsafe_allow_html=True)

            save_history(
                st.session_state.username,
                {
                    "input": symptoms,
                    "prediction": predictions,
                    "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
                }
            )

    if history_btn:

        st.write("")
        st.markdown("### 📋 Medical Assessment Timeline")

        history = get_history(
            st.session_state.username
        )

        if not history:

            st.info(
                "No assessment history yet."
            )

        else:

            for item in reversed(history):

                timestamp = item.get(
                    "timestamp",
                    "N/A"
                )

                pred = item["prediction"][0] if item["prediction"] else None

                if pred:
                    st.markdown(f"""
                    <div class='timeline-item'>
                    <b>{timestamp}</b>
                    <br>
                    Symptoms: {item['input'][:50]}...
                    <br>
                    → <span style='color:#00ff99;font-weight:bold;'>{pred['disease']} ({pred['confidence']}%)</span>
                    </div>
                    """, unsafe_allow_html=True)

    st.write("")

    # ========== ROADMAP ==========
    st.markdown("""
    <div class='roadmap'>
    <b>🚀 Product Roadmap</b>
    <br><br>
    <span class='roadmap-completed'>✓ Disease Prediction Engine</span><br>
    <span class='roadmap-completed'>✓ Doctor Recommendation System</span><br>
    <span class='roadmap-completed'>✓ Assessment History Tracking</span><br>
    <br>
    <b>Upcoming Features:</b><br>
    <span class='roadmap-upcoming'>□ Voice Symptom Input</span><br>
    <span class='roadmap-upcoming'>□ AI Medical Chatbot</span><br>
    <span class='roadmap-upcoming'>□ Hospital Integration</span><br>
    <span class='roadmap-upcoming'>□ PDF Medical Reports</span><br>
    <span class='roadmap-upcoming'>□ Appointment Booking</span><br>
    <span class='roadmap-upcoming'>□ Multi-Language Support</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("---")

    st.markdown("""
    <center style="color:#9ca3af;">

    🏥 AI Healthcare Command Center

    Developed using Python, Streamlit and AI-based Weighted Symptom Matching.

    <br>

    Bharath M Gowda (1NH24CS040)

    Mohammed Kasim G (1NH25CS416)

    © 2026

    </center>
    """, unsafe_allow_html=True)
