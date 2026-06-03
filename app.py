import streamlit as st
from auth import register, login, save_history, get_history
from symptom_extractor import extract, is_medical_input
from prediction_engine import predict_disease
from datetime import datetime


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

.main-title{
    font-size:55px;
    font-weight:700;
    color:white;
}

.subtitle{
    color:#9ca3af;
    font-size:18px;
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

.result-card{
    background:#101b32;
    padding:25px;
    border-radius:18px;
    margin-top:15px;
}

.prediction-title{
    font-size:32px;
    font-weight:bold;
}

.doctor{
    color:#9ca3af;
    font-size:18px;
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
        st.caption(
            "AI-powered healthcare assistant ready for symptom analysis."
        )

    with col2:

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.page = "login"

            st.rerun()

    st.write("---")

    st.write("### 💬 Describe Your Symptoms")

    symptoms = st.text_input(
        "",
        placeholder="Example: I have fever and body pain for 2 days"
    )

    if st.button("Predict"):

        if not is_medical_input(symptoms):

            st.error(
                "Please enter valid medical symptoms."
            )

        else:

            features = extract(symptoms)

            detected_symptoms = [k for k, v in features.items() if v]

            st.markdown("""
            ### 🤖 AI Analysis
            """)

            st.info(
                f"**Detected Symptoms:** {', '.join(detected_symptoms)}\n\n"
                f"**Status:** Analyzing {25}+ diseases..."
            )

            # Emergency Alert
            if (
                features["chest pain"]
                and features["breathlessness"]
            ):

                st.markdown("""
                ### 🚨 Critical Symptom Combination Detected

                **Possible Causes:**
                • Severe Asthma
                • Pneumonia
                • Cardiac Conditions

                **Recommended Action:**
                • Visit Emergency Department
                • Seek Immediate Medical Advice
                • Avoid Physical Exertion
                """)

            predictions = predict_disease(
                features
            )

            st.write("---")

            st.markdown("""
            ### 📊 Health Risk Assessment
            """)

            if predictions[0]["confidence"] > 70:
                st.success("✅ Low Risk - Monitor Regularly")
            elif predictions[0]["confidence"] > 50:
                st.warning("⚠️ Moderate Risk - Consult Doctor")
            else:
                st.error("🔴 High Risk - Seek Medical Attention")

            st.write("---")

            st.markdown("""
            ### 📈 Analytics Dashboard
            """)

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Symptoms Detected",
                len(detected_symptoms)
            )

            col2.metric(
                "Predictions",
                len(predictions)
            )

            col3.metric(
                "Top Confidence",
                f"{predictions[0]['confidence']}%"
            )

            col4.metric(
                "Status",
                "Completed"
            )

            st.write("---")

            st.markdown("""
            ### 🎯 Prediction Results
            """)

            colors = [
                "#00ff99",
                "#facc15",
                "#ff4d4d"
            ]

            health_tips = {
                "Flu": "Drink fluids and get adequate rest.",
                "Dengue": "Stay hydrated and monitor platelet levels.",
                "Asthma": "Avoid dust, smoke and allergens.",
                "Food Poisoning": "Consume oral rehydration solutions.",
                "Pneumonia": "Get adequate rest and stay hydrated.",
                "Migraine": "Avoid bright lights and get proper rest.",
                "Vertigo": "Avoid sudden movements and stay hydrated.",
                "Gastritis": "Avoid spicy food and caffeine.",
                "IBS": "Maintain a balanced diet with fiber.",
                "Allergy": "Identify and avoid allergens.",
                "Eczema": "Keep skin moisturized and avoid irritants.",
                "Fungal Infection": "Keep affected area dry and clean.",
                "Diabetes": "Monitor blood sugar levels regularly.",
                "Hypertension": "Reduce salt intake and exercise regularly.",
                "Bronchitis": "Stay hydrated and avoid smoke."
            }

            for i, pred in enumerate(predictions):

                st.markdown(f"""
                <div style="
                    background:#101b32;
                    padding:25px;
                    border-radius:18px;
                    margin-top:15px;
                    border-left:6px solid {colors[i]};
                ">

                <div style="
                    color:{colors[i]};
                    font-size:38px;
                    font-weight:bold;
                ">
                    {i+1}. {pred['disease']}
                </div>

                <br>

                <div style="
                    color:white;
                    font-size:28px;
                ">
                    Confidence: {pred['confidence']}%
                </div>

                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                ### 👨‍⚕️ Recommended Specialist

                **{pred['doctor']}**

                This specialist commonly treats conditions related to the predicted disease.
                """)

                st.info(
                    health_tips.get(
                        pred["disease"],
                        "Maintain a healthy lifestyle and consult a healthcare professional."
                    )
                )

                st.write("---")

            save_history(
                st.session_state.username,
                {
                    "input": symptoms,
                    "prediction": predictions,
                    "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
                }
            )

    st.write("---")

    if st.button("📋 Show Medical Assessment History"):

        history = get_history(
            st.session_state.username
        )

        if not history:

            st.info(
                "No assessment history available yet."
            )

        else:

            st.markdown("""
            ### 📋 Medical Assessment History
            """)

            for item in reversed(history):

                timestamp = item.get(
                    "timestamp",
                    "N/A"
                )

                st.write(f"**Date/Time:** {timestamp}")
                st.write(f"**Symptoms:** {item['input']}")

                for pred in item["prediction"]:

                    st.write(
                        f"• **{pred['disease']}** ({pred['confidence']}%) "
                        f"→ {pred['doctor']}"
                    )

                st.write("---")

    st.markdown("---")

    st.markdown("""
    ### 🚀 Upcoming Features

    • Random Forest Disease Prediction
    • Hospital Integration
    • Appointment Booking
    • PDF Medical Reports
    • Cloud Database
    • AI Chatbot
    • Voice Symptom Input
    • Multi-language Support
    """)

    st.markdown("---")

    st.markdown("""
    <center style="color:#9ca3af;">

    AI Disease Prediction System

    Developed By

    Bharath M Gowda (1NH24CS040)

    Mohammed Kasim G (1NH25CS416)

    </center>
    """, unsafe_allow_html=True)
