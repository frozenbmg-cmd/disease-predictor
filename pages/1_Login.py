
import streamlit as st
from auth import login

st.set_page_config(page_title="Login")

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

.login-box {
    padding: 30px;
    border-radius: 20px;
    background-color: #121a2b;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🔐 Login")

st.markdown("### AI Disease Prediction System")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if login(username, password):

        st.session_state.logged_in = True
        st.session_state.username = username

        st.success("Login Successful")

    else:
        st.error("Invalid Username or Password")
