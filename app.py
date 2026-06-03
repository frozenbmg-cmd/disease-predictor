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
    background:#0B1220;
    color:#F3F4F6;
}

/* MAIN HEADER */
.header-section{
    padding:30px 0;
    margin-bottom:30px;
}

.header-title{
    font-size:36px;
    font-weight:700;
    color:#F3F4F6;
    margin-bottom:8px;
}

.header-subtitle{
    font-size:16px;
    color:#9CA3AF;
    font-weight:400;
}

.header-tags{
    margin-top:12px;
    display:flex;
    gap:12px;
}

.tag{
    background:#1F2937;
    padding:6px 12px;
    border-radius:6px;
    font-size:12px;
    color:#9CA3AF;
}

/* PATIENT PROFILE */
.patient-card{
    background:#111827;
    padding:20px;
    border-radius:8px;
    border:1px solid #1F2937;
    margin-bottom:20px;
}

.card-label{
    color:#9CA3AF;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:0.5px;
    margin-bottom:15px;
}

.profile-row{
    display:flex;
    justify-content:space-between;
    padding:10px 0;
    border-bottom:1px solid #1F2937;
    font-size:14px;
}

.profile-row:last-child{
    border-bottom:none;
}

.profile-key{
    color:#9CA3AF;
}

.profile-value{
    color:#F3F4F6;
    font-weight:500;
}

/* INPUT SECTION */
.input-card{
    background:#111827;
    padding:25px;
    border-radius:8px;
    border:1px solid #1F2937;
    margin:20px 0;
}

.input-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:12px;
}

.input-description{
    color:#9CA3AF;
    font-size:14px;
    margin-bottom:15px;
}

/* ANALYSIS SECTION */
.analysis-card{
    background:#111827;
    padding:25px;
    border-radius:8px;
    border:1px solid #1F2937;
    margin:20px 0;
}

.analysis-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:15px;
}

.symptom-badge{
    display:inline-block;
    background:#1F2937;
    color:#10B981;
    padding:6px 12px;
    border-radius:6px;
    margin:4px;
    font-size:13px;
}

/* PRIMARY DIAGNOSIS */
.diagnosis-card{
    background:#111827;
    padding:35px;
    border-radius:8px;
    border:2px solid #3B82F6;
    margin:30px 0;
}

.diagnosis-label{
    color:#9CA3AF;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:0.5px;
    margin-bottom:15px;
}

.diagnosis-name{
    font-size:42px;
    font-weight:700;
    color:#F3F4F6;
    margin:15px 0;
}

.diagnosis-grid{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:20px;
    margin-top:25px;
}

.diagnosis-stat{
    background:#0B1220;
    padding:15px;
    border-radius:6px;
    border:1px solid #1F2937;
}

.stat-label{
    color:#9CA3AF;
    font-size:12px;
    text-transform:uppercase;
    margin-bottom:8px;
}

.stat-value{
    color:#3B82F6;
    font-size:24px;
    font-weight:700;
}

/* SECONDARY DIAGNOSES */
.secondary-section{
    margin:30px 0;
}

.secondary-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:15px;
}

.secondary-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
}

.secondary-card{
    background:#111827;
    padding:20px;
    border-radius:8px;
    border:1px solid #1F2937;
}

.secondary-disease{
    font-size:18px;
    font-weight:600;
    color:#F3F4F6;
    margin-bottom:12px;
}

.secondary-stat{
    color:#9CA3AF;
    font-size:13px;
    margin:6px 0;
}

/* RISK ASSESSMENT */
.risk-card{
    background:#111827;
    padding:25px;
    border-radius:8px;
    border:1px solid #1F2937;
    margin:25px 0;
}

.risk-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:20px;
}

.risk-bar{
    background:#0B1220;
    height:8px;
    border-radius:4px;
    overflow:hidden;
    margin:15px 0;
}

.risk-fill{
    height:100%;
    background:linear-gradient(90deg, #10B981, #3B82F6);
}

.risk-label{
    font-size:14px;
    font-weight:600;
    color:#F3F4F6;
    margin-top:12px;
}

/* CLINICAL ADVICE */
.advice-card{
    background:#111827;
    padding:25px;
    border-radius:8px;
    border-left:4px solid #3B82F6;
    margin:25px 0;
}

.advice-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:12px;
}

.advice-text{
    color:#D1D5DB;
    font-size:14px;
    line-height:1.6;
    margin:8px 0;
}

.advice-warning{
    color:#9CA3AF;
    font-size:12px;
    margin-top:15px;
    padding-top:15px;
    border-top:1px solid #1F2937;
}

