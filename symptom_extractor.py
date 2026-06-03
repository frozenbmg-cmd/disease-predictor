def extract(text):

```
text = text.lower()

return {

    "fever": any(x in text for x in [
        "fever",
        "temperature",
        "high temperature"
    ]),

    "cough": any(x in text for x in [
        "cough",
        "coughing"
    ]),

    "headache": any(x in text for x in [
        "headache",
        "head pain"
    ]),

    "fatigue": any(x in text for x in [
        "fatigue",
        "tired",
        "weak",
        "exhausted",
        "no energy"
    ]),

    "body pain": any(x in text for x in [
        "body pain",
        "body ache",
        "muscle pain"
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
        "running nose",
        "nasal discharge"
    ]),

    "congestion": "congestion" in text,

    "sneezing": "sneezing" in text,

    "dizziness": any(x in text for x in [
        "dizziness",
        "giddiness"
    ]),

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

    "loss of taste": any(x in text for x in [
        "loss of taste",
        "cannot taste"
    ]),

    "acidity": any(x in text for x in [
        "acidity",
        "acid reflux"
    ]),

    "constipation": "constipation" in text,

    "weakness": "weakness" in text,

    "abdominal pain": "abdominal pain" in text,

    "sweating": any(x in text for x in [
        "sweating",
        "excess sweating"
    ]),

    "eye redness": any(x in text for x in [
        "eye redness",
        "red eyes"
    ]),

    "ear pain": "ear pain" in text
}
```
