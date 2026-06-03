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

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- REGISTER PAGE ----------------
if st.session_state.page == "register" and not st.session_state.logged_in:

    st.title("🩺 AI Health Assistant")
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):

        if password != confirm:
            st.error("Passwords do not match")

        elif register(username, password):
            st.success("Registration successful")
            st.session_state.page = "login"
            st.rerun()

        else:
            st.error("Username already exists")

    st.write("---")
    st.write("Already have an account?")

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- LOGIN PAGE ----------------
elif st.session_state.page == "login" and not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):

        if login(username, password):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()

        else:
            st.error("Invalid username or password")

    st.write("---")
    st.write("New user?")

    if st.button("Create Account"):
        st.session_state.page = "register"
        st.rerun()

# ---------------- MAIN APP ----------------
elif st.session_state.logged_in:

    st.title("🩺 AI Disease Prediction System")

    col1, col2 = st.columns([5, 1])

    with col1:
        st.write(f"Welcome, **{st.session_state.username}**")

    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("---")

    symptoms = st.text_input(
        "Enter symptoms separated by commas",
        placeholder="fever, cough, headache"
    )

    if st.button("Predict"):

        if not is_medical_input(symptoms):

            st.error("Please enter valid medical symptoms.")

        else:

            features = extract(symptoms)
            predictions = predict_disease(features)

            st.subheader("Prediction Results")

            for pred in predictions:

                st.success(
                    f"{pred['disease']} "
                    f"({pred['confidence']}%)"
                )

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
            st.info("No history available.")

        else:

            st.subheader("Prediction History")

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
