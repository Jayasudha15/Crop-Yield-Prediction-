import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils import check_login, add_logout_button, apply_styles  # Using utils functions

# --- Page Configuration ---
st.set_page_config(page_title="Model Comparison", layout="wide")
check_login("the Model Comparison page")

# --- Theme Initialization ---
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"

# --- Theme Palettes ---
light_palette = {
    "accent": "#005A9E", "text": "#1E2A38", "background": "#F4F6F8",
    "container_bg": "#F4F6F8", "container_border": "rgba(0,0,0,0.08)",
    "sidebar_bg": "#FFFFFF"
}
dark_palette = {
    "accent": "#00A9E0", "text": "#F0F2F6",
    "background": "#162138",
    "container_bg": "#162138",
    "container_border": "rgba(255, 255, 255, 0.2)",
    "sidebar_bg": "#19243B"
}
palette = light_palette if st.session_state.theme == "Light" else dark_palette

# --- Apply Styles ---
if st.session_state.theme == "Light":
    apply_styles(bg_color=palette["background"])
else:
    apply_styles()

# --- Extra CSS for fonts and transparent containers ---
st.markdown(
    """
    <style>
    /* Reduce top padding of the main page */
        .block-container {
          padding-top: 0rem;
        }  
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    h1 { font-size: 4.5rem !important; font-weight: 800 !important; text-align: center; }
    h2 { font-size: 3.2rem !important; font-weight: 700 !important; }
    h3 { font-size: 2.5rem !important; font-weight: 700 !important; }
    p, li, label, .stMarkdown { font-size: 1.25rem !important; font-weight: 700 !important; }
    [data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] > div > div {
        background: transparent !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Chart Layout ---
def get_chart_layout():
    template = "plotly_white" if st.session_state.theme == "Light" else "plotly_dark"
    return {
        "template": template,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 16, "family": "Poppins, sans-serif", "color": palette['text']},
        "title": {"font": {"size": 26, "family": "Poppins, sans-serif", "color": palette['text']}},
        "xaxis": {"title": {"font": {"size": 18, "color": palette['text']}}, "tickfont": {"size": 14, "color": palette['text']}},
        "yaxis": {"title": {"font": {"size": 18, "color": palette['text']}}, "tickfont": {"size": 14, "color": palette['text']}},
        "height": 500,
        "margin": dict(t=40, b=60, l=60, r=60),
        "showlegend": False,
    }

chart_layout_opts = get_chart_layout()

# --- Theme Toggle ---
def toggle_theme():
    st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"

st.sidebar.button(
    f"Switch to {'Dark' if st.session_state.theme == 'Light' else 'Light'} Mode",
    on_click=toggle_theme, use_container_width=True
)
add_logout_button()

# --- Load Data ---
try:
    performance_data = joblib.load('model_performance.joblib')
    performance_df = pd.DataFrame(performance_data).T.reset_index()
    performance_df.rename(columns={'index': 'Model'}, inplace=True)
    performance_df.columns = performance_df.columns.str.strip()
except FileNotFoundError:
    st.error("Model performance file not found. Please run `train_model.py` first.")
    st.stop()

# --- Main Content ---
st.title("🤖 Machine Learning Model Comparison")
st.markdown("""
This page shows the performance of different machine learning models trained to predict crop yield.  
We use two key metrics for evaluation:  
- **R-squared (R²):** Closer to 1 is better.  
- **Root Mean Squared Error (RMSE):** Lower is better.
""")
st.markdown("---")

# Performance Table
st.subheader("Model Performance Metrics")
st.markdown(performance_df.to_markdown(index=False), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Symlogical columns for charts with equal margins to prevent suppressed look
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("R-squared (R²) Comparison")
    fig1 = px.bar(
        performance_df,
        x="Model",
        y="R-squared",
        text="R-squared",
        labels={"Model": "Model", "R-squared": "R-squared (Higher is Better)"},
        color_discrete_sequence=[palette['accent']],
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        height=500,
        margin=dict(t=40, b=60, l=60, r=60),  # equal margins for natural alignment
        showlegend=False,
        template="plotly_white" if st.session_state.theme == "Light" else "plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Model",
        yaxis_title="R-squared (Higher is Better)"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Root Mean Squared Error (RMSE) Comparison")
    fig2 = px.bar(
        performance_df,
        x="Model",
        y="RMSE",
        text="RMSE",
        labels={"Model": "Model", "RMSE": "RMSE (Lower is Better)"},
        color_discrete_sequence=[palette['accent']],
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        height=500,
        margin=dict(t=40, b=60, l=60, r=60),  # equal margins for natural alignment
        showlegend=False,
        template="plotly_white" if st.session_state.theme == "Light" else "plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Model",
        yaxis_title="RMSE (Lower is Better)"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Styled, large Conclusion text
best_model_name = performance_df.loc[performance_df['R-squared'].idxmax()]['Model']
conclusion_text = f"🏆 **Conclusion:** Based on the R-squared metric, the **{best_model_name}** is the most suitable model for this prediction task."
st.markdown(
    f'<div style="background-color:{palette["container_bg"]}; '
    f'border-left: 6px solid {palette["accent"]}; border-radius: 12px; '
    f'padding: 20px; font-size: 1.5rem; font-weight: 700; margin-top: 1rem;">{conclusion_text}</div>',
    unsafe_allow_html=True,
)
