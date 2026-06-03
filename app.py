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
    margin:30px 0;
}

/* AI UNDERSTANDING */
.ai-understanding{
    background:#111827;
    border-left:4px solid #2563EB;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.ai-understanding-title{
    font-size:14px;
    font-weight:700;
    color:#2563EB;
    margin-bottom:12px;
}

.ai-understanding-text{
    font-size:14px;
    color:#CBD5E1;
    line-height:1.6;
    margin-bottom:12px;
}

.symptom-list{
    margin:12px 0;
}

.symptom-item{
    display:inline-block;
    background:#0B1220;
    color:#10B981;
    padding:6px 12px;
    border-radius:6px;
    margin:4px 4px 4px 0;
    font-size:13px;
    font-weight:500;
}

/* EMERGENCY ALERT */
.emergency-card{
    background:#7F1D1D;
    border:2px solid #DC2626;
    border-radius:8px;
    padding:25px;
    margin:25px 0;
}

.emergency-title{
    font-size:16px;
    font-weight:700;
    color:#FCA5A5;
    text-transform:uppercase;
    margin-bottom:12px;
}

.emergency-text{
    font-size:14px;
    color:#F3F4F6;
    line-height:1.6;
    margin:8px 0;
}

.emergency-actions{
    background:#6B1919;
    padding:12px;
    border-radius:6px;
    margin-top:12px;
    font-size:13px;
    color:#F3F4F6;
}

.emergency-action-item{
    margin:6px 0;
}

