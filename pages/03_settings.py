import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

# Page header
st.title("⚙️ Settings")
st.subheader("Configure application settings")

# Initialize session state for settings if not already present
if "settings" not in st.session_state:
    st.session_state["settings"] = {
        "auto_refresh": False,
        "refresh_interval": 5,
        "dark_mode": False,
        "show_statistics": True
    }

# Create a form for settings to batch the changes
with st.form("settings_form"):
    st.header("Application Settings")
    
    # Display settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Display Settings")
        dark_mode = st.toggle("Dark Mode", st.session_state["settings"]["dark_mode"])
        show_statistics = st.toggle("Show Statistics", st.session_state["settings"]["show_statistics"])
    
    with col2:
        st.subheader("Data Settings")
        auto_refresh = st.toggle("Auto Refresh", st.session_state["settings"]["auto_refresh"])
        refresh_interval = st.slider(
            "Refresh Interval (seconds)",
            min_value=1,
            max_value=60,
            value=st.session_state["settings"]["refresh_interval"],
            disabled=not auto_refresh
        )
    
    # Add a section for future data processing settings
    st.subheader("Data Processing Settings")
    st.info("Additional data processing settings will be available in future updates.")
    
    # Form submission button
    submitted = st.form_submit_button("Save Settings")
    
    if submitted:
        # Update session state with new settings
        st.session_state["settings"]["dark_mode"] = dark_mode
        st.session_state["settings"]["show_statistics"] = show_statistics
        st.session_state["settings"]["auto_refresh"] = auto_refresh
        st.session_state["settings"]["refresh_interval"] = refresh_interval
        
        st.success("Settings have been updated successfully!")

# Display current settings
st.header("Current Settings")
st.json(st.session_state["settings"])

# Error Handling Configuration
st.header("Error Handling")
st.markdown("""
Configure how errors are displayed and logged in the application.
This section will be expanded in future updates.
""")

# Future expansion section
st.header("Future Settings")
st.markdown("""
This area is reserved for additional settings that will be implemented in future updates:
- User authentication
- Export configurations
- API integrations
- Custom themes
- Notification preferences
""")

# Navigation section at the bottom
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Visualization"):
        st.switch_page("pages/02_visualization.py")

with col3:
    if st.button("Back to Home"):
        st.switch_page("app.py")
