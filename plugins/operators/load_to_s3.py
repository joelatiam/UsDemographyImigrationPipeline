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
                 file_formats=[],
                 *args, **kwargs):
        """ 
            Send files to CSV
            Parameters:
            local_directory: "String"
            s3_directory: "String"
            s3_bucket: "String"
            file_formats: "List of Strings"
            
        """

        super(LoadToS3Operator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.local_directory = local_directory
        self.s3_directory = s3_directory
        self.file_formats = file_formats

    def execute(self, context):
        s3_hook = S3Hook()
        action = f"Copying data from Source {self.local_directory} to S3 {self.s3_bucket}/{ self.s3_directory}"
        
        self.log.info(action)

        for root, dirs, files in os.walk(self.local_directory):
            
            for f in files:
                if(len(self.file_formats) > 0):
                    is_valid_format = True
                    for f_format in self.file_formats:
                        if(not f.endswith(f_format)):
                            is_valid_format = False
                            break
                    if(not is_valid_format):
                        continue

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
