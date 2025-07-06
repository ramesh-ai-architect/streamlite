import streamlit as st

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return  # already logged in

    st.title("🔐 Login")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.experimental_set_query_params(dummy="1")  # force rerun via URL change
            st.rerun()  # 🔁 This works even if experimental_rerun doesn't
        else:
            st.error("❌ Invalid credentials")
