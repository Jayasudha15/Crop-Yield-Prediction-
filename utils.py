import streamlit as st
import base64
import os

def check_login(page_name="the application"):
    """Ensure user is logged in before accessing a page."""
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning(f"🔒 Please log in to access {page_name}.")
        st.stop()

def add_logout_button():
    """Add a logout button to the sidebar."""
    if st.sidebar.button("Log Out"):
        st.session_state["logged_in"] = False
        st.info("You have been logged out.")
        st.switch_page("0_SignIn.py")

def apply_styles(image_file=None, bg_color=None):
    """
    Loads all styles from style.css and applies the correct page background.
    Works with either a background image or a solid background color.
    """
    # 1. Load the external CSS file
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("The 'style.css' file was not found. Please ensure it is in the root directory.")

    # 2. Set the page-specific background (image or color)
    background_style = ""
    content_wrapper_style = ""

    # If using background image
    if image_file and os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        background_style = f"""
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;          /* Fill entire viewport */
            background-position: center;     /* Keep image centered */
            background-repeat: no-repeat;    /* Prevent tiling */
            background-attachment: fixed;    /* Stay fixed on scroll */
            min-height: 100vh;               /* Ensure covers viewport height */
        """
        # Semi-transparent content area for readability
        content_wrapper_style = (
            ".content-wrapper { background: rgba(240, 242, 246, 0.85); "
            "backdrop-filter: blur(10px); }"
        )

    # If using solid background color
    elif bg_color:
        background_style = f"background-color: {bg_color};"
        # Solid white background for content
        content_wrapper_style = (
            ".content-wrapper { background: #FFFFFF; "
            "box-shadow: 0 4px 12px rgba(0,0,0,0.08); }"
        )

    # Inject final styles into Streamlit app
    st.markdown(f"""
        <style>
            .stApp {{ {background_style} }}
            {content_wrapper_style}
        </style>
    """, unsafe_allow_html=True)
