import os

from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults



class LoadToS3Operator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 local_directory="",
                 s3_directory="",
                 s3_bucket="",
                 *args, **kwargs):

        super(LoadToS3Operator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.local_directory = local_directory
        self.s3_directory = s3_directory

    def execute(self, context):
        s3_hook = S3Hook()
        action = f"Copying data from Source {self.local_directory} to S3 {self.s3_bucket}/{ self.s3_directory}"
        
        self.log.info(action)

        for root, dirs, files in os.walk(self.local_directory):
            
            for f in files:
                self.log.info(f"Copying {f}") 
                local_file_location = os.path.join(root,f)
                s3_key = f"{self.s3_directory}/{f}"
                self.log.info(s3_key)
                s3_hook.load_file(
                filename=local_file_location,
                bucket_name=self.s3_bucket,
                replace=True, 
                key=s3_key
                )

        self.log.info(f"Done {action}")
