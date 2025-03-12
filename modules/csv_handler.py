import pandas as pd

csv_data = None  # Global CSV Data

def load_csv(file_path):
    """Loads and validates a CSV file."""
    global csv_data
    try:
        csv_data = pd.read_csv(file_path)
        return f"CSV uploaded! {csv_data.shape[0]} rows, {csv_data.shape[1]} columns."
    except Exception as e:
        return f"Error loading CSV: {str(e)}"
