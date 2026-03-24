import pandas as pd

def get_statistics(file_path):
    try:
        df = pd.read_csv(file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')

    stats = []

    for column in df.columns:
        col_data = df[column]

        if col_data.dropna().empty:
            stats.append({
                'column': column,
                'type': 'empty',
                'data': {}
            })
            continue

        if pd.api.types.is_numeric_dtype(col_data):
            stats.append({
                'column': column,
                'type': 'numeric',
                'data': {
                    'count': int(col_data.count()),
                    'mean': round(float(col_data.mean()), 2),
                    'median': round(float(col_data.median()), 2),
                    'std': round(float(col_data.std()), 2),
                    'min': round(float(col_data.min()), 2),
                    'max': round(float(col_data.max()), 2),
                    'missing_values': int(col_data.isnull().sum())
                }
            })

        else:
            mode = col_data.mode()

            stats.append({
                'column': column,
                'type': 'categorical',
                'data': {
                    'unique_values': int(col_data.nunique()),
                    'most_frequent': str(mode[0]) if not mode.empty else None,
                    'missing_values': int(col_data.isnull().sum())
                }
            })

    return stats