demography_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
city_id INT NOT NULL UNIQUE,
state_id INT,
race_id INT,
male_population INTEGER,
female_population INTEGER,
total_population INTEGER,
foreign_born INTEGER,
foreign key(city_id) references cities(id),
foreign key(state_id) references states(id),
foreign key(race_id) references races(id)
""")

demography_columns_to_insert_values = ("""
city_id INT NOT NULL UNIQUE,
state_id INT,
race_id INT,
male_population INTEGER,
female_population INTEGER,
total_population INTEGER,
foreign_born INTEGER
""")

immigration_columns_definitions = ("""
id INT IDENTITY(1,1) PRIMARY KEY,
arrival_date DATE NOT NULL,
arrival_mode INT,
visa_type INT,
residential_state INT,
birth_year SMALLINT,
gender VARCHAR(256),
foreign key(arrival_date) references time(date),
foreign key(visa_type) references visa_types(id),
foreign key(residential_state) references states(id)
""")

immigration_columns_to_insert_values = ("""
arrival_date,
arrival_mode,
visa_type,
residential_state,
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
        "dist_style": "distkey(residential_state)"
    },
}
