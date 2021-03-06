states_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE,
code CHAR(2) UNIQUE
""")

states_columns_to_insert_values = ("""
name,
code
""")

cities_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE,
state_id INT,
foreign key(state_id) references states(id)
""")

cities_columns_to_insert_values = ("""
name,
state_id
""")

races_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE
""")

races_columns_to_insert_values = ("""
name
""")

demography_dimentions_tables = {
    "states": {
        "name": "states",
        "columns_definition": states_columns_definitions,
        "columns_to_insert_values": states_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "sortkey(code)",
        "data_quality": {
            "minimum_records": 1,
            "not_null_columns": ['name']
        }
    },
    "cities": {
        "name": "cities",
        "columns_definition": cities_columns_definitions,
        "columns_to_insert_values": cities_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "compound sortkey(name, state_id)",
        "data_quality": {
            "minimum_records": 1,
            "not_null_columns": ['name']
        }
    },
    "races": {
        "name": "races",
        "columns_definition": races_columns_definitions,
        "columns_to_insert_values": races_columns_to_insert_values,
        "dist_style": "diststyle all",
        "sort_key": "sortkey(name)",
        "data_quality": {
            "minimum_records": 1,
            "not_null_columns": ['name']
        }
    },
}
