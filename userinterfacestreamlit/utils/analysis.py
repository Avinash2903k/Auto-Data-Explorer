import pandas as pd

def get_basic_info(df: pd.DataFrame):
    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist()
    }
    return info

def get_missing_values(df: pd.DataFrame):
    return df.isnull().sum().to_frame("missing_count")

def get_column_types(df: pd.DataFrame):
    return df.dtypes.to_frame("dtype")

def get_descriptive_stats(df: pd.DataFrame):
    # include='all' na sometimes warning, so safe try
    try:
        desc = df.describe(include="all").T
    except Exception:
        desc = df.describe().T
    return desc
