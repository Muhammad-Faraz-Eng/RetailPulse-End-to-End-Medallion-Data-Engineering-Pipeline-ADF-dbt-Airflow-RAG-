import os
import urllib
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="docker/.env")


class AzureSQLClient:
    def __init__(self):
        server = os.getenv("AZURE_SQL_SERVER")
        db = os.getenv("AZURE_SQL_DATABASE")
        user = os.getenv("AZURE_SQL_USER")
        password = os.getenv("AZURE_SQL_PASSWORD")

        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER=tcp:{server},1433;"
            f"DATABASE={db};"
            f"UID={user};"
            f"PWD={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=yes;"
            f"Connection Timeout=30;"
        )

        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    def write_table(self, df: pd.DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)