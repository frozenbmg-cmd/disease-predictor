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
    layout="centered"
)

st.markdown("""
<style>

.stApp{
    background:#0B1220;
    color:#F8FAFC;
}

/* HERO SECTION */
.hero-container{
    padding:60px 40px;
    text-align:center;
    background:linear-gradient(135deg, #111827 0%, #0B1220 100%);
    border-radius:12px;
    margin:20px 0;
}

.hero-title{
    font-size:44px;
    font-weight:700;
    color:#F8FAFC;
    margin-bottom:12px;
}

.hero-subtitle{
    font-size:18px;
    color:#94A3B8;
    margin-bottom:24px;
    font-weight:400;
}

.hero-description{
    font-size:16px;
    color:#CBD5E1;
    line-height:1.6;
    margin-bottom:30px;
    max-width:600px;
    margin-left:auto;
    margin-right:auto;
}

.divider{
    height:1px;
    background:#1F2937;
    margin:30px 0;
}

/* INPUT SECTION */
.input-container{
    margin:30px 0;
}

.input-label{
    font-size:14px;
    font-weight:600;
    color:#F8FAFC;
    margin-bottom:12px;
    display:block;
}

/* REPORT SECTION */
.report-container{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:12px;
    padding:40px;
    margin:30px 0;
}

.report-header{
    text-align:center;
    margin-bottom:30px;
}

.report-title{
    font-size:18px;
    font-weight:700;
    color:#F8FAFC;
    margin-bottom:8px;
}

.report-divider{
    height:1px;
    background:#1F2937;
    margin:20px 0;
}

/* DETECTED SYMPTOMS */
.symptoms-section{
    margin:25px 0;
}

.section-title{
    font-size:14px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:15px;
}

.symptom-badge{
    display:inline-block;
    background:#1F2937;
    color:#10B981;
    padding:8px 16px;
    border-radius:6px;
    margin:6px 6px 6px 0;
    font-size:14px;
    font-weight:500;
}

/* PRIMARY ASSESSMENT */
.assessment-section{
    margin:30px 0;
    text-align:center;
}

.assessment-label{
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

.assessment-disease{
    font-size:36px;
    font-weight:700;
    color:#2563EB;
    margin:15px 0;
}

/* CONFIDENCE VISUAL */
.confidence-section{
    background:#0B1220;
    padding:25px;
    border-radius:8px;
    margin:20px 0;
    text-align:center;
}

.confidence-label{
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:15px;
}

.confidence-bar{
    background:#1F2937;
    height:12px;
    border-radius:6px;
    overflow:hidden;
    margin:15px 0;
}

.confidence-fill{
    height:100%;
    background:linear-gradient(90deg, #10B981 0%, #2563EB 100%);
}

.confidence-value{
    font-size:32px;
    font-weight:700;
    color:#2563EB;
    margin-top:10px;
}

/* SPECIALIST RECOMMENDATION */
.specialist-section{
    background:#0B1220;
    padding:25px;
    border-radius:8px;
    margin:20px 0;
}

.specialist-label{
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:10px;
}

.specialist-name{
    font-size:20px;
    font-weight:600;
    color:#F8FAFC;
}

/* AI CLINICAL NOTE */
.clinical-note{
    background:#0B1220;
    border-left:4px solid #2563EB;
    padding:20px;
    border-radius:8px;
    margin:25px 0;
}

.clinical-note-title{
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

.clinical-note-text{
    font-size:15px;
    color:#CBD5E1;
    line-height:1.7;
}

/* SECONDARY DIAGNOSES */
.secondary-section{
    margin:30px 0;
}

.secondary-title{
    font-size:14px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:15px;
    text-align:center;
}

.secondary-cards{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
    margin-top:15px;
}

.secondary-card{
    background:#0B1220;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:15px;
    text-align:center;
}

.secondary-number{
    font-size:12px;
    font-weight:700;
    color:#94A3B8;
    text-transform:uppercase;
}

.secondary-disease{
    font-size:18px;
    font-weight:700;
    color:#F8FAFC;
    margin:8px 0;
}

.secondary-confidence{
    font-size:14px;
    color:#10B981;
    font-weight:600;
}

/* DISCLAIMER */
.disclaimer-card{
    background:#1F2937;
    border:1px solid #374151;
    border-radius:8px;
    padding:20px;
    margin:25px 0;
}

.disclaimer-title{
    font-size:13px;
    font-weight:700;
    color:#FBBF24;
    margin-bottom:8px;
    text-transform:uppercase;
}

.disclaimer-text{
    font-size:14px;
    color:#CBD5E1;
    line-height:1.6;
}

/* EMERGENCY ALERT */
.emergency-card{
    background:#7F1D1D;
    border:2px solid #DC2626;
    border-radius:8px;
    padding:20px;
    margin:25px 0;
}

.emergency-title{
    font-size:13px;
    font-weight:700;
    color:#FCA5A5;
    text-transform:uppercase;
    margin-bottom:8px;
}

.emergency-text{
    font-size:14px;
    color:#F3F4F6;
    line-height:1.6;
}

/* HISTORY */
.history-container{
    margin:30px 0;
}

.history-item{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:15px;
    margin-bottom:12px;
}

.history-date{
    font-size:12px;
    color:#94A3B8;
    font-weight:600;
}

.history-disease{
    font-size:16px;
    color:#2563EB;
    font-weight:600;
    margin-top:6px;
}

.history-confidence{
    font-size:14px;
    color:#10B981;
    margin-top:4px;
}

/* FOOTER */
.footer-container{
    text-align:center;
    margin-top:60px;
    padding:30px 0;
    border-top:1px solid #1F2937;
    color:#94A3B8;
}

.footer-title{
    font-size:14px;
    font-weight:600;
    color:#F8FAFC;
    margin-bottom:8px;
}

.footer-text{
    font-size:12px;
    color:#94A3B8;
    line-height:1.8;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)


# ========== SESSION STATE ==========
if "page" not in st.session_state:
    st.session_state.page = "register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_report" not in st.session_state:
    st.session_state.show_report = False

if "report_data" not in st.session_state:
    st.session_state.report_data = None


# =====================================================
# REGISTER PAGE
# =====================================================
if (
    st.session_state.page == "register"
    and not st.session_state.logged_in
):

    st.title("🩺 AI Healthcare Assistant")
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):

        if password != confirm:
            st.error("Passwords do not match")

        elif register(username, password):
            st.success("Registration Successful")
            st.session_state.page = "login"
            st.rerun()

        else:
            st.error("Username already exists")

    st.write("---")
    st.write("Already have an account?")

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

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):

        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid username or password")

    st.write("---")
    st.write("New user?")

    if st.button("Create Account"):
        st.session_state.page = "register"
        st.rerun()

# =====================================================
# MAIN APPLICATION - DXGPT STYLE
# =====================================================
elif st.session_state.logged_in:

    # Logout button
    col_logout = st.columns([10, 1])[1]
    with col_logout:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("")

    # ========== HERO SECTION ==========
    if not st.session_state.show_report:

        st.markdown("""
        <div class='hero-container'>
        <div class='hero-title'>🩺 AI Healthcare Assistant</div>
        <div class='hero-subtitle'>Intelligent Clinical Decision Support</div>
        <div class='hero-description'>
        Analyze your symptoms, identify potential medical conditions, and receive specialist recommendations. Our AI provides clinical insights to support your healthcare decisions.
        </div>
        <div class='divider'></div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ========== SYMPTOM INPUT ==========
        st.markdown("<span class='input-label'>Describe Your Symptoms</span>", unsafe_allow_html=True)

        symptoms = st.text_area(
            "",
            placeholder="Example: I've had fever, cough and body aches for 3 days",
            height=140,
            label_visibility="collapsed"
        )

        st.write("")

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            analyze_btn = st.button("Analyze", use_container_width=True, key="analyze")

        with col2:
            history_btn = st.button("History", use_container_width=True, key="history")

        if analyze_btn:

            if not is_medical_input(symptoms):
                st.error("Please enter valid medical symptoms.")

            else:

                # Processing
                with st.spinner("Analyzing symptoms..."):
                    time.sleep(1)
                    features = extract(symptoms)
                    detected_symptoms = [k for k, v in features.items() if v]
                    predictions = predict_disease(features)

                # Store in session
                st.session_state.show_report = True
                st.session_state.report_data = {
                    "symptoms": symptoms,
                    "detected": detected_symptoms,
                    "predictions": predictions,
                    "timestamp": datetime.now()
                }

                # Save to history
                save_history(
                    st.session_state.username,
                    {
                        "input": symptoms,
                        "prediction": predictions,
                        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
                    }
                )

                st.rerun()

        if history_btn:
            st.session_state.show_report = "history"
            st.rerun()

    # ========== REPORT VIEW ==========
    elif st.session_state.show_report == True and st.session_state.report_data:

        data = st.session_state.report_data

        if st.button("← Back"):
            st.session_state.show_report = False
            st.session_state.report_data = None
            st.rerun()

        st.write("")

        # ========== CLINICAL ASSESSMENT REPORT ==========
        st.markdown("""
        <div class='report-container'>
        <div class='report-header'>
        <div class='report-title'>Clinical Assessment Report</div>
        <div class='report-divider'></div>
        </div>
        """, unsafe_allow_html=True)

        # Detected Symptoms
        st.markdown("<div class='section-title'>Detected Symptoms</div>", unsafe_allow_html=True)

        for symptom in data["detected"]:
            st.markdown(f"<span class='symptom-badge'>✓ {symptom.title()}</span>", unsafe_allow_html=True)

        st.write("")

        # Primary Assessment
        if data["predictions"]:
            primary = data["predictions"][0]

            st.markdown(f"""
            <div class='assessment-section'>
            <div class='assessment-label'>Primary Assessment</div>
            <div class='assessment-disease'>{primary['disease']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence Visual
            st.markdown("""
            <div class='confidence-section'>
            <div class='confidence-label'>Clinical Confidence</div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='confidence-bar'>
            <div class='confidence-fill' style='width:{min(primary['confidence'], 100)}%;'></div>
            </div>
            <div class='confidence-value'>{primary['confidence']}%</div>
            </div>
            """, unsafe_allow_html=True)

            # Specialist Recommendation
            st.markdown(f"""
            <div class='specialist-section'>
            <div class='specialist-label'>Recommended Specialist</div>
            <div class='specialist-name'>{primary['doctor']}</div>
            </div>
            """, unsafe_allow_html=True)

            # AI Clinical Note
            st.markdown(f"""
            <div class='clinical-note'>
            <div class='clinical-note-title'>AI Clinical Note</div>
            <div class='clinical-note-text'>
            The symptom combination suggests a possible diagnosis of <b>{primary['disease'].lower()}</b>. 
            A consultation with a <b>{primary['doctor']}</b> is recommended for proper evaluation and treatment.
            </div>
            </div>
            """, unsafe_allow_html=True)

            # Emergency Alert
            if (
                data["detected"] and
                "chest pain" in data["detected"] and
                "breathlessness" in data["detected"]
            ):
                st.markdown("""
                <div class='emergency-card'>
                <div class='emergency-title'>⚠️ Clinical Alert</div>
                <div class='emergency-text'>
                The combination of chest pain and breathlessness may indicate a serious condition. 
                <b>Seek immediate medical attention.</b>
                </div>
                </div>
                """, unsafe_allow_html=True)

            # Secondary Diagnoses
            if len(data["predictions"]) > 1:
                st.markdown("<div class='secondary-title'>Alternative Assessments</div>", unsafe_allow_html=True)

                st.markdown("<div class='secondary-cards'>", unsafe_allow_html=True)

                for i, pred in enumerate(data["predictions"][1:3]):
                    st.markdown(f"""
                    <div class='secondary-card'>
                    <div class='secondary-number'>Alternative {i+2}</div>
                    <div class='secondary-disease'>{pred['disease']}</div>
                    <div class='secondary-confidence'>{pred['confidence']}% • {pred['doctor']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        # ========== DISCLAIMER ==========
        st.markdown("""
        <div class='disclaimer-card'>
        <div class='disclaimer-title'>⚠️ Important Notice</div>
        <div class='disclaimer-text'>
        This system provides AI-assisted health insights and is not a substitute for professional medical diagnosis, 
        treatment, or advice. Always consult with licensed healthcare professionals for medical concerns.
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ========== HISTORY VIEW ==========
    elif st.session_state.show_report == "history":

        if st.button("← Back"):
            st.session_state.show_report = False
            st.rerun()

        st.write("")

        st.markdown("<h3>Assessment History</h3>", unsafe_allow_html=True)

        history = get_history(st.session_state.username)

        if not history:
            st.info("No assessment history yet.")
        else:
            st.markdown("<div class='history-container'>", unsafe_allow_html=True)

            for item in reversed(history):
                timestamp = item.get("timestamp", "N/A")
                pred = item["prediction"][0] if item["prediction"] else None

                if pred:
                    st.markdown(f"""
                    <div class='history-item'>
                    <div class='history-date'>{timestamp}</div>
                    <div class='history-disease'>{pred['disease']}</div>
                    <div class='history-confidence'>Confidence: {pred['confidence']}% • {pred['doctor']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # ========== FOOTER ==========
    st.write("")
    st.markdown("""
    <div class='footer-container'>
    <div class='footer-title'>AI Healthcare Assistant</div>
    <div class='footer-text'>
    Clinical Decision Support System
    <br><br>
    Developed By<br>
    Bharath M Gowda (1NH24CS040)<br>
    Mohammed Kasim G (1NH25CS416)<br>
    <br>
    © 2026
    </div>
    </div>
    """, unsafe_allow_html=True)
