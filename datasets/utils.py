import os
import pandas as pd

def get_statistics(file_path):
    try:
        df = pd.read_csv(file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')

    file_size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    stats_data = {
        'liczba_wierszy': len(df),
        'liczba_kolumn': len(df.columns),
        'puste': int(df.isnull().sum().sum()),
        'rozmiar': f"{file_size_mb} MB",
        'kolumny_szczegoly': []
    }
    for column in df.columns:
        col_data = df[column]

        if col_data.dropna().empty:
            stats_data['kolumny_szczegoly'].append({
                'column': column,
                'type': 'empty',
            })
            continue

        if pd.api.types.is_numeric_dtype(col_data):
            stats_data['kolumny_szczegoly'].append({
                'column': column,
                'type': 'numeric',
                'data': {
                    'mean': round(float(col_data.mean()), 2),
                    'min': round(float(col_data.min()), 2),
                    'max': round(float(col_data.max()), 2),
                    'missing_values': int(col_data.isnull().sum())
                }
            })

        else:
            mode = col_data.mode()

            stats_data['kolumny_szczegoly'].append({
                'column': column,
                'type': 'categorical',
                'data': {
                    'unique_values': int(col_data.nunique()),
                    'most_frequent': str(mode[0]) if not mode.empty else None,
                    'missing_values': int(col_data.isnull().sum())
                }
            })

    return stats_data