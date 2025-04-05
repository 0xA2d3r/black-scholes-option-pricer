"""
Utility functions for the Streamlit application.
This module contains helper functions that can be used across different pages of the application.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import List, Dict, Any, Optional, Union


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a file path.
    
    Parameters:
    -----------
    file_path : str
        Path to the data file to load
        
    Returns:
    --------
    pd.DataFrame
        Loaded data as a pandas DataFrame
        
    Raises:
    -------
    Exception
        If the file cannot be loaded or is not a valid data file
    """
    try:
        # Determine file type by extension
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading data from {file_path}: {str(e)}")


def display_dataframe_info(df: pd.DataFrame) -> None:
    """
    Display summary information about a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to display information about
    """
    if df is None or df.empty:
        st.warning("No data available to display.")
        return
    
    # Basic DataFrame information
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # Column types and missing values
    col_info = []
    for col in df.columns:
        col_info.append({
            "Column": col,
            "Type": str(df[col].dtype),
            "Missing Values": df[col].isna().sum(),
            "% Missing": round(df[col].isna().sum() / len(df) * 100, 2)
        })
    
    st.dataframe(pd.DataFrame(col_info))


def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply filters to a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to filter
    filters : Dict[str, Any]
        Dictionary of column names and filter values
        
    Returns:
    --------
    pd.DataFrame
        Filtered DataFrame
    """
    if df is None or df.empty:
        return df
    
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if column in filtered_df.columns:
            if pd.api.types.is_numeric_dtype(filtered_df[column]):
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    min_val, max_val = value
                    filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
            elif pd.api.types.is_string_dtype(filtered_df[column]):
                if isinstance(value, str):
                    filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
                elif isinstance(value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
    
    return filtered_df


def format_large_number(num: float) -> str:
    """
    Format large numbers for display.
    
    Parameters:
    -----------
    num : float
        Number to format
        
    Returns:
    --------
    str
        Formatted number string
    """
    if num is None:
        return "N/A"
    
    abs_num = abs(num)
    
    if abs_num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif abs_num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs_num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"


def get_numerical_columns(df: pd.DataFrame) -> List[str]:
    """
    Get a list of numerical columns from a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    List[str]
        List of column names with numerical data types
    """
    if df is None or df.empty:
        return []
    
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """
    Get a list of categorical columns from a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    List[str]
        List of column names with categorical or object data types
    """
    if df is None or df.empty:
        return []
    
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def create_download_link(df: pd.DataFrame, filename: str, format_type: str = "csv") -> str:
    """
    Create a download link for a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to download
    filename : str
        Filename for the download
    format_type : str
        Format type ("csv", "excel", or "json")
        
    Returns:
    --------
    str
        HTML link for download
    """
    try:
        import base64
        from io import BytesIO
        
        buffer = BytesIO()
        
        if format_type.lower() == "csv":
            df.to_csv(buffer, index=False)
            mime_type = "text/csv"
            file_ext = ".csv"
        elif format_type.lower() == "excel":
            df.to_excel(buffer, index=False)
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_ext = ".xlsx"
        elif format_type.lower() == "json":
            df.to_json(buffer, orient="records")
            mime_type = "application/json"
            file_ext = ".json"
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
        
        b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f'<a href="data:{mime_type};base64,{b64}" download="{filename}{file_ext}">Download {format_type.upper()}</a>'
    except Exception as e:
        st.error(f"Error creating download link: {e}")
        return ""
