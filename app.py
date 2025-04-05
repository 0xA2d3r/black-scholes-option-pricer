import streamlit as st
import numpy as np
import pandas as pd

# Configure page settings
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main application header
st.title("📊 Streamlit Dashboard")
st.subheader("Welcome to your Streamlit application")

# Introduction section
st.markdown("""
This is a blank Streamlit application template that you can build upon for your data analysis and visualization needs.
Use the navigation menu on the left to explore different sections of the application.
""")

# Application overview in the main page
st.header("Application Overview")

# Using columns for responsive layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Analysis")
    st.markdown("""
    In the Data Analysis section, you can:
    - Load your data
    - Explore data statistics
    - Perform data transformations
    """)
    
    # Navigation button to Data Analysis page
    if st.button("Go to Data Analysis"):
        st.switch_page("pages/01_data_analysis.py")

with col2:
    st.subheader("Data Visualization")
    st.markdown("""
    In the Data Visualization section, you can:
    - Create various types of charts
    - Customize visualizations
    - Export visualization results
    """)
    
    # Navigation button to Visualization page
    if st.button("Go to Data Visualization"):
        st.switch_page("pages/02_visualization.py")

# Settings section information
st.subheader("Settings")
st.markdown("""
Configure application settings and preferences in the Settings section.
""")

# Navigation button to Settings page
if st.button("Go to Settings"):
    st.switch_page("pages/03_settings.py")

# Sidebar for additional navigation
with st.sidebar:
    st.title("Navigation")
    st.markdown("Use this sidebar to navigate between different sections of the application.")
    
    # Session state initialization for tracking app state
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["data_loaded"] = False
    
    st.divider()
    st.info("Select a page from the menu above or use the buttons on the main page to navigate.")
