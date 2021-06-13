from helpers.sql.tables_definitions.staging import staging_tables
from helpers.sql.tables_definitions.dim_demography import (
    demography_dimentions_tables
)
from helpers.sql.tables_definitions.dim_airports import (
    airports_dimentions_tables
)
from helpers.sql.tables_definitions.dim_immigration import (
    immigrations_dimentions_tables
)

from helpers.sql.tables_definitions.facts import (
    fact_tables
)

queries_list = []

for table in staging_tables:
    queries_list.append(f"""
    CREATE TABLE IF NOT EXISTS {staging_tables[table]["name"]}
    ({staging_tables[table]["columns_definition"]})
    """)

fact_and_dim_tables = """
    CREATE TABLE IF NOT EXISTS {table}
    ({columns})
    {dist_style}
    {sort_key}
    """

for table in demography_dimentions_tables:
    queries_list.append(
        fact_and_dim_tables.format(
            table = demography_dimentions_tables[table]["name"],
            columns = demography_dimentions_tables[table]["columns_definition"],
            dist_style = demography_dimentions_tables[table]["dist_style"],
            sort_key = demography_dimentions_tables[table]["sort_key"]
        )
    )

for table in airports_dimentions_tables:
    queries_list.append(
        fact_and_dim_tables.format(
            table = airports_dimentions_tables[table]["name"],
            columns = airports_dimentions_tables[table]["columns_definition"],
            dist_style = airports_dimentions_tables[table]["dist_style"],
            sort_key = airports_dimentions_tables[table]["sort_key"]
        )
    )

for table in immigrations_dimentions_tables:
    queries_list.append(
        fact_and_dim_tables.format(
            table = immigrations_dimentions_tables[table]["name"],
            columns = immigrations_dimentions_tables[table]["columns_definition"],
            dist_style = immigrations_dimentions_tables[table]["dist_style"],
            sort_key = immigrations_dimentions_tables[table]["sort_key"]
        )
    )

for table in fact_tables:
    queries_list.append(
        fact_and_dim_tables.format(
            table = fact_tables[table]["name"],
            columns = fact_tables[table]["columns_definition"],
            dist_style = fact_tables[table]["dist_style"],
            sort_key = fact_tables[table]["sort_key"]
        )
    )

create_tables_queries = queries_list
