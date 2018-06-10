import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import reduce

#TODO: Refactor.. a lot


df = pd.read_csv('FakeData.csv',parse_dates=['createdon'])


now = datetime.now()
# investicate dt.normalize for this instead. would be cleaner
week_start = (datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)).replace(hour=0,minute=0,second=0,microsecond=0)
month_start = datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0)

year = now.year




df['createdon'] = pd.to_datetime(df['createdon'])


df_24hours = df[df['createdon'] >= now-timedelta(hours=24)]
df_24hours = df_24hours.groupby('owner__username')['count'].sum().reset_index()
df_24hours.columns = ['owner__username','Last 24 Hours']


df_week = df[df['createdon'] >= week_start][['count','owner__username']]
df_week = df_week.groupby('owner__username')['count'].sum().reset_index()
df_week.columns = ['owner__username','Week']


cur_quarter = pd.to_datetime('today').quarter
df_quarter = df[(df['createdon'].dt.quarter == cur_quarter) & (df['createdon'].dt.year == year) ][['count','owner__username']]
df_quarter = df_quarter.groupby('owner__username')['count'].sum().reset_index()
df_quarter.columns = ['owner__username','Quarter']



df_month = df[df['createdon'] >= month_start][['count','owner__username']]
df_month = df_month.groupby('owner__username')['count'].sum().reset_index()
df_month.columns = ['owner__username','Month']

df_year = df[df['createdon'].dt.year == year][['count','owner__username']]
df_year = df_year.groupby('owner__username')['count'].sum().reset_index()
df_year.columns = ['owner__username','Year']

final_df = df_year.merge(df_quarter, on=['owner__username'], how='outer')
final_df = final_df.merge(df_month, on=['owner__username'], how='outer')
final_df = final_df.merge(df_week, on=['owner__username'], how='outer')
final_df = final_df.merge(df_24hours, on=['owner__username'], how='outer')

