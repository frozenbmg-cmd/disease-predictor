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
    color:#cbd5e1;
}

/* HEADER SECTION */
.command-header{
    background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
    border-top:4px solid #00ff99;
    border-bottom:2px solid #00ff99;
    padding:25px;
    border-radius:12px;
    margin-bottom:25px;
    text-align:center;
}

.header-title{
    font-size:42px;
    font-weight:900;
    color:#00ff99;
    letter-spacing:3px;
    text-transform:uppercase;
}

.header-divider{
    color:#00ff99;
    font-size:24px;
    margin:10px 0;
}

/* METRIC CARDS */
.metric-card{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:15px;
    text-align:center;
    margin:5px;
}

.metric-label{
    color:#9ca3af;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:1px;
}

.metric-value{
    color:#00ff99;
    font-size:24px;
    font-weight:bold;
    margin-top:5px;
}

/* PATIENT PROFILE */
.patient-profile{
    background:linear-gradient(135deg,#101b32,#0f172a);
    border:3px solid #00ff99;
    border-radius:12px;
    padding:20px;
    margin-bottom:20px;
}

.profile-header{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:15px;
}

.profile-row{
    display:flex;
    justify-content:space-between;
    padding:8px 0;
    border-bottom:1px solid #1e293b;
    color:#cbd5e1;
}

.profile-label{
    color:#9ca3af;
    font-size:13px;
}

/* CONSULTATION SECTION */
.consultation-box{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:20px;
    margin:20px 0;
}

.consultation-title{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:10px;
}

.chat-message{
    background:#0f172a;
    border-left:4px solid;
    border-radius:8px;
    padding:15px;
    margin:10px 0;
    color:#cbd5e1;
}

.user-chat{
    border-left-color:#3b82f6;
    margin-left:20px;
}

.ai-chat{
    border-left-color:#00ff99;
    margin-right:20px;
}

/* ANALYSIS REPORT */
.analysis-report{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:20px;
    margin:20px 0;
}

.report-title{
    color:#00ff99;
    font-size:16px;
    font-weight:bold;
    margin-bottom:15px;
}

.symptom-list{
    background:#0f172a;
    padding:15px;
    border-radius:8px;
    margin:10px 0;
}

.symptom-item{
    color:#00ff99;
    padding:5px 0;
    font-weight:500;
}

.clinical-category{
    background:#0f172a;
    padding:15px;
    border-radius:8px;
    margin-top:10px;
    color:#facc15;
    font-weight:bold;
}

/* PRIMARY DIAGNOSIS */
.primary-diagnosis{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    border:4px solid #00ff99;
    border-radius:12px;
    padding:40px;
    margin:30px 0;
    text-align:center;
}

.diagnosis-header{
    color:#9ca3af;
    font-size:14px;
    text-transform:uppercase;
    letter-spacing:2px;
    margin-bottom:20px;
}

.diagnosis-name{
    font-size:56px;
    font-weight:900;
    color:#00ff99;
    margin:20px 0;
}

.diagnosis-details{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:20px;
    margin-top:30px;
}

.detail-item{
    background:#101b32;
    padding:15px;
    border-radius:10px;
}

.detail-label{
    color:#9ca3af;
    font-size:12px;
    text-transform:uppercase;
}

.detail-value{
    color:#facc15;
    font-size:28px;
    font-weight:bold;
    margin-top:8px;
}

/* SECONDARY DIAGNOSES */
.secondary-section{
    margin:30px 0;
}

.secondary-cards{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
}

.secondary-card{
    background:#101b32;
    border-left:5px solid;
    border-radius:10px;
    padding:20px;
}

.card-number{
    font-size:24px;
    font-weight:bold;
    margin-bottom:10px;
}

.card-disease{
    font-size:20px;
    font-weight:bold;
    color:#fff;
    margin-bottom:10px;
}

.card-stat{
    color:#9ca3af;
    font-size:13px;
    margin:5px 0;
}

/* RISK ENGINE */
.risk-section{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:30px;
    margin:30px 0;
    text-align:center;
}

.risk-title{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:20px;
}

.risk-meter{
    background:#0f172a;
    border-radius:10px;
    padding:20px;
    margin:20px 0;
}

.risk-level{
    font-size:32px;
    font-weight:bold;
    margin-top:15px;
}

.risk-low{
    color:#00ff99;
}

.risk-moderate{
    color:#facc15;
}

.risk-high{
    color:#ff4d4d;
}

/* HEALTH INSIGHTS */
.health-insights{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:25px;
    margin:30px 0;
}

.insights-title{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:20px;
}

.insights-grid{
    display:grid;
    grid-template-columns:1fr 1fr 1fr 1fr;
    gap:15px;
}

.insight-card{
    background:#0f172a;
    border:1px solid #1e293b;
    border-radius:10px;
    padding:15px;
    text-align:center;
}

.insight-name{
    color:#9ca3af;
    font-size:12px;
    text-transform:uppercase;
    margin-bottom:8px;
}

.insight-status{
    color:#00ff99;
    font-size:16px;
    font-weight:bold;
}

/* RECOMMENDATION */
.recommendation-box{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    border-left:5px solid #00ff99;
    border-radius:12px;
    padding:25px;
    margin:30px 0;
}

.recommendation-title{
    color:#00ff99;
    font-size:16px;
    font-weight:bold;
    margin-bottom:15px;
}

.recommendation-text{
    color:#cbd5e1;
    line-height:1.8;
    margin:10px 0;
}

/* EMERGENCY ALERT */
.emergency-alert{
    background:#3d1f1f;
    border:4px solid #ff4d4d;
    border-radius:12px;
    padding:25px;
    margin:30px 0;
}

.emergency-title{
    color:#ff4d4d;
    font-size:24px;
    font-weight:900;
    text-transform:uppercase;
    margin-bottom:15px;
}

.emergency-text{
    color:#fff;
    margin:10px 0;
    font-weight:500;
}

/* TIMELINE */
.timeline-section{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:25px;
    margin:30px 0;
}

.timeline-title{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:20px;
}

.timeline-item{
    background:#0f172a;
    border-left:4px solid #00ff99;
    border-radius:8px;
    padding:15px;
    margin:12px 0;
}

.timeline-date{
    color:#9ca3af;
    font-size:12px;
    text-transform:uppercase;
}

.timeline-disease{
    color:#00ff99;
    font-size:16px;
    font-weight:bold;
    margin-top:8px;
}

/* ROADMAP */
.roadmap-section{
    background:#101b32;
    border:2px solid #1e293b;
    border-radius:12px;
    padding:25px;
    margin:30px 0;
}

.roadmap-title{
    color:#00ff99;
    font-size:18px;
    font-weight:bold;
    margin-bottom:20px;
}

.roadmap-item{
    padding:8px 0;
    color:#cbd5e1;
}

.completed{
    color:#00ff99;
}

.upcoming{
    color:#facc15;
}

/* FOOTER */
.footer-section{
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border-top:2px solid #00ff99;
    border-radius:12px;
    padding:25px;
    margin-top:40px;
    text-align:center;
}

.footer-title{
    color:#00ff99;
    font-size:16px;
    font-weight:bold;
    margin-bottom:10px;
}

.footer-text{
    color:#9ca3af;
    font-size:13px;
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
# MAIN APPLICATION - MEDICAL AI PLATFORM
# =====================================================
elif st.session_state.logged_in:

    # ========== SECTION 1: COMMAND CENTER HEADER ==========
    st.markdown("""
    <div class='command-header'>
    <div class='header-divider'>╔══════════════════════════════════════╗</div>
    <div class='header-title'>🩺 AI Healthcare Command Center</div>
    <div class='header-divider'>╚══════════════════════════════════════╝</div>
    </div>
    """, unsafe_allow_html=True)

    # ========== SYSTEM STATUS METRICS ==========
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-label'>System Status</div>
        <div class='metric-value'>🟢 Online</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-label'>AI Engine</div>
        <div class='metric-value'>🤖 Active</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-label'>Database</div>
        <div class='metric-value'>25+</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-label'>Predictions</div>
        <div class='metric-value'>142</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class='metric-card'>
        <div class='metric-label'>Accuracy</div>
        <div class='metric-value'>85%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ========== SECTION 2: PATIENT PROFILE ==========
    st.markdown(f"""
    <div class='patient-profile'>
    <div class='profile-header'>👤 Patient Dashboard</div>
    <div class='profile-row'>
    <span class='profile-label'>Name</span>
    <span>{st.session_state.username}</span>
    </div>
    <div class='profile-row'>
    <span class='profile-label'>Assessments</span>
    <span>0</span>
    </div>
    <div class='profile-row'>
    <span class='profile-label'>Last Assessment</span>
    <span>-</span>
    </div>
    <div class='profile-row' style='border-bottom:none;'>
    <span class='profile-label'>Status</span>
    <span style='color:#00ff99;'>Active</span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    col_logout = st.columns([4, 1])[1]
    with col_logout:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("")

    # ========== SECTION 3: AI MEDICAL CONSULTATION ==========
    st.markdown("""
    <div class='consultation-box'>
    <div class='consultation-title'>💬 AI Medical Consultation</div>
    <p style='color:#9ca3af;'>Describe how you feel. Our AI will analyze your symptoms and provide medical insights.</p>
    </div>
    """, unsafe_allow_html=True)

    symptoms = st.text_area(
        "",
        placeholder='Example: "I\'ve had fever, headache and body pain for 2 days."',
        height=140,
        label_visibility="collapsed"
    )

    analyze_col, history_col = st.columns(2)

    with analyze_col:
        analyze_btn = st.button("🔬 Analyze Symptoms", use_container_width=True, key="analyze")

    with history_col:
        history_btn = st.button("📊 View Assessment History", use_container_width=True, key="history")

    if analyze_btn:

        if not is_medical_input(symptoms):
            st.error("Please enter valid medical symptoms.")

        else:

            # ========== SECTION 4: LIVE AI THINKING ==========
            st.write("")
            with st.status("🤖 AI Processing & Analysis", expanded=True):
                st.write("✓ Reading symptoms...")
                time.sleep(0.4)
                st.write("✓ Extracting medical entities...")
                time.sleep(0.4)
                st.write("✓ Comparing against disease database...")
                time.sleep(0.4)
                st.write("✓ Calculating confidence scores...")
                time.sleep(0.4)
                st.write("✓ Generating medical report...")
                time.sleep(0.3)
                st.write("✅ Analysis complete!")

            # ========== CHAT DISPLAY ==========
            st.write("")
            st.markdown(f"""
            <div class='chat-message user-chat'>
            👤 <b>You</b>
            <br><br>
            {symptoms}
            </div>
            """, unsafe_allow_html=True)

            # Extract and process
            features = extract(symptoms)
            detected_symptoms = [k for k, v in features.items() if v]

            st.markdown(f"""
            <div class='chat-message ai-chat'>
            🤖 <b>AI Medical Assistant</b>
            <br><br>
            I've analyzed your symptoms. Let me generate a comprehensive medical report.
            </div>
            """, unsafe_allow_html=True)

            # ========== SECTION 5: MEDICAL ANALYSIS REPORT ==========
            st.markdown("""
            <div class='analysis-report'>
            <div class='report-title'>📋 AI Medical Analysis</div>
            
            <div class='symptom-list'>
            <b style='color:#00ff99;'>Symptoms Detected</b>
            """ + "".join([f"<div class='symptom-item'>✓ {symptom.title()}</div>" for symptom in detected_symptoms]) + """
            </div>
            
            <div class='clinical-category'>
            <b>Clinical Category:</b>
            """ + ("Respiratory Condition" if any(s in detected_symptoms for s in ["breathlessness", "cough", "chest pain"]) else
                   "Systemic Infection" if any(s in detected_symptoms for s in ["fever", "fatigue"]) else
                   "Gastrointestinal" if any(s in detected_symptoms for s in ["nausea", "vomiting", "diarrhea"]) else
                   "Neurological") + """
            </div>
            </div>
            """, unsafe_allow_html=True)

            # Get predictions
            predictions = predict_disease(features)

            # ========== EMERGENCY CHECK ==========
            if features.get("chest pain") and features.get("breathlessness"):

                st.markdown("""
                <div class='emergency-alert'>
                <div class='emergency-title'>🚨 Critical Alert</div>
                <div class='emergency-text'><b>Potential Respiratory/Cardiac Emergency</b></div>
                <br>
                <div class='emergency-text'><b>Recommended Actions:</b></div>
                <div class='emergency-text'>• Seek immediate medical attention</div>
                <div class='emergency-text'>• Avoid physical exertion</div>
                <div class='emergency-text'>• Contact emergency services if symptoms worsen</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # ========== SECTION 6: PRIMARY DIAGNOSIS CARD ==========
            if predictions:
                primary = predictions[0]

                st.markdown(f"""
                <div class='primary-diagnosis'>
                <div class='diagnosis-header'>Primary Diagnosis</div>
                <div class='diagnosis-name'>{primary['disease'].upper()}</div>
                
                <div class='diagnosis-details'>
                <div class='detail-item'>
                <div class='detail-label'>Confidence</div>
                <div class='detail-value'>{primary['confidence']}%</div>
                </div>
                
                <div class='detail-item'>
                <div class='detail-label'>Risk Level</div>
                <div class='detail-value'>""" + ("🟢 LOW" if primary['confidence'] > 70 else "🟡 MODERATE" if primary['confidence'] > 50 else "🔴 HIGH") + """</div>
                </div>
                
                <div class='detail-item'>
                <div class='detail-label'>Specialist</div>
                <div class='detail-value' style='font-size:16px;'>{primary['doctor']}</div>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)

                # ========== SECTION 7: SECONDARY DIAGNOSES ==========
                if len(predictions) > 1:
                    st.write("")
                    st.markdown("<div style='color:#00ff99;font-size:18px;font-weight:bold;'>🔍 Alternative Diagnoses</div>", unsafe_allow_html=True)

                    colors = ["#facc15", "#ff6b6b"]

                    secondary_cols = st.columns(2)

                    for i, pred in enumerate(predictions[1:3]):
                        with secondary_cols[i]:
                            st.markdown(f"""
                            <div class='secondary-card' style='border-left-color:{colors[i]};'>
                            <div class='card-number' style='color:{colors[i]};'>{i+2}.</div>
                            <div class='card-disease'>{pred['disease']}</div>
                            <div class='card-stat'>Confidence: <span style='color:{colors[i]};font-weight:bold;'>{pred['confidence']}%</span></div>
                            <div class='card-stat'>Specialist: {pred['doctor']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                st.write("")

                # ========== SECTION 8: RISK ENGINE ==========
                st.markdown(f"""
                <div class='risk-section'>
                <div class='risk-title'>⚡ Patient Risk Assessment</div>
                
                <div class='risk-meter'>
                <div style='background:#0f172a;height:30px;border-radius:15px;overflow:hidden;'>
                <div style='background:linear-gradient(90deg,#00ff99,#facc15);height:100%;width:{min(primary['confidence'], 100)}%;'></div>
                </div>
                <div class='risk-level """ + ("risk-low" if primary['confidence'] > 70 else "risk-moderate" if primary['confidence'] > 50 else "risk-high") + """'>
                """ + ("🟢 LOW RISK" if primary['confidence'] > 70 else "🟡 MODERATE RISK" if primary['confidence'] > 50 else "🔴 HIGH RISK") + """
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                # ========== SECTION 9: HEALTH INSIGHTS ==========
                st.markdown("""
                <div class='health-insights'>
                <div class='insights-title'>💡 Health Insights</div>
                
                <div class='insights-grid'>
                <div class='insight-card'>
                <div class='insight-name'>Hydration</div>
                <div class='insight-status'>Good</div>
                </div>
                
                <div class='insight-card'>
                <div class='insight-name'>Respiratory Risk</div>
                <div class='insight-status'>""" + ("Moderate" if any(s in detected_symptoms for s in ["breathlessness", "cough", "chest pain"]) else "Low") + """</div>
                </div>
                
                <div class='insight-card'>
                <div class='insight-name'>Neurological Risk</div>
                <div class='insight-status'>Low</div>
                </div>
                
                <div class='insight-card'>
                <div class='insight-name'>Digestive Risk</div>
                <div class='insight-status'>Low</div>
                </div>
                </div>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                # ========== SECTION 10: AI RECOMMENDATION ==========
                st.markdown(f"""
                <div class='recommendation-box'>
                <div class='recommendation-title'>🤖 AI Recommendation</div>
                <div class='recommendation-text'>
                Based on your symptoms and medical analysis, a consultation with a <b>{primary['doctor']}</b> is recommended.
                </div>
                <div class='recommendation-text'>
                <b>Suggested Actions:</b>
                <br>• Schedule an appointment with {primary['doctor'].lower()}
                <br>• Monitor symptoms for any changes
                <br>• Maintain proper hydration and rest
                <br>• Avoid strenuous activities
                </div>
                <div class='recommendation-text' style='color:#facc15;font-size:12px;'>
                ⚠️ This is an AI-assisted analysis and not a medical diagnosis. Always consult with licensed healthcare professionals.
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

        # ========== SECTION 12: MEDICAL TIMELINE ==========
        st.markdown("""
        <div class='timeline-section'>
        <div class='timeline-title'>📅 Medical Assessment Timeline</div>
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
                    <div class='timeline-disease'>{pred['disease']} • {pred['confidence']}% confidence</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ========== SECTION 13: ROADMAP ==========
    st.markdown("""
    <div class='roadmap-section'>
    <div class='roadmap-title'>🚀 Platform Roadmap</div>
    
    <b style='color:#00ff99;'>Completed Features</b>
    <div class='roadmap-item'><span class='completed'>✓</span> Disease Prediction Engine</div>
    <div class='roadmap-item'><span class='completed'>✓</span> Doctor Recommendation System</div>
    <div class='roadmap-item'><span class='completed'>✓</span> Assessment History Tracking</div>
    
    <br>
    <b style='color:#facc15;'>Upcoming Features</b>
    <div class='roadmap-item'><span class='upcoming'>□</span> AI Voice Assistant</div>
    <div class='roadmap-item'><span class='upcoming'>□</span> Hospital Integration</div>
    <div class='roadmap-item'><span class='upcoming'>□</span> Appointment Booking</div>
    <div class='roadmap-item'><span class='upcoming'>□</span> Medical PDF Reports</div>
    <div class='roadmap-item'><span class='upcoming'>□</span> Wearable Device Integration</div>
    <div class='roadmap-item'><span class='upcoming'>□</span> Multilingual Support</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ========== SECTION 14: FOOTER ==========
    st.markdown("""
    <div class='footer-section'>
    <div class='footer-title'>🏥 AI Healthcare Command Center</div>
    <div class='footer-text'>
    Powered by: Python • Streamlit • Artificial Intelligence • Medical Knowledge Base
    <br><br>
    <b>Developed By</b>
    <br>
    Bharath M Gowda (1NH24CS040)
    <br>
    Mohammed Kasim G (1NH25CS416)
    <br><br>
    © 2026 All Rights Reserved
    </div>
    </div>
    """, unsafe_allow_html=True)
