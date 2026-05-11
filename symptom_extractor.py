
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

# ---------------- EXTRACTION ----------------
def extract(text):

    text = text.lower()

    return {

        "fever": any(x in text for x in [
            "fever",
            "temperature",
            "high temperature"
        ]),

        "cough": "cough" in text,

        "headache": "headache" in text,

        "fatigue": any(x in text for x in [
            "fatigue",
            "tired",
            "weak"
        ]),

        "body pain": any(x in text for x in [
            "body pain",
            "body ache"
        ]),

        "diarrhea": any(x in text for x in [
            "diarrhea",
            "loose motion"
        ]),

        "vomiting": any(x in text for x in [
            "vomiting",
            "vomit"
        ]),

        "sore throat": "sore throat" in text,

        "chills": any(x in text for x in [
            "chills",
            "shivering"
        ]),

        "nausea": "nausea" in text,

        "runny nose": any(x in text for x in [
            "runny nose",
            "running nose"
        ]),

        "congestion": "congestion" in text,

        "sneezing": "sneezing" in text,

        "dizziness": "dizziness" in text,

        "stomach pain": any(x in text for x in [
            "stomach pain",
            "stomach ache"
        ]),

        "bloating": "bloating" in text,

        "breathlessness": any(x in text for x in [
            "breathlessness",
            "shortness of breath"
        ]),

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

        "eye redness": any(x in text for x in [
            "eye redness",
            "red eyes"
        ]),

        "ear pain": "ear pain" in text
    }
