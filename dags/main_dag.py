from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.contrib.operators.spark_submit_operator import (
    SparkSubmitOperator
)

from operators import (
    PandasCleanCsvOperator,
    LoadToS3Operator,
    RedshifQueriesOperator,
    S3ToRedshiftOperator,
    DataQualityOperator,
)
from helpers import (
    tables_list,
    create_tables_queries,
    drop_tables_queries,
    staging_data,
    staging_tables,
    dim_tables_insert_queries,
    facts_tables_insert_queries
)

s3_bucket = Variable.get("s3_bucket")

start_date = datetime(2021, 6, 15)

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
s3_scripts_dir = 'UsDemographyImmigration/scripts'


clean_demography_csv = PandasCleanCsvOperator(
    task_id='clean_demography_csv',
    source_directory_path='data/raw/demography',
    destination_directory_path='data/cleaned/demography',
    delimiter=';',
    data_definition = staging_data["demography"],
    dag=dag,
)

copy_demography_to_S3 = LoadToS3Operator(
    task_id='copy_demography_to_S3',
    local_directory='data/cleaned/demography',
    s3_directory=f"{s3_data_dir}/demography",
    s3_bucket=s3_bucket,
    dag=dag,
)

clean_airports_csv = PandasCleanCsvOperator(
    task_id='clean_airports_csv',
    source_directory_path='data/raw/airports',
    destination_directory_path='data/cleaned/airports',
    delimiter=',',
    data_definition = staging_data["airports"],
    dag=dag,
)

copy_airports_to_S3 = LoadToS3Operator(
    task_id='copy_airports_to_S3',
    local_directory='data/cleaned/airports',
    s3_directory=f"{s3_data_dir}/airports",
    s3_bucket=s3_bucket,
    dag=dag,
)


clean_immigration_parquet = SparkSubmitOperator(
    task_id='clean_immigration_parquet',
    conn_id='spark_standalone',
    application='scripts/immigration/spark_immigration.py',
    dag=dag,
)

copy_immigration_to_S3 = LoadToS3Operator(
    task_id='copy_immigration_to_S3',
    local_directory='data/cleaned/immigration',
    s3_directory=f"{s3_data_dir}/immigration",
    s3_bucket=s3_bucket,
    file_formats=['parquet'],
    dag=dag,
)

drop_redshift_tables = RedshifQueriesOperator(
    task_id='drop_redshift_tables',
    redshift_conn_id='redshift',
    query_list=drop_tables_queries,
    query_type='drop tables',
    dag=dag,
)

create_redshift_tables = RedshifQueriesOperator(
    task_id='create_redshift_tables',
    redshift_conn_id='redshift',
    query_list=create_tables_queries,
    query_type='create tables',
    dag=dag,
)

stage_demography_to_redshift = S3ToRedshiftOperator(
    task_id='stage_demography_to_redshift',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table=staging_tables["demography"],
    s3_directory=f"{s3_data_dir}",
    s3_bucket=s3_bucket,
    dag=dag
)

stage_airports_to_redshift = S3ToRedshiftOperator(
    task_id='stage_airports_to_redshift',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table=staging_tables["airports"],
    s3_directory=f"{s3_data_dir}",
    s3_bucket=s3_bucket,
    dag=dag
)

stage_immigration_to_redshift = S3ToRedshiftOperator(
    task_id='stage_immigration_to_redshift',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table=staging_tables["immigration"],
    s3_directory=f"{s3_data_dir}",
    s3_bucket=s3_bucket,
    dag=dag
)

insert_dim_tables = RedshifQueriesOperator(
    task_id='insert_dim_tables',
    redshift_conn_id='redshift',
    query_list=dim_tables_insert_queries,
    query_type='insert',
    dag=dag,
)

insert_facts_tables = RedshifQueriesOperator(
    task_id='insert_facts_tables',
    redshift_conn_id='redshift',
    query_list=facts_tables_insert_queries,
    query_type='insert',
    dag=dag,
)

run_quality_checks = DataQualityOperator(
    task_id='run_quality_checks',
    redshift_conn_id='redshift',
    tables_list = tables_list,
    dag=dag
)



clean_demography_csv >> copy_demography_to_S3

clean_airports_csv >> copy_airports_to_S3

clean_immigration_parquet >> copy_immigration_to_S3

[
    copy_demography_to_S3, copy_airports_to_S3, copy_immigration_to_S3
] >> drop_redshift_tables >> create_redshift_tables  >> [
    stage_demography_to_redshift, stage_airports_to_redshift, stage_immigration_to_redshift
    ] >> insert_dim_tables >> insert_facts_tables >> run_quality_checks

