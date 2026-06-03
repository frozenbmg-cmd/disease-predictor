import streamlit as st
from auth import register, login, save_history, get_history
from symptom_extractor import extract, is_medical_input
from prediction_engine import predict_disease

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="AI Healthcare Assistant",
page_icon="🩺",
layout="wide"
)

# ---------------- SESSION ----------------

if "page" not in st.session_state:
st.session_state.page = "register"

if "logged_in" not in st.session_state:
st.session_state.logged_in = False

# ---------------- CSS ----------------

st.markdown("""

<style>

.stApp {
    background-color: #050816;
    color: white;
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:#b0b0b0;
}

.result-card {
    padding:20px;
    border-radius:15px;
    background:#101b32;
    margin-top:15px;
}

</style>

""", unsafe_allow_html=True)

# =====================================================

# REGISTER

# =====================================================

if (
st.session_state.page == "register"
and not st.session_state.logged_in
):

```
st.markdown(
    "<div class='title'>🩺 AI Healthcare Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Create your account</div>",
    unsafe_allow_html=True
)

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

confirm = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("Register"):

    if password != confirm:

        st.error("Passwords do not match")

    else:

        if register(username, password):

            st.success(
                "Registration Successful"
            )

            st.session_state.page = "login"
            st.rerun()

        else:

            st.error(
                "Username already exists"
            )

st.markdown("---")

st.write("Already have an account?")

if st.button("Login Here"):

    st.session_state.page = "login"
    st.rerun()
```

# =====================================================

# LOGIN

# =====================================================

elif (
st.session_state.page == "login"
and not st.session_state.logged_in
):

```
st.markdown(
    "<div class='title'>🔐 Login</div>",
    unsafe_allow_html=True
)

username = st.text_input(
    "Username",
    key="login_user"
)

password = st.text_input(
    "Password",
    type="password",
    key="login_pass"
)

if st.button("Login"):

    if login(username, password):

        st.session_state.logged_in = True
        st.session_state.username = username

        st.rerun()

    else:

        st.error(
            "Invalid Username or Password"
        )

st.markdown("---")

st.write("New User?")

if st.button("Create Account"):

    st.session_state.page = "register"
    st.rerun()
```

# =====================================================

# MAIN APP

# =====================================================

elif st.session_state.logged_in:

```
st.title(
    f"Welcome, {st.session_state.username}"
)

col1, col2 = st.columns([5,1])

with col2:

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.page = "login"

        st.rerun()

user_input = st.text_input(
    "Enter Symptoms"
)

if st.button("Predict"):

    if not is_medical_input(
        user_input
    ):

        st.error(
            "Please enter valid symptoms."
        )

    else:

        features = extract(
            user_input
        )

        predictions = predict_disease(
            features
        )

        st.subheader(
            "Prediction Results"
        )

        for pred in predictions:

            st.markdown(f"""
            <div class='result-card'>

            <h3>
            {pred['disease']}
            </h3>

            <p>
            Confidence:
            {pred['confidence']}%
            </p>

            </div>
            """, unsafe_allow_html=True)

        save_history(
            st.session_state.username,
            {
                "input": user_input,
                "prediction": predictions
            }
        )

st.markdown("---")

if st.button("View History"):

    history = get_history(
        st.session_state.username
    )

    st.subheader(
        "Prediction History"
    )

    for item in reversed(history):

        st.write(
            f"Symptoms: {item['input']}"
        )

        for pred in item["prediction"]:

            st.write(
                f"{pred['disease']} - {pred['confidence']}%"
            )

        st.markdown("---")
```
