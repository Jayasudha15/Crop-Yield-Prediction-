import streamlit as st
import base64

def apply_styling():
    """
    Applies custom CSS for the login page and a general background for others.
    """
    # Use login_bg.png for the login page, and background.jpg for others.
    # We check session state to see if we are on the login page.
    if st.session_state.get("is_login_page", False):
        image_path = 'assets/login_bg.png'
    else:
        image_path = 'assets/background.jpg'

    try:
        with open(image_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            /* --- Page Background --- */
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/png;base64,{b64_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* --- Professional Login Form Container (as per the example) --- */
            .login-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 90vh; /* Full viewport height */
            }}
            .login-box {{
                background-color: white;
                padding: 2.5rem; /* More padding for a cleaner look */
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                width: 100%;
                max-width: 420px; /* Controls the 'small' size of the box */
            }}

            /* --- Styling Form Elements --- */
            .login-box h2 {{
                text-align: center;
                margin-bottom: 1.5rem;
                color: #333;
            }}
            .login-box .stButton>button {{
                width: 100%;
                border-radius: 5px;
                background-color: #008037; /* Green color from example */
                color: white;
                height: 45px;
            }}
            .login-box .stTextInput label {{
                font-weight: 500;
                color: #555;
            }}

            /* --- Link at the bottom --- */
            .signup-link {{
                text-align: center;
                margin-top: 1.5rem;
                color: #666;
            }}
            .signup-link a {{
                color: #007bff;
                text-decoration: none;
                font-weight: 600;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Background image not found at path: {image_path}")