import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url



    if url.endswith('.parquet.gz'):
        csv_name = 'output.parquet.gz'
    else:
        csv_name = 'output.parquet'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


    #df_iter = pd.read_parquet(csv_name, iterator = True, chunksize = 100000, engine='pyarrow')
    df = pd.read_parquet(csv_name, engine='pyarrow')
    
    #df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists = 'replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    #while True:
    #    try:
    #        t_start = time()

            #df = next(df_iter)

            #df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            #df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            #df.to_sql(name = table_name, con = engine, if_exists = 'append')

            #t_end = time()

            #print('insterted another chunk, took %.3f seconds' % (t_end - t_start))

        #except StopIteration:
         #   print("Finished ingesting data into the postgres database")
          #  break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Ingest Parquet data to Postgres')

    parser.add_argument('--user',       required = True, help = 'user name for postgres')
    parser.add_argument('--password',   required = True, help = 'password for postgres')
    parser.add_argument('--host',       required = True, help = 'host for postgres')
    parser.add_argument('--port',       required = True, help = 'port for postgres')
    parser.add_argument('--db',         required = True, help = 'db for postgres')
    parser.add_argument('--table_name', required = True, help = 'name of the table where we will write the results to')
    parser.add_argument('--url',        required = True, help = 'url for parquet file')

    args = parser.parse_args()

    main(args)
