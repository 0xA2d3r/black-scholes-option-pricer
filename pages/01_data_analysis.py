import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Analysis",
    page_icon="📊",
    layout="wide"
)

# Page header
st.title("📊 Data Analysis")
st.subheader("Load and analyze your data")

# Main content
st.markdown("""
This page is for loading and analyzing your data. Currently, there is no data loaded.
You can implement data loading functionality here based on your needs.
""")

# Data loading section
st.header("Data Loading")

# File uploader placeholder - you can customize this based on your needs
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Update the session state to track that data is loaded
        st.session_state["data_loaded"] = True
        
        # Basic error handling for data loading
        df = pd.read_csv(uploaded_file)
        st.session_state["data"] = df
        
        # Display data information
        st.success(f"Data loaded successfully! Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        # Data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Data statistics
        st.subheader("Data Statistics")
        st.dataframe(df.describe())
        
        # Data information
        st.subheader("Data Information")
        
        # Display data types and non-null values
        buffer = []
        for col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].count()
            null_values = df[col].isna().sum()
            buffer.append({
                "Column": col,
                "Data Type": dtype,
                "Non-Null Count": non_null,
                "Null Values": null_values
            })
        
        st.dataframe(pd.DataFrame(buffer))
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.session_state["data_loaded"] = False
else:
    st.info("Please upload a CSV file to begin analysis")
    if "data" in st.session_state:
        del st.session_state["data"]
    st.session_state["data_loaded"] = False

# Navigation section at the bottom
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home"):
        st.switch_page("app.py")

with col3:
    if st.button("Continue to Visualization →"):
        st.switch_page("pages/02_visualization.py")
