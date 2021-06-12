from helpers.sql.tables_definitions.facts import (
    fact_tables as tables
)

queries_list = []

# Insert into arrival demography
queries_list.append([f"""
    INSERT INTO {tables["demography"]["name"]} ({tables["demography"]["columns_to_insert_values"]})
    SELECT DISTINCT city_id, race_id, male_population, female_population,
     total_population, foreign_born FROM
        (
        SELECT
        cities.id AS city_id, races.id AS race_id, staging.male_population, staging.female_population,
        staging.total_population, staging.foreign_born
        FROM staging_demography staging
        INNER JOIN cities ON TRIM(' ' FROM staging.city) = cities.name
        INNER JOIN races ON TRIM(' ' FROM staging.race) = races.name
        )
    ORDER BY city_id ASC
""", tables["demography"]["name"]])

# Insert into immigration
queries_list.append([f"""
    INSERT INTO {tables["immigration"]["name"]} ({tables["immigration"]["columns_to_insert_values"]})
    SELECT arrival_date, arrival_mode_id, visa_type_id, residential_state_id,
     birth_year, gender FROM
        (
        SELECT time.date AS arrival_date, arrival_modes.id AS arrival_mode_id,
        visa_types.id as visa_type_id, states.id AS residential_state_id,
        birth_year, gender
        FROM staging_immigration staging
        LEFT JOIN time ON TRIM(' ' FROM staging.arrival_date) = time.date
        LEFT JOIN arrival_modes ON TRIM(' ' FROM staging.arrival_mode) = arrival_modes.name
        LEFT JOIN visa_types ON TRIM(' ' FROM staging.visa_type) = visa_types.type
        LEFT JOIN states ON TRIM(' ' FROM staging.residential_state) = states.code
        )
    ORDER BY arrival_date ASC
""", tables["immigration"]["name"]])

insert_facts = queries_list
