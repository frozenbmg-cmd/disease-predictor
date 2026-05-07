import streamlit as st
from auth import register, login, save_history, get_history

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background-color: #050816;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SYMPTOMS ----------------
SYMPTOMS = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "body pain",
    "diarrhea",
    "vomiting",
    "sore throat",
    "chills",
    "nausea",
    "runny nose",
    "running nose",
    "congestion",
    "sneezing",
    "dizziness",
    "stomach pain",
    "bloating",
    "breathlessness",
    "rash",
    "itching",
    "chest pain",
    "joint pain",
    "loss of taste",
    "acidity",
    "constipation",
    "weakness",
    "abdominal pain",
    "sweating",
    "eye redness",
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

        "fever": "fever" in text,

        "cough": "cough" in text,

        "headache": "headache" in text,

        "fatigue": any(
            x in text for x in ["fatigue", "tired"]
        ),

        "body pain": any(
            x in text for x in ["body pain", "body ache"]
        ),

        "diarrhea": any(
            x in text for x in ["diarrhea", "loose motion"]
        ),

        "vomiting": any(
            x in text for x in ["vomiting", "vomit"]
        ),

        "sore throat": "sore throat" in text,

        "chills": "chills" in text,

        "nausea": "nausea" in text,

        "runny nose": any(
            x in text for x in [
                "runny nose",
                "running nose"
            ]
        ),

        "congestion": "congestion" in text,

        "sneezing": "sneezing" in text,

        "dizziness": "dizziness" in text,

        "stomach pain": any(
            x in text for x in [
                "stomach pain",
                "stomach ache"
            ]
        ),

        "bloating": "bloating" in text,

        "breathlessness": any(
            x in text for x in [
                "breathlessness",
                "shortness of breath"
            ]
        ),

        "rash": "rash" in text,

        "itching": "itching" in text,

        "chest pain": "chest pain" in text,

        "joint pain": "joint pain" in text,

        "loss of taste": "loss of taste" in text,

        "acidity": "acidity" in text,

        "constipation": "constipation" in text,

        "weakness": "weakness" in text,

        "abdominal pain": "abdominal pain" in text,

        "sweating": "sweating" in text,

        "eye redness": any(
            x in text for x in [
                "eye redness",
                "red eyes"
            ]
        ),

        "ear pain": "ear pain" in text
    }

# ---------------- DISEASE DATABASE ----------------
DISEASES = {

    "Flu": {
        "fever": 3,
        "cough": 3,
        "body pain": 2,
        "fatigue": 2,
        "headache": 1
    },

    "Common Cold": {
        "cough": 3,
        "runny nose": 4,
        "sneezing": 3,
        "congestion": 2
    },

    "COVID-19": {
        "fever": 3,
        "cough": 3,
        "loss of taste": 5,
        "breathlessness": 3
    },

    "Dengue": {
        "fever": 4,
        "body pain": 4,
        "headache": 2,
        "chills": 2
    },

    "Typhoid": {
        "fever": 4,
        "weakness": 2,
        "abdominal pain": 3
    },

    "Food Poisoning": {
        "vomiting": 5,
        "diarrhea": 5,
        "stomach pain": 4,
        "nausea": 3
    },

    "Migraine": {
        "headache": 5,
        "dizziness": 3,
        "nausea": 2
    },

    "Asthma": {
        "breathlessness": 5,
        "cough": 2,
        "chest pain": 2
    },

    "Allergy": {
        "rash": 4,
        "itching": 4,
        "sneezing": 2
    },

    "Gastritis": {
        "acidity": 5,
        "stomach pain": 3,
        "bloating": 2
    }
}

# ---------------- PREDICTION ----------------
def predict_disease(features):

    results = []

    for disease, symptoms in DISEASES.items():

        score = 0
        total = 0

        for symptom, weight in symptoms.items():

            total += weight

            if features.get(symptom):
                score += weight

        confidence = round(
            (score / total) * 100,
            2
        )

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

# ---------------- LOGIN ----------------
if st.session_state.user is None:

    st.title("🩺 AI Health Assistant")

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

        st.title("AI Health Assistant")

        st.write(
            "Enter symptoms separated by commas"
        )

        user_input = st.text_input(
            "Enter symptoms"
        )

        if st.button("Predict"):

            if user_input.strip() == "":

                st.warning(
                    "Please enter symptoms."
                )

            elif not is_medical_input(user_input):

                st.error(
                    "Please enter valid medical symptoms."
                )

            else:

                features = extract(user_input)

                predictions = predict_disease(features)

                st.subheader("Prediction Result")

                top3 = predictions[:3]

                for i, (disease, confidence) in enumerate(top3):

                    st.success(
                        f"{i+1}. {disease}"
                    )

                    st.write(
                        f"Confidence: {confidence}%"
                    )

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

    # ---------------- HISTORY ----------------
    elif menu == "History":

        st.title("Prediction History")

        history = get_history(
            st.session_state.user
        )

        if history:

            for item in history[::-1]:

                st.write(
                    f"Symptoms: {item['input']}"
                )

                st.write(
                    f"Prediction: {item['result']}"
                )

                st.divider()

        else:
            st.warning("No history available")

    # ---------------- ABOUT ----------------
    else:

        st.title("About Project")

        st.write("""
        AI-based disease prediction system
        using NLP and weighted symptom analysis.
        """)
