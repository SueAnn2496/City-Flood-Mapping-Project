import streamlit as st
import pandas as pd

st.set_page_config(page_title="Risk Map - Export CSV", layout="wide")

st.write("### 📍 Risk Map: Urban Waterlogging Coordinates")

@st.cache_data
def load_data():
    return pd.read_csv("Urban_Waterlogging_UTM_Coordinates.csv")

try:
    df = load_data()
    
    st.write(f"Successfully loaded **{len(df)}** waterlogging risk points.")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Export CSV File",
        data=csv_data,
        file_name="Urban_Waterlogging_UTM_Coordinates.csv",
        mime="text/csv",
    )

except FileNotFoundError:
    st.error("File not found. Please ensure 'Urban_Waterlogging_UTM_Coordinates.csv' and 'app.py' are located in the same root directory of your GitHub repository.")
