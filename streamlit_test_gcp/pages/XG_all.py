import streamlit as st
import pandas as pd
import altair as alt

from menu import menu

menu()

@st.cache_data(ttl=3600, show_spinner="正在加載資料...")
def load_data(url):
    df = pd.read_csv(url)
    return df

data_2012_2017 = {
    'Feature': ['屋齡區間_未滿3年', '建材種類_鋼筋', '屋齡區間_12年以上－未滿21年', '建築型態_公寓', 
                '建材種類_未知', '屋齡區間_21年以上－未滿30年', '屋齡區間_3年以上－未滿12年', 
                '屋齡區間_30年以上', '南科房屋交易密度1km', '建築型態_其他'],
    'Importance': [0.202681, 0.099877, 0.097316, 0.080442, 0.072742, 0.052455, 
                   0.034760, 0.025517, 0.025161, 0.025105]
}

data_2018_2023 = {
    'Feature': ['屋齡區間_21年以上－未滿30年', '陽台有無', '建築型態_公寓', '是否包含車位', 
                '土地用途_未知', '南科房屋交易密度1km', '屋齡區間_12年以上－未滿21年', 
                '屋齡區間_3年以上－未滿12年', '屋齡區間_未滿3年', '建材種類_磚石'],
    'Importance': [0.310060, 0.113863, 0.108146, 0.095158, 0.042647, 0.022632, 
                   0.022046, 0.020895, 0.018399, 0.017951]
}

# Creating dataframes
df_2012_2017 = pd.DataFrame(data_2012_2017)
df_2018_2023 = pd.DataFrame(data_2018_2023)

# Altair chart
chart = alt.Chart(df_2012_2017).mark_bar().encode(
    x=alt.X('Importance', title="特徵重要性"),
    y=alt.Y('Feature', sort='-x', title="2012-2017 特徵"),
    color=alt.Color("Feature:N").legend(None),
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
    y=alt.Y('Feature', sort='-x', title="2012-2017 特徵"),
    color=alt.Color("Feature:N").legend(None),
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
    "屋齡等級": [0.329273, 0.210073, 0.289471, 0.324261, 0.278667, 0.273782, 0.261632, 0.241245, 0.242537, 0.249110, 0.135712, 0.159118],
    "有無電梯": [0.132175, 0.074796, 0.073288, 0.101453, 0.108569, 0.115470, 0.158196, 0.086267, 0.055491, 0.035112, 0.021067, 0.015827],
    "新型建材": [0.089081, 0.086640, 0.116456, 0.122060, 0.181700, 0.074802, 0.046172, 0.048967, 0.019804, 0.021122, 0.011137, 0.017675],
    "外圍迎毗設施": [0.072234, 0.056972, 0.041239, 0.041141, 0.040006, 0.044667, 0.040219, 0.038469, 0.044641, 0.019576, 0.015764, 0.018332],
    "建物移轉總面積坪": [0.057760, 0.041599, 0.053488, 0.037522, 0.039192, 0.051823, 0.047882, 0.030072, 0.028145, 0.018312, 0.010725, 0.009910],
    "外圍嫌惡設施": [0.053655, 0.033752, 0.044885, 0.048363, 0.032265, 0.048029, 0.060988, 0.033330, 0.047203, 0.031979, 0.017805, 0.020961],
    "KDE_1km": [0.050436, 0.055765, 0.099903, 0.061787, 0.072864, 0.068952, 0.064945, 0.093379, 0.085174, 0.071874, 0.041418, 0.031148],
    "有無管理組織": [0.044647, 0.018442, 0.059075, 0.032211, 0.035612, 0.023975, 0.026443, 0.036327, 0.030201, 0.031015, 0.012477, 0.032503],
    "周邊迎毗設施評分": [0.038250, 0.028661, 0.039087, 0.032999, 0.032470, 0.031758, 0.038926, 0.042880, 0.030267, 0.020721, 0.013648, 0.015687],
    "陽台有無": [0.036162, 0.041994, 0.071849, 0.106848, 0.100113, 0.164624, 0.172763, 0.205878, 0.196630, 0.220428, 0.191807, 0.163099],
    "功能性空間比例": [0.036071, 0.024810, 0.034369, 0.032954, 0.030916, 0.031947, 0.029619, 0.038500, 0.035518, 0.023761, 0.012634, 0.015692],
    "是否包含車位": [0.030444, 0.296183, 0.035663, 0.027247, 0.022244, 0.036799, 0.020031, 0.061644, 0.154199, 0.230231, 0.500377, 0.481525],
    "周邊嫌惡設施指數": [0.029811, 0.030313, 0.041228, 0.031154, 0.025383, 0.033373, 0.032185, 0.043043, 0.030191, 0.026760, 0.015429, 0.018523]
}


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
