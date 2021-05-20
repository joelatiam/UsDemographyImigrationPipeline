from datetime import datetime

from airflow import DAG
from airflow.models import Variable

from operators import (
    PandasCleanCsvOperator, 
    LoadToS3Operator,
    # RedshifQueriesOperator, S3ToRedshiftOperator
    )
from helpers import (
    # create_tables_queries, drop_tables_queries,
    staging_data, 
    # staging_tables
    )

s3_bucket = Variable.get("s3_bucket")

start_date = datetime(2021, 5, 20)

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

s3_data_dir = 'UsDemographyImmigration/data'


clean_demography_csv = PandasCleanCsvOperator(
    task_id='clean_demography_csv',
    source_directory_path='dags/data/raw/demography',
    destination_directory_path='dags/data/cleaned/demography',
    delimiter=';',
    data_definition = staging_data["demography"],
    dag=dag,
)

clean_airports_csv = PandasCleanCsvOperator(
    task_id='clean_airports_csv',
    source_directory_path='dags/data/raw/airports',
    destination_directory_path='dags/data/cleaned/airports',
    delimiter=',',
    data_definition = staging_data["airports"],
    dag=dag,
)

copy_demography_to_S3 = LoadToS3Operator(
    task_id='copy_demography_to_S3',
    local_directory='dags/data/cleaned/demography',
    s3_directory=f"{s3_data_dir}/demography",
    s3_bucket=s3_bucket,
    dag=dag,
)

copy_airports_to_S3 = LoadToS3Operator(
    task_id='copy_airports_to_S3',
    local_directory='dags/data/cleaned/airports',
    s3_directory=f"{s3_data_dir}/airports",
    s3_bucket=s3_bucket,
    dag=dag,
)

# drop_redshift_tables = RedshifQueriesOperator(
#     task_id='drop_redshift_tables',
#     redshift_conn_id='redshift',
#     query_list=drop_tables_queries,
#     query_type='drop tables',
#     dag=dag,
# )

# create_redshift_tables = RedshifQueriesOperator(
#     task_id='create_redshift_tables',
#     redshift_conn_id='redshift',
#     query_list=create_tables_queries,
#     query_type='create tables',
#     dag=dag,
# )

# stage_events_to_redshift = S3ToRedshiftOperator(
#     task_id='Stages_to_Redshift',
#     redshift_conn_id='redshift',
#     aws_credentials_id='aws_credentials',
#     tables=staging_tables,
#     s3_directory=f"{s3_data_dir}",
#     s3_bucket=s3_bucket,
#     dag=dag
# )

clean_demography_csv >> copy_demography_to_S3

clean_airports_csv >> copy_airports_to_S3