/* EMERGENCY ALERT */
.emergency-card{
    background:#7F1D1D;
    padding:25px;
    border-radius:8px;
    border-left:4px solid #DC2626;
    margin:25px 0;
}

.emergency-title{
    color:#FCA5A5;
    font-size:16px;
    font-weight:700;
    margin-bottom:12px;
}

.emergency-text{
    color:#F3F4F6;
    font-size:14px;
    line-height:1.6;
    margin:8px 0;
}

/* TIMELINE */
.timeline-card{
    background:#111827;
    padding:25px;
    border-radius:8px;
    border:1px solid #1F2937;
    margin:25px 0;
}

.timeline-title{
    color:#F3F4F6;
    font-size:16px;
    font-weight:600;
    margin-bottom:20px;
}

.timeline-item{
    padding:15px;
    background:#0B1220;
    border-radius:6px;
    border-left:3px solid #3B82F6;
    margin-bottom:12px;
}

.timeline-date{
    color:#9CA3AF;
    font-size:12px;
}

.timeline-content{
    color:#F3F4F6;
    font-size:14px;
    margin-top:8px;
    font-weight:500;
}

/* FOOTER */
.footer-section{
    padding:30px 0;
    margin-top:40px;
    border-top:1px solid #1F2937;
    text-align:center;
}

.footer-title{
    color:#F3F4F6;
    font-size:14px;
    font-weight:600;
    margin-bottom:12px;
}