/* DETECTED SYMPTOMS */
.detected-symptoms{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.section-title{
    font-size:13px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

/* PRIMARY DIAGNOSIS */
.primary-diagnosis{
    background:#111827;
    border:2px solid #2563EB;
    border-radius:8px;
    padding:30px;
    margin:25px 0;
    text-align:center;
}

.diagnosis-label{
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

.diagnosis-name{
    font-size:36px;
    font-weight:700;
    color:#2563EB;
    margin:15px 0;
}

.diagnosis-stat{
    display:inline-block;
    background:#0B1220;
    padding:12px 20px;
    border-radius:6px;
    margin:8px;
}

.stat-label{
    font-size:11px;
    font-weight:700;
    text-transform:uppercase;
    color:#94A3B8;
}

.stat-value{
    font-size:24px;
    font-weight:700;
    color:#10B981;
    margin-top:4px;
}

/* SECONDARY DIAGNOSES */
.secondary-section{
    margin:25px 0;
}

.secondary-title{
    font-size:13px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

.secondary-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
}

.secondary-card{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:15px;
    text-align:center;
}

.secondary-disease{
    font-size:16px;
    font-weight:700;
    color:#F8FAFC;
    margin-bottom:8px;
}

.secondary-stat{
    font-size:14px;
    color:#10B981;
    font-weight:600;
    margin:4px 0;
}

.secondary-specialist{
    font-size:12px;
    color:#94A3B8;
}

/* CONFIDENCE VISUAL */
.confidence-section{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.confidence-bar{
    background:#0B1220;
    height:8px;
    border-radius:4px;
    overflow:hidden;
    margin:15px 0;
}

.confidence-fill{
    height:100%;
    background:linear-gradient(90deg, #10B981 0%, #2563EB 100%);
}

.confidence-text{
    font-size:14px;
    color:#CBD5E1;
    text-align:center;
}

/* RISK LEVEL */
.risk-section{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
    text-align:center;
}

.risk-level-badge{
    font-size:32px;
    font-weight:700;
    margin:15px 0;
}

.risk-low{
    color:#10B981;
}

.risk-moderate{
    color:#FBBF24;
}

.risk-high{
    color:#DC2626;
}

/* CLINICAL EXPLANATION */
.clinical-explanation{
    background:#111827;
    border-left:4px solid #2563EB;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.explanation-title{
    font-size:13px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    color:#94A3B8;
    margin-bottom:12px;
}

.explanation-text{
    font-size:14px;
    color:#CBD5E1;
    line-height:1.7;
}

/* DOCTOR RECOMMENDATION */
.doctor-section{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.doctor-name{
    font-size:18px;
    font-weight:700;
    color:#2563EB;
    margin:10px 0;
}

.doctor-reason{
    font-size:13px;
    color:#CBD5E1;
    line-height:1.6;
    margin-top:12px;
    padding-top:12px;
    border-top:1px solid #1F2937;
}

/* HEALTH GUIDANCE */
.health-guidance{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:8px;
    padding:20px;
    margin:20px 0;
}

.guidance-item{
    font-size:14px;
    color:#CBD5E1;
    margin:8px 0;
    padding-left:20px;
}

/* DISCLAIMER */
.disclaimer-card{
    background:#1F2937;
    border:1px solid #374151;
    border-radius:8px;
    padding:15px;
    margin:20px 0;
}

.disclaimer-title{
    font-size:12px;
    font-weight:700;
    color:#FBBF24;
    text-transform:uppercase;
    margin-bottom:6px;
}

.disclaimer-text{
    font-size:13px;
    color:#CBD5E1;
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
    font-size:15px;
    color:#2563EB;
    font-weight:700;
    margin-top:6px;
}

.history-confidence{
    font-size:13px;
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
# MAIN APPLICATION - HYBRID DESIGN
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
                    "features": features,
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

    # ========== CONSULTATION REPORT VIEW ==========
    elif st.session_state.show_report == True and st.session_state.report_data:

        data = st.session_state.report_data

        if st.button("← Back to Input"):
            st.session_state.show_report = False
            st.session_state.report_data = None
            st.rerun()

        st.write("")

        # ========== 1. AI UNDERSTANDING PANEL ==========
        st.markdown("""
        <div class='ai-understanding'>
        <div class='ai-understanding-title'>🤖 AI Assistant Understanding</div>
        <div class='ai-understanding-text'>
        I've analyzed your description and detected the following symptoms:
        </div>
        <div class='symptom-list'>
        """ + "".join([f"<span class='symptom-item'>• {symptom.title()}</span>" for symptom in data["detected"]]) + """
        </div>
        <div class='ai-understanding-text' style='margin-top:12px;'>
        Now comparing these symptoms against our medical knowledge base to identify potential conditions...
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ========== 2. EMERGENCY ALERT ENGINE ==========
        if data["features"].get("chest pain") and data["features"].get("breathlessness"):

            st.markdown("""
            <div class='emergency-card'>
            <div class='emergency-title'>🚨 High Priority Medical Alert</div>
            <div class='emergency-text'>
            <b>Critical Finding:</b> The combination of chest pain and breathlessness has been detected.
            </div>
            <div class='emergency-text'>
            <b>Clinical Significance:</b> This symptom combination may indicate a potentially serious respiratory or cardiac condition that requires immediate medical evaluation.
            </div>
            <div class='emergency-actions'>
            <b style='color:#FCA5A5;'>Recommended Actions:</b>
            <div class='emergency-action-item'>• Seek medical attention immediately</div>
            <div class='emergency-action-item'>• Avoid strenuous activity</div>
            <div class='emergency-action-item'>• Contact emergency services if symptoms worsen</div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

        # ========== 3. DETECTED SYMPTOMS SECTION ==========
        st.markdown(f"""
        <div class='detected-symptoms'>
        <div class='section-title'>Detected Symptoms ({len(data['detected'])})</div>
        """ + "".join([f"<span class='symptom-item'>✓ {symptom.title()}</span>" for symptom in data["detected"]]) + """
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ========== 4. PRIMARY DIAGNOSIS ==========
        if data["predictions"]:
            primary = data["predictions"][0]

            st.markdown(f"""
            <div class='primary-diagnosis'>
            <div class='diagnosis-label'>Primary Assessment</div>
            <div class='diagnosis-name'>{primary['disease']}</div>
            <div style='margin-top:15px;'>
            <div class='diagnosis-stat'>
            <div class='stat-label'>Confidence Score</div>
            <div class='stat-value'>{primary['confidence']}%</div>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # ========== 5. ALTERNATIVE DIAGNOSES ==========
            if len(data["predictions"]) > 1:
                st.markdown(f"""
                <div class='secondary-section'>
                <div class='secondary-title'>Secondary Possibilities</div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='secondary-grid'>", unsafe_allow_html=True)

                for i, pred in enumerate(data["predictions"][1:3]):
                    st.markdown(f"""
                    <div class='secondary-card'>
                    <div class='secondary-disease'>{pred['disease']}</div>
                    <div class='secondary-stat'>{pred['confidence']}%</div>
                    <div class='secondary-specialist'>{pred['doctor']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.write("")

            # ========== 6. CONFIDENCE VISUAL ==========
            st.markdown(f"""
            <div class='confidence-section'>
            <div class='section-title'>Confidence Assessment</div>
            <div class='confidence-bar'>
            <div class='confidence-fill' style='width:{min(primary['confidence'], 100)}%;'></div>
            </div>
            <div class='confidence-text'><b>{primary['confidence']}%</b> confidence in this assessment</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # ========== 7. RISK LEVEL ENGINE ==========
            if data["features"].get("chest pain") and data["features"].get("breathlessness"):
                risk_level = "High"
                risk_emoji = "🔴"
                risk_class = "risk-high"
            elif primary['confidence'] > 80:
                risk_level = "Moderate"
                risk_emoji = "🟡"
                risk_class = "risk-moderate"
            else:
                risk_level = "Low"
                risk_emoji = "🟢"
                risk_class = "risk-low"

            st.markdown(f"""
            <div class='risk-section'>
            <div class='section-title'>Patient Risk Level</div>
            <div class='risk-level-badge {risk_class}'>{risk_emoji} {risk_level} Risk</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # ========== 8. DOCTOR RECOMMENDATION ==========
            st.markdown(f"""
            <div class='doctor-section'>
            <div class='section-title'>Recommended Specialist</div>
            <div class='doctor-name'>{primary['doctor']}</div>
            <div class='doctor-reason'>
            <b>Clinical Reasoning:</b> The detected symptoms and diagnosis indicate a possible {primary['disease'].lower()} condition. 
            A consultation with a {primary['doctor']} is recommended for proper evaluation, diagnosis confirmation, and treatment planning.
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # ========== 9. AI CLINICAL EXPLANATION ==========
            st.markdown(f"""
            <div class='clinical-explanation'>
            <div class='explanation-title'>AI Clinical Explanation</div>
            <div class='explanation-text'>
            The prediction of <b>{primary['disease']}</b> is based on the presence of the following symptom patterns:
            <br><br>
            """ + ", ".join([f"<b>{s.title()}</b>" for s in data["detected"][:3]]) + f"""
            <br><br>
            These symptoms commonly appear together in respiratory and systemic conditions such as {primary['disease'].lower()}. 
            The high confidence score ({primary['confidence']}%) indicates a strong match with known clinical presentations of this condition.
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # ========== 10. HEALTH GUIDANCE ==========
            st.markdown("""
            <div class='health-guidance'>
            <div class='section-title'>Health Guidance</div>
            <div class='guidance-item'>• Stay hydrated and maintain adequate rest</div>
            <div class='guidance-item'>• Monitor your symptoms for any changes or worsening</div>
            <div class='guidance-item'>• Schedule an appointment with the recommended specialist</div>
            <div class='guidance-item'>• Avoid self-medication without professional guidance</div>
            <div class='guidance-item'>• Keep track of when symptoms started and how they've progressed</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

        # ========== DISCLAIMER ==========
        st.markdown("""
        <div class='disclaimer-card'>
        <div class='disclaimer-title'>⚠️ Important Notice</div>
        <div class='disclaimer-text'>
        This system provides AI-assisted health insights and is not a substitute for professional medical diagnosis, treatment, or advice. 
        Always consult with licensed healthcare professionals for medical concerns.
        </div>
        </div>
        """, unsafe_allow_html=True)

    # ========== HISTORY VIEW ==========
    elif st.session_state.show_report == "history":

        if st.button("← Back to Input"):
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
