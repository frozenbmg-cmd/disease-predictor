from disease_database import DISEASES

def predict_disease(features):

    results = []

    doctor_map = {

        "Asthma": "Pulmonologist",
        "Pneumonia": "Pulmonologist",
        "Bronchitis": "Pulmonologist",

        "Migraine": "Neurologist",
        "Vertigo": "Neurologist",

        "Food Poisoning": "Gastroenterologist",
        "Gastritis": "Gastroenterologist",
        "IBS": "Gastroenterologist",

        "Allergy": "Dermatologist",
        "Eczema": "Dermatologist",
        "Fungal Infection": "Dermatologist",

        "Diabetes": "Endocrinologist",
        "Hypertension": "Cardiologist"
    }

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

            results.append({

                "disease": disease,

                "confidence": confidence,

                "doctor": doctor_map.get(
                    disease,
                    "General Physician"
                )

            })

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results[:3]
