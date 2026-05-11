
import streamlit as st
from auth import register

st.set_page_config(page_title="Register")

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📝 Register")

st.markdown("### Create New Account")

username = st.text_input("Create Username")

password = st.text_input(
    "Create Password",
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

            st.success("Registration Successful")

        else:
            st.error("Username already exists")
