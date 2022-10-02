import datetime
import requests

from airflow_postgres import AirflowPostgres

def create_rate_table():
    '''
    Create the table for rates.
    '''
    conn = AirflowPostgres.get_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS btc_usd_rate (
                 currency_pair TEXT NOT NULL,
                 rate_date DATE NOT NULL,
                 rate FLOAT NOT NULL,
                 CONSTRAINT btc_usd_rate_pk
                     PRIMARY KEY (currency_pair, rate_date));
                 """)

def get_rates(endpoint, add_params={}):
    '''
    Get the rates data of BTC/USD with parameters.
    @param endpoint:  API connection endpoint.
    @param add_params:  Additional parameters/filters for data selection.
    @return: Dictionary that contains dates of rates and rate values.
             Throws exception when response code from a service doesn't equal 200.
    '''
    url = f'https://api.exchangerate.host/{endpoint}'
    params = {'base': 'BTC', 'symbols': 'USD', **add_params}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f'A response recieved with code {response.status_code}: {response.text}')

def update_latest_rate():
    '''
    Update the latest (today's) rate of BTC/USD.
    '''
    rate = get_rates('latest')
    rate_date = rate['date']
    rate_value = rate['rates']['USD']
    conn = AirflowPostgres.get_connection()
    conn.execute(f"INSERT INTO btc_usd_rate (currency_pair, rate_date, rate) " + \
                 f"VALUES ('BTC/USD', '{rate_date}', {rate_value}) " + \
                 f"ON CONFLICT ON CONSTRAINT btc_usd_rate_pk " + \
                 f"DO UPDATE SET rate = {rate_value};")

def update_historical_rates(start_date):
    '''
    Update historical rates of BTC/USD from start_date up to now.
    @param start_date: Start date of a history of rates.
    '''
    rates = get_rates('timeseries', {
        'start_date': start_date,
        'end_date': datetime.datetime.now().strftime("%Y-%m-%d")
    })
    rate_ins_str = ','.join([f"('BTC/USD', '{dt}', {rt['USD']})"
        for dt, rt in rates['rates'].items()])
    conn = AirflowPostgres.get_connection()
    conn.execute(f"INSERT INTO btc_usd_rate (currency_pair, rate_date, rate) " + \
                 f"VALUES {rate_ins_str} " + \
                 f"ON CONFLICT ON CONSTRAINT btc_usd_rate_pk " + \
                 f"DO UPDATE SET rate = excluded.rate;")
