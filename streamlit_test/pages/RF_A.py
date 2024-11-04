import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static, st_folium
from menu import menu  # 確保您有一個名為 menu 的模塊
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px

# 初始化 session state 用於保存點擊的位置和提交的表單數據
if 'clicked_location' not in st.session_state:
    st.session_state.clicked_location = None

if 'submitted_data' not in st.session_state:
    st.session_state.submitted_data = None

# 調用自定義的菜單函數
menu()

# 使用快取裝飾器來緩存數據加載函數
@st.cache_data
def load_geojson(filepath, ttl=3600, show_spinner="正在加載資料..."):
    try:
        return gpd.read_file(filepath)
    except Exception as e:
        st.error(f"無法加載 GeoJSON 文件: {e}")
        st.stop()

@st.cache_data
def load_csv(filepath, ttl=3600, show_spinner="正在加載資料..."):
    try:
        df = pd.read_csv(filepath)
        # 計算 'good_count_0_1500' 和 'bad_count_0_1500'
        # df['good_count_0_1500'] = df['good_count_0_500'] + df['good_count_500_1000'] + df['good_count_1000_1500']
        # df['bad_count_0_1500'] = df['bad_count_0_500'] + df['bad_count_500_1000'] + df['bad_count_0_1500']
        # # 填補缺失值
        # df['good_count_0_1500'] = df['good_count_0_1500'].fillna(0)
        # df['bad_count_0_1500'] = df['bad_count_0_1500'].fillna(0)
        return df[df['交易年份'] >= 2022]
    except Exception as e:
        st.error(f"無法加載地圖數據: {e}")
        st.stop()

# 加載數據（只會在應用啟動時讀取一次）
counties = load_geojson('data/Tainan_County.geojson')
df = load_csv("data/newmap.csv")

# 定義選項
housetype = ["住商大樓", "公寓", "透天厝", "其他"]
materialtype = ["鋼骨", "鋼筋", "磚石", "竹木"]
YNtype = ["有", "無"]

# 定義 KDE_class 的映射字典
KDE_class_mapping = {
    3: "交易熱區: 熱門",
    2: "交易熱區: 中等",
    1: "交易熱區: 普通"
}

# 計算哈弗辛距離的函數
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半徑，單位：公里
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# 創建基礎地圖
m = folium.Map(
    location=[23.13, 120.312480],
    zoom_start=10,
)

# 添加縣界 GeoJSON 圖層
folium.GeoJson(
    counties,
    style_function=lambda feature: {
        'fillColor': 'white',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.4,
    }
).add_to(m)

# 添加代表南科的灰色標記（預先顯示）
folium.Marker(
    location=(23.11210179661455, 120.27042389614857),
    popup='南科',
    tooltip='南科',
    icon=folium.Icon(color='gray')
).add_to(m)

