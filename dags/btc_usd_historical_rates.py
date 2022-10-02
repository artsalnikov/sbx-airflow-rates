from airflow import DAG, utils
from airflow.operators.python_operator import PythonOperator

from datetime import timedelta, datetime
from btc_usd_rate_functions import create_rate_table, update_historical_rates

# Load historical rates of BTC/USD triggered manual.
#
# Optionally used parameter 'start_date' for history depth.

def run_load(**context):
    start_date = context['dag_run'].conf.get('start_date') or '2022-01-01'
    update_historical_rates(start_date)

with DAG(
    dag_id='btc_usd_historical_rates',
    start_date=utils.dates.days_ago(1),
    schedule_interval=None
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