from helpers.sql.queries.insert.dim_demography import (
    insert_dim_demography as demography_dim
)
from helpers.sql.queries.insert.dim_airports import (
    insert_dim_airports as airports_dim
)
from helpers.sql.queries.insert.dim_immigration import (
    insert_dim_demography as immigration_dim
)

dim_tables_insert_queries = []

dim_tables_insert_queries.extend(demography_dim)
dim_tables_insert_queries.extend(airports_dim)
dim_tables_insert_queries.extend(immigration_dim)
