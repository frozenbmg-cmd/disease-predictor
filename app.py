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
    box-shadow: 0px 0px 10px rgba(0,255,153,0.2);
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

# ---------------- VALIDATION ----------------
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

# ---------------- PREDICTION ENGINE ----------------
def predict_disease(features):

    disease_data = {

        "Flu": {
            "fever": 3,
            "cough": 3,
            "body pain": 2,
            "fatigue": 2,
            "headache": 1
        },

        "Common Cold": {
            "cough": 3,
            "runny nose": 3,
            "sneezing": 2,
            "congestion": 2
        },

        "COVID-19": {
            "fever": 3,
            "cough": 3,
            "loss of taste": 4,
            "breathlessness": 3,
            "fatigue": 2
        },

        "Typhoid": {
            "fever": 3,
            "abdominal pain": 3,
            "weakness": 2,
            "headache": 1,
            "sweating": 2
        },

        "Dengue": {
            "fever": 3,
            "body pain": 3,
            "headache": 2,
            "chills": 2,
            "weakness": 2
        },

        "Malaria": {
            "fever": 3,
            "chills": 3,
            "sweating": 3,
            "dizziness": 2,
            "fatigue": 2
        },

        "Food Poisoning": {
            "vomiting": 4,
            "diarrhea": 4,
            "stomach pain": 3,
            "nausea": 2,
            "bloating": 1
        },

        "Migraine": {
            "headache": 4,
            "dizziness": 2,
            "nausea": 2
        },

        "Asthma": {
            "breathlessness": 4,
            "cough": 2,
            "chest pain": 2
        },

        "Pneumonia": {
            "fever": 3,
            "cough": 3,
            "breathlessness": 3,
            "chest pain": 2
        },

        "Allergy": {
            "rash": 3,
            "itching": 3,
            "sneezing": 2,
            "eye redness": 2
        },

        "Sinusitis": {
            "headache": 3,
            "congestion": 3,
            "runny nose": 2
        },

        "Gastritis": {
            "acidity": 4,
            "stomach pain": 3,
            "bloating": 2,
            "nausea": 1
        },

        "Constipation": {
            "constipation": 4,
            "abdominal pain": 2,
            "bloating": 2
        },

        "Arthritis": {
            "joint pain": 4,
            "body pain": 2,
            "weakness": 1
        },

        "Viral Fever": {
            "fever": 3,
            "fatigue": 2,
            "headache": 2
        },

        "Dehydration": {
            "weakness": 3,
            "dizziness": 3,
            "fatigue": 2
        },

        "Chickenpox": {
            "fever": 2,
            "rash": 4,
            "itching": 3
        },

        "Tuberculosis": {
            "cough": 3,
            "fever": 2,
            "weakness": 3,
            "chest pain": 2
        }
    }

    results = []

    for disease, symptoms in disease_data.items():

        score = 0
        total = 0

        for symptom, weight in symptoms.items():

            total += weight

            if features.get(symptom):
                score += weight

        confidence = round((score / total) * 100, 2)

        if confidence > 0:
            results.append((disease, confidence))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results

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

                if user_input.strip() == "":
                    st.warning("Please enter symptoms.")

                elif not is_medical_input(user_input):
                    st.error("Please enter valid medical symptoms.")

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

                    for i, (disease, confidence) in enumerate(top3):

                        card_html = f"""
                        <div class='result-card'>

                            <h2 style="color:{colors[i]};">
                                {i+1}. {disease}
                            </h2>

                            <p style="font-size:22px; color:white;">
                                Confidence: {confidence}%
                            </p>

                        </div>
                        """

                        st.markdown(
                            card_html,
                            unsafe_allow_html=True
                        )

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

                    save_history(
                        st.session_state.user,
                        {
                            "input": user_input,
                            "result": top3[0][0]
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
        """)
