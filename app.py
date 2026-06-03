import streamlit as st
from auth import register, login, save_history, get_history
from symptom_extractor import extract, is_medical_input
from prediction_engine import predict_disease


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Assistant",
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
    <div class='main-title'>
    🩺 AI Disease Prediction System
    </div>

    <div class='subtitle'>
    Intelligent Symptom Analysis and Healthcare Assistance
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

    st.write("### Enter Symptoms")

    symptoms = st.text_input(
        "",
        placeholder="Example: fever, cough, body pain"
    )

    if st.button("Predict"):

        if not is_medical_input(symptoms):

            st.error(
                "Please enter valid medical symptoms."
            )

        else:

            features = extract(symptoms)

            # Emergency Alert
            if (
                features["chest pain"]
                and features["breathlessness"]
            ):

                st.error(
                    "🚨 Emergency Alert: Possible serious respiratory or cardiac condition detected. Please consult a doctor immediately."
                )

            predictions = predict_disease(
                features
            )

            st.subheader(
                "Prediction Results"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Diseases",
                len(predictions)
            )

            col2.metric(
                "Top Confidence",
                f"{predictions[0]['confidence']}%"
            )

            col3.metric(
                "Status",
                "Analyzed"
            )

            st.write("---")

            colors = [
                "#00ff99",
                "#facc15",
                "#ff4d4d"
            ]

            for i, pred in enumerate(
                predictions
            ):

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

                <br>

                <div style="
                    color:#9ca3af;
                    font-size:20px;
                ">
                    Recommended Doctor: {pred['doctor']}
                </div>

                </div>
                """, unsafe_allow_html=True)

            save_history(
                st.session_state.username,
                {
                    "input": symptoms,
                    "prediction": predictions
                }
            )

    st.write("---")

    if st.button("Show History"):

        history = get_history(
            st.session_state.username
        )

        if not history:

            st.info(
                "No history available."
            )

        else:

            st.subheader(
                "Prediction History"
            )

            for item in reversed(history):

                st.write(
                    f"Symptoms: {item['input']}"
                )

                for pred in item["prediction"]:

                    st.write(
                        f"- {pred['disease']} "
                        f"({pred['confidence']}%)"
                    )

                st.write("---")

    st.markdown("---")

    st.markdown("""
    <center>

    AI Disease Prediction System

    Developed By

    Bharath M Gowda (1NH24CS040)

    Mohammed Kasim G (1NH25CS416)

    </center>
    """, unsafe_allow_html=True)
