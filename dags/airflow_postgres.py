import os
from sqlalchemy import create_engine

class AirflowPostgres:
    __conn = None
    
    @staticmethod
    def get_connection():
        if not AirflowPostgres.__conn:
            conn_string = os.environ['AIRFLOW__DATABASE__SQL_ALCHEMY_CONN']
            AirflowPostgres.__conn = create_engine(conn_string)
        return AirflowPostgres.__conn
