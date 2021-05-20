from helpers.sql.tables_definitions.staging import staging_tables

tables_list = staging_tables
queries_list = []

for table in tables_list:
    queries_list.append(f"""
    CREATE TABLE IF NOT EXISTS {tables_list[table]["name"]}
    ({tables_list[table]["columns_definition"]})
    """)

create_tables_queries = queries_list
