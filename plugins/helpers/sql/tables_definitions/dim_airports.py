airports_types_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
name VARCHAR(256) NOT NULL UNIQUE
""")

airports_types_columns_to_insert_values = ("""
name
""")

airports_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
ident VARCHAR(256),
name VARCHAR(256) NOT NULL UNIQUE,
type_id INT,
state_id INT,
gps_code VARCHAR(12) UNIQUE,
iata_code VARCHAR(12) UNIQUE,
local_code VARCHAR(12) UNIQUE,
foreign key(type_id) references airports_types(id),
foreign key(state_id) references states(id)
""")

airports_columns_to_insert_values = ("""
ident,
name,
type_id,
state_id,
gps_code,
iata_code,
local_code
""")



airports_dimentions_tables = {
    "airports_types": {
        "name": "airports_types",
        "columns_definition": airports_types_columns_definitions,
        "columns_to_insert_values": airports_types_columns_to_insert_values,
        "dist_style": "diststyle all"
    },
    "airports": {
        "name": "airports",
        "columns_definition": airports_columns_definitions,
        "columns_to_insert_values": airports_columns_to_insert_values,
        "dist_style": "diststyle all"
    },
}
