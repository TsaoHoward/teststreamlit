import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from shapely import wkt
import streamlit as st
import folium
from streamlit_folium import st_folium  # 需要安裝 streamlit-folium

def read_mysql_to_geojson(table_name, db_config):
    """
    從 MySQL 資料庫讀取指定表格的資料並轉換為 GeoDataFrame。

    :param table_name: 要讀取的 MySQL 表格名稱
    :param db_config: MySQL 連接配置字典
    :return: GeoDataFrame 物件
    """
    # 建立資料庫引擎
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # 撰寫 SQL 查詢，將幾何欄位轉換為 WKT 格式
    query = f"SELECT *, ST_AsText(`geometry`) as geom_wkt FROM `{table_name}`;"

    # 使用 pandas 讀取資料
    df = pd.read_sql(query, engine)

    # 將幾何欄位從 WKT 轉換為 Shapely 幾何物件
    df['geometry'] = df['geom_wkt'].apply(lambda geom: wkt.loads(geom) if geom else None)

    # 轉換為 GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # 設置坐標參考系統（根據您的資料設定 SRID）
    gdf.set_crs(epsg=4326, inplace=True)  # 假設使用 WGS84

    return gdf

# MySQL 資料庫連接參數
db_config = {
    'user': 'bigred',
    'password': 'bigred',
    'host': '192.168.31.42',
    'port': 30002,
    'database': 'd1'
}

# 讀取 MySQL 中的 GeoJSON 資料
@st.cache_data(ttl=3600)  # 緩存讀取結果，避免重複查詢
def load_data_from_mysql():
    return read_mysql_to_geojson('Tainan_County', db_config=db_config)

counties = load_data_from_mysql()

# 顯示 GeoJSON 資料在 Folium 地圖上
def display_map(gdf):
    # 計算地圖中心
    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    
    # 建立 Folium 地圖
    m = folium.Map(location=center, zoom_start=10)
    
    # 將 GeoDataFrame 添加到地圖上
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=list(gdf.columns.drop(['geometry', 'geom_wkt'])),  # 顯示所有屬性
            aliases=[col.capitalize() for col in gdf.columns.drop(['geometry', 'geom_wkt'])],
            localize=True
        )
    ).add_to(m)
    
    return m

# 顯示地圖
m = display_map(counties)
st.write("地圖顯示:")
st_folium(m, width=700, height=500)

# 顯示資料表
st.write("從 MySQL 讀取的資料:")
st.dataframe(counties.drop(columns=['geom_wkt']))
