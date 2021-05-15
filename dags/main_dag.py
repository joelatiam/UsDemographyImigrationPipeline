from datetime import datetime, timedelta
from airflow import DAG
from operators import (LoadToS3Operator)
from airflow.models import Variable

s3_bucket = Variable.get("s3_bucket")

start_date = datetime(2021, 5, 15);

default_args = {
    'owner': 'joelatiam',
    'start_date': start_date,
    'depends_on_past': False,
    'catchup': False,
    'email_on_retry': False
}

DAG_NAME = 'us_demography_and_immigration'

dag = DAG(
        DAG_NAME,
        default_args=default_args,
        description='ETL with Airflow, Redshift, Spark, S3',
        # schedule_interval=None
        )
s3_raw_data_dir = 'UsDemographyImmigration/data/raw'

demography_to_s3 = LoadToS3Operator(
        task_id='copy_demography_to_S3',
        local_directory='dags/data/demography',
        s3_directory=f"{s3_raw_data_dir}/demography",
        s3_bucket=s3_bucket,
        dag=dag,
    )

airpots_dag = LoadToS3Operator(
        task_id='copy_airports_to_S3',
        local_directory='dags/data/airports',
        s3_directory=f"{s3_raw_data_dir}/airports",
        s3_bucket=s3_bucket,
        dag=dag,
    )

