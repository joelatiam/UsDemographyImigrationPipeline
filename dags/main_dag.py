from datetime import datetime, timedelta
from airflow import DAG

default_args = {
    'owner': 'joelatiam',
    'start_date': datetime(2016, 1, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('us_demography_and_immigration',
          default_args=default_args,
          description='ETL with Airflow, Redshift, Spark, S3',
          schedule_interval='@daily'
        )
