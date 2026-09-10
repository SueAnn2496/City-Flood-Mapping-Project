import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Multi-Map Point Plotter", layout="wide")

st.title("Surveying Data Point Plotter for Multiple Maps")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File uploaded successfully!")
        st.write("Data Preview:", df.head())
        
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            lat_col = st.selectbox("Select Latitude Column", columns)
        with col2:
            lon_col = st.selectbox("Select Longitude Column", columns)
            
        if lat_col and lon_col:
            df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
            df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
            df = df.dropna(subset=[lat_col, lon_col])
            
            if not df.empty:
                center_lat = df[lat_col].mean()
                center_lon = df[lon_col].mean()
                
                tab1, tab2, tab3, tab4 = st.tabs(["Map 1", "Map 4", "Map 5", "Map 6"])
                
                with tab1:
                    st.subheader("Map 1 - Standard View")
                    map1 = folium.Map(location=[center_lat, center_lon], zoom_start=15)
                    for _, row in df.iterrows():
                        folium.Marker(
                            location=[row[lat_col], row[lon_col]],
                            popup=f"Lat: {row[lat_col]}, Lon: {row[lon_col]}"
                        ).add_to(map1)
                    st_folium(map1, width=700, height=500, key="map1_render")
                    
                with tab2:
                    st.subheader("Map 4 - Satellite View")
                    map4 = folium.Map(
                        location=[center_lat, center_lon], 
                        zoom_start=15, 
                        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                        attr="Esri"
                    )
                    for _, row in df.iterrows():
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=6,
                            color="red",
                            fill=True,
                            fill_color="red"
                        ).add_to(map4)
                    st_folium(map4, width=700, height=500, key="map4_render")
                    
                with tab3:
                    st.subheader("Map 5 - Terrain View")
                    map5 = folium.Map(
                        location=[center_lat, center_lon], 
                        zoom_start=15,
                        tiles="Stamen Terrain"
                    )
                    for _, row in df.iterrows():
                        folium.Marker(
                            location=[row[lat_col], row[lon_col]],
                            icon=folium.Icon(color="green", icon="info-sign")
                        ).add_to(map5)
                    st_folium(map5, width=700, height=500, key="map5_render")
                    
                with tab4:
                    st.subheader("Map 6 - Dark Mode View")
                    map6 = folium.Map(
                        location=[center_lat, center_lon], 
                        zoom_start=15,
                        tiles="CartoDB dark_matter"
                    )
                    for _, row in df.iterrows():
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=8,
                            color="cyan",
                            fill=True,
                            fill_color="blue"
                        ).add_to(map6)
                    st_folium(map6, width=700, height=500, key="map6_render")
            else:
                st.error("No valid numeric coordinates found in the selected columns.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV or Excel file to begin.")
