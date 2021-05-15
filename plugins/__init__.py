from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class DemographyImmigrationPlugin(AirflowPlugin):
    name = "pipeline_plugin"
    operators = [
        operators.LoadToS3Operator,
    ]
    helpers = [

    ]
