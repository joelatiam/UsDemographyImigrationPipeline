staging_demography_columns_definitions = ("""
city VARCHAR(256),
state VARCHAR(256),
male_population INTEGER,
female_population INTEGER,
total_population INTEGER,
foreign_born INTEGER,
state_code VARCHAR(256),
race VARCHAR(256)
""")

staging_demography_columns_names = ("""
city,
state,
male_population,
female_population,
total_population,
foreign_born,
state_code,
race
""")

staging_airports_columns_definitions = ("""
ident VARCHAR(256),
type VARCHAR(256),
name VARCHAR(256),
iso_region VARCHAR(256),
gps_code VARCHAR(256),
iata_code VARCHAR(256),
local_code VARCHAR(256)
""")

staging_airports_columns_names= ("""
ident,
type,
name,
iso_region,
gps_code,
iata_code,
local_code
""")

staging_immigration_columns_definitions = ("""
arrival_date DATE,
arrival_mode VARCHAR(256),
visa_type SMALLINT,
birth_year SMALLINT,
gender VARCHAR(256),
residential_state VARCHAR(256)
""")

staging_immigration_columns_names= ("""
arrival_date,
arrival_mode,
visa_type,
birth_year,
gender,
residential_state
""")

staging_tables = {
    "demography": {
        "name": "staging_demography",
        "columns_definition": staging_demography_columns_definitions,
        "columns_names": staging_demography_columns_names,
        "s3": {
            "key": "demography",
            "format": "csv",
            "delimiter": ",",
            "ignoreheader": "ignoreheader as 1 "
        },
    },
    "airports": {
        "name": "staging_airports",
        "s3_directory": "airports",
        "columns_definition": staging_airports_columns_definitions,
        "columns_names": staging_airports_columns_names,
        "s3": {
            "key": "airports",
            "format": "csv",
            "delimiter": ",",
            "ignoreheader": "ignoreheader as 1 "
        },
    },
    "immigration": {
        "name": "staging_immigration",
        "s3_directory": "immigration",
        "columns_definition": staging_immigration_columns_definitions,
        "columns_names": staging_immigration_columns_names,
        "s3": {
            "key": "immigration",
            "format": "parquet",
            "delimiter": '',
            "ignoreheader": ''
        },
    }
}
