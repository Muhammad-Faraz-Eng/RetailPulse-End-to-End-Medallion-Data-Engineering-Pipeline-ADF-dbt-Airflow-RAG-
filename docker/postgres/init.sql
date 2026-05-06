CREATE TABLE IF NOT EXISTS bronze_audit_log (
    id SERIAL PRIMARY KEY,
    source_name TEXT,
    rows_read INT,
    rows_valid INT,
    rows_invalid INT,
    ingestion_time TIMESTAMP DEFAULT NOW()
);