# 根據 session_state 添加動態標記
if st.session_state.clicked_location:
    if st.session_state.submitted_data:
        submitted = st.session_state.submitted_data
        market_status = submitted['市場狀態']
        # 根據市場狀態設定標記顏色
        if market_status == "行情看漲":
            marker_color = 'green'
        elif market_status == "行情看跌":
            marker_color = 'red'
        else:
            marker_color = 'yellow'  # 持平或其他狀態可以設定為黃色或其他顏色

        # 根據 KDE_class 取得顯示文本
        kde_class_display = KDE_class_mapping.get(submitted.get('KDE_class', '無資料'), '無資料')

        # 確認 'good_count_0_1500' 和 'bad_count_0_1500' 的值
        good_count_0_1500 = submitted.get('good_count_0_1500', '無資料')
        bad_count_0_1500 = submitted.get('bad_count_0_1500', '無資料')
        forecast_prices = submitted.get('forecast_prices', {})  # 獲取預測價格字典

        # 如果是數字，可以轉換為字符串
        if not isinstance(good_count_0_1500, str):
            good_count_0_1500 = str(good_count_0_1500)

        if not isinstance(bad_count_0_1500, str):
            bad_count_0_1500 = str(bad_count_0_1500)

        # 創建更新後的 popup 內容，顯示三個日期的價格
        popup_content = folium.Popup(f"""
        <b>1.5KM內嫌惡設施:</b> {bad_count_0_1500}<br>
        <b>1.5KM內好設施:</b> {good_count_0_1500}<br>
        <b>{kde_class_display}</b><br>
        <b>行政區:</b> {submitted['行政區'] if submitted['行政區'] else '未找到'}<br>
        <b>市場狀態:</b> {submitted['市場狀態']}<br>
        <b>預測價格:</b><br>
        {''.join([f"{date}: {price} 元<br>" for date, price in forecast_prices.items()])}
        """, max_width=300)

    else:
        # 尚未提交，提示用戶提交表單，標記顏色為紅色
        marker_color = 'red'
        popup_content = folium.Popup("請填寫並提交表單以顯示詳情。", max_width=250)

    folium.Marker(
        location=st.session_state.clicked_location,
        popup=popup_content,
        tooltip='點擊查看詳情',
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

# 顯示地圖並獲取點擊數據
map_data = st_folium(m, width=1000, height=500, key="map")

# 如果使用者點擊地圖，更新 session state
if map_data and map_data.get('last_clicked'):
    st.session_state.clicked_location = (map_data['last_clicked']['lat'], map_data['last_clicked']['lng'])
    st.session_state.submitted_data = None  # 重置提交數據

# 表單輸入區，分為兩行顯示
with st.form("input_form"):
    # 第一行：建築型態、主要建材、有無車位、屋齡、房屋坪數
    row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns(5)
    with row1_col1:
        house = st.selectbox("建築型態", housetype, key='select1')
    with row1_col2:
        material = st.multiselect("主要建材", materialtype, key='select2', default=materialtype[1])
    with row1_col3:
        parking = st.radio("有無車位", YNtype, key='select3')
    with row1_col4:
        age = st.number_input("屋齡", min_value=0, max_value=100, value=5)
    with row1_col5:
        area = st.number_input("房屋坪數", min_value=0.5, value=30.0, step=1.0)

    # 第二行：房間數、客廳數、衛浴數、隔間數
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    with row2_col1:
        room = st.number_input("房間數", min_value=1, value=1, step=1)
    with row2_col2:
        living_room = st.number_input("客廳數", min_value=1, value=1, step=1)
    with row2_col3:
        bathroom = st.number_input("衛浴數", min_value=1, value=1, step=1)
    with row2_col4:
        compartment = st.number_input("隔間數", min_value=0, value=0, step=1)

    # 提交按鈕
    submit_button = st.form_submit_button("提交")

# 當表單提交時處理數據
if submit_button:
    if st.session_state.clicked_location:
        clicked_lat, clicked_lon = st.session_state.clicked_location
        point = Point(clicked_lon, clicked_lat)

        town = ""
        # 判斷所點選的行政區
        for index, row in counties.iterrows():
            if row['geometry'].contains(point):
                town = row['TOWN']  
                break

        # 找到距離最短的點
        # 如果 'distance' 欄位不存在，則計算距離
        if 'distance' not in df.columns:
            df['distance'] = df.apply(lambda row: haversine(clicked_lat, clicked_lon, row['緯度'], row['經度']), axis=1)

        closest_row = df.loc[df['distance'].idxmin()]

        closest_price_per_ping = closest_row.get('單價元每坪', 0)
        closest_ID = closest_row.get('編號', '無編號')

        # 假設 newmap.csv 包含 'Predicted', 'Date', 'bad_count_0_1500', 'good_count_0_1500', 'KDE_class' 欄位
        bad_count_0_1500 = closest_row.get('bad_count_0_1500', '無資料')
        good_count_0_1500 = closest_row.get('good_count_0_1500', '無資料')
        KDE_class = closest_row.get('KDE_class', '無資料')

        # 根據 '編號' 和 'Date' 選擇特定時點的 'Predicted'
        forecast_dates = ['2024-12', '2025-01', '2025-02']
        forecast_prices = {}
        for date in forecast_dates:
            # 查找相同 '編號' 和特定 'Date' 的行
            matched_rows = df[(df['編號'] == closest_ID) & (df['Date'] == date)]
            if not matched_rows.empty:
                # 假設每個編號和日期只有一行
                predicted_price = matched_rows.iloc[0]['Predicted']
                forecast_prices[date] = predicted_price
            else:
                forecast_prices[date] = '無資料'

        # 計算行情價格
        actual_price = closest_price_per_ping * area

        if isinstance(predicted_price, (int, float)):
            lower_bound = 0.9 * actual_price
            upper_bound = 1.1 * actual_price
            if predicted_price < lower_bound or predicted_price > upper_bound:
                adjusted_predicted_price = 1.05 * actual_price
                predicted_price = adjusted_predicted_price
        else:
            st.warning("預測價格資料不完整，無法進行調整。")
            predicted_price = '無資料'

        # 比較價格並設定市場狀態
        # 這裡可以選擇如何比較多個預測價格
        # 例如，取最新一個預測價格來比較
        latest_predicted = forecast_prices.get('2025-02', '無資料')
        if isinstance(latest_predicted, (int, float)):
            if latest_predicted > actual_price:
                market_status = "行情看漲"
            elif latest_predicted < actual_price:
                market_status = "行情看跌"
            else:
                market_status = "行情持平"
        else:
            market_status = "無法判斷"

        # 存儲提交的數據到 session_state
        st.session_state.submitted_data = {
            '建築型態': house,
            '主要建材': material,
            '有無車位': parking,
            '屋齡': age,
            '房屋坪數': area,
            '房間數': room,
            '客廳數': living_room,
            '衛浴數': bathroom,
            '隔間數': compartment,
            '行政區': town,
            'bad_count_0_1500': bad_count_0_1500,
            'good_count_0_1500': good_count_0_1500,  # 確保使用正確的欄位名稱
            'KDE_class': KDE_class,
            '市場狀態': market_status,
            'forecast_prices': forecast_prices  # 新增未來三個時點的價格
        }

        # **顯示未來三個時點的價格折線圖，並畫一條紅線顯示行情價**
        price_col1, price_col2 = st.columns([1,3])
        with price_col1:
            st.markdown("### 行情價格:")
            st.write(f"總價: **{round(actual_price, 2)}** 元")
            st.write(f"單價: **{round(actual_price/area, 2)}** 元/坪")
        with price_col2:
            st.markdown("### 價格趨勢:")
            # 準備數據
            forecast_df = pd.DataFrame({
                'Date': list(forecast_prices.keys()),
                'Predicted': [value / 10 for value in forecast_prices.values()]
            })
            # 將 '無資料' 替換為 NaN 以便繪圖
            forecast_df['Predicted'] = pd.to_numeric(forecast_df['Predicted'], errors='coerce')

            # 使用 Plotly 繪製折線圖
            fig = px.line(forecast_df, x='Date', y='Predicted', markers=True, title='價格趨勢')
            fig.update_layout(xaxis_title='日期', yaxis_title='價格 (元)')

            # 添加行情價的紅色水平線
            # fig.add_hline(y=actual_price/area, line_dash="dash", line_color="red",
            #              annotation_text="行情價", annotation_position="bottom right")

            st.plotly_chart(fig, use_container_width=True)

        # 顯示市場狀態，帶有背景色
        # 如果需要，可以保留這部分
        # if market_status == "行情看漲":
        #     bg_color = "background-color: green; color: white; padding: 10px;"
        # elif market_status == "行情看跌":
        #     bg_color = "background-color: red; color: white; padding: 10px;"
        # else:
        #     bg_color = "background-color: yellow; color: black; padding: 10px;"
        # st.markdown(f'<p style="{bg_color}"><strong>市場狀態:</strong> {market_status}</p>', unsafe_allow_html=True)

        # 刪除資料編號顯示
        # st.write(f"**資料編號**: {closest_ID}")
    else:
        st.warning("請先在地圖上點選一個位置。")

# 如果已提交，並且有標記，重新渲染地圖以顯示更新後的 popup
if st.session_state.clicked_location and st.session_state.submitted_data:
    # 重新創建地圖以顯示更新後的標記
    m = folium.Map(
        location=st.session_state.clicked_location,
        zoom_start=15,
    )

    # 添加縣界 GeoJSON 圖層
    folium.GeoJson(
        counties,
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4,
        }
    ).add_to(m)

    # 添加代表南科的灰色標記（預先顯示）
    folium.Marker(
        location=(23.11210179661455, 120.27042389614857),
        popup='南科',
        tooltip='南科',
        icon=folium.Icon(color='gray')
    ).add_to(m)

    # 獲取市場狀態以設定標記顏色
    submitted = st.session_state.submitted_data
    market_status = submitted['市場狀態']
    if market_status == "行情看漲":
        marker_color = 'green'
    elif market_status == "行情看跌":
        marker_color = 'red'
    else:
        marker_color = 'yellow'  # 持平或其他狀態可以設定為黃色或其他顏色

    # 根據 KDE_class 取得顯示文本
    kde_class_display = KDE_class_mapping.get(submitted.get('KDE_class', '無資料'), '無資料')

    # 確認 submitted 的內容
    # 確認 'good_count_0_1500' 和 'bad_count_0_1500' 的值
    good_count_0_1500 = submitted.get('good_count_0_1500', '無資料')
    bad_count_0_1500 = submitted.get('bad_count_0_1500', '無資料')
    forecast_prices = submitted.get('forecast_prices', {})  # 獲取預測價格字典

    # 如果是數字，可以轉換為字符串
    if not isinstance(good_count_0_1500, str):
        good_count_0_1500 = str(good_count_0_1500)

    if not isinstance(bad_count_0_1500, str):
        bad_count_0_1500 = str(bad_count_0_1500)

    # 創建更新後的 popup 內容，顯示三個日期的價格
    popup_content = folium.Popup(f"""
    <b>1.5KM內嫌惡設施:</b> {bad_count_0_1500}<br>
    <b>1.5KM內好設施:</b> {good_count_0_1500}<br>
    <b>{kde_class_display}</b><br>
    <b>行政區:</b> {submitted['行政區'] if submitted['行政區'] else '未找到'}<br>
    <b>市場狀態:</b> {submitted['市場狀態']}<br>
    <b>預測價格:</b><br>
    {''.join([f"{date}: {price} 元<br>" for date, price in forecast_prices.items()])}
    """, max_width=300)

    # 添加動態標記並設定顏色
    folium.Marker(
        location=st.session_state.clicked_location,
        popup=popup_content,
        tooltip='點擊查看詳情',
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

    # 重新顯示更新後的地圖
    folium_static(m, width=1000, height=500)
