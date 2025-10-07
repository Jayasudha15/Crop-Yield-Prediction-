import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from utils import apply_styles, check_login, add_logout_button

# Color palettes for light/dark mode
light_palette = {
    "accent": "#005A9E", "text": "#1E2A38", "background": "#F4F6F8",
    "container_bg": "#FFFFFF", "container_border": "rgba(0,0,0,0.08)",
    "sidebar_bg": "#FFFFFF",
    "season_colors": {'Kharif': '#0068C9', 'Rabi': '#3E9BEE', 'Whole Year': '#7F7F7F',
                      'Autumn': '#FFA500', 'Summer': '#FF6347', 'Winter': '#4682B4'},
    "treemap_scale": "Blues"
}
dark_palette = {
    "accent": "#00A9E0", "text": "#F0F2F6",
    "container_bg": "rgba(255, 255, 255, 0.08)",
    "container_border": "rgba(255, 255, 255, 0.2)",
    "sidebar_bg": "rgba(255, 255, 255, 0.05)",
    "season_colors": {'Kharif': '#00A9E0', 'Rabi': '#1effbc', 'Whole Year': '#f0f2f6',
                      'Autumn': '#ffab00', 'Summer':'#ff5e78','Winter':'#a77eff'},
    "treemap_scale": "GnBu"
}
CHART_HEIGHT = 400

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("train.csv")
        df['Area'] = df['Area'].replace(0, 1e-6)
        df.dropna(subset=['Yield', 'Fertilizer', 'Area', 'Production'], inplace=True)
        df['Pesticide'] = df['Fertilizer'] * 0.2
        return df
    except FileNotFoundError:
        st.error("Dataset 'train.csv' not found.")
        return None

@st.cache_data
def get_feature_importance(df):
    features = ['Season', 'Area', 'Fertilizer', 'Pesticide']
    target = 'Yield'
    preprocessor = ColumnTransformer(transformers=[
        ('num', 'passthrough', ['Area', 'Fertilizer', 'Pesticide']),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['Season'])
    ])
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    model.fit(df[features], df[target])

    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
    clean_names = [name.replace('num__','').replace('cat__','') for name in feature_names]
    importances = model.named_steps['regressor'].feature_importances_

    return pd.DataFrame({'Feature': clean_names, 'Importance': importances}).sort_values('Importance', ascending=False).head(10)

def get_chart_layout(palette, height=CHART_HEIGHT, x_tick_size=16, y_tick_size=16, **kwargs):
    template = "plotly_white" if st.session_state.theme == "Light" else "plotly_dark"
    layout = {
        "template": template,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Poppins, sans-serif", "size": 14, "color": palette['text']},
        "title_font_size": 5,
        "xaxis": {"title_font_size": 18, "tickfont": {"size": x_tick_size, "color": palette['text']}},
        "yaxis": {"title_font_size": 18, "tickfont": {"size": y_tick_size, "color": palette['text']}},
        "height": height,
        "margin": dict(t=40, b=60, l=140, r=40),
        "showlegend": False
    }
    layout.update(kwargs)
    return layout

def display_kpis(df_crop):
    avg_yield = df_crop['Yield'].mean()
    total_area = df_crop['Area'].sum()
    avg_fertilizer = df_crop['Fertilizer'].mean()
    avg_pesticide = df_crop['Pesticide'].mean()

    kpi_data = [
        ("🌱", "Average Yield", f"{avg_yield:.2f}", "tonnes / ha"),
        ("🗺️", "Total Cultivation Area", f"{total_area/1e6:,.2f}M", "hectares"),
        ("🧪", "Average Fertilizer Use", f"{avg_fertilizer:.2f}", "kg / ha"),
        ("🐞", "Avg. Pesticide Use", f"{avg_pesticide:.2f}", "kg / ha (Est.)")
    ]

    kpi_cols = st.columns(4)
    for col, (icon, title, value, unit) in zip(kpi_cols, kpi_data):
        with col, st.container(border=True):
            st.markdown(f"""
                <div style="text-align:center; padding: 10px;">
                <div style="font-size:2.5rem;">{icon}</div>
                <div style="font-size:1rem; opacity:0.7;">{title}</div>
                <div style="font-size:1.8rem; font-weight:600;">{value}</div>
                <div style="font-size:0.9rem; opacity:0.7;">{unit}</div>
                </div>""", unsafe_allow_html=True)

