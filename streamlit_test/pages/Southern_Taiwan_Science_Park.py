import streamlit as st
import pandas as pd
import altair as alt
from menu import menu

@st.cache_data(ttl=3600, show_spinner="正在加載資料...")
def load_data(url):
    df = pd.read_csv(url)
    return df

menu()

# Load the data
df = load_data("data/park1015.csv")

# Drop the specified column
df = df.drop(columns='平均單價元平方公尺')

# Ensure '西元年月' is present before setting it as the index
if '西元年月' in df.columns:
    df.sort_values('西元年月', inplace=True)
    df.set_index('西元年月', inplace=True)
else:
    st.error("欄位 '西元年月' 不存在於資料中，請檢查資料檔案。")

st.title('南科各項指標')

# Transform df1 for the Altair line chart
df1 = df[['博士', '碩士', '大學', '專科', '高中', '其他學歷']].reset_index()
line_chart = alt.Chart(df1).transform_fold(
    ['博士', '碩士', '大學', '專科', '高中', '其他學歷'],
    as_=['Category', 'Value']
).mark_line().encode(
    x='西元年月:T',
    y='Value:Q',
    color=alt.Color('Category:N', legend=alt.Legend(orient='right'))  # 將圖例固定在右側
).properties(
    width=800,  # 固定圖表寬度
    height=400,
    bounds='flush',  # 確保圖表邊界不會擴展
    padding={'right': 100}  # 增加右側內邊距以容納圖例
)

st.altair_chart(line_chart)

# Transform df2 for another Altair line chart
df2_formatted = df[['積體電路營業額(億元)', '光電營業額(億元)', '電腦及周邊營業額(億元)', '通訊營業額(億元)', '精密機械營業額(億元)', '生物技術營業額(億元)', '其他營業額']].reset_index()
df2_chart = alt.Chart(df2_formatted).transform_fold(
    ['積體電路營業額(億元)', '光電營業額(億元)', '電腦及周邊營業額(億元)', '通訊營業額(億元)', '精密機械營業額(億元)', '生物技術營業額(億元)', '其他營業額'],
    as_=['Category', 'Value']
).mark_line().encode(
    x='西元年月:T',
    y='Value:Q',
    color=alt.Color('Category:N', legend=alt.Legend(orient='right'))  # 將圖例固定在右側
).properties(
    width=800,  # 固定圖表寬度
    height=400,
    bounds='flush',  # 確保圖表邊界不會擴展
    padding={'right': 100}  # 增加右側內邊距以容納圖例
)
st.altair_chart(df2_chart)

# Transform df4 for the last Altair line chart
df4_formatted = df[['用水量(CMD)', '污水處理量(CMD)']].reset_index()
df4_chart = alt.Chart(df4_formatted).transform_fold(
    ['用水量(CMD)', '污水處理量(CMD)'],
    as_=['Category', 'Value']
).mark_line().encode(
    x='西元年月:T',
    y='Value:Q',
    color=alt.Color('Category:N', legend=alt.Legend(orient='right'))  # 將圖例固定在右側
).properties(
    width=800,  # 固定圖表寬度
    height=400,
    bounds='flush',  # 確保圖表邊界不會擴展
    padding={'right': 100}  # 增加右側內邊距以容納圖例
)

st.altair_chart(df4_chart)

# Dropdown selection for columns
selected_columns = st.multiselect("選擇要查看的欄位", df.columns)

# Check if any columns are selected
if selected_columns:
    st.line_chart(df[selected_columns], use_container_width=True)
else:
    st.write("請選擇至少一個欄位來顯示圖表")
