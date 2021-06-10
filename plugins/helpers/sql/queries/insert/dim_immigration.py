from helpers.sql.tables_definitions.dim_immigration import (
    immigrations_dimentions_tables as tables
)

queries_list = []

# Insert into arrival modes table
queries_list.append([f"""
    INSERT INTO {tables["arrival_modes"]["name"]} ({tables["arrival_modes"]["columns_to_insert_values"]})
    SELECT DISTINCT name FROM
        (
        SELECT
        TRIM(' ' FROM arrival_mode) AS name
        FROM staging_immigration
        WHERE
            LENGTH(TRIM(' ' FROM arrival_mode)) >= 3
        )
    ORDER BY name ASC
""", tables["arrival_modes"]["name"]])

# Insert into cities table
queries_list.append([f"""
    INSERT INTO {tables["visa_types"]["name"]} ({tables["visa_types"]["columns_to_insert_values"]})
    SELECT DISTINCT name, type FROM
        (
        SELECT
        visa_type AS type,
        (CASE
            WHEN staging.visa_type = 1 THEN 'Business'
            WHEN staging.visa_type = 2 THEN 'Pleasure'
            WHEN staging.visa_type = 3 THEN 'Student'
            ELSE null
        END
        ) AS name
        FROM staging_immigration staging
        )
    ORDER BY name ASC
""", tables["visa_types"]["name"]])

# # Insert into time table
queries_list.append([f"""
    INSERT INTO {tables["time"]["name"]} ({tables["time"]["columns_to_insert_values"]})
    SELECT DISTINCT date, day, week, month, year, weekday FROM
        (
        SELECT arrival_date AS date,
        extract(day from arrival_date) AS day, extract(week from arrival_date) AS week ,
        extract(month from arrival_date) AS month, extract(year from arrival_date) AS year,
        extract(dayofweek from arrival_date) AS weekday
        FROM staging_immigration staging
        )
    ORDER BY date ASC
""", tables["time"]["name"]])

insert_dim_demography = queries_list