def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"

    check_login("the Data Analysis page")
    df = load_data()
    if df is None:
        st.stop()

    palette = light_palette if st.session_state.theme == "Light" else dark_palette
    if st.session_state.theme == "Light":
        apply_styles(bg_color=palette["background"])
    else:
        apply_styles()

    # --- UPDATED CSS BLOCK ---
    st.markdown("""
    <style>
                /* Reduce top padding of the main page */
        .block-container {
          padding-top: 0rem;
        }  
    /* Corrected CSS for the Sidebar Selectbox */

    /* Style the main container of the selectbox */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #374151;
        border: 2px solid #05e9ff;
        border-radius: 8px;
        padding: 1px; /* Adjusted padding */
    }

    /* CRITICAL FIX: Target the container for the selected value and style the text */
    [data-testid="olid #05e9ff;stSidebar"] div[data-baseweb="select"] .baseweb-Select__value-container {
        color: white !important; /* This makes the selected crop name visible */
        font-weight: 700;
        font-size: 1.15rem;
    }

    /* Style the dropdown arrow to be white */
    [data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: white !important;
    }

    /* Style the dropdown menu that appears on click */
    ul[role="listbox"] li {
        background-color: #374151;
        color: white;
    }
    ul[role="listbox"] li:hover {
        background-color: #4B5563;
    }
    </style>
    """, unsafe_allow_html=True)
    # --- END OF UPDATE ---


    with st.sidebar:

        all_crops = sorted(df['Crop'].dropna().unique())
        selected_crop = st.selectbox(
            "Select a Crop",
            options=all_crops,
            index=all_crops.index('Rice') if 'Rice' in all_crops else 0
        )
        
        add_logout_button()

    crop_df = df[df['Crop'] == selected_crop].copy()
    st.title(f"🌿 Interactive Analysis for {selected_crop}")
    if crop_df.empty:
        st.warning(f"No data available for the selected crop: {selected_crop}")
        st.stop()

    display_kpis(crop_df)

    row1_col1, row1_col2 = st.columns(2, gap="large")
    with row1_col1, st.container(border=True):
        st.subheader("Top States by Average Yield")
        top_states_yield = crop_df.groupby('State')['Yield'].mean().nlargest(10).sort_values()
        fig = go.Figure(go.Bar(
            x=top_states_yield.values, y=top_states_yield.index,
            orientation='h', marker_color=palette['accent']
        ))
        layout = get_chart_layout(palette, x_tick_size=16, y_tick_size=16)
        layout['margin']['l'] = 160
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    with row1_col2, st.container(border=True):
        st.subheader("Key Factors for the Yield")
        importance_df = get_feature_importance(crop_df)
        fig = px.bar(
            importance_df, x='Importance', y='Feature', orientation='h',
            text_auto='.2f', color_discrete_sequence=[palette['accent']]
        )
        layout = get_chart_layout(palette, x_tick_size=16, y_tick_size=16)
        layout['yaxis']['categoryorder'] = "total ascending"
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2, gap="large")
    with row2_col1, st.container(border=True):
        st.subheader("Seasonal Performance")
        seasonal_yield = crop_df.groupby('Season')['Yield'].mean().reset_index()
        fig = px.bar(
            seasonal_yield, x='Season', y='Yield', color='Season',
            color_discrete_map=palette['season_colors']
        )
        fig.update_layout(**get_chart_layout(palette, x_tick_size=16, y_tick_size=16, showlegend=True))
        st.plotly_chart(fig, use_container_width=True)

    with row2_col2, st.container(border=True):
        st.subheader("Top Producing States")
        production_df = crop_df.groupby('State')['Production'].sum().nlargest(10).reset_index()
        fig = px.treemap(
            production_df, path=[px.Constant("All States"), 'State'], values='Production',
            color='Production', color_continuous_scale=palette['treemap_scale']
        )
        fig.update_traces(textinfo="label+value", hoverinfo="label+value+percent root")
        fig.update_layout(**get_chart_layout(palette))
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Inputs vs. Cultivation Area")
        area_min, area_max = float(crop_df['Area'].min()), float(crop_df['Area'].max())
        selected_range = st.slider(
            "Filter by Cultivation Area (Hectares)",
            min_value=area_min, max_value=area_max,
            value=(area_min, area_max)
        )
        chart_df = crop_df[crop_df['Area'].between(*selected_range)]

        fig = px.scatter(
            chart_df, x='Area', y='Fertilizer', color='Season', size='Pesticide',
            hover_data=['State', 'Yield'], color_discrete_map=palette['season_colors']
        )
        fig.update_layout(**get_chart_layout(palette, height=500, x_tick_size=16, y_tick_size=16, showlegend=True))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(f"View Filtered Data for {selected_crop}", expanded=False):
            st.dataframe(chart_df)

if __name__ == "__main__":
    main()