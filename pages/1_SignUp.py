import streamlit as st
import json
import os
import time
from utils import apply_styles

# --- Page Config ---
st.set_page_config(page_title="Sign Up", page_icon="📝", layout="wide")

# Apply background style
apply_styles('assets/login_bg.png')

USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# Load existing users
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

import base64
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

    # Sign Up heading
    st.markdown('<div class="glass-box" style="margin-bottom: 0.8rem;"><h1>📝 Sign Up</h1></div>', unsafe_allow_html=True)

    # Form
    new_username = st.text_input("Choose a Username", placeholder="Enter a username")
    new_password = st.text_input("Choose a Password", placeholder="Enter a password", type="password")

    if st.button("Create Account", use_container_width=True):
        if new_username in users:
            st.error("Username already exists. Please choose another.")
        elif not new_username or not new_password:
            st.error("Please fill in all fields.")
        else:
            users[new_username] = new_password
            with open(USERS_FILE, "w") as f:
                json.dump(users, f)
            st.success("Account created successfully! Redirecting to Sign In...")
            time.sleep(1)
            st.switch_page("0_SignIn.py")  # ✅ Redirect to Sign In page

    # "Already have an account?" box in green style
    # --- Sign In redirect button in Sign Up page ---
st.markdown(
    """
    <div style="text-align:center; margin-top:1rem;">
        <p style="margin-bottom:0.5rem; font-weight:600;">Already have an account?</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("🔑 Sign In", use_container_width=True):
    st.switch_page("0_SignIn.py")
