import streamlit as st
import os
from model import train_and_save, load_model
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

# ---------------- TRAIN MODEL ----------------
if not os.path.exists("model.pkl"):
    train_and_save()

model = load_model()

# ---------------- MEDICAL KEYWORDS ----------------
MEDICAL_KEYWORDS = [
    "fever", "cough", "cold", "headache", "vomiting", "nausea",
    "body pain", "fatigue", "tired", "diarrhea", "loose motion",
    "sore throat", "throat", "chills", "shiver", "runny nose",
    "congestion", "sneezing", "dizziness", "stomach pain",
    "bloating", "abdominal pain", "breathlessness", "rash",
    "itching", "weakness", "chest pain", "constipation",
    "acidity", "loss of taste", "joint pain", "anxiety"
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
        int(any(x in text for x in ["anxiety", "stress"])),
        int("joint pain" in text),
        int("loss of taste" in text),
        int(any(x in text for x in ["eye redness", "red eyes"])),
        int("ear pain" in text),
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

# ---------------- RULE FILTER ----------------
def rule_filter(results, f):

    filtered = []

    for d, p in results:

        # Food Poisoning
        if d == "Food Poisoning":
            if f[5] == 0 and f[6] == 0:
                continue

        # Typhoid
        if d == "Typhoid":
            if f[0] == 0 or f[28] == 0:
                continue

        # Allergy
        if d == "Allergy":
            if f[17] == 0 and f[18] == 0 and f[12] == 0:
                continue

        # Asthma
        if d == "Asthma":
            if f[16] == 0:
                continue

        # Migraine
        if d == "Migraine":
            if f[2] == 0:
                continue

        filtered.append((d, p))

    return filtered if filtered else results
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

                    # Feature Extraction
                    f = extract(user_input)

                    # Prediction
                    probs = model.predict_proba([f])[0]
                    diseases = model.classes_

                    results = list(zip(diseases, probs))

                    # Sort
                    results.sort(key=lambda x: x[1], reverse=True)

                    # Filter
                    results = rule_filter(results, f)

                    st.subheader("Prediction Result")

                    colors = ["#00ff99", "#facc15", "#ff4d4d"]

                    # Display Top 3
                    for i, (d, p) in enumerate(results[:3]):

                        st.markdown(f"""
                        <div class='result-card'>
                            <h2 style='color:{colors[i]};'>
                            {i+1}. {d}
                            </h2>
                            <h4>Confidence: {round(p*100,2)}%</h4>
                        </div>
                        """, unsafe_allow_html=True)

                    # Save History
                    save_history(
                        st.session_state.user,
                        {
                            "input": user_input,
                            "result": results[0][0]
                        }
                    )

                    st.info(
                        "This is not a medical diagnosis. Consult a doctor."
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
        - Machine Learning
        - Random Forest Algorithm
        - Streamlit
        - Rule-Based Filtering
        - NLP-Based Symptom Extraction

        Features:
        - Real-time prediction
        - Symptom analysis
        - Exception handling
        - Smart medical validation
        - Prediction history
        - Interactive UI
        """)
