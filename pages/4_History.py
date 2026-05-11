import streamlit as st
from auth import get_history

# ---------------- LOGIN CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.warning("Please login first.")
    st.stop()

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="History",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

.history-card {
    background-color: #121a2b;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📜 Prediction History")

history = get_history(
    st.session_state.username
)

if history:

    for item in reversed(history):

        st.markdown(f"""
        <div class='history-card'>

        <h3>Symptoms</h3>
        <p>{item['input']}</p>

        </div>
        """, unsafe_allow_html=True)

        for pred in item["prediction"]:

            st.write(
                f"{pred['disease']} — {pred['confidence']}%"
            )

        st.markdown("---")

else:

    st.warning("No history available.")
