import streamlit as st
import time
import json
import os
from utils import apply_styles
import base64

# --- Page Config ---
st.set_page_config(page_title="Sign In", page_icon="🔒", layout="wide")

# Redirect if already logged in
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.switch_page("pages/1_Home.py")

# Apply background
apply_styles('assets/login_bg.png')

# Users file
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

with open(USERS_FILE, "r") as f:
    users = json.load(f)

# CSS
st.markdown("""
    <style>
        .login-form { max-width: 650px; margin: auto; }
        .block-container { padding-top: 1rem !important; }
        .glass-box h1 {
            font-size: 2rem !important;
            font-weight: 800 !important;
            color: #1E2A38 !important;
            text-align: center !important;
            margin: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("assets/logo.png")

# Layout
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    # Logo
    st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 0.5rem;">
            <img src="data:image/png;base64,{logo_base64}" width="320">
        </div>
    """, unsafe_allow_html=True)

    # Sign In heading
    st.markdown('<div class="glass-box" style="margin-bottom: 0.8rem;"><h1>🔒 Sign In</h1></div>', unsafe_allow_html=True)

    # Username & Password
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Sign In", use_container_width=True):
        if username in users and users.get(username) == password: # Used .get for safer access
            st.session_state["logged_in"] = True
            st.success("Sign In successful! Redirecting...")
            time.sleep(1)
            st.switch_page("pages/2_Home.py")
        else:
            st.error("Invalid username or password.")

    # --- FIX: MOVED THE "SIGN UP" SECTION INSIDE THE COLUMN ---
    # This aligns it with the "Sign In" button above.
    st.markdown(
        """
        <div style="text-align:center; margin-top:1rem;">
            <p style="margin-bottom:0.5rem; font-weight:600;">Don't have an account?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("👉 Sign Up", use_container_width=True):
        st.switch_page("pages/1_SignUp.py")
    # --- END OF FIX ---

# This section is now empty because its contents were moved up into the 'with col2:' block.