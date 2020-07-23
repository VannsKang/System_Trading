import pandas as pd
from pandas import Series, DataFrame
import pandas_datareader.data as web
import sqlite3
import datetime


start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 6, 12)
df = web.DataReader("078930.KS", "yahoo", start, end)

# print(df)

con = sqlite3.connect("/Users/soom/OneDrive/Documents/python/kospi.db")

df.to_sql('078930', con, if_exists='replace')

readed_df = pd.read_sql("SELECT * FROM '078930'", con, index_col='Date')

print(readed_df.head())

# raw_data = {'col0': [1, 2, 3, 4], 'col1': [
#     10, 20, 30, 40], 'col2': [100, 200, 300, 400]}
# df = DataFrame(raw_data)

# df.to_sql('test', con, chunksize=1000)

# df = pd.read_sql("SELECT * FROM kakao", con, index_col=None)

# print(df)

# df = pd.read_sql("SELECT * FROM test", con, index_col="index")
# print(df)
