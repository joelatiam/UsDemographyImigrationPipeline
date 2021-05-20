
staging_demography = {
    "columns": [
        "City",
        "State",
        "Male Population",
        "Female Population",
        "Total Population",
        "Foreign-born",
        "State Code",
        "Race"
    ],
    "rename": {
        "City": "city",
        "State": "state",
        "Male Population": "male_population",
        "Female Population": "female_population",
        "Total Population": "total_population",
        "Foreign-born": "foreign_born",
        "State Code": "state_code",
        "Race": "race"
    },
    "replace_na": {
        "male_population": 0,
        "female_population": 0,
        "total_population": 0,
        "foreign_born": 0,
    },
    "convert": {
        "male_population": "int32",
        "female_population": "int32",
        "total_population": "int32",
        "foreign_born": "int32",
    }

}

staging_airports= {
    "columns": [
        "ident",
        "type",
        "name",
        "iso_region",
        "gps_code",
        "iata_code",
        "local_code",
    ],
    "rename": None,
    "replace_na": None,
    "convert": None,
}


staging_data = {
    "demography": staging_demography,
    "airports": staging_airports
}
