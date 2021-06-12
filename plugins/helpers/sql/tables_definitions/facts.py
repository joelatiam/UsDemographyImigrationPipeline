demography_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
city_id INT NOT NULL,
race_id INT NOT NULL,
male_population INTEGER,
female_population INTEGER,
total_population INTEGER,
foreign_born INTEGER,
foreign key(city_id) references cities(id),
foreign key(race_id) references races(id)
""")

demography_columns_to_insert_values = ("""
city_id,
race_id,
male_population,
female_population,
total_population,
foreign_born
""")

immigration_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
arrival_date DATE NOT NULL,
arrival_mode_id INT,
visa_type_id INT,
residential_state_id INT,
birth_year SMALLINT,
gender VARCHAR(256),
foreign key(arrival_date) references time(date),
foreign key(arrival_mode_id) references arrival_modes(id),
foreign key(visa_type_id) references visa_types(id),
foreign key(residential_state_id) references states(id)
""")

immigration_columns_to_insert_values = ("""
arrival_date,
arrival_mode_id,
visa_type_id,
residential_state_id,
birth_year,
gender
""")

fact_tables = {
    "demography": {
        "name": "demography",
        "columns_definition": demography_columns_definitions,
        "columns_to_insert_values": demography_columns_to_insert_values,
        "dist_style": "diststyle all"
    },
    "immigration": {
        "name": "immigration",
        "columns_definition": immigration_columns_definitions,
        "columns_to_insert_values": immigration_columns_to_insert_values,
        "dist_style": "distkey(residential_state_id)"
    },
}
