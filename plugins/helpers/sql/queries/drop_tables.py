from helpers.sql.tables_definitions.staging import staging_tables

tables_list = staging_tables
queries_list = []

for table in tables_list:
    queries_list.append(f"""
    DROP TABLE IF EXISTS {tables_list[table]["name"]}
    """)

drop_tables_queries = queries_list
