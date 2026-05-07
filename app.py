import streamlit as st
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
    font-size: 52px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SYMPTOMS ----------------
SYMPTOMS = [
    "fever", "cough", "headache", "fatigue", "body pain",
    "diarrhea", "vomiting", "sore throat", "chills",
    "nausea", "runny nose", "congestion", "sneezing",
    "dizziness", "stomach pain", "bloating",
    "breathlessness", "rash", "itching",
    "chest pain", "joint pain", "loss of taste",
    "acidity", "constipation", "weakness",
    "abdominal pain", "sweating", "eye redness",
    "ear pain"
]

# ---------------- MEDICAL VALIDATION ----------------
def is_medical_input(text):

    text = text.lower()

    for symptom in SYMPTOMS:
        if symptom in text:
            return True

    return False

# ---------------- FEATURE EXTRACTION ----------------
def extract(text):

    text = text.lower()

    return {

        "fever": any(x in text for x in ["fever", "temperature"]),
        "cough": any(x in text for x in ["cough", "cold"]),
        "headache": "headache" in text,
        "fatigue": any(x in text for x in ["fatigue", "tired"]),
        "body pain": any(x in text for x in ["body pain", "body ache"]),
        "diarrhea": any(x in text for x in ["diarrhea", "loose motion"]),
        "vomiting": any(x in text for x in ["vomiting", "vomit"]),
        "sore throat": any(x in text for x in ["sore throat", "throat"]),
        "chills": any(x in text for x in ["chills", "shiver"]),
        "nausea": "nausea" in text,
        "runny nose": any(x in text for x in ["runny nose", "running nose"]),
        "congestion": "congestion" in text,
        "sneezing": "sneezing" in text,
        "dizziness": "dizziness" in text,
        "stomach pain": any(x in text for x in ["stomach pain", "stomach ache"]),
        "bloating": "bloating" in text,
        "breathlessness": any(x in text for x in ["breathlessness", "shortness of breath"]),
        "rash": any(x in text for x in ["rash", "skin rash"]),
        "itching": "itching" in text,
        "chest pain": "chest pain" in text,
        "joint pain": "joint pain" in text,
        "loss of taste": "loss of taste" in text,
        "acidity": "acidity" in text,
        "constipation": "constipation" in text,
        "weakness": "weakness" in text,
        "abdominal pain": "abdominal pain" in text,
        "sweating": "sweating" in text,
        "eye redness": any(x in text for x in ["eye redness", "red eyes"]),
        "ear pain": "ear pain" in text
    }

# ---------------- DISEASE DATABASE ----------------
DISEASES = {

    "Flu": [
        "fever", "cough", "body pain", "fatigue", "headache"
    ],

    "Common Cold": [
        "cough", "runny nose", "sneezing", "congestion"
    ],

    "COVID-19": [
        "fever", "cough", "loss of taste",
        "breathlessness", "fatigue"
    ],

    "Typhoid": [
        "fever", "abdominal pain", "weakness",
        "headache", "sweating"
    ],

    "Dengue": [
        "fever", "body pain", "headache",
        "chills", "weakness"
    ],

    "Malaria": [
        "fever", "chills", "sweating",
        "dizziness", "fatigue"
    ],

    "Food Poisoning": [
        "vomiting", "diarrhea", "stomach pain",
        "nausea", "bloating"
    ],

    "Migraine": [
        "headache", "dizziness", "nausea"
    ],

    "Asthma": [
        "breathlessness", "cough", "chest pain"
    ],

    "Bronchitis": [
        "cough", "chest pain", "sore throat"
    ],

    "Pneumonia": [
        "fever", "cough", "breathlessness",
        "chest pain"
    ],

    "Allergy": [
        "rash", "itching", "sneezing",
        "eye redness"
    ],

    "Sinusitis": [
        "headache", "congestion", "runny nose"
    ],

    "Gastritis": [
        "acidity", "stomach pain",
        "bloating", "nausea"
    ],

    "Constipation": [
        "constipation", "abdominal pain",
        "bloating"
    ],

    "Arthritis": [
        "joint pain", "body pain", "weakness"
    ],

    "Viral Fever": [
        "fever", "fatigue", "headache"
    ],

    "Dehydration": [
        "weakness", "dizziness", "fatigue"
    ],

    "Chickenpox": [
        "fever", "rash", "itching"
    ],

    "Tuberculosis": [
        "cough", "fever", "weakness",
        "chest pain"
    ]
}

# ---------------- PREDICTION ENGINE ----------------
def predict_disease(features):

    scores = {}

    for disease, symptom_list in DISEASES.items():

        score = 0

        for symptom in symptom_list:

            if features.get(symptom):
                score += 1

        scores[disease] = score

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_scores

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if st.session_state.user is None:

    st.markdown(
        "<h1 class='big-title'>🩺 AI Health Assistant</h1>",
        unsafe_allow_html=True
    )

    st.subheader("Login / Register")

    mode = st.selectbox(
        "Select Mode",
        ["Login", "Register"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

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
                    st.error(
                        "Please enter valid medical symptoms."
                    )

                else:

                    features = extract(user_input)

                    predictions = predict_disease(features)

                    st.subheader("Prediction Result")

                    top3 = predictions[:3]

                    colors = [
                        "#00ff99",
                        "#facc15",
                        "#ff4d4d"
                    ]

                    for i, (disease, score) in enumerate(top3):

                        confidence = round(
                            (score / 5) * 100,
                            2
                        )

                        st.markdown(f"""
                        <div class='result-card'>
                            <h2 style='color:{colors[i]};'>
                            {i+1}. {disease}
                            </h2>

                            <h4>
                            Confidence: {confidence}%
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)

                    # Emergency Detection
                    if (
                        features["chest pain"]
                        and features["breathlessness"]
                    ):

                        st.error(
                            "Emergency Warning: Seek medical attention immediately."
                        )

                    st.info(
                        "This is not a medical diagnosis. Consult a doctor."
                    )

                    # Save History
                    save_history(
                        st.session_state.user,
                        {
                            "input": user_input,
                            "result": top3[0][0]
                        }
                    )

            except Exception as e:

                st.error(
                    "Prediction Error Occurred"
                )

                st.exception(e)

    # ---------------- HISTORY ----------------
    elif menu == "History":

        st.title("📜 Prediction History")

        history = get_history(
            st.session_state.user
        )

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

        st.write(\"\"\"
        This project is an AI-based disease prediction system
        developed using:

        - Python
        - Streamlit
        - NLP-Based Symptom Extraction
        - Hybrid Rule-Based Prediction
        - Medical Validation
        - Exception Handling

        Features:
        - Real-time prediction
        - 20+ disease support
        - Smart symptom analysis
        - Prediction history
        - Emergency detection
        - Interactive UI
        - Top 3 disease prediction
        \"\"\")
