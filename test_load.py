# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:20:40 2019

@author: GaurangPrasadML
"""

import psycopg2
from sqlalchemy import create_engine
import pandas as pd

conn = psycopg2.connect("host=localhost dbname=test5 user=test5 password=test5")
print("Connected to PSQL")
df = pd.read_csv("./testingcsv.csv")
# print(df.columns)
cur = conn.cursor()
engine = create_engine('postgresql+psycopg2://test5:test5@localhost/test5')


# Health Dept County Map
print("Loading Health Dept to County Map")
healthMap = df[['COUNTY', 'LOCAL HEALTH DEPARTMENT']]
healthMap = healthMap.drop_duplicates(keep="first", inplace=False)
healthMap.dropna()

healthMap.columns = ['county', 'local_health_department']

healthMap.to_sql('health_dept_county_map', engine, schema='public',index=False, if_exists='append')


conn.commit()
print("Done")
