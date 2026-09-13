import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Risk Map - Export CSV", layout="wide")

st.write("### 📍 Risk Map: Urban Waterlogging Coordinates")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "Urban_Waterlogging_UTM_Coordinates.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

try:
    df = load_data(file_path)
    
    st.write(f"Successfully loaded **{len(df)}** waterlogging risk points.")
    st.dataframe(df, use_container_width=True)

    csv_data = convert_df_to_csv(df)

    st.download_button(
        label="📥 Export CSV File",
        data=csv_data,
        file_name="Urban_Waterlogging_UTM_Coordinates.csv",
        mime="text/csv",
    )

except FileNotFoundError:
    st.error(f"找不到文件，请确保 'Urban_Waterlogging_UTM_Coordinates.csv' 和代码放在同一个文件夹中。当前检查路径: {current_dir}")
