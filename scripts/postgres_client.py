import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="docker/.env")

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT"),
)


def insert_audit(source_name, rows_read, rows_valid, rows_invalid):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO bronze_audit_log
        (source_name, rows_read, rows_valid, rows_invalid)
        VALUES (%s, %s, %s, %s)
        """,
        (source_name, rows_read, rows_valid, rows_invalid),
    )
    conn.commit()
