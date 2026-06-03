from disease_database import DISEASES

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

           doctor = {
    "Asthma":"Pulmonologist",
    "Pneumonia":"Pulmonologist",
    "Migraine":"Neurologist",
    "Food Poisoning":"Gastroenterologist",
    "Allergy":"Dermatologist",
    "Flu":"General Physician",
    "Dengue":"General Physician",
    "Malaria":"General Physician"
}

results.append({
    "disease": disease,
    "confidence": confidence,
    "doctor": doctor.get(
        disease,
        "General Physician"
    )
})

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results[:3]
