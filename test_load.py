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
df = pd.read_csv("C:/Users/GaurangPrasadML/DBMS_project/itws6960-2017-final-project-master/scripts/testingcsv.csv")
print(df.columns)
cur = conn.cursor()
engine = create_engine('postgresql+psycopg2://test5:test5@localhost/test5')
df1 = df[['VIOLATION ITEM', 'VIOLATION DESCRIPTION']]
print(df1.size)
df_distinct = df1.drop_duplicates(keep="first", inplace=False)
print(df_distinct.size)
print()
print("Getting columns for table: FOOD_SERVICE_VIOLATIONS")
print(df_distinct.columns)
print(df_distinct['VIOLATION ITEM'])
df_distinct.to_sql('food_service_violations_distinct', engine,schema='public',index=False, if_exists='replace')
cur.execute("""Select count(*) from food_service_violations_distinct""");

records = cur.fetchall()
print(records)
cur.execute("""ALTER TABLE food_service_violations_distinct ADD PRIMARY KEY ("VIOLATION ITEM")""");

print('Altered')

df2 = df[['LOCAL HEALTH DEPARTMENT', 'COUNTY']]
df2_distinct = df2.drop_duplicates(keep="first", inplace=False)
df2_distinct.to_sql('health_dept_county_map_distinct', engine,schema='public',index=False, if_exists='replace')
cur.execute("""ALTER TABLE health_dept_county_map_distinct ADD PRIMARY KEY ("COUNTY")""");

df3 = df[['NYS HEALTH OPERATION ID', 'OPERATION NAME', 'LATITUDE', 'LONGITUDE', 'FACILITY CODE', 'FACILITY ADDRESS', 'FACILITY MUNICIPALITY',
          'FACILITY CITY', 'FACILITY POSTAL ZIPCODE', 'FS FACILITY STATE', 'PERMITTED  DBA', 'PERMITTED  CORP. NAME', 'PERM. OPERATOR LAST NAME',
          'PERM. OPERATOR FIRST NAME', 'FOOD SERVICE TYPE', 'FOOD SERVICE DESCRIPTION', 'PERMIT EXPIRATION DATE']]
df3_distinct = df3.drop_duplicates(subset='NYS HEALTH OPERATION ID', keep="first", inplace=False)
print(df3.shape)
print(df3_distinct.shape)
df3_distinct.to_sql('food_service_operator_distinct', engine,schema='public',index=False, if_exists='replace')
#duplicateRowsDF = df3_distinct[df3_distinct.duplicated(['NYS HEALTH OPERATION ID'])]
#print(duplicateRowsDF.shape)
#df3proc = df3_distinct[~df3_distinct['NYS HEALTH OPERATION ID'].isin(duplicateRowsDF['NYS HEALTH OPERATION ID'])]
#print(df3proc.shape)
cur.execute("""ALTER TABLE food_service_operator_distinct ADD PRIMARY KEY ("NYS HEALTH OPERATION ID")""");
#print(duplicateRowsDF)
print("Done")

df4 = df[['COUNTY','DATE OF INSPECTION','NYS HEALTH OPERATION ID','VIOLATION ITEM',
          'CRITICAL VIOLATION','TOTAL # CRITICAL VIOLATIONS','TOTAL #CRIT.  NOT CORRECTED',
          'TOTAL # NONCRITICAL VIOLATIONS', 'NYSDOH GAZETTEER 1980', 'INSPECTION TYPE',
          'INSPECTION COMMENTS']]
df4.to_sql('food_service_inspections', engine,schema='public',index=False, if_exists='replace')
cur.execute("""ALTER TABLE food_service_inspections ADD PRIMARY KEY ("NYS HEALTH OPERATION ID", "DATE OF INSPECTION")""");
print(df4.shape)
conn.commit()



"""
Rockland, Albany, Hamilton
18, 14, 15
SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = 'food_service_operator_distinct'::regclass
AND    i.indisprimary;
"""
