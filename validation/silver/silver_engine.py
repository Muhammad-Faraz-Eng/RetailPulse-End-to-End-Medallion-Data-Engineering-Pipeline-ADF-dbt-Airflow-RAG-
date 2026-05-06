import pandas as pd
from validation.bronze.adls_client import ADLSClient
from validation.silver.transformer import TRANSFORMER_REGISTRY
from validation.bronze.config_loader import load_config
from validation.silver.sql_client import AzureSQLClient

adls = ADLSClient()
sql = AzureSQLClient()


def read_bronze(container, blob_name):
    blob = adls.download_file(container, blob_name)
    return pd.read_parquet(pd.io.common.BytesIO(blob))


def run_silver():
    config = load_config()

    bronze_container = config["storage"]["container_bronze"]
    silver_config = config["silver"]

    for name, job in silver_config.items():
        print(f"Processing: {name}")

        bronze_path = job["bronze_path"]
        target_table = job["target_table"]
        transformer_name = job["transformer"]

        transformer_func = TRANSFORMER_REGISTRY[transformer_name]

        files = adls.list_files(bronze_container, bronze_path)

        if not files:
            print(f"No Files Found for {name}")
            continue

        latest_file = sorted(files)[-1]

        df = read_bronze(bronze_container, latest_file)

        df_clean = transformer_func(df)

        sql.write_table(df_clean, target_table)

        print(f"Loaded: {target_table}")


    print("SILVER PIPELINE COMPLETED")


if __name__ == "__main__":
    run_silver()
