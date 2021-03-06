from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class


class DemographyImmigrationPlugin(AirflowPlugin):
    name = "pipeline_plugin"
    operators = [
        operators.PandasCleanCsvOperator,
        operators.LoadToS3Operator,
        operators.RedshifQueriesOperator,
        operators.S3ToRedshiftOperator,
        operators.DataQualityOperator,
    ]
    helpers = [
        helpers.tables_list,
        helpers.staging_data,
        helpers.staging_tables,
        helpers.create_tables_queries,
        helpers.drop_tables_queries,
        helpers.dim_tables_insert_queries
    ]
