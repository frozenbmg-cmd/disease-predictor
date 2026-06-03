# ---------------- MAIN APP ----------------

elif st.session_state.logged_in:

```
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

        # Emergency Alert
        if (
            features["chest pain"]
            and features["breathlessness"]
        ):

            st.error("""
```

🚨 Emergency Alert

Possible serious respiratory or cardiac condition detected.

Please consult a doctor immediately.
""")

```
        predictions = predict_disease(features)

        st.subheader("Prediction Results")

        colors = [
            "#00ff99",
            "#facc15",
            "#ff4d4d"
        ]

        for i, pred in enumerate(predictions):

            st.markdown(f"""
            <div style="
                background:#101b32;
                padding:20px;
                border-radius:15px;
                margin-top:15px;
                border-left:5px solid {colors[i]};
            ">

            <h2 style="color:{colors[i]};">
            {i+1}. {pred['disease']}
            </h2>

            <h4 style="color:white;">
            Confidence: {pred['confidence']}%
            </h4>

            <p style="color:white;">
            Doctor: {pred['doctor']}
            </p>

            </div>
            """, unsafe_allow_html=True)

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
```