.footer-text{
    color:#9CA3AF;
    font-size:12px;
    line-height:1.8;
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
# MAIN APPLICATION - PROFESSIONAL HEALTHCARE
# =====================================================
elif st.session_state.logged_in:

    # ========== HEADER ==========
    st.markdown("""
    <div class='header-section'>
    <div class='header-title'>🩺 AI Healthcare Assistant</div>
    <div class='header-subtitle'>Clinical Symptom Analysis & Decision Support System</div>
    <div class='header-tags'>
    <span class='tag'>Secure</span>
    <span class='tag'>Explainable</span>
    <span class='tag'>Fast</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ========== PATIENT PROFILE ==========
    st.markdown(f"""
    <div class='patient-card'>
    <div class='card-label'>Patient Profile</div>
    <div class='profile-row'>
    <span class='profile-key'>Username</span>
    <span class='profile-value'>{st.session_state.username}</span>
    </div>
    <div class='profile-row'>
    <span class='profile-key'>Assessments</span>
    <span class='profile-value'>0</span>
    </div>
    <div class='profile-row'>
    <span class='profile-key'>Last Assessment</span>
    <span class='profile-value'>-</span>
    </div>
    <div class='profile-row'>
    <span class='profile-key'>Status</span>
    <span class='profile-value' style='color:#10B981;'>Active</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    col_logout = st.columns([4, 1])[1]
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("")

    # ========== SYMPTOM INPUT ==========
    st.markdown("""
    <div class='input-card'>
    <div class='input-title'>Symptom Assessment</div>
    <div class='input-description'>Describe your symptoms in your own words. Example: "I've had fever, headache and body pain for 2 days."</div>
    </div>
    """, unsafe_allow_html=True)

    symptoms = st.text_area(
        "",
        placeholder='Describe your symptoms...',
        height=120,
        label_visibility="collapsed"
    )

    col_analyze, col_history = st.columns(2)

    with col_analyze:
        analyze_btn = st.button("Analyze", use_container_width=True, key="analyze")

    with col_history:
        history_btn = st.button("Assessment History", use_container_width=True, key="history")

    if analyze_btn:

        if not is_medical_input(symptoms):
            st.error("Please enter valid medical symptoms.")

        else:

            st.write("")

            # ========== ANALYSIS PROCESSING ==========
            with st.status("Processing analysis...", expanded=False):
                st.write("Reading symptoms...")
                time.sleep(0.3)
                st.write("Extracting medical information...")
                time.sleep(0.3)
                st.write("Comparing with disease database...")
                time.sleep(0.3)
                st.write("Calculating confidence scores...")
                time.sleep(0.2)

            # Extract features
            features = extract(symptoms)
            detected_symptoms = [k for k, v in features.items() if v]

            # ========== ANALYSIS RESULTS ==========
            st.markdown("""
            <div class='analysis-card'>
            <div class='analysis-title'>Analysis Results</div>
            """, unsafe_allow_html=True)

            for symptom in detected_symptoms:
                st.markdown(f"<span class='symptom-badge'>✓ {symptom.title()}</span>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.write("")

            # Get predictions
            predictions = predict_disease(features)

            # ========== EMERGENCY ALERT ==========
            if features.get("chest pain") and features.get("breathlessness"):

                st.markdown("""
                <div class='emergency-card'>
                <div class='emergency-title'>⚠️ Clinical Alert</div>
                <div class='emergency-text'>
                <b>Detected combination:</b> Chest pain + Breathlessness
                </div>
                <div class='emergency-text'>
                <b>Potential concern:</b> Respiratory or cardiac condition
                </div>
                <div class='emergency-text'>
                <b>Recommended action:</b> Seek immediate medical attention
                </div>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

            # ========== PRIMARY DIAGNOSIS ==========
            if predictions:
                primary = predictions[0]

                st.markdown(f"""
                <div class='diagnosis-card'>
                <div class='diagnosis-label'>Primary Assessment</div>
                <div class='diagnosis-name'>{primary['disease']}</div>
                
                <div class='diagnosis-grid'>
                <div class='diagnosis-stat'>
                <div class='stat-label'>Confidence Score</div>
                <div class='stat-value'>{primary['confidence']}%</div>
                </div>
                
                <div class='diagnosis-stat'>
                <div class='stat-label'>Risk Level</div>
                <div class='stat-value'>""" + ("Low" if primary['confidence'] > 70 else "Moderate" if primary['confidence'] > 50 else "High") + """</div>
                </div>
                
                <div class='diagnosis-stat'>
                <div class='stat-label'>Specialist</div>
                <div class='stat-value' style='font-size:16px;'>{primary['doctor']}</div>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                # ========== SECONDARY DIAGNOSES ==========
                if len(predictions) > 1:
                    st.markdown(f"""
                    <div class='secondary-section'>
                    <div class='secondary-title'>Alternative Assessments</div>
                    """, unsafe_allow_html=True)

                    cols = st.columns(2)

                    for i, pred in enumerate(predictions[1:3]):
                        with cols[i]:
                            st.markdown(f"""
                            <div class='secondary-card'>
                            <div class='secondary-disease'>{i+2}. {pred['disease']}</div>
                            <div class='secondary-stat'>Confidence: {pred['confidence']}%</div>
                            <div class='secondary-stat'>Specialist: {pred['doctor']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                st.write("")

                # ========== RISK ASSESSMENT ==========
                st.markdown(f"""
                <div class='risk-card'>
                <div class='risk-title'>Risk Assessment</div>
                <div class='risk-bar'>
                <div class='risk-fill' style='width:{min(primary['confidence'], 100)}%;'></div>
                </div>
                <div class='risk-label'>""" + ("Low Risk" if primary['confidence'] > 70 else "Moderate Risk" if primary['confidence'] > 50 else "High Risk") + """</div>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                # ========== CLINICAL ADVICE ==========
                st.markdown(f"""
                <div class='advice-card'>
                <div class='advice-title'>Clinical Recommendation</div>
                <div class='advice-text'>
                <b>Assessment:</b> Based on the symptom analysis, {primary['disease'].lower()} is the primary diagnosis.
                </div>
                <div class='advice-text'>
                <b>Recommended specialist:</b> {primary['doctor']}
                </div>
                <div class='advice-text'>
                <b>Suggested actions:</b>
                <br>• Schedule an appointment with a {primary['doctor'].lower()}
                <br>• Monitor symptoms for changes
                <br>• Maintain adequate rest and hydration
                </div>
                <div class='advice-warning'>
                ℹ️ This assessment is AI-assisted analysis only. Always consult with licensed healthcare professionals for diagnosis and treatment.
                </div>
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

        # ========== ASSESSMENT TIMELINE ==========
        st.markdown("""
        <div class='timeline-card'>
        <div class='timeline-title'>Assessment Timeline</div>
        """, unsafe_allow_html=True)

        history = get_history(
            st.session_state.username
        )

        if not history:
            st.info("No assessment history yet.")
        else:
            for item in reversed(history):
                timestamp = item.get("timestamp", "N/A")
                pred = item["prediction"][0] if item["prediction"] else None

                if pred:
                    st.markdown(f"""
                    <div class='timeline-item'>
                    <div class='timeline-date'>{timestamp}</div>
                    <div class='timeline-content'>{pred['disease']} • {pred['confidence']}% confidence</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ========== FOOTER ==========
    st.markdown("""
    <div class='footer-section'>
    <div class='footer-title'>AI Healthcare Assistant</div>
    <div class='footer-text'>
    Powered by: Python • Streamlit • Machine Learning • Medical Knowledge Base
    <br><br>
    Developed By<br>
    Bharath M Gowda (1NH24CS040)<br>
    Mohammed Kasim G (1NH25CS416)
    <br><br>
    © 2026
    </div>
    </div>
    """, unsafe_allow_html=True)
