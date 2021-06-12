from helpers.sql.tables_definitions.dim_demography import (
    demography_dimentions_tables as tables
)

queries_list = []

# Insert into State table
queries_list.append([f"""
    INSERT INTO {tables["states"]["name"]} ({tables["states"]["columns_to_insert_values"]})
    SELECT DISTINCT state, code FROM
        (
        SELECT
        TRIM(' ' FROM state) AS state, TRIM(' ' FROM state_code) AS code
        FROM staging_demography
        WHERE
            LENGTH(TRIM(' ' FROM state_code)) <= 2 AND LENGTH(TRIM(' ' FROM state_code)) > 0
            AND LENGTH(TRIM(' ' FROM state)) >=2
        )
    ORDER BY state ASC
""", tables["states"]["name"]])

# Insert into cities table
queries_list.append([f"""
    INSERT INTO {tables["cities"]["name"]} ({tables["cities"]["columns_to_insert_values"]})
    SELECT DISTINCT name, state_id FROM
        (
        SELECT
        TRIM(' ' FROM staging.city) AS name, TRIM(' ' FROM staging.state) AS state,
        states.id AS state_id
        FROM staging_demography staging
        LEFT JOIN states ON TRIM(' ' FROM staging.state) = states.name
        WHERE
            LENGTH(TRIM(' ' FROM staging.city)) >=2
        )
    ORDER BY name ASC
""", tables["cities"]["name"]])

# Insert into races table
queries_list.append([f"""
    INSERT INTO {tables["races"]["name"]} ({tables["races"]["columns_to_insert_values"]})
    SELECT DISTINCT name FROM
        (
        SELECT
        TRIM(' ' FROM staging.race) AS name
        FROM staging_demography staging
        WHERE
            LENGTH(TRIM(' ' FROM staging.race)) >=3
        )
    ORDER BY name ASC
""", tables["races"]["name"]])

insert_dim_demography = queries_list
