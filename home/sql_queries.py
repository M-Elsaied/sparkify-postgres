"""
This file consists of three parts
    Drop tables: Drops tables if already exists
    Create tables: Create tables with having incremental Ids and primary keys
    Insert tables: Inerts values that will be added from etl pipeline
"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays 
    (songplay_id SERIAL PRIMARY KEY, start_time varchar, user_id int,
    level varchar, song_id varchar, session_id int, location varchar, user_agent varchar)
    -- ,
    -- FOREIGN KEY (user_id) REFERENCES public."users" (user_id) ,
    -- FOREIGN KEY (song_id) REFERENCES public."songs" (song_id))
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users 
    (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
    (song_id varchar PRIMARY KEY, title varchar, artist_id varchar, year int, duration float )
""") 

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS 
    artists (artist_id varchar, name varchar, location varchar, longitude float, latitude float)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS
    time (start_time varchar, hour int, day varchar, week int, month int, year int, weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays 
    ( start_time, user_id, level, song_id, session_id, location, user_agent) 
                 VALUES ( %s, %s,%s, %s, %s,%s, %s)
""")

user_table_insert = ("""
INSERT INTO "users" 
    (user_id, first_name, last_name, gender, level) \
                 VALUES (%s, %s, %s,%s, %s)
                     ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO "songs"
    (song_id, title, artist_id, year, duration) \
                 VALUES (%s, %s, %s,%s, %s)
""")

artist_table_insert = ("""
INSERT INTO "artists" 
    (artist_id, name, location, longitude, latitude) \
                 VALUES (%s, %s, %s,%s, %s)
""")


time_table_insert = ("""
INSERT INTO "time" 
    (start_time, hour, day, week, month, year, weekday) \
                 VALUES (%s, %s, %s,%s, %s,%s, %s)
""")

# FIND SONGS

song_select = ("""
SELECT song_id, songs.artist_id, location
    FROM songs 
    JOIN artists on songs.artist_id = artists.artist_id 
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration=%s 
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]