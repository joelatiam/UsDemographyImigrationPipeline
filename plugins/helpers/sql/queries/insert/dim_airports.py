from helpers.sql.tables_definitions.dim_airports import (
    airports_dimentions_tables as tables
)

queries_list = []

# Insert into Airports types
queries_list.append([f"""
    INSERT INTO {tables["airports_types"]["name"]} ({tables["airports_types"]["columns_to_insert_values"]})
    SELECT DISTINCT name FROM
        (
        SELECT
        TRIM(' ' FROM type) AS name
        FROM staging_airports
        WHERE
            LENGTH(TRIM(' ' FROM type)) >= 2
        )
    ORDER BY name ASC
""", tables["airports_types"]["name"]])

# Insert into airports table
queries_list.append([f"""
    INSERT INTO {tables["airports"]["name"]} ({tables["airports"]["columns_to_insert_values"]})
    SELECT DISTINCT ident, name, type_id, state_id, gps_code, iata_code, local_code FROM
        (
        SELECT
        TRIM(' ' FROM staging.ident) AS ident,
        TRIM(' ' FROM staging.name) AS name, airports_types.id AS type_id,
        states.id AS state_id, TRIM(' ' FROM staging.gps_code) AS gps_code,
        TRIM(' ' FROM staging.iata_code) AS iata_code,
        TRIM(' ' FROM staging.local_code) AS local_code
        FROM staging_airports staging
        LEFT JOIN  airports_types ON TRIM(' ' FROM staging.type) = airports_types.name
        LEFT JOIN states ON TRIM(' ' FROM REPLACE(staging.iso_region, 'US-', '')) = states.code
        WHERE
            LENGTH(TRIM(' ' FROM staging.name)) >=3
        )
    ORDER BY name ASC
""", tables["airports"]["name"]])

insert_dim_airports = queries_list
