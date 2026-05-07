import streamlit as st
import os
from auth import register, login, save_history, get_history

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

.result-card {
    background-color: #121a2b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #00ff99;
}

.big-title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MEDICAL KEYWORDS ----------------
MEDICAL_KEYWORDS = [
    "fever", "cough", "cold", "headache", "vomiting", "nausea",
    "body pain", "fatigue", "tired", "diarrhea", "loose motion",
    "sore throat", "throat", "chills", "shiver", "runny nose",
    "congestion", "sneezing", "dizziness", "stomach pain",
    "bloating", "abdominal pain", "breathlessness", "rash",
    "itching", "weakness", "chest pain", "constipation",
    "acidity", "loss of taste", "joint pain"
]

# ---------------- SYMPTOM EXTRACTION ----------------
def extract(text):

    text = text.lower()

    return [
        int(any(x in text for x in ["fever", "temperature"])),
        int(any(x in text for x in ["cough", "cold"])),
        int("headache" in text),
        int(any(x in text for x in ["fatigue", "tired"])),
        int(any(x in text for x in ["body pain", "body ache"])),
        int(any(x in text for x in ["diarrhea", "loose motion"])),
        int(any(x in text for x in ["vomiting", "vomit"])),
        int(any(x in text for x in ["sore throat", "throat"])),
        int(any(x in text for x in ["chills", "shiver"])),
        int("nausea" in text),
        int(any(x in text for x in ["runny nose", "running nose"])),
        int("congestion" in text),
        int("sneezing" in text),
        int("dizziness" in text),
        int(any(x in text for x in ["stomach pain", "stomach ache"])),
        int("bloating" in text),
        int(any(x in text for x in ["breathlessness", "shortness of breath"])),
        int(any(x in text for x in ["rash", "skin rash"])),
        int("itching" in text),
        int("chest pain" in text),
        int("joint pain" in text),
        int("loss of taste" in text),
        int("acidity" in text),
        int("constipation" in text),
        int("weakness" in text),
        int("abdominal pain" in text),
        int("sweating" in text)
    ]

# ---------------- VALIDATION ----------------
def is_medical_input(text):

    text = text.lower()

    for word in MEDICAL_KEYWORDS:
        if word in text:
            return True

    return False

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN PAGE ----------------
if st.session_state.user is None:

    st.markdown(
        "<h1 class='big-title'>🩺 AI Health Assistant</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Login / Register")

    mode = st.selectbox("Select Mode", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Register":

        if st.button("Register"):

            if register(username, password):
                st.success("Registration Successful")
            else:
                st.error("Username already exists")

    else:

        if st.button("Login"):

            if login(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid username or password")

# ---------------- MAIN APP ----------------
else:

    st.sidebar.title(f"👤 {st.session_state.user}")

    menu = st.sidebar.radio(
        "Menu",
        ["Chat", "History", "About"]
    )

    # ---------------- CHAT ----------------
    if menu == "Chat":

        st.markdown(
            "<h1 class='big-title'>AI Health Assistant</h1>",
            unsafe_allow_html=True
        )

        st.write("Enter symptoms separated by commas")

        user_input = st.text_input(
            "Enter symptoms",
            placeholder="Example: fever, cough, headache"
        )

        if st.button("Predict"):

            try:

                # Empty Input
                if user_input.strip() == "":
                    st.warning("Please enter symptoms.")

                # Invalid Input
                elif not is_medical_input(user_input):
                    st.error("Please enter valid medical symptoms.")

                else:

                    f = extract(user_input)

                    # ---------------- SMART RULE PREDICTION ----------------

                    prediction = "Unable to determine disease"

                    # Flu
                    if f[0] and f[1] and f[4]:
                        prediction = "Flu"

                    # Common Cold
                    elif f[1] and f[10]:
                        prediction = "Common Cold"

                    # Food Poisoning
                    elif f[5] and f[6] and f[14]:
                        prediction = "Food Poisoning"

                    # Typhoid
                    elif f[0] and f[25] and f[24]:
                        prediction = "Typhoid"

                    # Migraine
                    elif f[2] and f[13]:
                        prediction = "Migraine"

                    # Allergy
                    elif f[17] or f[18] or f[12]:
                        prediction = "Allergy"

                    # Asthma
                    elif f[16] and f[1]:
                        prediction = "Asthma"

                    # COVID-19
                    elif f[0] and f[1] and f[21]:
                        prediction = "COVID-19"

                    # Gastritis
                    elif f[14] and f[22]:
                        prediction = "Gastritis"

                    # Arthritis
                    elif f[20] and f[4]:
                        prediction = "Arthritis"

                    # Dengue
                    elif f[0] and f[8] and f[4]:
                        prediction = "Dengue"

                    # Malaria
                    elif f[0] and f[8] and f[13]:
                        prediction = "Malaria"

                    # Viral Fever
                    elif f[0] and f[1]:
                        prediction = "Viral Fever"

                    # Pneumonia
                    elif f[0] and f[1] and f[16] and f[19]:
                        prediction = "Pneumonia"

                    # Bronchitis
                    elif f[1] and f[7] and f[19]:
                        prediction = "Bronchitis"

                    # ---------------- OUTPUT ----------------

                    st.subheader("Prediction Result")

                    st.markdown(f"""
                    <div class='result-card'>
                        <h2 style='color:#00ff99;'>
                        {prediction}
                        </h2>
                    </div>
                    """, unsafe_allow_html=True)

                    st.info(
                        "This is not a medical diagnosis. Consult a doctor."
                    )

                    # Save History
                    save_history(
                        st.session_state.user,
                        {
                            "input": user_input,
                            "result": prediction
                        }
                    )

            except Exception as e:

                st.error("Prediction Error Occurred")
                st.exception(e)

    # ---------------- HISTORY ----------------
    elif menu == "History":

        st.title("📜 Prediction History")

        history = get_history(st.session_state.user)

        if history:

            for item in history[::-1]:

                st.markdown(f"""
                <div class='result-card'>
                    <h4>Symptoms:</h4>
                    <p>{item['input']}</p>

                    <h4>Prediction:</h4>
                    <p>{item['result']}</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("No history available")

    # ---------------- ABOUT ----------------
    else:

        st.title("ℹ️ About Project")

        st.write("""
        This project is an AI-based disease prediction system
        developed using:

        - Python
        - Streamlit
        - NLP-Based Symptom Extraction
        - Rule-Based Disease Prediction
        - Smart Medical Validation
        - Exception Handling

        Features:
        - Real-time prediction
        - Interactive UI
        - Symptom analysis
        - Medical validation
        - Prediction history
        - Stable disease prediction
        """)
