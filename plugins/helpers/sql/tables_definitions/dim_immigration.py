arrival_modes_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE
""")

arrival_modes_columns_to_insert_values = ("""
name
""")

visa_types_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE,
type SMALLINT NOT NULL
""")

visa_types_columns_to_insert_values = ("""
name,
type
""")

time_columns_definitions = ("""
date  DATE PRIMARY KEY,
day SMALLINT NOT NULL,
week SMALLINT NOT NULL,
month SMALLINT NOT NULL,
year SMALLINT NOT NULL,
weekday SMALLINT NOT NULL
""")

time_columns_to_insert_values = ("""
date,
day,
week,
month,
year,
weekday
""")

immigrations_dimentions_tables = {
    "arrival_modes": {
        "name": "arrival_modes",
        "columns_definition": arrival_modes_columns_definitions,
        "columns_to_insert_values": arrival_modes_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "sortkey(name)",
        "data_quality": {
            "minimum_records": 0,
            "not_null_columns": ['name']
        }
    },
    "visa_types": {
        "name": "visa_types",
        "columns_definition": visa_types_columns_definitions,
        "columns_to_insert_values": visa_types_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "compound sortkey(type, name)",
        "data_quality": {
            "minimum_records": 0,
            "not_null_columns": ['name', 'type']
        }
    },
    "time": {
        "name": "time",
        "columns_definition": time_columns_definitions,
        "columns_to_insert_values": time_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "sortkey(date)",
        "data_quality": {
            "minimum_records": 0,
            "not_null_columns": ['date', 'day', 'week', 'month', 'year', 'weekday']
        }
    },
}
