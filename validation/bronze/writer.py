import pandas as pd
import io


def df_to_parquet_bytes(df):
    if isinstance(df, pd.Series):
        df = df.to_frame().T

    if df.empty:
        return None
    
    buffer = io.BytesIO()
    df.to_parquet(buffer, engine="pyarrow", compression="snappy", index=False)
    return buffer.getvalue()
