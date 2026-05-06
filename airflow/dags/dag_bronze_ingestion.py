from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBT_PROJECT_DIR = PROJECT_ROOT / "retailpulse"


default_args = {
    "owner": "retailpulse",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bronze_layer_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 5, 4),
    schedule_interval=None,  # manual trigger for learning
    catchup=False,
) as dag:
    run_bronze = BashOperator(
        task_id="run_bronze_engine",
        bash_command=f'cd "{PROJECT_ROOT}" && python -m validation.bronze.bronze_engine',
    )
    run_silver = BashOperator(
        task_id="run_silver_engine",
        bash_command=f'cd "{PROJECT_ROOT}" && python -m validation.silver.silver_engine',
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command=f'cd "{DBT_PROJECT_DIR}" && dbt run',
    )

    run_bronze >> run_silver >> run_dbt
