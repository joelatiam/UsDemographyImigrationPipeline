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

tables_list  = []

for table in staging_tables:
    tables_list.append(staging_tables[table])

for table in demography_dimentions_tables:
    tables_list.append(demography_dimentions_tables[table])

for table in airports_dimentions_tables:
    tables_list.append(airports_dimentions_tables[table])

for table in immigrations_dimentions_tables:
    tables_list.append(immigrations_dimentions_tables[table])

for table in fact_tables:
    tables_list.append(fact_tables[table])
