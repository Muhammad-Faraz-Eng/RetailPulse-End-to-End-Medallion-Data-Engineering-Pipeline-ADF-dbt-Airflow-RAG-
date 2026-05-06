from validation.bronze.config_loader import load_config
from validation.bronze.adls_client import ADLSClient
from validation.bronze.reader import read_data
from validation.bronze.validator import validate_and_cast
from validation.bronze.writer import df_to_parquet_bytes
from scripts.postgres_client import insert_audit
from datetime import datetime


def run_bronze():
    config = load_config()
    adls = ADLSClient()

    landing_container = config["storage"]["container_landing"]
    bronze_container = config["storage"]["container_bronze"]

    for source_name, source_cfg in config["bronze"].items():
        print(f"Reading file: {source_name}")

        files = adls.list_files(landing_container, source_cfg["path"])

        for file in files:
            data_bytes = adls.download_file(landing_container, file)

            df = read_data(data_bytes, source_cfg["format"], source_name)

            valid_df, invalid_df = validate_and_cast(
                df, source_cfg["required_columns"], source_cfg["dtypes"]
            )

            today = datetime.today().strftime("%Y-%m-%d")

            if valid_df is not None and not valid_df.empty:
                parquet_bytes = df_to_parquet_bytes(valid_df)

                output_path = f"{source_name}/ingestion_date={today}/data.parquet"

                if parquet_bytes:
                    adls.upload_file(bronze_container, output_path, parquet_bytes)

            if invalid_df is not None and not invalid_df.empty:
                quarantine_bytes = df_to_parquet_bytes(invalid_df)

                q_path = f"_quarantine/{source_name}/data.parquet"

                if quarantine_bytes:
                    adls.upload_file(bronze_container, q_path, quarantine_bytes)
            insert_audit(
                source_name=source_name,
                rows_read=len(df),
                rows_valid=len(valid_df),
                rows_invalid=len(invalid_df),
            )
            print(f"Done {source_name}")


if __name__ == "__main__":
    run_bronze()
