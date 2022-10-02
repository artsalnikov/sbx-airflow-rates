from airflow import DAG, utils
from airflow.operators.python_operator import PythonOperator

from datetime import timedelta, datetime
from btc_usd_rate_functions import create_rate_table, update_latest_rate

# Load the latest rate of BTC/USD every 3 hours.

def run_load(**context):
    update_latest_rate()

with DAG(
    dag_id='btc_usd_daily_rate',
    start_date=utils.dates.days_ago(1),
    schedule_interval=timedelta(hours=3)
) as dag:

    create_rate_table = PythonOperator(
        task_id='create_rate_table',
        python_callable=create_rate_table,
        provide_context=True
    )

    load_rate = PythonOperator(
        task_id='load_rate',
        python_callable=run_load,
        provide_context=True
    )

create_rate_table >> load_rate