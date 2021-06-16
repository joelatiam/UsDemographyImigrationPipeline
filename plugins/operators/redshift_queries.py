from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class RedshifQueriesOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query_list=[],
                 query_type="",
                 append_data = False,
                 *args, **kwargs):
        """ 
            Run queries on Redshift
            Parameters:
            redshift_conn_id: "String"
            query_list: "List of Query Strings"
            query_type: "String"
            append_data: "Boolean"
            
        """

        super(RedshifQueriesOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query_list = query_list
        self.query_type = query_type
        self.append_data = append_data

    def execute(self, context):
        action = f"Redshift {len(self.query_list)} queries of {self.query_type} "
        self.log.info(f"Start {action}")
        self.log.info(self.redshift_conn_id)
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for query in self.query_list:
            if self.query_type == 'insert':
                if not self.append_data:
                    self.log.info(f"Clearing data from destination Redshift table {query[1]}")
                    redshift.run("DELETE FROM {}".format(query[1]))
                
                self.log.info(f"Insert data into destination Redshift table {query[1]}")
                redshift.run(query[0])
            else:
                redshift.run(query)

        self.log.info(f"End {action}")
        
