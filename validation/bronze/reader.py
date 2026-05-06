import io
import json
import pandas as pd


def read_data(file_bytes, file_format, source_name=None):
    if file_format == "csv":
        return pd.read_csv(io.BytesIO(file_bytes))

    elif file_format == "json":
        data = json.loads(file_bytes)

        if source_name == "currency":
            base = data["base_code"]
            rates = data["rates"]

            rows = []

            for k, v in rates.items():
                rows.append(
                    {
                        "base_code": base,
                        "currency_code": k,
                        "rate": v,
                    }
                )
            return pd.DataFrame(rows)

        if isinstance(data, list):
            return pd.json_normalize(data)
        else:
            return pd.json_normalize(data)

    else:
        raise ValueError(f"Unsupported file format {file_format}")
