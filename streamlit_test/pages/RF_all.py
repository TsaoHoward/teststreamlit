import streamlit as st
import pandas as pd
import altair as alt

# Custom menu function
from menu import menu

menu()

# Load data with caching
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")
def load_data(url):
    df = pd.read_csv(url)
    return df

data_2012_2017 = {
    'Feature': ['南科房屋交易密度1km', '建物移轉總面積坪', '屋齡區間_未滿3年', '嫌惡設施_1000m_1500m',
                '嫌惡設施_500m_1000m', '迎毗設施_1000m_1500m', '嫌惡設施_0m_500m', '建材種類_鋼筋',
                '交易日', '迎毗設施_500m_1000m'],
    'Importance': [0.161147, 0.144616, 0.123807, 0.086624, 0.046105, 0.042527, 
                   0.035032, 0.029498, 0.028447, 0.027357]
}

data_2018_2023 = {
    'Feature': ['南科房屋交易密度1km', '屋齡區間_21年以上－未滿30年', '陽台有無', '嫌惡設施_1000m_1500m',
                '建物移轉總面積坪', '是否包含車位', '嫌惡設施_500m_1000m', '嫌惡設施_0m_500m',
                '迎毗設施_1000m_1500m', '迎毗設施_500m_1000m'],
    'Importance': [0.203884, 0.105928, 0.092646, 0.080877, 0.070971, 0.053769, 
                   0.042363, 0.038192, 0.032098, 0.031010]}

# Creating dataframes
df_2012_2017 = pd.DataFrame(data_2012_2017)
df_2018_2023 = pd.DataFrame(data_2018_2023)

# Altair chart
chart = alt.Chart(df_2012_2017).mark_bar().encode(
    x=alt.X('Importance', title="特徵重要性"),
    y=alt.Y('Feature', sort='-x', title="2012-2017 特徵"),
    color='Feature:N',
    tooltip=['Feature', 'Importance']
).properties(
    width=800,
    height=400
)

# Streamlit app
st.title("Yearly Feature Importance Changes")
st.altair_chart(chart, use_container_width=True)

chart = alt.Chart(df_2012_2017).mark_bar().encode(
    x=alt.X('Importance', title="特徵重要性"),
    y=alt.Y('Feature', sort='-x', title="2018-2023 特徵"),
    color='Feature:N',
    tooltip=['Feature', 'Importance']
).properties(
    width=800,
    height=400
)

# Streamlit app
st.title("Yearly Feature Importance Changes")
st.altair_chart(chart, use_container_width=True)


data = {
    "year": [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "屋齡等級": [0.212276, 0.161982, 0.180656, 0.197343, 0.193817, 0.154248, 0.151360, 0.145616, 0.174389, 0.165569, 0.138923, 0.137386],
    "建物移轉總面積坪": [0.204430, 0.198052, 0.179977, 0.163105, 0.173457, 0.181475, 0.168218, 0.122992, 0.123445, 0.106105, 0.091251, 0.101763],
    "KDE_1km": [0.172320, 0.215064, 0.264660, 0.221705, 0.261713, 0.227436, 0.228081, 0.294876, 0.264986, 0.277946, 0.238179, 0.187211],
    "外圍嫌惡設施": [0.098329, 0.094806, 0.077010, 0.096296, 0.073067, 0.098365, 0.117224, 0.077063, 0.097850, 0.081301, 0.063514, 0.064936],
    "外圍迎毗設施": [0.077337, 0.065225, 0.047151, 0.056002, 0.052789, 0.053996, 0.046686, 0.047813, 0.054786, 0.033012, 0.030797, 0.033254],
    "周邊嫌惡設施指數": [0.066518, 0.067801, 0.070573, 0.067339, 0.058878, 0.062795, 0.057574, 0.069265, 0.058374, 0.067034, 0.052746, 0.061351],
    "功能性空間比例": [0.055581, 0.047769, 0.050272, 0.051186, 0.046999, 0.046452, 0.039377, 0.049684, 0.052659, 0.041385, 0.032402, 0.038277],
    "周邊迎毗設施評分": [0.049076, 0.037113, 0.036944, 0.038639, 0.036083, 0.040526, 0.039443, 0.041092, 0.029763, 0.029746, 0.028846, 0.027258],
    "有無電梯": [0.017172, 0.016223, 0.017807, 0.026646, 0.020794, 0.024147, 0.036409, 0.019817, 0.016008, 0.010734, 0.008170, 0.005955],
    "有無管理組織": [0.013932, 0.008059, 0.017080, 0.013178, 0.012655, 0.009340, 0.011889, 0.011312, 0.011648, 0.019482, 0.008759, 0.037414],
    "新型建材": [0.013250, 0.011495, 0.016019, 0.013024, 0.016193, 0.015188, 0.010649, 0.009518, 0.002647, 0.003158, 0.002109, 0.001126],
    "陽台有無": [0.012769, 0.025361, 0.035105, 0.051105, 0.047859, 0.077423, 0.087178, 0.100618, 0.079148, 0.100441, 0.145582, 0.105491],
    "是否包含車位": [0.007011, 0.051050, 0.006748, 0.004430, 0.005696, 0.008610, 0.005912, 0.010333, 0.034297, 0.064087, 0.158720, 0.198579]
}

# Creating the DataFrame
df1 = pd.DataFrame(data)

df_melted = df1.melt(id_vars=["year"], var_name="Feature", value_name="Importance")

# Create a stacked bar chart with Altair
chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("year:N", title="Year"),
    y=alt.Y("Importance:Q", stack="zero", title="Cumulative Importance"),
    color="Feature:N",
    tooltip=["Feature", "Importance"]
).properties(
    width=800,
    height=400
)

# Streamlit app
st.title("Yearly Feature Importance Changes")
st.altair_chart(chart, use_container_width=True)
