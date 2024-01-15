import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.point import Point
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import time 
import dask.dataframe as dd

start_time = time.time()

geolocator = Nominatim(user_agent="otodom")
    
engine = create_engine(URL(
                    account = 'cjekfuw-kdb12867',
                    user = 'fs487',
                    password = 'PASSWORD!',
                    database = 'demo',
                    schema = 'public',
                    warehouse = 'demo_wh'))

# Runs an SQL query in SnowflakeSQL that flattens latitude and longitude data

with engine.connect() as conn:
    try:
        query = """ SELECT RN, concat(latitude,',',longitude) as LOCATION
                    FROM (SELECT RN
                            , SUBSTR(location, REGEXP_INSTR(location,' ',1,4)+1) AS LATITUDE 
                            , SUBSTR(location, REGEXP_INSTR(location,' ',1,1)+1, (REGEXP_INSTR(location,' ',1,2) - REGEXP_INSTR(location,' ',1,1) - 1) ) AS LONGITUDE
                        FROM otodom_data_flatten WHERE rn between 1 and 1000
                        ORDER BY rn  ) """
        print("--- %s seconds ---" % (time.time() - start_time))

        # Loads data into Pandas data frame 'df'
        
        df = pd.read_sql(query,conn)

        # Converts columns into uppercase to prep for to_sql function
        
        df.columns = map(lambda x: str(x).upper(), df.columns)

        # Loads data from pandas into dask.dataframe 'dd' which enables multiple pandas data frames to run simultaneously 
        
        ddf = dd.from_pandas(df,npartitions=10)
        print(ddf.head(5,npartitions=-1))
        
        # Creates new column 'Address' and passes latitude and longitude data into geolocator API  which then converts the data
        # into country, city, zip code, etc.. 
        
        ddf['ADDRESS'] = ddf['LOCATION'].apply(lambda x: geolocator.reverse(x).raw['address'],meta=(None, 'str'))
        print("--- %s seconds ---" % (time.time() - start_time))

        # Moves data from dask_dataframe back into pandas
        
        pandas_df = ddf.compute()
        print(pandas_df.head())
        print("--- %s seconds ---" % (time.time() - start_time))

        # Loads data from pandas into SnowflakeSQL
        
        pandas_df.to_sql('otodom_data_flatten_address', con=engine, if_exists='append', index=False, chunksize=16000, method=pd_writer)
    except Exception as e:
        print('--- Error --- ',e)
    finally:
        conn.close()
engine.dispose()

print("--- %s seconds ---" % (time.time() - start_time))
