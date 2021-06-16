import os

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd

class PandasCleanCsvOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 source_directory_path="",
                 destination_directory_path="",
                 data_definition = None,
                 delimiter=',',
                 *args, **kwargs):
        """ 
            Process CSV files with Pandas
            Parameters:
            source_directory_path: "String"
            destination_directory_path: "String"
            data_definition: "Dictionary"
            delimiter: "String"
            
        """

        super(PandasCleanCsvOperator, self).__init__(*args, **kwargs)
        self.source_directory_path = source_directory_path
        self.destination_directory_path = destination_directory_path
        self.delimiter = delimiter
        self.data_definition = data_definition

    def execute(self, context):
        action = f"Read and Clean CSV {self.source_directory_path} to {self.destination_directory_path}"
        self.log.info(f"Start {action}")

        dest_directory = self.destination_directory_path

        for root, dirs, files in os.walk(self.source_directory_path):

            for f in files:
                file_path = os.path.join(root,f)
                df = pd.read_csv(file_path,  self.delimiter)

                if(self.data_definition):
                    if(self.data_definition["columns"]):
                        df = df[self.data_definition["columns"]]
                    if(self.data_definition["rename"]):
                        df = df.rename(columns=self.data_definition["rename"])
                    if(self.data_definition["replace_na"]):
                        df = df.fillna(value = self.data_definition["replace_na"])
                    if(self.data_definition["convert"]):
                        df = df.astype(self.data_definition["convert"])
                
                cleaned_file = os.path.join(dest_directory,f)
                df.to_csv(cleaned_file, index = False)
                self.log.info(f"Saved {dest_directory}")

        self.log.info(f"End {action}")
        