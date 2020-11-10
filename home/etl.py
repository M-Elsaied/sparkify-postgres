import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from itertools import chain 
import datetime

def process_song_file(cur, filepath):
    """
    This function inputs annd preprocess and write to the Database the songs and artists data
        Inputs: cur - Cursor fot the Database
                filepath - filepath to extract the data
        Outputs: No output, data gets inserted to the Database
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(chain.from_iterable( df[['song_id', 'title', 'artist_id', 'year', 'duration']].values))
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(chain.from_iterable( df[['artist_id', 'artist_name', 'artist_location', 'artist_longitude', 'artist_latitude']].values))
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function inputs annd preprocess and write to the Database the songs and artists data
        Inputs: cur - Cursor fot the Database
                filepath - filepath to extract the data
        Outputs: No output, data gets inserted to the Database
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
#     t = 
    
#     # insert time data records
#     time_data = 
#     column_labels = 
#     time_df = 
    convert = lambda x: datetime.datetime.fromtimestamp(x / 1e3)
    df['time_stamp'] = df['ts'].apply(convert)
    convert2 = lambda x: datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S.%f") 
    df['my_date'] =  df['time_stamp'].apply(convert2)
    df['hour'] = df.my_date.apply(lambda x: x.hour)
    df['day'] = df.my_date.apply(lambda x: x.day)
    df['weekofyear'] = df.my_date.apply(lambda x: x.weekofyear)
    df['month'] = df.my_date.apply(lambda x: x.month)
    df['year'] = df.my_date.apply(lambda x: x.year)
    df['weekday'] = df.my_date.apply(lambda x: x.weekday())
    time_df = df[['time_stamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName','gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
#         print(results)
        
        if results:
            songid, artistid = None, None
#             songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data =  row.time_stamp, row.userId, row.level,row.song, row.sessionId, row.location, row.userAgent
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function processes the data and iterates over it, this is the main orchestrator that uses the process functions for log and songs
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()