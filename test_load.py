# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:20:40 2019

@author: GaurangPrasadML
"""

import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import threading;
import pymongo;
import json;
conn = psycopg2.connect("host=localhost dbname=test5 user=test5 password=test5")
print("Connected to PSQL")
# print(df.columns)
def loadFoodServices():
    df = pd.read_csv("./testingcsv.csv")
    cur = conn.cursor()
    engine = create_engine('postgresql+psycopg2://test5:test5@localhost/test5')

    # Food Service Violations
    print("Loading Food Service Violations")
    df1 = df[['VIOLATION ITEM', 'VIOLATION DESCRIPTION']]
    df_distinct = df1.drop_duplicates(keep="first", inplace=False)
    df_distinct.dropna()

    df_distinct.columns = ['violation_item', 'violation_description']

    df_distinct.to_sql('food_service_violations', engine, schema='public',index=False, if_exists='append')


    # Health Dept County Map
    print("Loading Health Dept to County Map")
    healthMap = df[['COUNTY', 'LOCAL HEALTH DEPARTMENT']]
    healthMap = healthMap.drop_duplicates(keep="first", inplace=False)
    healthMap.dropna()

    healthMap.columns = ['county', 'local_health_department']

    healthMap.to_sql('health_dept_county_map', engine, schema='public',index=False, if_exists='append')


    # Food Service Operators
    print("Loading Food Service Operators")

    df3 = df[['NYS HEALTH OPERATION ID', 'OPERATION NAME', 'LATITUDE', 'LONGITUDE', 'FACILITY CODE', 'FACILITY ADDRESS', 'FACILITY MUNICIPALITY',
            'FACILITY CITY', 'FACILITY POSTAL ZIPCODE', 'FS FACILITY STATE', 'PERMITTED  DBA', 'PERMITTED  CORP. NAME', 'PERM. OPERATOR LAST NAME',
            'PERM. OPERATOR FIRST NAME', 'FOOD SERVICE TYPE', 'FOOD SERVICE DESCRIPTION', 'PERMIT EXPIRATION DATE']]
    df3_distinct = df3.drop_duplicates(subset='NYS HEALTH OPERATION ID', keep="first", inplace=False)

    df3_distinct.columns = ['nys_health_operation_id', 'operation_name','latitude','longitude',
    'facility_code','facility_address','facility_municipality','facility_city','facility_postal_zipcode',
    'fs_facility_state','permitted_dba','permitted_corp_name','perm_operator_last_name','perm_operator_first_name',
    'food_service_type','food_service_description','permit_expiration_date']

    df3_distinct.to_sql('food_service_operator', engine,schema='public',index=False, if_exists='append')


    # Food Service Inspections
    print("Loading Food Service Inspections")

    df4 = df[['COUNTY','DATE OF INSPECTION','NYS HEALTH OPERATION ID','VIOLATION ITEM',
            'CRITICAL VIOLATION','TOTAL # CRITICAL VIOLATIONS','TOTAL #CRIT.  NOT CORRECTED',
            'TOTAL # NONCRITICAL VIOLATIONS', 'NYSDOH GAZETTEER 1980', 'INSPECTION TYPE',
            'INSPECTION COMMENTS']]

    df4 = df4.dropna(how='any',axis=0) 

    df4.columns = ['county','date_of_inspection','nys_health_operation_id', 
    'violation_item','critical_violation','total_critical_violations','total_crit_not_corrected',
    'total_noncritical_violations','nysdoh_gazetteer_1980','inspection_type','inspection_comments']

    df4_distinct = df4.drop_duplicates(subset=['nys_health_operation_id','date_of_inspection','violation_item'], keep="first", inplace=False)

    df4_distinct.to_sql('food_service_inspections', engine,schema='public',index=False, if_exists='append')
    
    conn.commit()
    print("Done")

def loadAdultArrests():
    df = pd.read_csv("./Adult_Arrests_by_County___Beginning_1970.csv")
    cur = conn.cursor()
    engine = create_engine('postgresql+psycopg2://test5:test5@localhost/test5')

    # Food Service Violations
    print("Loading Main Table")
    df1 = df[['County','Year','Drug Felony','Violent Felony','DWI Felony','Other Felony','Drug Misd','DWI Misd','Property Misd','Other Misd']]
    
    df_distinct = df1.drop_duplicates(keep="first", inplace=False)
    df_distinct = df_distinct.dropna(how='any',axis=0) 

    df_distinct.columns = ['county','year','drug_felony','violent_felony','dwi_felony','other_felony','drug_misdemeanor','dwi_misdemeanor',
    'property_misdemeanor','other_misdemeanor']
    
    df_distinct.to_sql('adult_arrests', engine, schema='public',index=False, if_exists='append')
    conn.commit()
    print("Done")


def loadLiquorDataset():
    df = pd.read_csv("./Liquor_Authority_Quarterly_List_of_Active_Licenses.csv", low_memory = False)
    cur = conn.cursor()
    engine = create_engine('postgresql+psycopg2://test5:test5@localhost/test5')

    # city_zip_map Violations
    print("Loading Liquor Table")

    df1 = df[['Zip','City','State']]

    df1.columns = ['zip','city','state']
    result_df = df1.drop_duplicates(subset=['zip'])
    result_df.to_sql('city_zip_map', engine, schema='public',index=False, if_exists='append')

    #LIQUOR_AGENCY
    print("Loading Liquor Agency")
    df2 = df[['Agency Zone Office Number','Agency Zone Office Name']]
    df2.columns = ['office_number','office_name']
    df2_unique = df2.drop_duplicates(subset=['office_number'])
    df2_unique.to_sql('liquor_agency', engine, schema='public',index=False, if_exists='append')
    conn.commit()

    #LIQUOR_LICENSE
    print("Loading License Type")
    df3 = df[['License Type Code','License Class Code','License Type Name']]
    df3.columns = ['license_type_code','license_class_code','license_type_name']
    df3_unique = df3.drop_duplicates(subset=['license_type_code'])
    df3_unique.to_sql('license_types', engine, schema='public',index=False, if_exists='append')
    conn.commit()

    #LIQUOR_LICENSE
    print("Loading Liquor License")
    df4 = df[['County Name (Licensee)','License Serial Number','License Type Code','Premises Name','Doing Business As (DBA)','Actual Address of Premises (Address1)',
    'Zip','Latitude','Longitude','License Original Issue Date','License Effective Date','License Expiration Date','License Certificate Number']]
    df4.columns = ['county','license_serial_no','license_type_code','premise_name','doing_business_as','address','zipcode',
    'latitude','longitude','issue_date','effective_date','expiration_date','license_certificate_number']
    df4_unique = df4.drop_duplicates(subset=['license_serial_no'])
    df4_unique.to_sql('liquor_license', engine, schema='public',index=False, if_exists='append')
    conn.commit()

    print("Done")

def loadNoSQLData():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["dbms"]
    mycol = mydb["insuranceBeneficiaries"]
    with open('unemploymentBenefits.json','r') as data_file:    
        data_json = json.load(data_file)
    #Insert Data
    mycol.remove()
    mycol.insert(data_json)
      



liquorDataset = threading.Thread(target=loadLiquorDataset(), args=(1,))
arrestDataset = threading.Thread(target=loadAdultArrests(), args=(1,))
foodServiceDataset = threading.Thread(target=loadFoodServices(), args=(1,))
insuranceDataset = threading.Thread(target=loadNoSQLData(), args=(1,))

liquorDataset.start()
arrestDataset.start()
foodServiceDataset.start()
insuranceDataset.start()