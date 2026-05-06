import pandas as pd


def validate_and_cast(df, required_columns, dtypes):
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing Columns: {missing_cols}")

    valid_df = df.copy()
    invalid_df = pd.DataFrame()

    for col, dtypes in dtypes.items():
        try:
            if dtypes == "int":
                valid_df[col] = pd.to_numeric(valid_df[col], errors="coerce").astype(
                    "Int64"
                )
            elif dtypes == "float":
                valid_df[col] = pd.to_numeric(valid_df[col], errors="coerce")
            elif dtypes == "datetime":
                valid_df[col] = pd.to_datetime(valid_df[col], errors="coerce")
            elif dtypes == "str":
                valid_df[col] = valid_df[col].astype(str)
        except Exception as e:
            print(f"Error Casting {col}: {e}")

    invalid_mask = valid_df.isnull().any(axis=1)
    invalid_df = valid_df[invalid_mask]
    valid_df = valid_df[~invalid_mask]

    if isinstance(invalid_df, pd.Series):
        invalid_df = invalid_df.to_frame().T

    if isinstance(valid_df, pd.Series):
        valid_df = valid_df.to_frame().T
        
    return valid_df, invalid_mask
