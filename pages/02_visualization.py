import streamlit as st
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Data Visualization",
    page_icon="📈",
    layout="wide"
)

# Page header
st.title("📈 Data Visualization")
st.subheader("Create and customize visualizations")

# Check if data is loaded
if "data_loaded" not in st.session_state or not st.session_state["data_loaded"]:
    st.warning("No data has been loaded. Please go to the Data Analysis page to load data first.")
    
    if st.button("Go to Data Analysis"):
        st.switch_page("pages/01_data_analysis.py")
        
else:
    # Get the data from the session state
    df = st.session_state["data"]
    
    # Visualization options section
    st.header("Visualization Options")
    
    # Visualization type selector
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"]
    )
    
    # Layout for customization options using columns
    col1, col2 = st.columns(2)
    
    with col1:
        # First column options
        st.subheader("Data Selection")
        
        # Get numerical columns for visualization
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if not numerical_cols:
            st.error("No numerical columns found in the data for visualization.")
        else:
            # X-axis selection for applicable charts
            if viz_type in ["Line Chart", "Bar Chart", "Scatter Plot"]:
                x_axis = st.selectbox("Select X-axis", numerical_cols)
            
            # Y-axis selection for applicable charts
            if viz_type in ["Line Chart", "Bar Chart", "Scatter Plot"]:
                y_axis = st.selectbox("Select Y-axis", [col for col in numerical_cols if col != x_axis] if len(numerical_cols) > 1 else numerical_cols)
            
            # Column selection for histogram
            if viz_type == "Histogram":
                hist_column = st.selectbox("Select Column for Histogram", numerical_cols)
    
    with col2:
        # Second column for additional options
        st.subheader("Chart Options")
        
        # Common options
        use_container_width = st.checkbox("Use container width", value=True)
        
        # Chart specific options
        if viz_type == "Histogram":
            bins = st.slider("Number of bins", min_value=5, max_value=100, value=20)
        
        if viz_type == "Scatter Plot":
            marker_size = st.slider("Marker Size", min_value=10, max_value=200, value=50)
    
    # Render the visualization
    st.header("Visualization")
    
    try:
        if viz_type == "Line Chart" and 'x_axis' in locals() and 'y_axis' in locals():
            st.line_chart(data=df, x=x_axis, y=y_axis, use_container_width=use_container_width)
            
        elif viz_type == "Bar Chart" and 'x_axis' in locals() and 'y_axis' in locals():
            st.bar_chart(data=df, x=x_axis, y=y_axis, use_container_width=use_container_width)
            
        elif viz_type == "Scatter Plot" and 'x_axis' in locals() and 'y_axis' in locals():
            st.scatter_chart(data=df, x=x_axis, y=y_axis, use_container_width=use_container_width)
            
        elif viz_type == "Histogram" and 'hist_column' in locals():
            # Create histogram using Streamlit's charting capability
            hist_values = np.histogram(df[hist_column].dropna(), bins=bins)
            st.bar_chart(pd.DataFrame({
                'range': [f"{hist_values[1][i]:.2f}-{hist_values[1][i+1]:.2f}" for i in range(len(hist_values[0]))],
                'frequency': hist_values[0]
            }).set_index('range'), use_container_width=use_container_width)
            
    except Exception as e:
        st.error(f"Error creating visualization: {e}")
        st.info("Try selecting different columns or visualization types.")

# Navigation section at the bottom
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Data Analysis"):
        st.switch_page("pages/01_data_analysis.py")

with col3:
    if st.button("Continue to Settings →"):
        st.switch_page("pages/03_settings.py")
