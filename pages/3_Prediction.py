import streamlit as st
import pandas as pd
import joblib
from utils import check_login, add_logout_button, apply_styles  # Custom utilities

# ------------------ CONFIG ------------------ #
st.set_page_config(page_title="Prediction", page_icon="📈", layout="wide")
check_login("the Prediction Page")
apply_styles('assets/background.jpg')
add_logout_button()

# ------------------ LOAD MODEL & ENCODERS ------------------ #
@st.cache_resource
def load_resources():
    """Load model and label encoders with caching."""
    try:
        model = joblib.load('best_model.joblib')
        label_encoders = joblib.load('label_encoders.joblib')
        return model, label_encoders
    except Exception as e:
        st.error(f"Could not load model files. Error: {e}")
        return None, None

model, label_encoders = load_resources()
if model is None or label_encoders is None:
    st.stop()

# ------------------ FORM FUNCTION ------------------ #
def build_form():
    """Builds the prediction form and returns input values."""
    # Title in glass box, use span with custom class for size control
    st.markdown('<div class="glass-box"><span class="glass-box-title">📈 Crop Yield Prediction</span></div>', unsafe_allow_html=True)

    # Forced visible space between title and form
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    with st.form(key='prediction_form'):
        st.markdown("<h2>Enter Prediction Details</h2>", unsafe_allow_html=True)

        state = st.selectbox(
            "State :", label_encoders['State'].classes_,
            key="state_input", help="Example: Tamil Nadu, Punjab, Maharashtra"
        )
        season = st.selectbox(
            "Season :", label_encoders['Season'].classes_,
            key="season_input", help="Example: Kharif, Rabi, Summer"
        )
        crop = st.selectbox(
            "Crop :", label_encoders['Crop'].classes_,
            key="crop_input", help="Example: Rice, Wheat, Maize"
        )
        area = st.number_input(
            "Area (Hectares) :", min_value=0.1, step=0.1, format="%.1f",
            key="area_input", help="Example: 5.5"
        )
        fertilizer = st.number_input(
            "Fertilizer Usage (kg/ha) :", min_value=0.0, step=1.0, format="%.1f",
            key="fertilizer_input", help="Example: 150.0"
        )
        pesticide = st.number_input(
            "Pesticide Usage (kg/ha) :", min_value=0.0, step=1.0, format="%.1f",
            key="pesticide_input", help="Example: 3.5"
        )
        rainfall = st.number_input(
            "Annual Rainfall (mm) :", min_value=0.0, step=1.0, format="%.1f",
            key="rainfall_input", help="Example: 900.0"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Predict Crop Yield")

    return submitted, state, season, crop, area, rainfall, fertilizer, pesticide

# ------------------ PREDICTION FUNCTION ------------------ #
def predict_yield(state, season, crop, area, rainfall, fertilizer, pesticide):
    """Encodes inputs and predicts yield."""
    input_data = pd.DataFrame([{
        'State': label_encoders['State'].transform([state])[0],
        'Season': label_encoders['Season'].transform([season])[0],
        'Crop': label_encoders['Crop'].transform([crop])[0],
        'Area': area,
        'Annual_Rainfall': rainfall,
        'Fertilizer': fertilizer,
        'Pesticide': pesticide
    }])

    if hasattr(model, 'feature_names_in_'):
        try:
            input_data = input_data[model.feature_names_in_]
        except KeyError as e:
            st.error(f"Feature mismatch: {e}")
            st.stop()

    prediction = model.predict(input_data)[0]
    return prediction

# ------------------ MAIN APP ------------------ #
left_space, main_col, right_space = st.columns((0.5, 2.5, 0.5))
with main_col:
    submitted, state, season, crop, area, rainfall, fertilizer, pesticide = build_form()

    if submitted:
        if area <= 0 or rainfall <= 0:
            st.warning("Area and Rainfall should be greater than zero for realistic predictions.")
        else:
            with st.spinner("Calculating the prediction..."):
                prediction = predict_yield(state, season, crop, area, rainfall, fertilizer, pesticide)

            st.markdown(
                f"""
                <div class="result-box">
                    <span style="font-size: 1.5rem;">Estimated Crop Yield</span><br>
                    <p class="yield-value">{prediction:.2f}</p>
                    <span style="font-size: 1.5rem;">tonnes per hectare</span>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Leave your style.css and all other assets as is; just add the .glass-box-title ---


# --- CUSTOM CSS (UNCHANGED, ALREADY CORRECT) --- #
st.markdown(
    """
    <style>
        /* Reduce top padding of the main page */
        .block-container {
            padding-top: 2rem; /* Adjusted for better initial spacing */
        }
        /* Add right padding to the main container to avoid overlay with deploy button */
        .main {
            padding-right: 90px !important;
        }

        .glass-box-title {
    font-size: 3rem !important;        /* Adjust to your preference */
    font-weight: 800 !important;
    color: #1E2A38 !important;
    white-space: nowrap;
    text-align: center;
    display: block;
}


        /* --- FIX 1: TITLE STYLING --- */
        .glass-box {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 0rem;
            text-align: center;
        }
        .glass-box h1 {
            white-space: nowrap; /* Keep it on one line */
            font-size: 2rem;
            font-weight: 700;
            color: #1E2A38;
            margin: 0;
        }

        /* --- FIX 2: FORM HEADER SPACING --- */
        div[data-testid="stForm"] h2 {
            margin-bottom: rem !important; /* Reduces the space below "Enter Prediction Details" */
            text-align: center;
            font-size: 1.8rem;
            color: #1E2A38;
        }

        /* Form background */
        div[data-testid="stForm"] {
            background-color: #E6F3FA;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        }
        /* Select and number inputs uniform height */
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] div[role="combobox"],
        div[data-baseweb="input"] > div {
            min-height: 60px !important;
            font-size: 1rem !important;
            display: flex !important;
            align-items: center !important;
        }
        /* Text inside selects */
        div[data-baseweb="select"] span {
            line-height: normal !important;
            font-size: 1rem !important;
        }
        /* Input text alignment */
        input {
            font-size: 1rem !important;
            padding: 8px !important;
        }
        /* Wider selects and dropdowns */
        div[data-baseweb="select"] {
            min-width: 260px !important;
        }
        ul[role="listbox"] {
            min-width: 260px !important;
        }
        /* Labels */
        label {
            color: #1E2A38 !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }
        /* Buttons */
        div.stButton > button, div.stForm button, button {
            background: linear-gradient(90deg, #4CAF50 0%, #2E8B57 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !importan;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 8px 20px rgba(46,139,87,0.18) !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease !important;
        }
        div.stButton > button:hover, div.stForm button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 14px 30px rgba(46,139,87,0.22) !important;
        }
        div[data-testid="stForm"] div.stButton > button {
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
