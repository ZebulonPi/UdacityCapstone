
# Drop Table queries
fct_immigration_table_drop = "DROP TABLE IF EXISTS fct_immigration;"
dim_global_temp_table_drop = "DROP TABLE IF EXISTS dim_global_temp;"
dim_us_city_demo_table_drop = "DROP TABLE IF EXISTS dim_us_city_demo;"
dim_airports_table_drop = "DROP TABLE IF EXISTS dim_airports;"
dim_I94_country_table_drop = "DROP TABLE IF EXISTS dim_i94_country;"
dim_I94_ports_table_drop = "DROP TABLE IF EXISTS dim_i94_ports;"
dim_I94_travel_mode_table_drop = "DROP TABLE IF EXISTS dim_i94_travel_mode;"
dim_I94_state_table_drop = "DROP TABLE IF EXISTS dim_i94_state;"
dim_I94_visa_type_table_drop = "DROP TABLE IF EXISTS dim_i94_visa_type;"


# Create fact table SQL
fct_immigration_table_create = ("""CREATE TABLE IF NOT EXISTS fct_immigration (
                                        cicid           float NOT NULL PRIMARY KEY,
                                        year            float,
                                        month           float,
                                        cit             float,
                                        res             float,
                                        port            varchar,
                                        arrdate         float,
                                        travel_mode     float,
                                        addr            varchar,
                                        depdate         float,
                                        bir             float,
                                        visa            float,
                                        count           float,
                                        dtadfile        varchar,
                                        entdepa         varchar,
                                        entdepd         varchar,
                                        matflag         varchar,
                                        biryear         float,
                                        dtaddto         varchar,
                                        gender          varchar,
                                        airline         varchar,
                                        admnum          float,
                                        fltno           varchar,
                                        visa_type       varchar
                                    )
                                    diststyle all
                                    sortkey(cicid);
""")

# Create dimension tables SQL
dim_global_temp_table_create = ("""CREATE TABLE IF NOT EXISTS dim_global_temp (
                                        global_temp_id    int   GENERATED BY DEFAULT AS IDENTITY(0, 1) PRIMARY KEY,
                                        avg_temp          float,
                                        avg_temp_unc      float,
                                        city              varchar,
                                        country           varchar,
                                        lat               varchar,
                                        long              varchar
                                    )
                                    diststyle all
                                    sortkey(global_temp_id);
""")

dim_us_city_demo_table_create = ("""CREATE TABLE IF NOT EXISTS dim_us_city_demo (
                                        city_demo_id      int   GENERATED BY DEFAULT AS IDENTITY(0, 1) PRIMARY KEY,
                                        city              varchar,
                                        state             varchar,
                                        median_age        float,
                                        male_pop          float,
                                        female_pop        float,
                                        total_pop         float,
                                        veteran_cnt       float,
                                        foreign_cnt       float,
                                        avg_household_sz  float,
                                        state_code        varchar,
                                        race              varchar,
                                        count             float
                                    )
                                    diststyle all
                                    sortkey(city_demo_id);
""")

dim_airports_table_create = ("""CREATE TABLE IF NOT EXISTS dim_airports (
                                    airport_id    varchar        NOT NULL PRIMARY KEY,
                                    type          varchar,
                                    name          varchar,
                                    elevation_ft  float,
                                    region        varchar,
                                    muni          varchar,
                                    gps_code      varchar,
                                    local_code    varchar,
                                    coords        varchar
                                )
                                diststyle all
                                sortkey(airport_id);
""")

dim_i94_country_table_create = ("""CREATE TABLE IF NOT EXISTS dim_i94_country (
                                       country_cd   int     NOT NULL PRIMARY KEY,
                                       country_desc varchar
                                   )
                                   diststyle all
                                   sortkey(country_cd);
""")

dim_i94_ports_table_create = ("""CREATE TABLE IF NOT EXISTS dim_i94_ports (
                                     port_cd   int     NOT NULL PRIMARY KEY,
                                     port_desc varchar
                                 )
                                 diststyle all
                                 sortkey(port_cd);
""")

dim_i94_travel_mode_table_create = ("""CREATE TABLE IF NOT EXISTS dim_i94_travel_mode (
                                           travel_mode_cd   int     NOT NULL PRIMARY KEY,
                                           travel_mode_desc varchar
                                       )
                                       diststyle all
                                       sortkey(travel_mode_cd);
""")

dim_i94_state_table_create = ("""CREATE TABLE IF NOT EXISTS dim_i94_state (
                                     state_cd      int     NOT NULL PRIMARY KEY,
                                     state_full_nm varchar
                             )
                             diststyle all
                             sortkey(state_cd);
""")

dim_i94_visa_type_table_create = ("""CREATE TABLE IF NOT EXISTS dim_i94_visa_type (
                                         visa_type_cd   int     NOT NULL PRIMARY KEY,
                                         visa_type_desc varchar
                                     )
                                     diststyle all
                                     sortkey(visa_type_cd);
""")


# Queries to load tables
fct_immigration_insert = """
INSERT INTO fct_immigration (cicid, year, month, cit, res, port, arrdate, travel_mode, addr, depdate, bir, visa, count,   
    dtadfile, entdepa, entdepd, matflag, biryear, dtaddto, gender, airline, admnum, fltno, visa_type) 
    VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"""

dim_global_temp_insert = """
INSERT INTO dim_global_temp (avg_temp, avg_temp_unc, city, country, lat, long) VALUES (%s, %s, %s, %s, %s, %s)"""

dim_us_city_demo_insert = """
INSERT INTO dim_us_city_demo (city, state, median_age, male_pop, female_pop, total_pop, veteran_cnt, foreign_cnt,
avg_household_sz, state_code, race, count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

dim_airports_insert = """
INSERT INTO dim_airports (airport_id, type, name, elevation_ft, region, muni, gps_code, local_code, coords) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

dim_i94_country_insert = """
INSERT INTO dim_i94_country (country_cd, country_desc) VALUES (%s, %s)"""

dim_i94_ports_insert = """
INSERT INTO dim_i94_ports (port_cd, port_desc) VALUES (%s, %s)"""

dim_i94_travel_mode_insert = """
INSERT INTO dim_i94_travel_mode (travel_mode_cd, travel_mode_desc) VALUES (%s, %s)"""

dim_i94_state_insert = """
INSERT INTO dim_i94_state (state_cd, state_full_nm) VALUES (%s, %s)"""

dim_i94_visa_type_insert = """
INSERT INTO dim_i94_visa_type (visa_type_cd, visa_type_desc) VALUES (%s, %s)"""


# List objects containing type-related queries

drop_table_queries = [fct_immigration_table_drop, dim_global_temp_table_drop, dim_airports_table_drop, dim_us_city_demo_table_drop,           dim_I94_country_table_drop, dim_I94_ports_table_drop, dim_I94_travel_mode_table_drop, dim_I94_state_table_drop, dim_I94_visa_type_table_drop]

create_table_queries = [fct_immigration_table_create, dim_global_temp_table_create, dim_us_city_demo_table_create, dim_airports_table_create, dim_i94_country_table_create, dim_i94_ports_table_create, dim_i94_travel_mode_table_create, dim_i94_state_table_create, dim_i94_visa_type_table_create]

insert_table_queries = [fct_immigration_insert, dim_global_temp_insert, dim_us_city_demo_insert, dim_airports_insert, dim_i94_country_insert, dim_i94_ports_insert, dim_i94_travel_mode_insert, dim_i94_state_insert, dim_i94_visa_type_insert]
