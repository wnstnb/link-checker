import pandas as pd
import streamlit as st
from typing import Optional

class CSVHandler:
    """Handles CSV file upload, validation, and processing"""
    
    def __init__(self):
        self.required_columns = ['business_name', 'URL']
    
    def load_csv(self, uploaded_file) -> pd.DataFrame:
        """
        Load and validate CSV file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            pd.DataFrame: Validated dataframe
            
        Raises:
            ValueError: If CSV doesn't meet requirements
        """
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Validate columns
            self._validate_columns(df)
            
            # Validate data
            self._validate_data(df)
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error processing CSV: {str(e)}")
    
    def _validate_columns(self, df: pd.DataFrame):
        """Validate that required columns exist"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _validate_data(self, df: pd.DataFrame):
        """Validate data quality"""
        # Check for empty dataframe
        if df.empty:
            raise ValueError("CSV file is empty")
        
        # Check for missing values in required columns
        for col in self.required_columns:
            if df[col].isnull().any():
                raise ValueError(f"Column '{col}' contains missing values")
        
        # Validate URL format (basic check)
        invalid_urls = []
        for idx, url in enumerate(df['URL']):
            if not self._is_valid_url(url):
                invalid_urls.append(f"Row {idx + 1}: {url}")
        
        if invalid_urls:
            st.warning(f"Some URLs may be invalid: {invalid_urls[:5]}...")
    
    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation"""
        if pd.isna(url):
            return False
        
        url_str = str(url).strip()
        return url_str.startswith(('http://', 'https://'))
    
    def save_results(self, results: list, filename: str = "link_checker_results.csv") -> str:
        """
        Save results to CSV
        
        Args:
            results: List of result dictionaries
            filename: Output filename
            
        Returns:
            str: CSV content as string
        """
        df = pd.DataFrame(results)
        return df.to_csv(index=False) 