import streamlit as st
from utils import check_login, add_logout_button, apply_styles

# --- Page Configuration ---
st.set_page_config(page_title="Home", page_icon="🌾", layout="wide")

# ✅ Redirect if not logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("0_SignIn.py")

# Apply styles/background and add logout
apply_styles('assets/home_background.jpg')
add_logout_button()

# ===== Main Title =====
st.markdown("""
    <div style='max-width:1800px; margin:auto; text-align:center;'>
        <div class="glass-box" style="padding: 1rem 2rem;">
            <h1 style="margin-bottom:0;">🌾 Welcome to the Crop Yield Prediction App!</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# ===== Details Section in Glass Container =====
st.markdown("""
    <div style='max-width:1700px; margin:2rem auto;'>
        <div class="glass-box" style="padding: 1.5rem 2rem;">
            <div /* Reduce top padding of the main page */
        .block-container {
            padding-top: 0rem;
        }
            <h2 style="margin-top:0;">Getting Started</h2>
            <p style="margin-bottom:1rem; font-size:1.15rem;">
                Navigate through the dashboard using the sidebar menu to explore the following features:
            </p>
            <ol style="margin-top:0.5rem; padding-left:1.35rem; font-size:1.12rem; line-height:1.7;">
                <li><strong>Make a Prediction:</strong> Instantly estimate crop yield.</li>
                <li><strong>Analyze the Data:</strong> Explore interactive data visualizations.</li>
                <li><strong>Compare Models:</strong> See a performance breakdown of various algorithms.</li>
            </ol>
        </div>
    </div>
""", unsafe_allow_html=True)

# ===== Additional Factors Section =====
st.markdown("""
    <div style='max-width:1800px; margin: 3rem auto;'>
        <div class="glass-box" style="padding: 1rem 2rem; background-color: white;">
            <h2 style="margin-bottom:0;">🌱 Other Factors Affecting Crop Yield</h2>
        </div>
    </div>
""", unsafe_allow_html=True)


factors = [
    ("assets/pest_infestation.jpg", "Pest Infestation",
     "Pests can severely damage crops, reducing yield significantly."),
    ("assets/soil_health.jpg", "Soil Health Degradation",
     "Loss of soil nutrients and organic matter affects crop productivity."),
    ("assets/extreme_weather.jpg", "Extreme Weather Events",
     "Floods, droughts, and storms can cause substantial crop losses.")
]

for img, title, desc in factors:
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            # Image with readable caption
            st.image(img, use_container_width=True)
            st.markdown(
                f"<div style='background-color:rgba(255,255,255,0.85); padding:6px; "
                f"border-radius:6px; text-align:center; font-weight:600; font-size:1.05rem; "
                f"color:#1E2A38;'>{title}</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
        f"""
        <div style='background:rgba(255,255,255,0.92); padding:1rem; border-radius:12px; 
                    box-shadow:0 4px 20px rgba(0,0,0,0.08); display:flex; flex-direction:column; 
                    justify-content:center; height:100%; padding-top:20px;'>
            <h3 style="margin-bottom:0.5rem;">{title}</h3>
            <p style="font-size:1.1rem; line-height:1.6;">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Gap between sections
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)




st.markdown("""
    <div style='max-width:1800px; margin: 2rem auto;'>
        <div class="glass-box" style="padding: 1.5rem 2rem;">
            <h2 style="margin-top:0; font-weight:700;">💡 Suggestions to Improve Crop Yield</h2>
            <ul style="font-size:1.1rem; line-height:1.8; margin-top:1rem;">
                <li><strong>Pest Infestation:</strong> Implement integrated pest management (IPM) and use biological pest control methods.</li>
                <li><strong>Soil Health Degradation:</strong> Rotate crops, use organic compost, and minimize chemical fertilizer overuse.</li>
                <li><strong>Extreme Weather Events:</strong> Adopt climate-resilient crop varieties and efficient irrigation systems.</li>
            </ul>
        </div>
    </div>
""", unsafe_allow_html=True)

# ===== Go to Prediction Button =====
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔮 Go to Prediction Page", use_container_width=True):
    st.switch_page("pages/3_Prediction.py")

# ===== CSS =====
# ===== CSS =====
st.markdown("""
    <style>
        .glass-box {
            background: rgba(255,255,255,0.92); /* Softer white with slight transparency */
            border-radius: 12px;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        .glass-box h1, .glass-box h2 {
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)
