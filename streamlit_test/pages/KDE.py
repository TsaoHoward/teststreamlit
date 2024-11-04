import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import pydeck as pdk

from menu import menu

menu()

@st.cache_data()
def load_data(url):
    df = pd.read_csv(url)
    return df

df = pd.read_csv("data/map.csv")

# Create a slider for selecting the year
year_min = int(df['交易年份'].min()) + 1
year_max = int(df['交易年份'].max()) - 1
selected_year = st.sidebar.slider("選擇交易年份", year_min, year_max, year_min)

# Filter the data based on the selected year
map_data = df[df['交易年份'] == selected_year][['經度', '緯度', 'KDE_class']]
map_data = map_data.rename(columns={'經度': 'longitude', '緯度': 'latitude'})

# Define a function to map 'Region' to colors
# Define a function to map 'Region' to colors for categories A-F
def get_color(region):
    color_map = {
        1: [255, 0, 0],    # Red
        2: [0, 255, 0],    # Green
        3: [0, 0, 255],    # Blue
        }
    return color_map.get(region, [0, 0, 0])  # Default to black if region is not in A-F

# Apply the color function to the data
map_data['color'] = map_data['KDE_class'].apply(get_color)

# Create PyDeck layer using the map data with colors based on 'Region'
selected_layers = [
    pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[longitude, latitude]',
        get_radius=100,
        get_fill_color='color',
        opacity=1.0,
    )
]

# Render the map
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state={
            "latitude": 23.13,
            "longitude": 120.312480,
            "zoom": 9,
            "pitch": 10,
        },
        layers=selected_layers,
    )
)