from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class S3ToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table='',
                 s3_directory="",
                 s3_bucket="",
                 *args, **kwargs):

        super(S3ToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table= table
        self.s3_bucket = s3_bucket
        self.s3_directory = s3_directory
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id, client_type="redshift")
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        s3_path = "s3://{}/{}/{}".format(
                self.s3_bucket, self.s3_directory, self.table["s3"]["key"]
            )
        files_format =  self.table["s3"]["format"]
        delimiter =  self.table["s3"]["delimiter"]
        ignoreheader = self.table["s3"]["ignoreheader"]
        delimiter_text = ''


        if (delimiter):
            delimiter_text = f"delimiter '{delimiter}'"

        self.log.info(
            f"Start Copying data from {s3_path} to Table { self.table['name']}")

        redshift.run(f"""
        COPY { self.table["name"]}
        FROM '{s3_path}'
        ACCESS_KEY_ID '{credentials.access_key}'
        SECRET_ACCESS_KEY '{credentials.secret_key}'
        {files_format}
        {delimiter_text}
        {ignoreheader}
        """)
