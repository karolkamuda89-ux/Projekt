import pandas as pd

def calculate_stats(df: pd.DataFrame) -> dict:
    stats = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            stats[column] = {
                'count': df[column].count(),
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max()
            }
        elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
            stats[column] = {
                'unique_values': df[column].nunique(),
                'most_frequent': df[column].mode()[0] if not df[column].mode().empty else None
            }
    return stats


def laod_dataframe(dataset):
    return pd.read_csv(dataset.file.path)